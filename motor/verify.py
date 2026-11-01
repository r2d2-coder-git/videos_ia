import sys, subprocess, numpy as np
from faster_whisper.vad import get_speech_timestamps, VadOptions
for f in sys.argv[1:]:
    raw = subprocess.run(["ffmpeg","-nostdin","-loglevel","error","-i",f,"-ac","1","-ar","16000","-f","f32le","-"],capture_output=True).stdout
    a = np.frombuffer(raw, np.float32)
    ts = get_speech_timestamps(a, VadOptions(min_silence_duration_ms=100, speech_pad_ms=0))
    if not ts:
        print(f, "sin voz"); continue
    gaps = [(ts[i+1]["start"]-ts[i]["end"])/16000 for i in range(len(ts)-1)]
    mg = max(gaps) if gaps else 0; at = ts[[g for g in gaps].index(mg)]["end"]/16000 if gaps else 0
    print(f"{f.split('/')[-1]:40s} dur {len(a)/16000:6.1f}s  lead {ts[0]['start']/16000:.2f}s  maxgap {mg:.2f}s @ {at:.1f}s")
