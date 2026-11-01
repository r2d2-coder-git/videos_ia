"""Renderiza una historia (canvas en Chrome headless) a PNGs o a MP4 1080x1920.
Uso: ../motor/.venv/bin/python capture.py <historia> stills t1 t2 ...   |   capture.py <historia> full [fps]"""
import json, os, sys, time, base64, subprocess, shutil, tempfile, urllib.request
import websocket, threading, http.server, functools

HERE = os.path.dirname(os.path.abspath(__file__))
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
PORT = 9339
HTTP = 9340

def serve():
    """Sirve la carpeta por HTTP: los módulos ES (Three.js) no cargan desde file://."""
    class Quiet(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *a): pass
    h = functools.partial(Quiet, directory=HERE)
    srv = http.server.ThreadingHTTPServer(("127.0.0.1", HTTP), h)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return srv

def start_chrome():
    prof = tempfile.mkdtemp(prefix="hist_chrome_")
    p = subprocess.Popen([CHROME, "--headless=new", f"--remote-debugging-port={PORT}", f"--user-data-dir={prof}",
                          "--window-size=1080,1920", "--hide-scrollbars", "--force-device-scale-factor=1",
                          "--allow-file-access-from-files", "--enable-gpu", "--ignore-gpu-blocklist", "--use-angle=metal", "about:blank"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    for _ in range(50):
        try:
            tabs = json.load(urllib.request.urlopen(f"http://127.0.0.1:{PORT}/json")); break
        except Exception: time.sleep(0.2)
    page = next(t for t in tabs if t["type"] == "page")
    return p, prof, websocket.create_connection(page["webSocketDebuggerUrl"], timeout=120, max_size=None)

class CDP:
    def __init__(self, ws): self.ws, self.i = ws, 0
    def __call__(self, method, **params):
        self.i += 1; self.ws.send(json.dumps({"id": self.i, "method": method, "params": params}))
        while True:
            m = json.loads(self.ws.recv())
            if m.get("id") == self.i:
                if "error" in m: raise RuntimeError(m["error"])
                return m.get("result", {})
    def ev(self, expr):
        r = self("Runtime.evaluate", expression=expr, returnByValue=True, awaitPromise=True)
        if "exceptionDetails" in r: raise RuntimeError(r["exceptionDetails"])
        return r["result"].get("value")

def open_story(name):
    proc, prof, ws = start_chrome(); cdp = CDP(ws)
    cdp("Emulation.setDeviceMetricsOverride", width=1080, height=1920, deviceScaleFactor=1, mobile=False)
    cdp("Page.enable"); serve(); cdp("Page.navigate", url=f"http://127.0.0.1:{HTTP}/{name}/index.html")
    for _ in range(300):
        time.sleep(0.1)
        try:
            if cdp.ev("typeof window.TIMELINE") == "object": break
        except Exception: pass
    if cdp.ev("typeof window.TIMELINE") != "object":
        raise RuntimeError("La historia no ha cargado (no hay window.TIMELINE): mira la consola del navegador o los archivos de la historia")
    cdp.ev("document.fonts.ready.then(()=>1)")
    return proc, prof, cdp

def shot(cdp, t, frame):
    cdp.ev(f"(async () => {{ if (window.CARA) await seekCara({t:.5f}); renderFrame({t:.5f},{frame}); return 1; }})()")
    return base64.b64decode(cdp("Page.captureScreenshot", format="png", optimizeForSpeed=True)["data"])

def main():
    name, mode = sys.argv[1], sys.argv[2]
    out_dir = os.path.join(HERE, name, "out"); os.makedirs(out_dir, exist_ok=True)
    proc, prof, cdp = open_story(name)
    try:
        tl = cdp.ev("window.TIMELINE")
        json.dump(tl, open(os.path.join(out_dir, "timeline.json"), "w"), indent=1)
        if mode == "hoja":
            # un fotograma en el centro de cada beat (scene) → out/hoja.png, 5 por fila
            import glob
            for f in glob.glob(os.path.join(out_dir, "hoja_*.png")): os.remove(f)
            ends = tl["starts"][1:] + [tl["total"]]
            for k, (a, b) in enumerate(zip(tl["starts"], ends)):
                open(os.path.join(out_dir, f"hoja_{k:03d}.png"), "wb").write(shot(cdp, (a + b) / 2, 0))
            n = len(tl["starts"]); cols = 5; rows = -(-n // cols)
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "1", "-i", os.path.join(out_dir, "hoja_%03d.png"),
                            "-vf", f"scale=360:640,tile={cols}x{rows}:padding=6", "-frames:v", "1", os.path.join(out_dir, "hoja.png")], check=True)
            print("hoja ok", os.path.join(out_dir, "hoja.png"), f"{n} beats")
            return
        if mode == "stills":
            for s in sys.argv[3:]:
                open(os.path.join(out_dir, f"still_{float(s):05.2f}.png"), "wb").write(shot(cdp, float(s), 0))
            print("stills ok", tl["total"])
            return
        fps = int(sys.argv[3]) if len(sys.argv) > 3 else 30
        n = int(round(tl["total"] * fps))
        sys.path.insert(0, HERE); import audio
        wav = os.path.join(out_dir, "audio.wav")
        voz = os.path.join(HERE, name, "voz.wav")
        audio.build(tl, wav, voz if os.path.exists(voz) else None)
        mp4 = os.path.join(out_dir, f"{name}.mp4")
        ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "image2pipe", "-framerate", str(fps), "-c:v", "png", "-i", "-",
                               "-i", wav, "-c:v", "libx264", "-preset", "slow", "-crf", "14", "-pix_fmt", "yuv420p",
                               "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-ar", "48000", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", mp4], stdin=subprocess.PIPE)
        t0 = time.time()
        for f in range(n):
            ff.stdin.write(shot(cdp, f / fps, f))
            if f % 150 == 0: print(f"{f}/{n}  {time.time() - t0:.0f}s", flush=True)
        ff.stdin.close(); ff.wait()
        print("ok", mp4, f"{time.time() - t0:.0f}s")
    finally:
        proc.terminate(); shutil.rmtree(prof, ignore_errors=True)

if __name__ == "__main__":
    main()
