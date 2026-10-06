#!/usr/bin/env python3
"""Remove (DROP_DRIVE) or repair the 'Match key terms' games imported from Study Notes (ids *-g-drive*): their right-hand texts were cut at
~120 characters (often mid-formula, leaving an odd number of $$), some pairs were markdown-table fragments or
labels like 'Definition:' / '💡 Did You Know?', and the same game was often added twice to a unit.
Cut-off texts are trimmed back to the last complete clause; junk pairs are dropped; duplicate games are removed;
a game with fewer than 3 good pairs is removed. History/Physics untouched."""
import glob, json, os, re

DROP_DRIVE = True  # trimming produced half-sentences; the imported key-term games are dropped instead
BASE = os.path.join(os.path.dirname(__file__), '..', '..', 'assets/high/notes/notes')


def trim(b):
    b = b.strip()
    if re.search(r'[\.\)!?]$', b) and b.count('$$') % 2 == 0:
        return b
    if len(b) < 100 and b.count('$$') % 2 == 0 and b.count('(') <= b.count(')'):
        return b  # short and complete enough
    for sep in ['. ', '; ', ', where', ', which', ', such as', ' — ', ' – ', ' (', ', and', ', ']:
        k = b.rfind(sep)
        while k > 30:
            cand = b[:k].rstrip(' ,;(—–')
            if cand.count('$$') % 2 == 0 and cand.count('(') <= cand.count(')') and cand.count('**') % 2 == 0 and not re.search(r'(\$\$\w\$\$|\b\w+)\s*,\s*(\$\$\w\$\$|\w+)$', cand[-25:]):
                return cand + ('' if cand.endswith('.') else '.')
            k = b.rfind(sep, 0, k)
    return None


def good_a(a):
    a = a.strip()
    return bool(a) and not a.endswith(':') and not re.match(r'^[^\w$(]', a) and 'did you know' not in a.lower() and 'pro-tip' not in a.lower()


def main():
    tot = {'games_removed': 0, 'pairs_dropped': 0, 'pairs_trimmed': 0}
    for f in sorted(glob.glob(os.path.join(BASE, '*_*.json'))):
        b = os.path.basename(f)
        if 'index' in b or b.startswith(('history', 'physics', 'unit_')):
            continue
        d = json.load(open(f))
        n0 = dict(tot)
        for u in d['units']:
            out, seen = [], set()
            for g in u.get('games') or []:
                if g.get('type') == 'match' and 'drive' in g.get('id', '') and DROP_DRIVE:
                    tot['games_removed'] += 1
                    tot['pairs_dropped'] += len(g.get('pairs', []))
                    continue
                if g.get('type') == 'match' and 'drive' in g.get('id', ''):
                    pairs = []
                    for p in g.get('pairs', []):
                        a, bb = p['a'], p['b']
                        if not good_a(a) or bb.lstrip().startswith('|') or ' | ' in bb:
                            tot['pairs_dropped'] += 1
                            continue
                        t = trim(bb)
                        if t is None:
                            tot['pairs_dropped'] += 1
                            continue
                        if t != bb:
                            tot['pairs_trimmed'] += 1
                        pairs.append({'a': a.strip().strip('*'), 'b': t})
                    # one pair per left-hand term
                    uniq, keys = [], set()
                    for p in pairs:
                        if p['a'].lower() not in keys:
                            keys.add(p['a'].lower())
                            uniq.append(p)
                    g['pairs'] = uniq
                    if len(uniq) < 3:
                        tot['games_removed'] += 1
                        continue
                sig = json.dumps({k: v for k, v in g.items() if k not in ('id', 'lesson')}, sort_keys=True)
                if sig in seen:
                    tot['games_removed'] += 1
                    continue
                seen.add(sig)
                out.append(g)
            if 'games' in u:
                u['games'] = out
        open(f, 'w').write(json.dumps(d, indent=2, ensure_ascii=False) + '\n')
        print(b, {k: tot[k] - n0[k] for k in tot})
    print('total', tot)


if __name__ == '__main__':
    main()
