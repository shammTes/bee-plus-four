#!/usr/bin/env python3
"""Replace 'Textbook p.N: <OCR quote>' explanation lines with a written explanation.
Input: tool/notes_audit/why/<book>.txt, lines 'qid|explanation' (optional 'qid!answer|new answer' and
'qid!q|new question text'). The OCR quote is removed even when it was the only reason line."""
import json, os, re, sys
HERE = os.path.dirname(__file__)
BASE = os.path.join(HERE, '..', '..', 'assets/high/notes/notes')
TB = re.compile(r'^Textbook p\.\s*\d+[:\.]?\s*', re.I)
TB2 = re.compile(r'^(The )?textbook\b', re.I)  # 'The textbook: ...' quote lines are dropped too when we write a reason


def main(book):
    why, fix = {}, {}
    for line in open(os.path.join(HERE, 'why', book + '.txt'), encoding='utf-8'):
        line = line.rstrip('\n')
        if not line.strip() or line.startswith('#'):
            continue
        k, v = line.split('|', 1)
        if '!' in k:
            qid, field = k.split('!')
            fix.setdefault(qid, {})[field] = v
        else:
            why[k.strip()] = v.strip()
    p = os.path.join(BASE, book + '.json')
    d = json.load(open(p))
    done, missing = 0, []
    for u in d['units']:
        for q in u['exercise']['questions']:
            for f, v in fix.get(q['id'], {}).items():
                q[f] = v
            w = q['why'] if isinstance(q['why'], list) else [q['why']]
            has_tb = any(TB.match(x) for x in w)
            if q['id'] in why:
                keep = [x for x in w if not TB.match(x) and not TB2.match(x)]
                if q.get('why_src') == 'written' and keep:
                    keep = keep[:-1]  # re-run: replace our own previous explanation
                if q['type'] == 'short':
                    keep = [x for x in keep if not x.startswith('Answer')]
                q['why'] = keep + [why[q['id']]]
                q['why_src'] = 'written'
                done += 1
            elif has_tb:
                missing.append(q['id'])
    open(p, 'w').write(json.dumps(d, indent=2, ensure_ascii=False) + '\n')
    print(book, 'explanations written:', done, 'still quoting the book:', missing)


if __name__ == '__main__':
    for b in sys.argv[1:]:
        main(b)
