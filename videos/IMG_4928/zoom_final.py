import subprocess, sys
# (tiempo de salida, zoom): cada tramo es un acercamiento o alejamiento lento con curva suave
KF=[(0,1.00),(11.1,1.12),(15.6,1.03),(22.1,1.12),(26.7,1.03),(31.7,1.11),(36.3,1.02),(43.5,1.11),(48.5,1.02),(55.5,1.12)]
terms=[]
for (a,za),(b,zb) in zip(KF,KF[1:]):
    u=f"((t-{a})/{b-a})"
    terms.append(f"between(t,{a},{b}-0.0001)*({za}+({zb}-{za})*{u}*{u}*(3-2*{u}))")
terms.append(f"gte(t,{KF[-1][0]})*{KF[-1][1]}")
Z="("+"+".join(terms)+")"
src,ass,aud,out=sys.argv[1:5]
vf=(f"scale=w='2*trunc(1080*{Z}/2)':h='2*trunc(1920*{Z}/2)':eval=frame:flags=bicubic,"
    f"crop=1080:1920:x='(iw-1080)*0.40':y='(ih-1920)*0.44',ass={ass}")
subprocess.run(["ffmpeg","-v","error","-y","-i",src,"-i",aud,"-map","0:v","-map","1:a","-vf",vf,
  "-c:v","libx264","-preset","veryfast","-crf","19","-profile:v","high","-pix_fmt","yuv420p","-movflags","+faststart",
  "-c:a","aac","-b:a","192k","-shortest",out],check=True)
