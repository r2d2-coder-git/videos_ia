"""Voz y tiempos de una historia.
  ../motor/.venv/bin/python voz.py provisional <id>          voz sintética (Mónica, macOS) del guion → <id>/voz.wav + tiempos
  ../motor/.venv/bin/python voz.py tiempos <id> [audio]      transcribe la voz real (o voz.wav) → <id>/voz.tiempos.json

voz.tiempos.json = {"duracion", "provisional", "palabras": [{"p","ini","fin"}], "frases": [{"texto","ini","fin"}]}
Las palabras son las del GUION (con su puntuación) con el tiempo oído: así los subtítulos dicen exactamente el guion."""
import json, os, re, subprocess, sys, tempfile, difflib, unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
SR = 48000


def guion_texto(id_):
    """Texto hablado del guion: sin títulos markdown ni comentarios; [pausa N] se conserva como marca."""
    src = open(os.path.join(HERE, id_, "guion.md"), encoding="utf-8").read()
    src = re.sub(r"<!--.*?-->", "", src, flags=re.S)
    lines = [l.strip() for l in src.splitlines()]
    return [l for l in lines if l and not l.startswith("#") and not l.startswith(">")]


def palabras_guion(id_):
    return [w for l in guion_texto(id_) for w in re.sub(r"\[pausa [\d.]+\]", " ", l).split()]


def limpia(w):
    w = unicodedata.normalize("NFD", w.lower())
    w = "".join(c for c in w if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-z0-9ñ%]", "", w)


def provisional(id_):
    out = os.path.join(HERE, id_, "voz.wav")
    tmp = tempfile.mkdtemp(prefix="voz_")
    parts = []
    for k, l in enumerate(guion_texto(id_)):
        m = re.fullmatch(r"\[pausa ([\d.]+)\]", l)
        if m:
            parts.append(("sil", float(m.group(1)))); continue
        aiff = os.path.join(tmp, f"{k}.aiff")
        subprocess.run(["say", "-v", "Mónica", "-r", "160", "-o", aiff, re.sub(r"\[pausa [\d.]+\]", ", ", l)], check=True)
        parts.append(("aud", aiff)); parts.append(("sil", 0.35))
    lst = os.path.join(tmp, "lista.txt")
    with open(lst, "w") as f:
        for k, (kind, v) in enumerate(parts):
            if kind == "aud":
                wav = v + ".wav"
                subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", v, "-ar", str(SR), "-ac", "1", wav], check=True)
            else:
                wav = os.path.join(tmp, f"sil_{k}.wav")
                subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "lavfi", "-i", f"anullsrc=r={SR}:cl=mono", "-t", str(v), wav], check=True)
            f.write(f"file '{wav}'\n")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst,
                    "-af", "loudnorm=I=-18:TP=-2", "-ar", str(SR), "-ac", "1", out], check=True)
    tiempos(id_, out, provisional=True)


def silencios(audio, db=-35, dur=0.4):
    """Tramos de silencio [(ini, fin)] de más de `dur` s."""
    err = subprocess.run(["ffmpeg", "-i", audio, "-af", f"silencedetect=noise={db}dB:d={dur}", "-f", "null", "-"], capture_output=True, text=True).stderr
    ini = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", err)]
    fin = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", err)]
    return list(zip(ini, fin))


def tiempos(id_, audio=None, provisional=False):
    from faster_whisper import WhisperModel
    audio = audio or os.path.join(HERE, id_, "voz.wav")
    model = WhisperModel("small", device="cpu", compute_type="int8")
    # PyAV 19 no acepta un argumento que usa faster-whisper al decodificar: le pasamos el audio ya en 16 kHz
    pcm = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", audio, "-ac", "1", "-ar", "16000", "-f", "s16le", "-"], capture_output=True, check=True).stdout
    import numpy as np
    segs, info = model.transcribe(np.frombuffer(pcm, np.int16).astype(np.float32) / 32768, language="es", word_timestamps=True)
    oidas = [(w.word.strip(), w.start, w.end) for s in segs for w in s.words]
    guion = palabras_guion(id_)
    # alinea palabras del guion con las oídas; las que Whisper se come se reparten en su hueco
    sm = difflib.SequenceMatcher(a=[limpia(w) for w in guion], b=[limpia(w[0]) for w in oidas], autojunk=False)
    t = [None] * len(guion)
    for a, b, n in sm.get_matching_blocks():
        for k in range(n):
            t[a + k] = (oidas[b + k][1], oidas[b + k][2])
    known = [i for i, x in enumerate(t) if x]
    for i in range(len(t)):
        if t[i]: continue
        prev = max([k for k in known if k < i], default=None); nxt = min([k for k in known if k > i], default=None)
        a = t[prev][1] if prev is not None else 0.0
        b = t[nxt][0] if nxt is not None else info.duration
        gap = [k for k in range(len(t)) if (prev is None or k > prev) and (nxt is None or k < nxt)]
        j = gap.index(i); step = (b - a) / len(gap)
        t[i] = (a + j * step, a + (j + 1) * step)
    # Whisper a veces adelanta la primera palabra tras una pausa: si empieza dentro de un silencio, va al final de él
    sil = silencios(audio)
    for i, (s, e) in enumerate(t):
        for a, b in sil:
            dentro = a + 0.05 < s < b - 0.05                            # empieza dentro del silencio
            cubre = s < b and min(e, b) - max(s, a) > 0.5 * (b - a)      # o se estira por encima de casi todo él
            if dentro or cubre:
                t[i] = (b, max(e, b + 0.12)); break
    palabras = [{"p": w, "ini": round(s, 3), "fin": round(e, 3)} for w, (s, e) in zip(guion, t)]
    frases, cur = [], []
    for w in palabras:
        cur.append(w)
        if re.search(r"[.?!…]$", w["p"]):
            frases.append({"texto": " ".join(x["p"] for x in cur), "ini": cur[0]["ini"], "fin": cur[-1]["fin"]}); cur = []
    if cur: frases.append({"texto": " ".join(x["p"] for x in cur), "ini": cur[0]["ini"], "fin": cur[-1]["fin"]})
    acierto = sum(1 for a, b, n in sm.get_matching_blocks() for _ in range(n)) / max(1, len(guion))
    data = {"duracion": round(info.duration, 3), "provisional": provisional, "acierto": round(acierto, 3), "palabras": palabras, "frases": frases}
    json.dump(data, open(os.path.join(HERE, id_, "voz.tiempos.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"tiempos ok · {info.duration:.1f} s · {len(palabras)} palabras · {acierto:.0%} oídas tal cual")


if __name__ == "__main__":
    cmd, id_ = sys.argv[1], sys.argv[2]
    if cmd == "provisional": provisional(id_)
    elif cmd == "tiempos": tiempos(id_, sys.argv[3] if len(sys.argv) > 3 else None)
