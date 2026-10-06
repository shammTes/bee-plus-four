"""Worked cards whose answer is a bare option letter ("D") shown without options: replace with the option text
(from the matching check card with the same src_qid) or the bold conclusion of the last step."""
import json, os, re, sys, glob
D = os.path.join(os.path.dirname(__file__), '../../assets/high/notes/notes')
LET = re.compile(r'\s*\(?([A-E])\)?\.?\s*$')

def run(book):
    p = os.path.join(D, book + '.json')
    b = json.load(open(p))
    checks = {}
    for u in b['units']:
        for l in u['lessons']:
            for c in l['cards']:
                if c.get('type') == 'check' and c.get('src_qid') and isinstance(c.get('options'), dict):
                    checks[c['src_qid']] = c
    n = miss = 0
    for u in b['units']:
        for l in u['lessons']:
            for c in l['cards']:
                if c.get('type') != 'worked' or not isinstance(c.get('answer'), str):
                    continue
                m = LET.fullmatch(c['answer'])
                if not m:
                    continue
                new = None
                ch = checks.get(c.get('src_qid'))
                if ch and m.group(1) in ch['options']:
                    new = str(ch['options'][m.group(1)]).strip()
                if not new:
                    for s in reversed(c.get('steps') or []):
                        t = s.get('text', '') if isinstance(s, dict) else str(s)
                        bold = re.findall(r'\*\*(.+?)\*\*', t)
                        bold = [x for x in bold if not re.match(r'(Step \d|Conclusion|Reasoning|Answer)', x)]
                        if bold:
                            new = bold[-1].strip().rstrip('.')
                            break
                if new:
                    c['answer'] = new; n += 1
                else:
                    miss += 1; print('  no answer for', c['id'])
    json.dump(b, open(p, 'w'), ensure_ascii=False, indent=2); open(p, 'a').write('\n')
    return n, miss

if __name__ == '__main__':
    for bk in sys.argv[1:]:
        print(bk, run(bk))
