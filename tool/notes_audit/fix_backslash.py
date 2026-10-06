"""Collapse doubled LaTeX backslashes (\\\\text -> \\text) left by a double-escaped import.
A real LaTeX row break (\\\\ followed by a letter inside matrices/vmatrix) is kept."""
import json, re, glob, os, sys
BASE = os.path.join(os.path.dirname(__file__), '..', '..', 'assets/high/notes/notes')
SKIP = ('physics', 'unit_phys', 'history', 'index')
CMD = re.compile(r'\\\\(?=[a-zA-Z{}])')
tot = 0
for f in sorted(glob.glob(os.path.join(BASE, '*.json'))):
    n = os.path.basename(f)
    if n.startswith(SKIP): continue
    b = json.load(open(f)); c = [0]
    def walk(o):
        if isinstance(o, dict): return {k: walk(v) for k, v in o.items()}
        if isinstance(o, list): return [walk(v) for v in o]
        if isinstance(o, str):
            if '\\begin{' in o: return o
            s, k = CMD.subn(r'\\', o); c[0] += k; return s
        return o
    b = walk(b)
    if c[0]:
        tot += c[0]; print(n, c[0])
        with open(f, 'w') as fh: json.dump(b, fh, ensure_ascii=False, indent=2); fh.write('\n')
print('total', tot)
