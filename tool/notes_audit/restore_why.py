import json,glob,os,re
d=json.load(open('/workspace/tmp-sync/drive/Study_Notes.json'))
expl={}
def walk(o):
    if isinstance(o,dict):
        if 'question' in o and 'explanation' in o and isinstance(o['explanation'],str):
            expl.setdefault(o['question'].strip(),[]).append(o['explanation'])
        for v in o.values(): walk(v)
    elif isinstance(o,list):
        for v in o: walk(v)
walk(d)
tot=0
for f in sorted(glob.glob('assets/high/notes/notes/*.json')):
    n=os.path.basename(f)
    if n.startswith(('physics','unit_phys','history','index')): continue
    b=json.load(open(f)); ch=0
    for u in b.get('units',[]):
        for l in u['lessons']:
            for c in l['cards']:
                if c.get('type')=='check' and isinstance(c.get('why'),str):
                    w=c['why']; cand=expl.get((c.get('q') or '').strip(),[])
                    for e in cand:
                        if len(e)>len(w)+5 and e.startswith(w[:len(w)-3]) :
                            c['why']=e; ch+=1; break
                if c.get('type')=='worked':
                    pass
    if ch:
        tot+=ch; print(n,ch)
        open(f,'w').write(json.dumps(b,ensure_ascii=False,indent=2)+'\n')
print(tot)
