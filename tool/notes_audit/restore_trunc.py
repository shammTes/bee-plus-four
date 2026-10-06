"""Complete strings that were cut off mid-sentence, using the full paragraphs in the Drive Study_Notes export."""
import json, os, sys
D = os.path.join(os.path.dirname(__file__), '../../assets/high/notes/notes')
SRC = '/workspace/tmp-sync/drive/Study_Notes.json'
END = tuple('.!?)*:"”$]»')

corpus = []
def collect(o):
    if isinstance(o, dict):
        [collect(v) for v in o.values()]
    elif isinstance(o, list):
        [collect(v) for v in o]
    elif isinstance(o, str) and len(o) > 80:
        corpus.append(o)
collect(json.load(open(SRC)))

def complete(s):
    st = s.rstrip()
    if len(st) < 100 or st.endswith(END) or '|' in st[-80:]:
        return None
    key = st[-60:]
    for t in corpus:
        i = t.find(key)
        if i < 0:
            continue
        j = i + len(key)
        k = t.find('\n', j)
        rest = t[j:k if k >= 0 else len(t)]
        if len(rest.strip()) < 10 or rest.lstrip().startswith(('|', '*')):
            continue
        return st + rest.rstrip()
    return None

def run(book):
    p = os.path.join(D, book + '.json')
    b = json.load(open(p)); n = [0]
    def walk(o, parent=None):
        it = o.items() if isinstance(o, dict) else enumerate(o) if isinstance(o, list) else []
        for k, v in list(it):
            if k in ('src', 'id', 'title'):
                continue
            if isinstance(v, str):
                if not (parent in ('body', 'rule') or k in ('why', 'text')):
                    continue
                f = complete(v)
                if f:
                    o[k] = f; n[0] += 1
            else:
                walk(v, k if isinstance(k, str) else parent)
    walk(b)
    json.dump(b, open(p, 'w'), ensure_ascii=False, indent=2); open(p, 'a').write('\n')
    return n[0]

if __name__ == '__main__':
    for bk in sys.argv[1:]:
        print(bk, run(bk))
