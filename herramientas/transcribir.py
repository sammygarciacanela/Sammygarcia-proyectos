import sys, json
from faster_whisper import WhisperModel
m = WhisperModel(sys.argv[2] if len(sys.argv)>2 else "medium", device="cpu", compute_type="int8")
import wave, numpy as np
w=wave.open(sys.argv[1]); a=np.frombuffer(w.readframes(w.getnframes()),dtype=np.int16).astype(np.float32)/32768
segs, info = m.transcribe(a, language="es", word_timestamps=True, vad_filter=False)
out=[]
for s in segs:
    print(f"[{s.start:6.2f}-{s.end:6.2f}] {s.text.strip()}", flush=True)
    out.append({"start":s.start,"end":s.end,"text":s.text.strip(),"words":[{"w":w.word,"s":w.start,"e":w.end} for w in s.words]})
json.dump(out, open(sys.argv[1]+".json","w"), ensure_ascii=False, indent=1)
