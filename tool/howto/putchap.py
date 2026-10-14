import json,re
S=1.45
ch=json.load(open('chapters.json'))
p='/workspace/wt-howto/lib/high/screens/how_to_video.dart';s=open(p).read()
body='\n'.join(f"  ({int(ms/S)}, {json.dumps(t,ensure_ascii=False).replace(chr(34),chr(39))})," for ms,t in ch)
s=re.sub(r"  // CHAPTERS-BEGIN\n.*?  // CHAPTERS-END",f"  // CHAPTERS-BEGIN\n{body}\n  // CHAPTERS-END",s,flags=re.S)
open(p,'w').write(s)
with open('chapters.txt','w') as f:
    for ms,t in ch: ms=int(ms/S); f.write(f'{ms//60000}:{ms//1000%60:02d} {t}\n')
print(open('chapters.txt').read())
