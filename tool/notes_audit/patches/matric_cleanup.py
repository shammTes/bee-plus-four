import sys, os, re, json, glob
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from patch import *
B = Book('chemistry_11')
a, b = B.card('chem11-u3-l3-3-mxw1'), B.card('chem11-u3-l3-4-mxw1')
if 'sulphuric' in a['problem']:
    B.remove('chem11-u3-l3-3-mxw1'); B.remove('chem11-u3-l3-4-mxw1')
    a['id'], b['id'] = 'chem11-u3-l3-4-mxw1', 'chem11-u3-l3-3-mxw1'
    B.add('chem11-u3-l3-4', [a]); B.add('chem11-u3-l3-3', [b])
B.save()
D = os.path.join(os.path.dirname(__file__), '../../../assets/high/notes/notes')
n = 0
for p in glob.glob(os.path.join(D, '*_*.json')):
    if os.path.basename(p).startswith(('physics', 'history', 'unit_')): continue
    d = json.load(open(p)); ch = False
    def walk(o):
        global n
        nonlocal_ch = False
        if isinstance(o, dict):
            if o.get('src') == 'matric':
                for k in ('q', 'problem'):
                    if isinstance(o.get(k), str) and re.match(r'\s*#+\s', o[k]):
                        o[k] = re.sub(r'^\s*#+\s*', '', o[k]); n += 1
            for v in o.values(): walk(v)
        elif isinstance(o, list):
            for v in o: walk(v)
    walk(d)
    json.dump(d, open(p, 'w'), ensure_ascii=False, indent=2); open(p, 'a').write('\n')
print('stripped headings', n)
