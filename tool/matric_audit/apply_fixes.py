#!/usr/bin/env python3
"""Apply answer_fixes.json (hand-checked edits), and accept every option whose text is identical to the keyed one
(papers with a repeated option, e.g. B and D both "16", marked only one right). Prints what changed."""
import json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '..', '..', 'assets', 'high', 'exams')


def norm(s):
    return re.sub(r'\s+', '', str(s)).rstrip('.')


def main():
    fixes = {k: v for k, v in json.load(open(os.path.join(HERE, 'answer_fixes.json'))).items() if not k.startswith('_')}
    idx = json.load(open(os.path.join(ROOT, 'index.json')))
    log = []
    for f in idx['exams']:
        p = os.path.join(ROOT, f)
        raw = open(p, encoding='utf-8').read()
        d = json.loads(raw)
        ch = False
        for q in d.get('questions', []):
            fx = fixes.get(q['id'])
            if fx:
                for k, v in fx.items():
                    if not k.startswith('_') and q.get(k) != v:
                        q[k] = v
                        ch = True
                log.append((q['id'], fx.get('_why', '')))
            o, a = q.get('options'), q.get('answer')
            if isinstance(o, dict) and a in o and norm(o[a]):
                same = sorted(k for k, v in o.items() if norm(v) == norm(o[a]))
                acc = sorted(set(q.get('accepted_answers') or [a]) | set(same))
                if len(same) == 2 and acc != sorted(q.get('accepted_answers') or []):
                    q['accepted_answers'] = acc
                    q.setdefault('review_flag', f"Options {' and '.join(same)} are printed identically; both are accepted.")
                    ch = True
                    log.append((q['id'], f'identical options {same} accepted'))
        if ch:
            with open(p, 'w', encoding='utf-8') as fh:
                if raw.startswith('{"'):
                    json.dump(d, fh, ensure_ascii=False, separators=(',', ':'))
                else:
                    json.dump(d, fh, ensure_ascii=False, indent=2)
                if raw.endswith('\n'):
                    fh.write('\n')
    for x in log:
        print(*x)


if __name__ == '__main__':
    main()
