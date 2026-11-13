import subprocess, json, sys
sys.path.insert(0,'.')
from segs import SEGS, TAIL_FREEZE, AX, AY
FPS=30
q=lambda x: round(x*FPS)/FPS
G="eq=contrast=1.10:brightness=-0.035:saturation=0.95:gamma=0.96,huesaturation=saturation=-0.55:colors=y,colorbalance=rs=-0.04:gs=-0.01:bs=0.06:rh=0.03:bh=-0.03,vignette=angle=PI/4.6,unsharp=5:5:0.35"
SRC="IMG_4928.MOV"
out=[]; zp=None; T=0.0
for i,(a,b,z0,z1,mode) in enumerate(SEGS):
    a,b=q(a),q(b); d=b-a
    last = i==len(SEGS)-1
    D = d + (TAIL_FREEZE if last else 0)
    fn=f"seg{i:02d}.mkv"
    afl=f"afade=t=in:d=0.015,afade=t=out:st={d-0.02:.3f}:d=0.02" + (f",apad=whole_dur={D:.3f}" if last else "")
    if mode=='card':
        # Pantalla azul marino con Sammy dentro de un círculo dorado
        cw=800; cx=int(1080*AX-cw/2); cy=int(1920*AY-cw/2)
        fc=(f"color=c=0x0B1F3A:s=1080x1920:r={FPS}:d={D:.3f}[bg];"
            f"[0:v]{G},crop={cw}:{cw}:{max(cx,0)}:{cy},scale=w='2*trunc(600*(1+0.05*t/{D:.3f})/2)':h='2*trunc(600*(1+0.05*t/{D:.3f})/2)':eval=frame,crop=600:600,format=yuva420p[f];"
            f"[f][1:v]alphamerge[fc];[bg][fc]overlay=240:700:shortest=1[b1];[b1][2:v]overlay=232:692:shortest=1,format=yuv420p[v];"
            f"[0:a]{afl}[a]")
        cmd=["ffmpeg","-v","error","-y","-ss",f"{a:.4f}","-t",f"{d:.4f}","-i",SRC,"-loop","1","-i","mask.png","-loop","1","-i","ring.png","-filter_complex",fc]
        zend=z1
    else:
        start = zp if (mode=='ease' and zp is not None) else z0
        Z=(f"(st(0,min(t/{D:.3f},1))*0+{z0}+({z1}-{z0})*ld(0)*ld(0)*(3-2*ld(0))"
           f"+({start}-{z0})*(1-st(1,min(t/0.45,1))*ld(1)*(3-2*ld(1))))")
        pre = f"tpad=stop_mode=clone:stop_duration={TAIL_FREEZE}," if last else ""
        vf=(f"[0:v]{pre}scale=w='2*trunc(1080*{Z}/2)':h='2*trunc(1920*{Z}/2)':eval=frame:flags=bicubic,"
            f"crop=1080:1920:x='(iw-1080)*{AX}':y='(ih-1920)*{AY}',{G},format=yuv420p[v];[0:a]{afl}[a]")
        cmd=["ffmpeg","-v","error","-y","-ss",f"{a:.4f}","-t",f"{d:.4f}","-i",SRC,"-filter_complex",vf]
        zend=z1
    cmd+=["-map","[v]","-map","[a]","-r",str(FPS),"-c:v","libx264","-preset","veryfast","-crf","14","-c:a","pcm_s16le","-ar","48000","-ac","1",fn]
    import os
    if not os.path.exists(fn): subprocess.run(cmd,check=True)
    out.append({"file":fn,"src":[a,b],"out":[T,T+D],"mode":mode}); T+=D; zp=zend
    print(f"{fn} {a:.2f}-{b:.2f} -> {out[-1]['out'][0]:.2f}-{T:.2f}",flush=True)
json.dump(out,open("timeline.json","w"),indent=1)
open("list.txt","w").write("".join(f"file '{o['file']}'\n" for o in out))
