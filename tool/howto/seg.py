import json, sys, subprocess, os
def ass_time(t):
    t=max(0,t); h=int(t//3600); m=int(t%3600//60); s=t%60
    return f'{h}:{m:02d}:{s:05.2f}'
def build(name):
    d=f'rec/{name}'; m=json.load(open(f'{d}/meta.json'))
    t0,t1=m['t0'],m['t1']; fr=sorted(m['frames']); cuts=m.get('cuts',[])
    def mp(t):
        o=t
        for a,b in cuts:
            if t>=b: o-=(b-a)
            elif t>a: o-=(t-a)
        return o
    # frames inside a cut: keep only the last one, placed at the cut end
    keep=[]
    for f in fr:
        inside=[c for c in cuts if c[0]<f[0]<c[1]]
        if inside: keep.append((inside[0][1]-0.001,f[1]))
        else: keep.append(tuple(f))
    fr=[(mp(t),fn) for t,fn in sorted(keep)]
    m['caps']=[(mp(t),x) for t,x in m['caps']]
    t1=mp(t1)
    # last frame before t0 becomes first
    pre=[f for f in fr if f[0]<=t0]; post=[f for f in fr if t0<f[0]<t1]
    seq=([(t0,pre[-1][1])] if pre else [])+post
    if not seq: seq=[(t0,fr[0][1])]
    with open(f'{d}/list.txt','w') as L:
        for i,(t,fn) in enumerate(seq):
            nt=seq[i+1][0] if i+1<len(seq) else t1
            L.write(f"file '{os.path.abspath(fn)}'\nduration {max(0.001,nt-t):.4f}\n")
        L.write(f"file '{os.path.abspath(seq[-1][1])}'\n")
    caps=m['caps']
    with open(f'{d}/cap.ass','w') as A:
        A.write("""[Script Info]
ScriptType: v4.00+
PlayResX: 540
PlayResY: 1170
WrapStyle: 0

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: C,Nunito,33,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,-1,0,0,0,100,100,0,0,1,0,0,5,24,24,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
""")
        for i,(t,txt) in enumerate(caps):
            e=caps[i+1][0] if i+1<len(caps) else t1
            A.write(f"Dialogue: 0,{ass_time(t-t0)},{ass_time(e-t0-0.05)},C,,0,0,0,,{{\\pos(270,1110)}}{txt}\n")
    out=f'rec/{name}.mp4'
    vf=f"fps=15,scale=540:1050:flags=lanczos,pad=540:1170:0:0:color=0x2B2118,ass={d}/cap.ass:fontsdir=/usr/share/fonts/truetype/sand-box/google/Nunito"
    subprocess.run(['ffmpeg','-y','-loglevel','error','-f','concat','-safe','0','-i',f'{d}/list.txt','-vf',vf,'-c:v','libx264','-crf','14','-preset','fast','-pix_fmt','yuv420p','-r','15',out],check=True)
    print(out, round(t1-t0,1),'s', len(seq),'frames')
if __name__=='__main__':
    for n in sys.argv[1:]: build(n)
