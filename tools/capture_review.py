#!/usr/bin/env python3
"""Visual acceptance review package generator.

Captures full-page screenshots of:
  1. the IMPLEMENTED homepage (dist/) in dark and light themes at
     1440 / 768 / 390 / 320 px;
  2. the APPROVED REFERENCE mockup at the same widths and themes.

Also archives any earlier /tmp/shot-home-*.png captures under a
`legacy-early-build-` prefix. Output: design-reference/review-screenshots/
Data gathered along the way: whether web fonts actually loaded, computed
colors of the light-mode mono labels, and full-page capture heights.
"""
import base64
import json
import os
import pathlib
import shutil
import subprocess
import sys
import time
import urllib.request
from contextlib import closing

sys.path.insert(0, os.path.dirname(__file__))
from cdp_check import CDP, CHROME  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "design-reference" / "review-screenshots"
OUT.mkdir(exist_ok=True)

MOCKUP = ROOT / "design-reference" / "homepage-approved.html"
DIST = ROOT / "dist"

PORT = 8796


def start_server():
    proc = subprocess.Popen(
        ["python3", "-m", "http.server", str(PORT)],
        cwd=str(DIST),
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    return proc


def shot(cdp, name):
    cdp.next_id += 1
    cdp.send(json.dumps({"id": cdp.next_id, "method": "Page.captureScreenshot",
                         "params": {"format": "png", "captureBeyondViewport": True}}))
    msg = cdp.until(id_=cdp.next_id, timeout=30)
    data = base64.b64decode(msg["result"]["data"])
    (OUT / f"{name}.png").write_bytes(data)
    print(f"📸 {name}.png")


def run():
    server = start_server()
    chrome = subprocess.Popen(
        [CHROME, "--headless=new", "--disable-gpu", "--remote-debugging-port=9222",
         "--no-first-run", "--user-data-dir=/tmp/tilak-cdp-profile", "about:blank"],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    try:
        for _ in range(60):
            try:
                urllib.request.urlopen(f"http://127.0.0.1:{PORT}/index.html", timeout=2)
                break
            except Exception:
                time.sleep(0.4)
        for _ in range(60):
            try:
                with urllib.request.urlopen("http://127.0.0.1:9222/json", timeout=2) as r:
                    targets = [t for t in json.load(r) if t.get("type") == "page"]
                if targets:
                    break
            except Exception:
                time.sleep(0.4)
        cdp = CDP(targets[0]["webSocketDebuggerUrl"])
        cdp.next_id = 10

        def cmd(method, params=None):
            cdp.next_id += 1
            cdp.send(json.dumps({"id": cdp.next_id, "method": method, "params": params or {}}))
            return cdp.until(id_=cdp.next_id, timeout=30)

        def js(expression):
            r = cmd("Runtime.evaluate", {"expression": expression, "returnByValue": True})
            res = r.get("result", {}).get("result", {})
            if res.get("type") == "string":
                return res.get("value")
            return json.dumps(res.get("value"))

        notes = []

        # ── implemented homepage ──
        sizes = [(1440, "desktop"), (768, "tablet"), (390, "mobile"), (320, "mobile-small")]
        target_url = f"http://127.0.0.1:{PORT}/index.html"
        for theme in ("dark", "light"):
            for w, label in sizes:
                mobile = w < 500
                cmd("Emulation.setDeviceMetricsOverride",
                    {"width": w, "height": 1200, "deviceScaleFactor": 1, "mobile": mobile})
                cmd("Page.navigate", {"url": target_url})
                cmd2 = cmd
                # wait for load event
                while True:
                    fr = cdp.recv()
                    if fr and json.loads(fr).get("method") == "Page.loadEventFired":
                        break
                    if fr is None:
                        break
                time.sleep(1.2)
                js("document.querySelectorAll('.reveal').forEach(el => el.classList.add('visible')); 'ok'")
                js(f"document.documentElement.setAttribute('data-theme','{theme}'); 'ok'")
                time.sleep(0.7)
                notes.append(js(
                    "JSON.stringify({h: document.documentElement.scrollHeight,"
                    " bg: getComputedStyle(document.body).backgroundColor,"
                    " fonts: (document.fonts && document.fonts.status) || 'n/a',"
                    " barlow: document.fonts && document.fonts.check ? document.fonts.check('1rem \"Barlow Semi Condensed\"') : null,"
                    " mono: document.fonts && document.fonts.check ? document.fonts.check('1rem \"JetBrains Mono\"') : null})"
                ))
                if theme == "dark" and w == 390:
                    meta = js("getComputedStyle(document.querySelector('.card-meta') || document.body).color")
                    notes.append(f"390 dark .card-meta color: {meta}")
                shot(cdp, f"implemented-{w}-{theme}")
                print(notes[-1])

        # ── approved reference mockup ──
        file_url = "file://" + str(MOCKUP)
        for theme in ("dark", "light"):
            for w, label in sizes:
                mobile = w < 500
                cmd("Emulation.setDeviceMetricsOverride",
                    {"width": w, "height": 1200, "deviceScaleFactor": 1, "mobile": mobile})
                cmd("Page.navigate", {"url": file_url})
                while True:
                    fr = cdp.recv()
                    if fr and json.loads(fr).get("method") == "Page.loadEventFired":
                        break
                    if fr is None:
                        break
                time.sleep(1.2)
                js(f"document.documentElement.setAttribute('data-theme','{theme}'); 'ok'")
                time.sleep(0.7)
                notes.append(js(
                    "JSON.stringify({h: document.documentElement.scrollHeight,"
                    " bg: getComputedStyle(document.body).backgroundColor,"
                    " barlow: document.fonts && document.fonts.check ? document.fonts.check('1rem \"Barlow Semi Condensed\"') : null})"
                ))
                shot(cdp, f"reference-{w}-{theme}")
                print(notes[-1])

        # ── light-mode label colors on the implemented page (re-serve to reset) ──
        cmd("Page.navigate", {"url": target_url})
        time.sleep(1.5)
        js("document.documentElement.setAttribute('data-theme','light'); 'ok'")
        time.sleep(0.5)
        label_colors = js(
            "var el = document.querySelector('.card-meta');"
            "'card-meta: ' + getComputedStyle(el).color + ' | bg under: ' + getComputedStyle(document.body).backgroundColor"
        )
        print(label_colors)
        notes.append(label_colors)

        (OUT / "capture-notes.json").write_text(json.dumps(notes, indent=2))
        print("notes → capture-notes.json")
    finally:
        chrome.terminate()
        try:
            chrome.wait(timeout=5)
        except subprocess.TimeoutExpired:
            chrome.kill()
        server.terminate()


if __name__ == "__main__":
    # archive legacy shots
    legacy = sorted(pathlib.Path("/tmp").glob("shot-home-*.png"))
    for src in legacy:
        shutil.copy2(src, OUT / f"legacy-early-build-{src.name}")
    print(f"archived {len(legacy)} legacy screenshots")
    run()
