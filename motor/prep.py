"""Prepare a raw recording for the hybrid "entrevista técnica" editor.
Usage: .venv/bin/python prep.py <name> <video>
Writes <name>_a16.npy (16 kHz mono audio, used by build_edl) and <name>_pieces.json (Silero VAD pieces, each one
transcribed on its own with word timestamps in ORIGINAL seconds) next to this file, and prints every piece so the
best take of each sentence can be chosen."""
import os, sys, json, subprocess
import numpy as np
from faster_whisper import WhisperModel
from faster_whisper.vad import get_speech_timestamps, VadOptions

HERE = os.path.dirname(os.path.abspath(__file__))
name, src = sys.argv[1], sys.argv[2]
info = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height,color_transfer,r_frame_rate",
                       "-of", "default=nw=1", src], capture_output=True, text=True).stdout
print(info.strip())
if "arib-std-b67" in info:
    print("!! HDR (HLG) source: make an SDR master first (swift hdr2prores.swift in.MOV master.mov) and edit from that")
raw = subprocess.run(["ffmpeg", "-nostdin", "-loglevel", "error", "-i", src, "-ac", "1", "-ar", "16000", "-f", "f32le", "-"],
                     capture_output=True, check=True).stdout          # faster_whisper.decode_audio breaks with new PyAV
a = np.frombuffer(raw, np.float32).copy()
np.save(os.path.join(HERE, f"{name}_a16.npy"), a)
sp = [(t["start"] / 16000, t["end"] / 16000) for t in get_speech_timestamps(
    a, VadOptions(threshold=0.5, min_silence_duration_ms=100, speech_pad_ms=0, min_speech_duration_ms=80))]
m = WhisperModel("small", device="cpu", compute_type="int8")
pieces = []
for s, e in sp:
    clip = a[int(max(0, s - 0.03) * 16000):int((e + 0.03) * 16000)]
    segs, _ = m.transcribe(clip, language="es", beam_size=5, condition_on_previous_text=False, word_timestamps=True)
    ws = [[round(w.start + s - 0.03, 2), round(w.end + s - 0.03, 2), w.word.strip()] for x in segs for w in x.words]
    pieces.append({"s": round(s, 2), "e": round(e, 2), "text": " ".join(w[2] for w in ws), "words": ws})
    print(f"{s:7.2f}-{e:7.2f}  {pieces[-1]['text']}", flush=True)
json.dump(pieces, open(os.path.join(HERE, f"{name}_pieces.json"), "w"), ensure_ascii=False)
print(f"{len(pieces)} pieces · {len(a) / 16000:.1f} s · words: motor/{name}_pieces.json")
