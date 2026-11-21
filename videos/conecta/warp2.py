import json, subprocess, numpy as np, sys
from scipy.interpolate import PchipInterpolator
SRC="/root/.claude/uploads/dcd155ca-a804-50d0-8338-cc367d9781ea/9a5a19fb-conecta-reel-50s.mp4"
OUT=sys.argv[2]
FPS=30; W,H=1080,1920
src_t=np.load(sys.argv[1]); N=len(src_t)
sl=np.diff(src_t)*FPS
print("velocidad: mín %.2fx máx %.2fx"%(sl.min(),sl.max()))
dec=subprocess.Popen(["ffmpeg","-v","error","-i",SRC,"-f","rawvideo","-pix_fmt","rgb24","-"],stdout=subprocess.PIPE)
enc=subprocess.Popen(["ffmpeg","-v","error","-y","-f","rawvideo","-pix_fmt","rgb24","-s",f"{W}x{H}","-r",str(FPS),"-i","-",
     "-c:v","libx264","-preset","veryfast","-crf","16","-pix_fmt","yuv420p",OUT],stdin=subprocess.PIPE)
fs=W*H*3; buf={}; nxt=0
def get(i):
    global nxt
    while nxt<=i:
        b=dec.stdout.read(fs)
        if len(b)<fs: return buf[max(buf)]
        buf[nxt]=np.frombuffer(b,dtype=np.uint8).reshape(H,W,3); nxt+=1
        for k in [k for k in buf if k<nxt-3]: del buf[k]
    return buf.get(i, buf[max(buf)])
for n in range(N):
    p=src_t[n]*FPS; i=int(p); a=p-i
    f0=get(i)
    if a<0.08: fr=f0
    elif a>0.92: fr=get(i+1)
    else: fr=(f0*(1-a)+get(i+1)*a).astype(np.uint8)   # mezcla de cuadros para cámara lenta fluida
    enc.stdin.write(fr.tobytes())
enc.stdin.close(); enc.wait(); dec.kill()
print("listo",N,"cuadros")
