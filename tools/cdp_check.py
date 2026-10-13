#!/usr/bin/env python3
"""Viewport/overflow check via Chrome DevTools Protocol (stdlib only).

Launches its own headless Chrome, then for each page emulates widths
1440 / 768 / 390 / 320 px and reports horizontal overflow (scrollWidth vs
clientWidth) plus elements wider than the viewport.

Usage: python tools/cdp_check.py BASE_URL page1 page2 ...
Example: python tools/cdp_check.py http://127.0.0.1:8791 index.html about.html
"""
import base64
import json
import os
import socket
import struct
import subprocess
import sys
import time
import urllib.request
import urllib.parse

DEBUG_PORT = 9222
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
SOCK_TIMEOUT = 8


class CDP:
    def __init__(self, ws_url):
        parsed = urllib.parse.urlparse(ws_url)
        path = parsed.path
        key = base64.b64encode(os.urandom(16)).decode()
        req = (
            f"GET {path} HTTP/1.1\r\nHost: {parsed.netloc}\r\n"
            "Upgrade: websocket\r\nConnection: Upgrade\r\n"
            f"Sec-WebSocket-Key: {key}\r\nSec-WebSocket-Version: 13\r\n\r\n"
        )
        self.sock = socket.create_connection((parsed.hostname, parsed.port), timeout=SOCK_TIMEOUT)
        self.sock.settimeout(SOCK_TIMEOUT)
        self.sock.sendall(req.encode())
        resp = b""
        while b"\r\n\r\n" not in resp:
            resp += self.sock.recv(4096)
        assert b"101" in resp.split(b"\r\n")[0], resp
        self.next_id = 10

    def send(self, payload):
        data = payload.encode()
        header = bytearray([0x81])
        n = len(data)
        if n < 126:
            header.append(0x80 | n)
        elif n < 65536:
            header.append(0x80 | 126)
            header += struct.pack(">H", n)
        else:
            header.append(0x80 | 127)
            header += struct.pack(">Q", n)
        mask = os.urandom(4)
        header += mask
        self.sock.sendall(bytes(header) + bytes(b ^ mask[i % 4] for i, b in enumerate(data)))

    def recv(self):
        try:
            hdr = self.sock.recv(2)
        except socket.timeout:
            return None
        if len(hdr) < 2:
            return None
        length = hdr[1] & 0x7F
        if length == 126:
            ext = b""
            while len(ext) < 2:
                ext += self.sock.recv(2 - len(ext))
            length = struct.unpack(">H", ext)[0]
        elif length == 127:
            ext = b""
            while len(ext) < 8:
                ext += self.sock.recv(8 - len(ext))
            length = struct.unpack(">Q", ext)[0]
        data = b""
        while len(data) < length:
            chunk = self.sock.recv(min(length - len(data), 65536))
            if not chunk:
                return None
            data += chunk
        return data.decode(errors="replace")

    def until(self, id_=None, method=None, timeout=SOCK_TIMEOUT):
        """Read frames until a matching id or method arrives (or timeout)."""
        deadline = time.time() + timeout
        while time.time() < deadline:
            frame = self.recv()
            if frame is None:
                continue
            try:
                msg = json.loads(frame)
            except json.JSONDecodeError:
                continue
            if id_ is not None and msg.get("id") == id_:
                return msg
            if method is not None and msg.get("method") == method:
                return msg
        return None

    def evaluate(self, expression):
        self.next_id += 1
        self.send(json.dumps({"id": self.next_id, "method": "Runtime.evaluate",
                              "params": {"expression": expression, "returnByValue": True}}))
        msg = self.until(id_=self.next_id)
        if not msg:
            return {}
        return msg["result"]["result"]["value"]

PROBE_JS = r"""
(() => {
  const vw = document.documentElement.clientWidth;
  const wide = [];
  document.querySelectorAll('*').forEach(el => {
    const r = el.getBoundingClientRect();
    if (r.width > vw + 1 && r.width < 4000 && !el.closest('pre, code')) {
      const cls = (el.className && String(el.getAttribute && el.getAttribute('class') || '') || String(el.tagName));
      wide.push(cls.slice(0, 50));
    }
  });
  return {
    scrollW: document.documentElement.scrollWidth,
    clientW: vw,
    docH: Math.round(document.documentElement.scrollHeight),
    wide: [...new Set(wide)].slice(0, 8),
  };
})()
"""


def main():
    base = sys.argv[1]
    pages = sys.argv[2:] or ["index.html"]
    chrome = subprocess.Popen(
        [CHROME, "--headless=new", "--disable-gpu", f"--remote-debugging-port={DEBUG_PORT}",
         "--no-first-run", "--user-data-dir=/tmp/tilak-cdp-profile", "about:blank"],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    try:
        for _ in range(30):
            try:
                urllib.request.urlopen(f"http://127.0.0.1:{DEBUG_PORT}/json", timeout=2)
                break
            except Exception:
                time.sleep(0.5)
        time.sleep(0.5)
        with urllib.request.urlopen(f"http://127.0.0.1:{DEBUG_PORT}/json") as r:
            targets = [t for t in json.load(r) if t.get("type") == "page"]

        for page in pages:
            url = base + "/" + page
            widths = [(1440, 4000, False), (768, 4400, False), (390, 5600, True), (320, 6000, True)]
            failed = None
            for attempt in range(3):
                try:
                    with urllib.request.urlopen(f"http://127.0.0.1:{DEBUG_PORT}/json", timeout=3) as r:
                        fresh = [t for t in json.load(r) if t.get("type") == "page"]
                    if not fresh:
                        raise EOFError("no page targets")
                    targets[0] = fresh[0]
                    cdp = CDP(targets[0]["webSocketDebuggerUrl"])
                    failed = []
                    for w, h, mobile in widths:
                        cdp.next_id = 1
                        cdp.send(json.dumps({"id": 1, "method": "Emulation.setDeviceMetricsOverride",
                                             "params": {"width": w, "height": h, "deviceScaleFactor": 1, "mobile": mobile}}))
                        cdp.until(id_=1, timeout=5)
                        cdp.next_id = 2
                        cdp.send(json.dumps({"id": 2, "method": "Page.navigate", "params": {"url": url}}))
                        cdp.until(method="Page.loadEventFired", timeout=15)
                        time.sleep(0.8)
                        # wait for webfonts to finish (fallback stacks can be wider and
                        # cause transient false overflows)
                        for _ in range(12):
                            st = (cdp.evaluate("document.fonts.status") or {})
                            if st == "loaded":
                                break
                            time.sleep(0.25)
                        r = cdp.evaluate(PROBE_JS) or {}
                        ok = r.get("scrollW", 0) <= r.get("clientW", 0) + 1
                        status = "OK       " if ok else "OVERFLOW "
                        print(f"{status} {page:<34} {w:>5}px scroll={r.get('scrollW')} client={r.get('clientW')} "
                              f"h={r.get('docH')} wide={r.get('wide')}")
                        if not ok:
                            failed.append(w)
                    break
                except Exception as exc:
                    if attempt == 2:
                        failed = ["ERROR"]
                        print(f"{page}: ERROR {exc.__class__.__name__}: {exc}")
                        break
                    print(f"  retrying {page} after {exc.__class__.__name__}: {exc}")
                    time.sleep(2)
            print(f"{page}: {'PASS' if not failed else 'FAIL at ' + str(failed)}px")
        return 0
    finally:
        chrome.terminate()
        try:
            chrome.wait(timeout=5)
        except subprocess.TimeoutExpired:
            chrome.kill()


if __name__ == "__main__":
    sys.exit(main())
