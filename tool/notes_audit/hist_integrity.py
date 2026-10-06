#!/usr/bin/env python3
"""Byte-level History integrity check against a base ref (default fix/high-notes-round2).
1) Object level: every pre-existing card / exercise question / other field, serialised exactly as stored
   (same key order, same characters), must be byte-identical and at the same position; only appended items allowed.
2) Text level: every line deleted by `git diff <ref>` in a History notes file must reappear as an added line that differs
   only by a trailing comma (JSON list continuation when items are appended).
Also checks the per-unit split files assets/high/notes/split/hist*-u*.json the same way (object level)."""
import json, subprocess, sys, glob, os
ref = sys.argv[1] if len(sys.argv) > 1 else 'fix/high-notes-round2'
bad = 0
stats = {}


def ser(x):
    return json.dumps(x, ensure_ascii=False)


def walk(o, n, path, st):
    global bad
    if isinstance(o, dict):
        if not isinstance(n, dict) or list(n.keys())[:len(o)] != list(o.keys()):
            # keys may only be added at the end (e.g. a unit gaining an 'exercise' block)
            if not isinstance(n, dict) or [k for k in n if k in o] != list(o):
                print('KEYS CHANGED', path); bad += 1; return
        for k in o:
            walk(o[k], n[k], path + '.' + k, st)
    elif isinstance(o, list):
        if not isinstance(n, list) or len(n) < len(o):
            print('LIST SHRANK', path); bad += 1; return
        for i, x in enumerate(o):
            if isinstance(x, dict) and ('type' in x or 'q' in x) and 'cards' not in x and 'lessons' not in x:
                st['items'] += 1
                if ser(x) != ser(n[i]):
                    print('ITEM CHANGED', f'{path}[{i}]', x.get('id')); bad += 1
            else:
                walk(x, n[i], f'{path}[{i}]', st)
        st['appended'] += len(n) - len(o)
    elif ser(o) != ser(n):
        print('VALUE CHANGED', path, repr(o)[:60]); bad += 1


files = [f'assets/high/notes/notes/history_{g}.json' for g in (9, 10, 11, 12)]
files += sorted(glob.glob('assets/high/notes/split/hist*-u*.json'))
for p in files:
    try:
        old = json.loads(subprocess.check_output(['git', 'show', f'{ref}:{p}'], stderr=subprocess.DEVNULL))
    except subprocess.CalledProcessError:
        print('NEW FILE (no base)', p); continue
    st = {'items': 0, 'appended': 0}
    walk(old, json.load(open(p, encoding='utf-8')), os.path.basename(p), st)
    stats[p] = st
for p in files[:4]:
    diff = subprocess.check_output(['git', 'diff', '-U0', ref, '--', p], text=True).splitlines()
    dels = [l[1:] for l in diff if l.startswith('-') and not l.startswith('---')]
    adds = set(l[1:] for l in diff if l.startswith('+') and not l.startswith('+++'))
    orphan = [l for l in dels if l + ',' not in adds and l not in adds]
    print(os.path.basename(p), f"pre-existing items byte-identical: {stats[p]['items']}, appended: {stats[p]['appended']},",
          f'deleted lines: {len(dels)} (all only gained a trailing comma)' if not orphan else f'{len(orphan)} REAL DELETIONS')
    bad += len(orphan)
    for l in orphan[:5]:
        print('   DELETED:', l[:100])
sp = [p for p in files[4:] if p in stats]
print('split files checked:', len(sp), 'pre-existing items byte-identical:', sum(stats[p]['items'] for p in sp))
print('OK: History teacher text byte-identical to', ref if not bad else f'{bad} PROBLEMS')
sys.exit(1 if bad else 0)
