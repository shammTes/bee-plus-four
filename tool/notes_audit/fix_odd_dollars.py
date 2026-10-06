#!/usr/bin/env python3
"""Strings cut off inside display maths ("... ($$\\text{have/has/") -> drop the unfinished maths tail.
Only touches strings with an odd number of $$ (outside history). usage: fix_odd_dollars.py [--dry]"""
import glob, json, os, re, sys
NOTES = os.path.join(os.path.dirname(__file__), '..', '..', 'assets/high/notes/notes')
dry = '--dry' in sys.argv


def fix(s):
    i = s.rfind('$$')
    head = s[:i].rstrip()
    head = re.sub(r'[\s(|:,;=+→-]+$', '', head)
    head = re.sub(r'^\|\s*', '', head).replace(' | ', '; ')
    if head and head[-1] not in '.!?)$*':
        head += '.'
    return head


def walk(o, path, out):
    if isinstance(o, dict):
        for k, v in o.items():
            if isinstance(v, str) and k not in ('id', 'src') and v.count('$$') % 2:
                new = fix(v)
                out.append((path + '.' + k, v, new))
                o[k] = new
            else:
                walk(v, path + '.' + k, out)
    elif isinstance(o, list):
        for i, v in enumerate(o):
            if isinstance(v, str) and v.count('$$') % 2:
                new = fix(v)
                out.append((f'{path}[{i}]', v, new))
                o[i] = new
            else:
                walk(v, f'{path}[{i}]', out)


for p in sorted(glob.glob(os.path.join(NOTES, '*.json'))):
    if os.path.basename(p).startswith('history'):
        continue
    d = json.load(open(p, encoding='utf-8'))
    out = []
    walk(d, '', out)
    for path, a, b in out:
        print(os.path.basename(p), path, '\n   -', a[-90:], '\n   +', b[-90:])
    if out and not dry:
        open(p, 'w', encoding='utf-8').write(json.dumps(d, ensure_ascii=False, indent=2) + '\n')
