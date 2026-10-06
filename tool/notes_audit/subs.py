"""Literal string substitutions applied to every string (except `src`) of a notes book.
Usage: from subs import apply; apply('chemistry_10', [(old, new), ...])"""
import json, os
D = os.path.join(os.path.dirname(__file__), '../../assets/high/notes/notes')

def apply(book, pairs, strict=True):
    p = os.path.join(D, book + '.json')
    b = json.load(open(p))
    hits = {o: 0 for o, _ in pairs}
    def walk(o):
        if isinstance(o, dict):
            for k, v in list(o.items()):
                if k == 'src':
                    continue
                if isinstance(v, str):
                    o[k] = sub(v)
                else:
                    walk(v)
        elif isinstance(o, list):
            for i, v in enumerate(o):
                if isinstance(v, str):
                    o[i] = sub(v)
                else:
                    walk(v)
    def sub(s):
        for a, c in pairs:
            if a in s:
                hits[a] += 1
                s = s.replace(a, c)
        return s
    walk(b)
    missing = [a for a, n in hits.items() if n == 0]
    if missing and strict:
        print(book, 'NOT FOUND:', missing)
    json.dump(b, open(p, 'w'), ensure_ascii=False, indent=2)
    open(p, 'a').write('\n')
    return sum(hits.values())


def apply_re(book, pairs):
    """Regex substitutions (pattern, repl) on every string except `src`."""
    import re
    comp = [(re.compile(a), c) for a, c in pairs]
    p = os.path.join(D, book + '.json')
    b = json.load(open(p)); n = [0]
    def walk(o):
        it = o.items() if isinstance(o, dict) else enumerate(o) if isinstance(o, list) else []
        for k, v in list(it):
            if k == 'src':
                continue
            if isinstance(v, str):
                s = v
                for r, c in comp:
                    s = r.sub(c, s)
                if s != v:
                    n[0] += 1; o[k] = s
            else:
                walk(v)
    walk(b)
    json.dump(b, open(p, 'w'), ensure_ascii=False, indent=2); open(p, 'a').write('\n')
    return n[0]
