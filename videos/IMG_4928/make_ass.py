import json, re, difflib, unicodedata
tl=json.load(open("timeline.json")); W=json.load(open("final_words.json"))  # [{w,s,e}] en tiempo de salida
CANON=("El ego no construye líderes. Porque si tú necesitas que constantemente la gente te vea como el jefe, quizás no has entendido lo que es el liderazgo. "
"Mira, con los años he aprendido algo. El liderazgo no se trata de siempre tener la razón, controlar todas las decisiones o buscar reconocimiento. "
"Porque cuando el ego dirige, la persona deja de sentirse valorada. Un verdadero líder escucha, reconoce sus errores, comparte su conocimiento y sobre todo, desarrolla personas. "
"Y esa muchas veces es la diferencia. Un líder inseguro necesita que todo dependa de él. Un líder humilde trabaja para que otros también triunfen. "
"Porque el éxito de un líder no se mide solamente por lo que logra personalmente, sino por las personas que ayuda a crecer. "
"Y ahora te pregunto, ¿tu equipo te sigue por tu posición o por cómo lo has ayudado? Te leo en los comentarios.")
toks=CANON.split()
norm=lambda s: unicodedata.normalize("NFD",re.sub(r"[^\wáéíóúñü]","",s.lower())).encode("ascii","ignore").decode()
A=[norm(t) for t in toks]; B=[norm(w["w"]) for w in W]
st=[None]*len(toks); en=[None]*len(toks)
for blk in difflib.SequenceMatcher(None,A,B,autojunk=False).get_matching_blocks():
    for k in range(blk.size): st[blk.a+k]=W[blk.b+k]["s"]; en[blk.a+k]=W[blk.b+k]["e"]
# interpolar palabras sin coincidencia
for i in range(len(toks)):
    if st[i] is None:
        p=next((en[j] for j in range(i-1,-1,-1) if en[j] is not None),0.0)
        n=next((st[j] for j in range(i+1,len(toks)) if st[j] is not None),p+0.3)
        st[i]=p; en[i]=n
def idx(phrase, start=0):
    p=phrase.split(); 
    for i in range(start,len(toks)):
        if [norm(t) for t in toks[i:i+len(p)]]==[norm(x) for x in p]: return i
    raise ValueError(phrase)
segout=[s["out"] for s in tl]
def ts(t):
    t=max(t,0); h=int(t//3600); m=int(t%3600//60); s=t%60
    return f"{h}:{m:02d}:{s:05.2f}"
GOLD="&H4CC9F2&"; WHITE="&HFFFFFF&"
KEY={"ego","lider","lideres","liderazgo","equipo","exito","crecer","personas"}
ev=[]
def dlg(layer,a,b,style,text): ev.append(f"Dialogue: {layer},{ts(a)},{ts(b)},{style},,0,0,0,,{text}")
def reveal(words_times, t0, alpha_on="&H00&"):
    out=[]
    for w,t in words_times:
        ms=max(0,int((t-t0)*1000))
        out.append(f"{{\\alpha&HFF&\\t({ms},{ms+140},\\alpha{alpha_on})}}{w}")
    return " ".join(out)
def fit(lines,size):
    n=max(len(" ".join(w for w,_ in L)) for L in lines)
    return min(size,int(940/(0.63*n)))
def bigtext(lines,t0,alpha_on="&H00&"):
    return "\\N".join(reveal(L,t0,alpha_on) for L in lines)
def title(a,b,small,big,y=330,size=110):
    """big: lista de líneas; cada línea = lista de (palabra, tiempo). y = borde superior del bloque grande"""
    if big and not isinstance(big[0],list): big=[big]
    fs=fit(big,size)
    if small: dlg(5,a,b,"TSmall",f"{{\\an2\\pos(540,{y+6})}}"+reveal(small,a))
    dlg(3,a,b,"TBig",f"{{\\an8\\pos(540,{y})\\fs{fs}\\c{GOLD}\\3c{GOLD}\\bord7\\blur14}}"+bigtext(big,a,"&HA8&"))
    dlg(4,a,b,"TBig",f"{{\\an8\\pos(540,{y})\\fs{fs}\\c{GOLD}}}"+bigtext(big,a))
    return y+len(big)*fs*1.21
hidden=[]   # ventanas sin subtítulos
def T(i): return st[i]
# 1) HOOK
i=idx("El ego no construye líderes.")
a,b=0.0,segout[0][1]
title(a,b,[("el",T(i)),("ego",T(i+1))],[[("NO",T(i+2)),("CONSTRUYE",T(i+3))],[("LÍDERES",T(i+4))]]); hidden.append((a,b))
# 2) Pantalla azul: Un verdadero LÍDER
card=[s for s in tl if s["mode"]=="card"][0]["out"]
i=idx("Un verdadero líder escucha,")
title(card[0],card[1],[("un",T(i)),("verdadero",T(i+1))],[("LÍDER",T(i+2))],y=470,size=150); hidden.append(tuple(card))
# 3) Lista #1–#4
items=[("escucha,","ESCUCHA"),("reconoce sus errores,","RECONOCE SUS ERRORES"),("comparte su conocimiento","COMPARTE LO QUE SABE"),("desarrolla personas.","DESARROLLA PERSONAS")]
starts=[T(idx(p,i)) for p,_ in items]
lend=en[idx("desarrolla personas.")+1]+0.35
for k,(p,txt) in enumerate(items):
    a=starts[k]; b=starts[k+1] if k<3 else lend
    dlg(1,a,b,"Num",f"{{\\an5\\pos(540,420)\\fad(120,0)}}#{k+1}")
    ws=txt.split(); lines=[ws] if len(txt)<=13 else [ws[:len(ws)//2], ws[len(ws)//2:]]
    lines=[[(w,a) for w in L] for L in lines]
    title(a,b,None,lines,y=330 if len(lines)==2 else 370,size=100)
hidden.append((starts[0],lend))
# 4) Inseguro vs humilde
i=idx("Un líder inseguro"); j=idx("todo dependa de él.")
a=st[i]-0.1; b=en[j+3]+0.25
title(a,b,[("líder",T(i+1)),("inseguro",T(i+2))],[[("TODO",T(j)),("DEPENDE",T(j+1))],[("DE",T(j+2)),("ÉL",T(j+3))]]); hidden.append((a,b))
i=idx("Un líder humilde"); j=idx("otros también triunfen.")
a=st[i]-0.05; b=en[j+2]+0.25
title(a,b,[("líder",T(i+1)),("humilde",T(i+2))],[("OTROS",T(j)),("TRIUNFAN",T(j+2))]); hidden.append((a,b))
# 5) El éxito se mide por las personas que ayudas a crecer
j=idx("sino por las personas que ayuda a crecer.")
a=st[j]-0.05; b=en[j+7]+0.35
title(a,b,[("el éxito se mide",a)],[[("LAS",T(j+2)),("PERSONAS",T(j+3))],[("QUE",T(j+4)),("AYUDAS",T(j+5)),("A",T(j+6)),("CRECER",T(j+7))]],size=96); hidden.append((a,b))
# 6) Pregunta final
j=idx("te sigue por tu posición"); k=idx("o por cómo lo has ayudado?")
a=st[j]-0.05; b=en[k+5]+0.35
title(a,b,[("¿te",T(j)),("siguen",T(j+1)),("por",T(j+2)),("tu",T(j+3)),("posición...",T(j+4))],
          [[("O",T(k)),("POR",T(k+1)),("CÓMO",T(k+2))],[("LOS",T(k+3)),("AYUDASTE?",T(k+4))]],size=104); hidden.append((a,b))
# 7) CTA + firma
j=idx("Te leo en los comentarios.")
end=tl[-1]["out"][1]; a=st[j]
dlg(2,a,end,"CTA","{\\an5\\pos(540,1430)\\fad(200,0)}compártelo con un líder que necesite escuchar esto")
s0=en[j+4]+0.15
yb=title(s0,end,None,[[("¡VAMOS",s0)],[("POR",s0+0.28),("TODO!",s0+0.56)]],y=330,size=130)
dlg(5,s0+0.7,end,"Firma",f"{{\\an8\\pos(540,{int(yb)+18})\\fad(200,0)}}Sammy García  ·  @sammygarcia"); hidden.append((s0,end))
# Subtítulos: bloques de 2–3 palabras, minúscula, palabra clave en dorado
def inhidden(t): return any(a-0.05<=t<b for a,b in hidden)
chunks=[]; cur=[]
for i,t in enumerate(toks):
    cur.append(i)
    brk = t[-1] in ",.?" or len(cur)==3 or (len(cur)==2 and i+1<len(toks) and len(toks[i+1])<=2 and toks[i+1][-1] not in ",.?")
    if brk: chunks.append(cur); cur=[]
if cur: chunks.append(cur)
for n,c in enumerate(chunks):
    a=st[c[0]]; b=min(en[c[-1]]+0.25, st[chunks[n+1][0]] if n+1<len(chunks) else en[c[-1]]+0.4)
    if inhidden(a) or inhidden((a+b)/2): continue
    words=[]
    for i in c:
        w=re.sub(r"[.,]","",toks[i]).lower()
        words.append(f"{{\\c{GOLD}\\b1}}{w}{{\\c{WHITE}\\b0}}" if norm(w) in KEY else w)
    dlg(0,a,b,"Sub","{\\an5\\pos(540,1330)}"+" ".join(words))
hdr="""[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 0
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Sub,Inter SemiBold,48,&H00FFFFFF,&H00FFFFFF,&H90000000,&H70000000,0,0,0,0,100,100,0,0,1,3,2,5,80,80,0,1
Style: TSmall,Inter Display ExtraBold,58,&H00FFFFFF,&H00FFFFFF,&H90000000,&H80000000,0,0,0,0,100,100,0,0,1,2,3,5,70,70,0,1
Style: TBig,Inter Display Black,104,&H004CC9F2,&H004CC9F2,&H00000000,&H90000000,0,0,0,0,100,100,-1,0,1,0,4,5,60,60,0,1
Style: Num,Inter Display Black,420,&HB44CC9F2,&HB44CC9F2,&H00000000,&H00000000,0,0,0,0,100,100,-4,0,1,0,0,9,40,40,0,1
Style: CTA,Inter SemiBold,40,&H00FFFFFF,&H00FFFFFF,&H90000000,&H70000000,0,0,0,0,100,100,0,0,1,3,2,5,90,90,0,1
Style: Firma,Inter Display ExtraBold,44,&H00FFFFFF,&H00FFFFFF,&H90000000,&H70000000,0,0,0,0,100,100,1,0,1,2,2,5,60,60,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
open("edit.ass","w").write(hdr+"\n".join(ev)+"\n")
print(len(ev),"eventos")
