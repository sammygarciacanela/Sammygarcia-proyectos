import json, re, unicodedata, numpy as np
from scipy.optimize import lsq_linear
W=json.load(open("vf_words.json")); FPS=30
norm=lambda s: unicodedata.normalize("NFD",re.sub(r"[^\wáéíóúñü]","",s.lower())).encode("ascii","ignore").decode()
ws=[norm(w["w"]) for w in W]; pos=[0]
def at(ph):
    p=ph.split(); i=next(i for i in range(pos[0],len(ws)) if ws[i:i+len(p)]==p); pos[0]=i; return W[i]["s"]
# escenas: (inicio, fin en el video, frase que arranca la escena, ajuste, [(segundo de aparición del texto, frase)])
SC=[(0.00,5.30,None,0,[(0.27,"si tus"),(0.83,"a su telefono"),(1.73,"que entre"),(3.23,"tu agencia"),(3.83,"perdiendo")]),
 (5.30,8.77,"lo lei",-0.05,[(6.53,"el juego")]),
 (8.77,14.03,"un equipo",-0.30,[(9.10,"un equipo"),(9.67,"no se conecta"),(10.70,"fracasara"),(11.40,"en su intento")]),
 (14.03,18.87,"en seguro",-0.20,[(14.27,"en seguro"),(15.07,"el agente"),(15.87,"solo"),(16.70,"se va")]),
 (18.87,21.40,"como lider",-0.25,[(19.10,"como lider"),(19.87,"intencional")]),
 (21.40,24.83,"crear espacios",-0.30,[(21.73,"crear espacios"),(22.40,"sin telefono")]),
 (24.83,28.30,"conversar mirando",-0.35,[(25.20,"conversar mirando"),(25.87,"a los ojos")]),
 (28.30,31.73,"usar el texto",-0.33,[(28.63,"usar el texto"),(29.30,"para sumar")]),
 (31.73,37.27,"en mi organizacion",-0.20,[(31.97,"en mi organizacion"),(32.67,"no reclutamos"),(33.90,"conectamos")]),
 (37.27,42.10,"y apoyamos",0.02,[(38.50,"que mas producen"),(39.67,"para que crezcan")]),
 (42.10,45.77,"quiere ser",-0.20,[(42.30,"quiere ser"),(42.90,"comenta"),(43.43,"equipo"),(44.50,"vamos")])]
starts=[0.0]; anchors=[]
for S,E,ph,off,an in SC:
    if ph: starts.append(at(ph)+off) if S>0 else None
    anchors.append([(vt,at(p)) for vt,p in an])
tend=W[-1]["e"]+0.45; starts.append(tend)
src=[]; report=[]
for k,(S,E,_,_,_) in enumerate(SC):
    o0,o1=starts[k],starts[k+1]; n=int(round(o1*FPS))-int(round(o0*FPS))
    lb=min(0.5,0.95*(E-S)/(n/FPS)); ub=2.5
    rows=[];b=[]
    for vt,ow in anchors[k]:
        j=int(round((ow-o0)*FPS)); r=np.zeros(n); r[:j]=1/FPS; rows.append(10*r); b.append(10*(vt-S))
    for i in range(1,n):
        r=np.zeros(n); r[i]=3; r[i-1]=-3; rows.append(r); b.append(0)
    for i in range(n):
        r=np.zeros(n); r[i]=0.3; rows.append(r); b.append(0.3)
    M=np.array(rows); bb=np.array(b)
    for it in range(3):
        s=lsq_linear(M,bb,bounds=(lb,ub)).x
        if S+s.sum()/FPS<=E-1/FPS: break
        r=np.full(n,1/FPS)*50; M=np.vstack([M,r]); bb=np.append(bb,50*(E-1/FPS-S))
    v=S+np.concatenate([[0],np.cumsum(s)[:-1]])/FPS
    src.extend(np.minimum(v,E-1/FPS))
    err=[ (np.searchsorted(v,vt)/FPS+o0)-ow for vt,ow in anchors[k]]
    report.append(f"escena {k:2d} vel {s.min():.2f}-{s.max():.2f}x | desfase texto vs palabra: "+" ".join(f"{e:+.2f}" for e in err))
# cierre a velocidad normal
n=int(round(4.23*FPS)); src.extend(45.77+np.arange(n)/FPS)
np.save("src_t.npy",np.array(src)); print("\n".join(report)); print("duración %.2f s"%(len(src)/FPS))
