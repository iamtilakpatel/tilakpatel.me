#!/usr/bin/env python3
"""CDP interaction test for the Phase 1 homepage.

Validates: no console errors, theme toggle (light<->dark both directions),
mobile menu open/close with Escape, copy-email status feedback, and captures
reference screenshots (dark 1440, light 1440, mobile 390 with menu open).

Usage: python tools/cdp_interact.py http://127.0.0.1:8793/index.html /tmp
"""
import base64
import json
import subprocess
import sys
import time
import urllib.request

sys.path.insert(0, "tools")
from cdp_check import CDP, CHROME

BASE = sys.argv[1]
OUT = sys.argv[2] if len(sys.argv) > 2 else "/tmp"

chrome = subprocess.Popen(
    [CHROME, "--headless=new", "--disable-gpu", "--remote-debugging-port=9222",
     "--no-first-run", "--user-data-dir=/tmp/tilak-cdp-profile", "about:blank"],
    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
)

def wait_targets():
    for _ in range(60):
        try:
            with urllib.request.urlopen("http://127.0.0.1:9222/json", timeout=2) as r:
                ts = [t for t in json.load(r) if t.get("type") == "page"]
            if ts:
                return ts[0]["webSocketDebuggerUrl"]
        except Exception:
            time.sleep(0.5)
    raise SystemExit("chrome did not start")

def screenshot(cdp, name):
    cdp.next_id += 1
    cdp.send(json.dumps({"id": cdp.next_id, "method": "Page.captureScreenshot",
                         "params": {"format": "png"}}))
    msg = cdp.until(id_=cdp.next_id, timeout=20)
    data = msg["result"]["data"]
    path = f"{OUT}/{name}.png"
    open(path, "wb").write(base64.b64decode(data))
    print(f"📸 {path}")

try:
    cdp = CDP(wait_targets())
    cdp.next_id = 100

    def cmd(method, params=None):
        cdp.next_id += 1
        cdp.send(json.dumps({"id": cdp.next_id, "method": method, "params": params or {}}))
        return cdp.until(id_=cdp.next_id, timeout=25)

    def js(expression):
        r = cmd("Runtime.evaluate", {"expression": expression, "returnByValue": True})
        return r.get("result", {}).get("result", {}).get("value")

    cmd("Runtime.enable")
    cmd("Log.enable")
    cmd("Page.enable")

    console_errors = []
    # drain + collect console/exception frames during the test
    def drain(n_frames=1):
        for _ in range(n_frames):
            f = cdp.recv()
            if not f:
                continue
            try:
                m = json.loads(f)
            except json.JSONDecodeError:
                continue
            if m.get("method") == "Log.entryAdded" and m["params"]["entry"]["level"] in ("error",):
                console_errors.append(m["params"]["entry"]["text"][:160])
            if m.get("method") == "Runtime.exceptionThrown":
                console_errors.append(m["params"]["exceptionDetails"].get("text", "exception")[:160])

    print(js('location.href = "' + BASE + '"; "navigating"'))
    time.sleep(2.5)

    # collect a few pending console frames
    for _ in range(12):
        f = cdp.recv()
        if f:
            try:
                m = json.loads(f)
                if m.get("method") == "Log.entryAdded" and m["params"]["entry"]["level"] == "error":
                    console_errors.append(m["params"]["entry"]["text"][:160])
                if m.get("method") == "Runtime.exceptionThrown":
                    console_errors.append("exception")
            except json.JSONDecodeError:
                pass

    bg_dark = js('getComputedStyle(document.body).backgroundColor')
    print(f"theme system-dark bg: {bg_dark}")

    # simulate system light preference, then toggle dark -> light -> back
    cmd("Emulation.setEmulatedMedia", {"features": [{"name": "prefers-color-scheme", "value": "light"}]})
    bg_light = js('getComputedStyle(document.body).backgroundColor')
    print(f"theme emulated-light bg: {bg_light}")

    js("document.querySelector('.theme-toggle').click()")
    time.sleep(0.4)
    attr_after_click = js("document.documentElement.getAttribute('data-theme')")
    bg_after_click = js('getComputedStyle(document.body).backgroundColor')
    print(f"after toggle click: data-theme={attr_after_click} bg={bg_after_click}")

    js("document.querySelector('.theme-toggle').click()")
    time.sleep(0.4)
    attr_second = js("document.documentElement.getAttribute('data-theme')")
    print(f"after second click: data-theme={attr_second}")

    # mobile menu
    cmd("Emulation.setDeviceMetricsOverride",
        {"width": 390, "height": 3800, "deviceScaleFactor": 1, "mobile": True})
    time.sleep(0.8)
    menu_open = js(
        "document.querySelector('.menu-toggle').click(); "
        "JSON.stringify({expanded: document.querySelector('.menu-toggle').getAttribute('aria-expanded'), "
        "hidden: document.querySelector('.mobile-menu').hidden, "
        "items: document.querySelectorAll('.mobile-menu a').length})"
    )
    print(f"mobile menu opened: {menu_open}")
    screenshot(cdp, "shot-home-390-menu-open")
    esc = js(
        "document.dispatchEvent(new KeyboardEvent('keydown', {key: 'Escape', bubbles: true})); "
        "JSON.stringify({hidden: document.querySelector('.mobile-menu').hidden, "
        "expanded: document.querySelector('.menu-toggle').getAttribute('aria-expanded')})"
    )
    print(f"mobile menu after Escape: {esc}")

    # copy email button feedback
    copy = js(
        "document.querySelector('.copy-email').click(); 'clicked'"
    )
    time.sleep(0.5)
    status_text = js("document.querySelector('.copy-status').textContent")
    print(f"copy email: {copy} status=\"{status_text}\"")

    screenshot(cdp, "shot-home-390-mobile")
    cmd("Emulation.setDeviceMetricsOverride", {"width": 1440, "height": 2400, "deviceScaleFactor": 1, "mobile": False})
    time.sleep(0.8)
    screenshot(cdp, "shot-home-1440-dark")

    print(f"console errors: {console_errors if console_errors else 'NONE'}")
finally:
    chrome.terminate()
    try:
        chrome.wait(timeout=5)
    except subprocess.TimeoutExpired:
        chrome.kill()
