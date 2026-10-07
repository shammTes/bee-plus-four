#!/usr/bin/env python3
"""Repair maths that flutter_math_fork cannot draw (the app then shows raw TeX), in every exam pack:
  * over-escaped TeX: inside a maths segment that has `\\\\frac`-style commands, every even backslash run is halved
    (\\\\frac -> \\frac, \\\\\\\\ row break -> \\\\); single-backslash commands next to them are kept
  * a bare `$` (dollar amount) inside $$..$$ -> `\\$`
  * `\\text{_____}` blanks (underscores are illegal in \\text) -> `\\underline{\\qquad}`
Usage: fix_tex.py [--check]   (prints counts; --check exits 1 if anything would change)"""
import glob, json, re, sys, os

ROOT = os.path.join(os.path.dirname(__file__), '..', '..', 'assets', 'high', 'exams')
SEG = re.compile(r'(\$\$)([\s\S]+?)(\$\$)|(\\\[)([\s\S]+?)(\\\])|(\\\()([\s\S]+?)(\\\))')
OVER = re.compile(r'(?<!\\)\\\\[a-zA-Z]')


def fix_math(m: str) -> str:
    if OVER.search(m):
        m = re.sub(r'\\+', lambda r: r[0] if len(r[0]) % 2 else '\\' * (len(r[0]) // 2), m)
    m = re.sub(r'(?<!\\)\$', r'\\$', m)
    m = re.sub(r'\\text\{\s*(\\[a-zA-Z]+)\s*\}', r'\\,\1', m)  # \text{ \Omega} -> \,\Omega
    m = re.sub(r'\\text\{\s*_{2,}\s*\}', r'\\underline{\\qquad}', m)
    return m


def fix_str(s: str) -> str:
    def rep(r):
        g = [x for x in r.groups() if x is not None]
        return g[0] + fix_math(g[1]) + g[2]
    return SEG.sub(rep, s)


def walk(x):
    if isinstance(x, str):
        return fix_str(x)
    if isinstance(x, list):
        return [walk(v) for v in x]
    if isinstance(x, dict):
        return {k: walk(v) for k, v in x.items()}
    return x


def main():
    check = '--check' in sys.argv
    files = json.load(open(os.path.join(ROOT, 'index.json')))['exams']
    paths = [os.path.join(ROOT, f) for f in files] + sorted(glob.glob(os.path.join(ROOT, 'matric_lazy', 'subjects', '*.json')))
    total = 0
    for p in paths:
        raw = open(p, encoding='utf-8').read()
        d = json.loads(raw)
        n = walk(d)
        if n != d:
            changed = sum(1 for q, r in zip(_qs(d), _qs(n)) if q != r)
            total += changed
            print(f'{os.path.relpath(p, ROOT)}: {changed} question(s)')
            if not check:
                with open(p, 'w', encoding='utf-8') as f:
                    if raw.startswith('{"'):
                        json.dump(n, f, ensure_ascii=False, separators=(',', ':'))
                    else:
                        json.dump(n, f, ensure_ascii=False, indent=2)
                    if raw.endswith('\n'):
                        f.write('\n')
    print('total questions changed:', total)
    sys.exit(1 if check and total else 0)


def _qs(d):
    if 'papers' in d:
        return [q for p in d['papers'] for q in p.get('questions', [])]
    return d.get('questions', [])


if __name__ == '__main__':
    main()
