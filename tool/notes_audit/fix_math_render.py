#!/usr/bin/env python3
"""Fix notes strings whose maths does not render (test/notes_math_all_subjects_test.dart). Idempotent.

    python3 tool/notes_audit/fix_math_render.py [--dry]

Each fix is (book, item id, old substring, new substring), applied to every string field of that item:
  * money written as a bare $ (business petty-cash questions, a History figure) pairs up with the next $ and turns
    into maths -> write it as \\$ (rich.dart shows \\$ as a plain dollar sign);
  * TeX commands broken by a JSON-escaping slip: "\\frac" lost to a form feed ("rac{"), "\\text" turned into a TAB;
  * an unknown macro (\\s{...}) and bare underscores inside \\text{}.
Then run tool/split_notes.py and tool/build_tutor_index.py."""
import json
import os
import re
import sys

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
NOTES = os.path.join(ROOT, 'assets', 'high', 'notes', 'notes')
DRY = '--dry' in sys.argv
INDENT = {'history_12': 1}

FIXES = [
    ('business_economics_11', 'be11-u1-l1-5-mx1', '= rac{', r'= \frac{'),
    ('chemistry_9', 'chem9-u3-chk12', '\text{O}', r'\text{O}'),
    ('mathematics_9', 'math9-u2-wrk2', r'\s{\{(0, 2), (1, 4), (2, 6), (3, 8)\}}', r'\{(0, 2), (1, 4), (2, 6), (3, 8)\}'),
    ('mathematics_9', 'math9-u2-chkM3', r'\s{\{(0, 2), (1, 4), (2, 6), (3, 8)\}}', r'\{(0, 2), (1, 4), (2, 6), (3, 8)\}'),
    ('agriculture_11', 'agri-g11-c3-q1', r'\text{______}', r'\text{\_\_\_\_\_\_}'),
    ('history_12', 'hist12-u4-l4-4-r4l1', 'from $2 (1973 start) to $34 a barrel', r'from \$2 (1973 start) to \$34 a barrel'),
]
# petty-cash questions: every amount is in dollars. "$$ $300 $$" / "$$ 300 $$" (display maths, a block of its own, and a bare
# $ inside maths) -> "\$300"; a worked sum "$$ 200 - 8 = 192 $$" -> inline "\(200 - 8 = 192\)"; a lone "$2." -> "\$2."
MONEY = [('business_economics_12', 'be12-u2-mx3'), ('business_economics_12', 'be12-u2-mx10')]


def money(s):
    s = re.sub(r'\$\$ \$?(\d[\d,]*) \$\$', r'\\$\1', s)
    s = re.sub(r'\$\$ ([\d ,+\-=]+?) \$\$', lambda m: r'\(' + m[1].strip() + r'\)', s)
    return re.sub(r'(?<![\\$])\$(\d)', r'\\$\1', s)


def apply(x, f):
    if isinstance(x, str):
        return f(x)
    if isinstance(x, list):
        return [apply(v, f) for v in x]
    if isinstance(x, dict):
        return {k: (v if k in ('id', 'src', 'src_qid', 'exam_question') else apply(v, f)) for k, v in x.items()}
    return x


def find(o, iid, f, hits):
    if isinstance(o, dict):
        for k, v in o.items():
            if isinstance(v, dict) and v.get('id') == iid:
                nv = apply(v, f)
                if nv != v:
                    hits.append(iid)
                o[k] = nv
            else:
                find(v, iid, f, hits)
    elif isinstance(o, list):
        for i, v in enumerate(o):
            if isinstance(v, dict) and v.get('id') == iid:
                nv = apply(v, f)
                if nv != v:
                    hits.append(iid)
                o[i] = nv
            else:
                find(v, iid, f, hits)


def main():
    books = {}
    jobs = [(b, i, (lambda s, a=a, n=n: s.replace(a, n))) for b, i, a, n in FIXES] + [(b, i, money) for b, i in MONEY]
    changed = []
    for b, iid, f in jobs:
        if b not in books:
            with open(os.path.join(NOTES, b + '.json'), encoding='utf-8') as fh:
                books[b] = json.load(fh)
        hits = []
        find(books[b], iid, f, hits)
        changed += [(b, h) for h in hits]
    for b, d in books.items():
        if not DRY:
            with open(os.path.join(NOTES, b + '.json'), 'w', encoding='utf-8') as fh:
                json.dump(d, fh, ensure_ascii=False, indent=INDENT.get(b, 2))
                fh.write('\n')
    for b, h in changed:
        print(f'{b}: {h}')
    print(f'{len(changed)} items changed')


if __name__ == '__main__':
    main()
