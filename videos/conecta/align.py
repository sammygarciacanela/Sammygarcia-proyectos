import subprocess, os
SRC="/root/.claude/uploads/dcd155ca-a804-50d0-8338-cc367d9781ea/9a5a19fb-conecta-reel-50s.mp4"
L=2.14   # segundo de la voz donde arranca el video
# (segundo en el video, segundo en la voz) — cada texto cae cuando Sammy lo dice
A=[(0.00,2.14),(1.77,5.40),(3.83,7.76),(5.30,8.90),(8.77,13.50),(10.73,15.24),(14.03,17.00),(15.90,19.22),
   (16.70,19.84),(18.87,21.15),(19.93,22.94),(21.40,23.70),(22.47,24.40),(25.90,28.92),(29.37,32.16),
   (31.73,35.20),(33.93,37.60),(37.27,38.30),(38.57,38.50),(42.10,42.70),(43.50,44.10),(44.53,45.06),(45.77,46.00),(50.00,50.23)]
FPS=30; files=[]
for i,((va,ta),(vb,tb)) in enumerate(zip(A,A[1:])):
    fa=round((ta-L)*FPS); fb=round((tb-L)*FPS); n=fb-fa; d=n/FPS
    k=d/(vb-va)
    if k<0.65:   # retención demasiado larga: se recorta a velocidad normal
        vf=f"fps={FPS},tpad=stop_mode=clone:stop_duration=1"; mode="recorte"
    elif k>1.05: # se alarga con interpolación suave
        vf=f"setpts={k:.5f}*(PTS-STARTPTS),minterpolate=fps={FPS}:mi_mode=blend,tpad=stop_mode=clone:stop_duration=1"; mode="lento"
    else:
        vf=f"setpts={k:.5f}*(PTS-STARTPTS),fps={FPS},tpad=stop_mode=clone:stop_duration=1"; mode="normal" if k>0.95 else "rápido"
    fn=f"a{i:02d}.mkv"
    subprocess.run(["ffmpeg","-v","error","-y","-ss",f"{va:.3f}","-t",f"{vb-va+0.2:.3f}","-i",SRC,"-an","-vf",vf,
        "-frames:v",str(n),"-c:v","libx264","-preset","veryfast","-crf","14","-r",str(FPS),fn],check=True)
    files.append(fn); print(f"{fn} video {va:5.2f}-{vb:5.2f} -> salida {fa/FPS:5.2f}-{fb/FPS:5.2f}  x{k:.2f} {mode}",flush=True)
open("alist.txt","w").write("".join(f"file '{f}'\n" for f in files))
