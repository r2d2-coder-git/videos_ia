"""Full-page screenshots through an already-open Chrome (keeps the user's own sign-in in that window).
Usage: cdp_shot.py <port> <url> <out.png> [css_width=540] [scale=2]   |   cdp_shot.py <port> --check <url>"""
import json, sys, time, base64, urllib.request
import websocket

port = sys.argv[1]
tabs = json.load(urllib.request.urlopen(f"http://127.0.0.1:{port}/json"))
page = next(t for t in tabs if t["type"] == "page")
ws = websocket.create_connection(page["webSocketDebuggerUrl"], timeout=60)
_id = 0
def cdp(method, **params):
    global _id
    _id += 1; ws.send(json.dumps({"id": _id, "method": method, "params": params}))
    while True:
        m = json.loads(ws.recv())
        if m.get("id") == _id: return m.get("result", m)

if sys.argv[2] == "--check":
    cdp("Page.navigate", url=sys.argv[3]); time.sleep(5)
    r = cdp("Runtime.evaluate", expression="document.body.innerText.includes('crear cuenta gratis') + ' | ' + [...document.querySelectorAll('header a, nav a')].map(a=>a.innerText).join(',')")
    print(r["result"]["value"]); sys.exit()

url, out = sys.argv[2], sys.argv[3]
w = int(sys.argv[4]) if len(sys.argv) > 4 else 540; sc = float(sys.argv[5]) if len(sys.argv) > 5 else 2
cdp("Emulation.setDeviceMetricsOverride", width=w, height=1000, deviceScaleFactor=sc, mobile=False)
cdp("Page.navigate", url=url); time.sleep(5)
h = cdp("Runtime.evaluate", expression="document.documentElement.scrollHeight")["result"]["value"]
cdp("Emulation.setDeviceMetricsOverride", width=w, height=h, deviceScaleFactor=sc, mobile=False); time.sleep(2)
img = cdp("Page.captureScreenshot", format="png", captureBeyondViewport=True)
open(out, "wb").write(base64.b64decode(img["data"]))
cdp("Emulation.clearDeviceMetricsOverride")
print(out, w * sc, h * sc)
