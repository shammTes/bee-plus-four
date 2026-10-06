"""Generic rewrite of 'The textbook: '...'' style attributions into plain statements (all strings except src)."""
import json, os, re, sys
D = os.path.join(os.path.dirname(__file__), '../../assets/high/notes/notes')
PRE = re.compile(r"(?:The textbook|Textbook)(?: \([^)]*\))?(?: Table \d+\.\d+(?: \([^)]*\))?)?:\s*|(?:The textbook|Textbook) Table \d+\.\d+(?: \([^)]*\))?:\s*|The textbook (?:states|says|mentions|notes|explains) that\s+")
FIG = re.compile(r"\s*\(\s*(?:[Ss]ee )?(?:fig\.?|figure|Fig\.?|Figure|Table|table) \d+\.\d+[a-z]?\s*\)")
CLOSE = re.compile(r"'(?=[\s.,;:)\u2013\u2014-]|$)")

def cap(s):
    return s[:1].upper() + s[1:] if s else s

def fix(s):
    out = s
    while True:
        m = PRE.search(out)
        if not m:
            break
        head, rest = out[:m.start()], out[m.end():]
        if rest.startswith("'"):
            rest = rest[1:]
            c = CLOSE.search(rest)
            if c:
                rest = rest[:c.start()] + rest[c.end():]
        out = head + cap(rest)
    out = FIG.sub('', out)
    return out

def run(book):
    p = os.path.join(D, book + '.json')
    b = json.load(open(p)); n = [0]
    def walk(o):
        it = o.items() if isinstance(o, dict) else enumerate(o) if isinstance(o, list) else []
        for k, v in list(it):
            if k == 'src':
                continue
            if isinstance(v, str):
                f = fix(v)
                if f != v:
                    n[0] += 1; o[k] = f
            else:
                walk(v)
    walk(b)
    json.dump(b, open(p, 'w'), ensure_ascii=False, indent=2); open(p, 'a').write('\n')
    return n[0]

if __name__ == '__main__':
    for bk in sys.argv[1:]:
        print(bk, run(bk))
