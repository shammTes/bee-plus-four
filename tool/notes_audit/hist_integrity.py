#!/usr/bin/env python3
"""Byte-level History integrity check against a base ref (default fix/high-notes-round3).
1) Object level: every pre-existing card / exercise question / item, serialised exactly as stored (same key order,
   same characters), must still be present, byte-identical, and in the same relative order. New items may be
   INSERTED anywhere in an item list (cards, questions, ...) but every inserted item must be a new round-4 card
   (id containing '-r4'). Every other field (units, lessons, titles, glossary, games, exercise blocks) must be
   identical, with the same keys in the same order.
2) Text level: every line deleted by `git diff <ref>` in a History notes file must reappear as an added line that
   differs at most by a trailing comma (JSON list continuation).
Also checks the per-unit split files assets/high/notes/split/hist*-u*.json the same way.
3) Owner-approved corrections: APPROVED lists the ONLY permitted edits to pre-existing teacher text (card id, old
   substring, new substring). For those cards the old card with exactly that one substitution applied must match the
   new card byte-for-byte, and every approved edit must be present (applied exactly once) in the notes file and in
   the split file that contains the card. Any other difference is still reported."""
import json, subprocess, sys, glob, os
ref = sys.argv[1] if len(sys.argv) > 1 else 'fix/high-notes-round3'
bad = 0
stats = {}
# Approved by the owner on 2026-10-06 (PR #31): correct 4 dates/figures to match the Grade 10/11 History textbooks.
APPROVED = [(i, a, b, 'teacher-text correction') for i, a, b in [
    ('hist10-u9-n04', 'captured Kabul (Afghanistan) in 1508', 'captured Kabul (Afghanistan) in 1504'),
    ('hist11-u3-n28', 'communist manifesto written in 1875', 'communist manifesto written in 1848'),
    ('hist11-u10-n01', 'Manchuria in 1939 and invade invaded Beijing and Nanjing in 1936',
     'Manchuria in 1931 and invade invaded Beijing and Nanjing in 1937'),
    ('hist11-u12-n09', '9 peoples were killed and 534 were wounded', 'scores of people were killed and over 80 were wounded'),
]]
# Own-content corrections (approved 2026-10-06): round-3 practice items (src "r3", added by us, not teacher text) that
# repeated the wrong figures. Substitutions are applied in order to the item's compact serialisation.
APPROVED += [(i, a, b, 'own-content correction (r3 item)') for i, a, b in [
    ('hist10-u9-r3q04', 'who captured Kabul in 1508', 'who captured Kabul in 1504'),
    ('hist11-u12-t9-r3c2', '"How many people were killed in the suppression of the 1958 strike?"',
     '"Roughly how many people were wounded when the 1958 workers\' demonstration was suppressed?"'),
    ('hist11-u12-t9-r3c2', '"A": "90"', '"A": "About 20"'),
    ('hist11-u12-t9-r3c2', '"B": "900"', '"B": "Over 80"'),
    ('hist11-u12-t9-r3c2', '"C": "9"', '"C": "About 500"'),
    ('hist11-u12-t9-r3c2', '"D": "534"', '"D": "Over 1,000"'),
    ('hist11-u12-t9-r3c2', '"answer": "C"', '"answer": "B"'),
    ('hist11-u12-t9-r3c2', 'civilians: 9 people were killed and 534 wounded.', 'civilians: scores of people were killed and over 80 were wounded.'),
    ('hist11-u12-t9-r3wk4', '9 killed, 534 wounded; organisers jailed', 'scores of people killed and over 80 wounded; organisers jailed'),
    ('hist11-u12-t9-r3wk4', 'crushed (9 killed, 534 wounded)', 'crushed (scores of people killed and over 80 wounded)'),
]]
APPROVED_BY_ID = {}
for _id, _a, _b, _k in APPROVED:
    APPROVED_BY_ID.setdefault(_id, []).append((_a, _b))
applied = {}  # file -> list of applied (id, old) pairs


def ser(x):
    return json.dumps(x, ensure_ascii=False)


def expected(x, st):
    """Serialisation the old item must have now: unchanged, or with its approved substitution(s) applied."""
    sx = ser(x)
    for a, b in APPROVED_BY_ID.get(x.get('id') if isinstance(x, dict) else None, []):
        if sx.count(a) != 1:
            return sx
        sx = sx.replace(a, b)
    return sx


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
                sx = expected(x, st)
                while j < len(n) and ser(n[j]) != sx:
                    if '-r4' not in str(n[j].get('id', '')) if isinstance(n[j], dict) else True:
                        print('UNEXPECTED ITEM / ORDER CHANGE', f'{path}[{j}]', str(n[j].get('id') if isinstance(n[j], dict) else n[j])[:60]); bad += 1
                    else:
                        st['inserted'] += 1
                    j += 1
                if j == len(n):
                    print('ITEM MISSING OR CHANGED', path, x.get('id')); bad += 1
                    return
                if sx != ser(x):
                    st['approved'].append(x.get('id'))
                else:
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
    st = {'items': 0, 'inserted': 0, 'approved': []}
    walk(old, json.load(open(p, encoding='utf-8')), os.path.basename(p), st)
    stats[p] = st
for p in files[:4]:
    diff = subprocess.check_output(['git', 'diff', '-U0', ref, '--', p], text=True).splitlines()
    dels = [l[1:] for l in diff if l.startswith('-') and not l.startswith('---')]
    adds = set(l[1:] for l in diff if l.startswith('+') and not l.startswith('+++'))
    def fixed(l):
        for _id, a, b, _k in APPROVED:
            l = l.replace(a, b)
        return l
    orphan = [l for l in dels if l + ',' not in adds and l not in adds and fixed(l) not in adds and fixed(l) + ',' not in adds]
    corrected = [l for l in dels if fixed(l) != l and (fixed(l) in adds or fixed(l) + ',' in adds)]
    print(os.path.basename(p), f"old items byte-identical & in order: {stats[p]['items']}, new r4 cards inserted: {stats[p]['inserted']},",
          f'deleted lines: {len(dels)} (approved corrections: {len(corrected)}, the rest only gained a trailing comma)' if not orphan else f'{len(orphan)} REAL DELETIONS')
    bad += len(orphan)
    for l in orphan[:5]:
        print('   DELETED:', l[:100])
# every approved edit must be applied exactly once in the notes file and in its split file
for _id, a, b, kind in APPROVED:
    hits = [p for p in stats if _id in stats[p]['approved']]
    books = [p for p in hits if '/notes/notes/' in p]
    splits = [p for p in hits if '/split/' in p]
    ok = len(books) == 1 and len(splits) == 1 and all(stats[p]['approved'].count(_id) == 1 for p in hits)
    print(f'approved {kind} {_id}: "{a}" -> "{b}":', 'applied in ' + ', '.join(os.path.basename(p) for p in hits) if ok else 'NOT APPLIED CORRECTLY ' + str(hits))
    if not ok:
        bad += 1
sp = [p for p in files[4:] if p in stats]
print('split files checked:', len(sp), '- old items byte-identical & in order:', sum(stats[p]['items'] for p in sp),
      '- new r4 cards:', sum(stats[p]['inserted'] for p in sp))
print(('OK: every pre-existing History item is byte-identical and in its original relative order vs ' + ref) if not bad else f'{bad} PROBLEMS')
sys.exit(1 if bad else 0)
