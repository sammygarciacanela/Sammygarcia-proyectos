import subprocess, os
SRC="/root/.claude/uploads/dcd155ca-a804-50d0-8338-cc367d9781ea/9a5a19fb-conecta-reel-50s.mp4"
L=0.0
A=[(0.00,0.00),(1.77,3.45),(3.83,5.55),(5.30,6.50),(8.77,11.85),(10.73,13.54),(14.03,16.20),(15.90,18.92),
   (16.70,19.38),(18.87,20.45),(19.93,22.50),(21.40,23.55),(22.47,24.34),(25.90,29.10),(29.37,33.74),
   (31.73,37.30),(33.93,40.86),(37.27,41.70),(38.57,41.80),(39.80,45.95),(42.10,48.50),(43.50,50.75),(44.53,51.88),(45.77,53.00),(50.00,57.23)]
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
    fn=f"b{i:02d}.mkv"
    subprocess.run(["ffmpeg","-v","error","-y","-ss",f"{va:.3f}","-t",f"{vb-va+0.2:.3f}","-i",SRC,"-an","-vf",vf,
        "-frames:v",str(n),"-c:v","libx264","-preset","veryfast","-crf","14","-r",str(FPS),fn],check=True)
    files.append(fn); print(f"{fn} video {va:5.2f}-{vb:5.2f} -> salida {fa/FPS:5.2f}-{fb/FPS:5.2f}  x{k:.2f} {mode}",flush=True)
open("blist.txt","w").write("".join(f"file '{f}'\n" for f in files))
