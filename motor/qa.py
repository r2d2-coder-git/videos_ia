"""Quality gate for every finished reel — run it before sending a video to Arturo.
Usage: motor/.venv/bin/python motor/qa.py <video.mp4> [--cuts 2.35,5.03,…] [--voz voz_sin_efectos.wav] [--expect texto.txt]
From code: qa.check(mp4, cuts=[…], expect="…")  (hybrid.run(cfg, "qa") and promo scripts pass their cut times).

Checks (each line prints OK or AVISO):
  formato   1080x1920, fps, SDR BT.709 tagged (not HLG), size
  voz       lead-in < 0.15 s, longest pause between phrases <= 0.35 s (Silero VAD on the output)
  cortes    at every cut: still voiced right before it = a word was probably clipped («2025» → «2020»)
  planos    shots shorter than 0.5 s (the stray "microframe" of his face between two graphics)
  texto     full transcript; with --expect, similarity to the expected script and the missing words
Outputs next to the video: <name>_hoja.jpg (one frame every 2 s)."""
import os, sys, json, subprocess, difflib, re
import numpy as np

SR = 16000
def sh(cmd): return subprocess.run(cmd, capture_output=True, text=True).stdout
def audio(mp4):
    raw = subprocess.run(["ffmpeg", "-nostdin", "-loglevel", "error", "-i", mp4, "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"],
                         capture_output=True).stdout
    return np.frombuffer(raw, np.float32).copy()

_W = None
def _whisper():
    global _W
    if _W is None:
        from faster_whisper import WhisperModel
        _W = WhisperModel("small", compute_type="int8")
    return _W

def clipped_words(a16, edl, starts):
    """For every take that ends mid-sentence, transcribe its last 1.6 s as cut and with 0.35 s more of the original.
    If the last word changes, the cut ate part of it (energy can't see this: cuts often land in a valley between
    two syllables, as with «2025» → «2020»). a16: original audio (16 kHz array). Returns [(output time, as cut, original)]."""
    norm = lambda t: re.sub(r"[^a-z0-9áéíóúñü ]", " ", t.lower()).split()
    pad = np.zeros(SR // 2, np.float32); m = _whisper(); out = []
    for (s, e), st in list(zip(edl, starts))[:-1]:
        lo = max(s, e - 1.6)
        def words(end):
            segs, _ = m.transcribe(np.concatenate([a16[int(lo * SR):int(end * SR)], pad]), language="es", condition_on_previous_text=False)
            return norm(" ".join(x.text for x in segs))
        cut, longer = words(e), words(e + 0.35)
        if not cut: continue
        sm = difflib.SequenceMatcher(None, cut, longer, autojunk=False)
        last_ok = any(i1 <= len(cut) - 1 < i2 for op, i1, i2, j1, j2 in sm.get_opcodes() if op == "equal")
        if not last_ok:                                   # the last word heard differs from the original one
            alt = next((longer[j1] for op, i1, i2, j1, j2 in sm.get_opcodes() if i1 <= len(cut) - 1 < i2 and j1 < len(longer)), "?")
            out.append((st + e - s, cut[-1], alt))
    return out

def check(mp4, cuts=None, expect=None, transcribe=True, voice=None, src_a16=None, edl=None):
    res = []; say = lambda ok, k, msg: (res.append((ok, k, msg)), print(f"{'OK   ' if ok else 'AVISO'} {k:8s} {msg}", flush=True))
    base = os.path.splitext(mp4)[0]
    # ---- formato
    pr = json.loads(sh(["ffprobe", "-v", "error", "-show_entries", "stream=codec_type,width,height,r_frame_rate,color_transfer,color_primaries:format=duration,size",
                        "-of", "json", mp4]))
    v = next(s for s in pr["streams"] if s["codec_type"] == "video"); dur = float(pr["format"]["duration"]); mb = int(pr["format"]["size"]) / 2**20
    say((v["width"], v["height"]) == (1080, 1920), "formato", f"{v['width']}x{v['height']} · {v['r_frame_rate']} fps · {dur:.1f} s · {mb:.1f} MB")
    trc = v.get("color_transfer", "?")
    say(trc == "bt709", "color", f"transfer={trc} primaries={v.get('color_primaries', '?')}"
        + ("  (HLG: se verá lavado; usa el máster SDR)" if trc == "arib-std-b67" else "")
        + ("  (sin etiqueta: añade h264_metadata BT.709)" if trc in ("?", None, "unknown") else ""))
    # ---- voz
    a = audio(mp4)
    from faster_whisper.vad import get_speech_timestamps, VadOptions
    ts = get_speech_timestamps(a, VadOptions(min_silence_duration_ms=100, speech_pad_ms=0))
    if ts:
        gaps = [((ts[i + 1]["start"] - ts[i]["end"]) / SR, ts[i]["end"] / SR) for i in range(len(ts) - 1)]
        mg = max(gaps) if gaps else (0, 0)
        say(ts[0]["start"] / SR < 0.15, "voz", f"arranque {ts[0]['start'] / SR:.2f} s")
        say(mg[0] <= 0.35, "voz", (f"pausa máx. {mg[0]:.2f} s en {mg[1]:.1f} s" if gaps else "voz continua, sin pausas detectables")
            + ("" if mg[0] <= 0.35 else "  (¿hueco o toma sobrante?)"))
    else:
        say(False, "voz", "no se detecta voz")
    # ---- cortes: voiced energy right before each cut means the cut fell inside a word
    av = audio(voice) if voice and os.path.exists(voice) else a                     # voice-only track if given (SFX fool the check)
    rms = np.sqrt(np.convolve(av ** 2, np.ones(160) / 160, "same"))[::160]           # 10 ms
    speech = np.median(rms[rms > np.percentile(rms, 60)]) if len(rms) else 0
    for c in (cuts or []):
        i = int(c * 100)
        if i < 8 or i >= len(rms): continue
        before = rms[i - 6:i - 2].mean()                                             # 20-60 ms before the cut (past the 15 ms fade)
        if before > 0.45 * speech:
            say(False, "cortes", f"corte en {c:.2f} s con voz justo antes (nivel {before / speech:.0%}): ¿palabra cortada? escúchalo / transcribe con la frase siguiente")
    if src_a16 is not None and edl:
        for t, w1, w2 in clipped_words(src_a16, edl, [0.0] + list(cuts or [])):
            say(False, "cortes", f"en {t:.2f} s se oye «{w1}» y en el original «{w2}»: el corte se come la palabra; alarga el fin de esa toma")
    if cuts: say(True, "cortes", f"{len(cuts)} cortes revisados")
    # ---- planos cortos (scene changes closer than 0.5 s)
    out = subprocess.run(["ffmpeg", "-nostdin", "-i", mp4, "-vf", "select='gt(scene,0.28)',showinfo", "-an", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    sc = [float(x) for x in re.findall(r"pts_time:([\d.]+)", out)]
    short = [(sc[k], sc[k + 1] - sc[k]) for k in range(len(sc) - 1) if sc[k + 1] - sc[k] < 0.5]
    say(not short, "planos", f"{len(sc)} cambios de plano" + "".join(f"  · plano de {d:.2f} s en {t:.2f} s" for t, d in short))
    # ---- hoja de fotogramas
    subprocess.run(["ffmpeg", "-nostdin", "-loglevel", "error", "-y", "-i", mp4, "-vf", "fps=1/2,scale=216:-1,tile=10x4", "-frames:v", "1",
                    base + "_hoja.jpg"])
    print(f"      hoja     {base}_hoja.jpg")
    # ---- texto
    if transcribe:
        segs, _ = _whisper().transcribe(a, language="es")
        text = " ".join(s.text.strip() for s in segs)
        print(f"      texto    {text}")
        if expect:
            norm = lambda t: re.sub(r"[^a-z0-9áéíóúñü ]", " ", t.lower()).split()
            e = open(expect).read() if os.path.exists(expect) else expect
            ratio = difflib.SequenceMatcher(None, norm(e), norm(text)).ratio()
            miss = [w for w in norm(e) if w not in set(norm(text))][:25]
            say(ratio > 0.85, "texto", f"parecido al guion {ratio:.0%}" + (f"  · faltan: {' '.join(miss)}" if miss else ""))
    n = sum(1 for ok, *_ in res if not ok)
    print(f"QA: {n} aviso(s)" if n else "QA: todo OK")
    return res

if __name__ == "__main__":
    args = sys.argv[1:]; mp4 = args[0]
    cuts = [float(x) for x in args[args.index("--cuts") + 1].split(",")] if "--cuts" in args else None
    voice = args[args.index("--voz") + 1] if "--voz" in args else None
    expect = args[args.index("--expect") + 1] if "--expect" in args else None
    check(mp4, cuts, expect, voice=voice)
