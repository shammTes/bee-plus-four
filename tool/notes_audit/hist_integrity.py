#!/usr/bin/env python3
"""Byte-level History integrity check against a base ref (default fix/high-notes-round3).
1) Object level: every pre-existing card / exercise question / item, serialised exactly as stored (same key order,
   same characters), must still be present, byte-identical, and in the same relative order. New items may be
   INSERTED anywhere in an item list (cards, questions, ...) but every inserted item must be a new round-4 card
   (id containing '-r4'). Every other field (units, lessons, titles, glossary, games, exercise blocks) must be
   identical, with the same keys in the same order.
2) Text level: every line deleted by `git diff <ref>` in a History notes file must reappear as an added line that
   differs at most by a trailing comma (JSON list continuation).
Also checks the per-unit split files assets/high/notes/split/hist*-u*.json the same way."""
import json, subprocess, sys, glob, os
ref = sys.argv[1] if len(sys.argv) > 1 else 'fix/high-notes-round3'
bad = 0
stats = {}


def ser(x):
    return json.dumps(x, ensure_ascii=False)


def is_item(x):
    return isinstance(x, dict) and ('type' in x or 'q' in x) and 'cards' not in x and 'lessons' not in x


def walk(o, n, path, st):
    global bad
    if isinstance(o, dict):
        if not isinstance(n, dict) or list(n.keys()) != list(o.keys()):
            print('KEYS CHANGED', path); bad += 1; return
        for k in o:
            walk(o[k], n[k], path + '.' + k, st)
    elif isinstance(o, list):
        if not isinstance(n, list):
            print('NOT A LIST', path); bad += 1; return
        if o and all(is_item(x) for x in o) or (not o and n and all(is_item(x) for x in n)):
            # item list: old items must appear in order, byte-identical; extra items must be new r4 cards
            j = 0
            for x in o:
                sx = ser(x)
                while j < len(n) and ser(n[j]) != sx:
                    if '-r4' not in str(n[j].get('id', '')) if isinstance(n[j], dict) else True:
                        print('UNEXPECTED ITEM / ORDER CHANGE', f'{path}[{j}]', str(n[j].get('id') if isinstance(n[j], dict) else n[j])[:60]); bad += 1
                    else:
                        st['inserted'] += 1
                    j += 1
                if j == len(n):
                    print('ITEM MISSING OR CHANGED', path, x.get('id')); bad += 1
                    return
                st['items'] += 1
                j += 1
            for y in n[j:]:
                if isinstance(y, dict) and '-r4' in str(y.get('id', '')):
                    st['inserted'] += 1
                else:
                    print('UNEXPECTED ITEM', path, str(y)[:60]); bad += 1
        else:
            if len(n) != len(o):
                print('LIST LENGTH CHANGED', path, len(o), '->', len(n)); bad += 1; return
            for i, x in enumerate(o):
                walk(x, n[i], f'{path}[{i}]', st)
    elif ser(o) != ser(n):
        print('VALUE CHANGED', path, repr(o)[:60]); bad += 1


files = [f'assets/high/notes/notes/history_{g}.json' for g in (9, 10, 11, 12)]
files += sorted(glob.glob('assets/high/notes/split/hist*-u*.json'))
for p in files:
    try:
        old = json.loads(subprocess.check_output(['git', 'show', f'{ref}:{p}'], stderr=subprocess.DEVNULL))
    except subprocess.CalledProcessError:
        print('NEW FILE (no base)', p); bad += 1; continue
    st = {'items': 0, 'inserted': 0}
    walk(old, json.load(open(p, encoding='utf-8')), os.path.basename(p), st)
    stats[p] = st
for p in files[:4]:
    diff = subprocess.check_output(['git', 'diff', '-U0', ref, '--', p], text=True).splitlines()
    dels = [l[1:] for l in diff if l.startswith('-') and not l.startswith('---')]
    adds = set(l[1:] for l in diff if l.startswith('+') and not l.startswith('+++'))
    orphan = [l for l in dels if l + ',' not in adds and l not in adds]
    print(os.path.basename(p), f"old items byte-identical & in order: {stats[p]['items']}, new r4 cards inserted: {stats[p]['inserted']},",
          f'deleted lines: {len(dels)} (each only gained a trailing comma)' if not orphan else f'{len(orphan)} REAL DELETIONS')
    bad += len(orphan)
    for l in orphan[:5]:
        print('   DELETED:', l[:100])
sp = [p for p in files[4:] if p in stats]
print('split files checked:', len(sp), '- old items byte-identical & in order:', sum(stats[p]['items'] for p in sp),
      '- new r4 cards:', sum(stats[p]['inserted'] for p in sp))
print(('OK: every pre-existing History item is byte-identical and in its original relative order vs ' + ref) if not bad else f'{bad} PROBLEMS')
sys.exit(1 if bad else 0)
