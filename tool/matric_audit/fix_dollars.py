#!/usr/bin/env python3
"""Raw '$' shown on the Matric screen (2026-10-12). Emulates the exam renderer's split (lib/high/notes/jr/notes/rich.dart
_split: \\$ literal, $x$ inline, $$x$$ / \\[ \\] / \\( \\) maths) and repairs every string where a '$' would stay visible:
  * truncated explanations (cut at ~280 chars mid-formula, so a '$$' never closes): restored from the full Drive source
    explanation (--source Matric_Questions.json) when its text starts with the cut text, else cut back before the
    dangling '$$' and ended with '…'
  * currency written as a bare '$' ("$600", "$9,900$", "US $") -> '\\$' (renderer shows a literal $)
  * over-escaped TeX inside single $..$ (\\\\circ) halved; '\\night' (eaten \\r of \\right) -> '\\right'
Usage: fix_dollars.py [--check] [--source PATH]   (test/matric_dollar_test.dart is the exact check)"""
import glob, json, os, re, sys

sys.path.insert(0, os.path.dirname(__file__))
from fix_tex import fix_str  # noqa: E402

ROOT = os.path.join(os.path.dirname(__file__), '..', '..', 'assets', 'high', 'exams')
MONEY = re.compile(r'(?<!\\)\\\$(?!\$)')
DOLLAR = re.compile(r'(^|[^$\\])\$([^$\n]+)\$(?!\$)')


def visible_dollars(s: str) -> int:
    s = MONEY.sub('\uE000', s)
    s = DOLLAR.sub(lambda m: m[1] + '\\(' + m[2] + '\\)', s)
    n, i = 0, 0
    while i < len(s):
        hit = None
        for o, c in (('$$', '$$'), ('\\[', '\\]'), ('\\(', '\\)')):
            if s.startswith(o, i):
                j = s.find(c, i + len(o))
                if j > i:
                    hit = j + len(c)
                    break
        if hit:
            i = hit
            continue
        n += s[i] == '$'
        i += 1
    return n


def norm(s):
    return re.sub(r'\s+|\\', '', s)


def load_source(path):
    out = {}
    if not path or not os.path.exists(path):
        return out
    for p in json.load(open(path, encoding='utf-8'))['papers']:
        qs = p['questions']
        if isinstance(qs, str):
            continue
        for q in qs:
            e = q.get('explanation')
            if isinstance(e, str) and len(e) > 200:
                out.setdefault(norm(e)[:120], []).append(e)
    return out


def _tex(t):
    # over-escaped single-$ maths (\\circ) halved; '\night' (eaten \r of \right) -> '\right'
    t = re.sub(r'(?<![$\\])\$([^$\n]+)\$(?!\$)', lambda m: '$' + (re.sub(r'\\+', lambda r: r[0] if len(r[0]) % 2 else '\\' * (len(r[0]) // 2), m[1]) if re.search(r'(?<!\\)\\\\[a-zA-Z]', m[1]) else m[1]) + '$', t)
    t = re.sub(r'(?:\\n|\n)(?=ight\s*[|)\]}.\\])', r'\\r', t)  # JSON "\r" of \right read as newline/eaten
    return re.sub(r'\\text\{([^{}·]*)·([^{}]*)\}', r'\\text{\1}\\cdot\\text{\2}', t)  # '·' cannot be drawn inside \text


def _money(t):
    t = re.sub(r'(?<![$\\])\$(\d[\d,]*(?:\.\d+)?)\$(?!\$)', r'\\$\1', t)  # "$9,900$" (money written as maths)
    t = re.sub(r'(?<![$\\])\$(?=\s?\(?\d)', r'\\$', t)  # "$600", "$ 20"
    t = re.sub(r'(?<=US )\$(?!\$)|(?<=US)\$(?!\$)|(?<=\()\$(?=\))|(?<=\u2018)\$(?=\u2019)|^\$$', r'\\$', t)  # "US $", "($)", a "$" column
    return t


def fix_one(s, src, stats):
    if '$' not in s:
        return s
    if visible_dollars(s) == 0:
        t = _tex(s)
        stats['tex'] += t != s
        return t
    if len(s) >= 240:  # explanation cut at ~280 chars
        cand = [e for e in src.get(norm(s)[:120], []) if len(e) > len(s) and norm(e).startswith(norm(s)[: max(60, len(norm(s)) - 12)])]
        for e in cand:
            full = _money(_tex(fix_str(e)))
            if visible_dollars(full) == 0:
                stats['restored'] += 1
                return full
    t = _money(_tex(s))
    if visible_dollars(t) == 0:
        stats['currency' if _money(_tex(s)) != _tex(s) else 'tex'] += 1
        return t
    if len(s) >= 240:  # no full source: cut back before the dangling delimiter
        while visible_dollars(t):
            t = t[: t.rfind('$')].rstrip('$').rstrip(' \n(:=,') + ' …'
        stats['trimmed'] += 1
        return t
    stats['left'] += 1
    print('left:', json.dumps(s[:200]), file=sys.stderr)
    return t


def walk(x, src, stats):
    if isinstance(x, str):
        return fix_one(x, src, stats)
    if isinstance(x, list):
        return [walk(v, src, stats) for v in x]
    if isinstance(x, dict):
        return {k: walk(v, src, stats) for k, v in x.items()}
    return x


def main():
    check = '--check' in sys.argv
    srcp = sys.argv[sys.argv.index('--source') + 1] if '--source' in sys.argv else None
    src = load_source(srcp)
    files = json.load(open(os.path.join(ROOT, 'index.json')))['exams']
    paths = [os.path.join(ROOT, f) for f in files] + sorted(glob.glob(os.path.join(ROOT, 'matric_lazy', 'subjects', '*.json')))
    stats = {'restored': 0, 'trimmed': 0, 'currency': 0, 'tex': 0, 'left': 0}
    left = 0
    for p in paths:
        raw = open(p, encoding='utf-8').read()
        d = json.loads(raw)
        n = walk(d, src, stats)
        def cnt(x):
            if isinstance(x, str):
                return 1 if visible_dollars(x) else 0
            if isinstance(x, list):
                return sum(cnt(v) for v in x)
            if isinstance(x, dict):
                return sum(cnt(v) for v in x.values())
            return 0
        left += cnt(n)
        if n != d and not check:
            compact = not raw.startswith('{\n')
            with open(p, 'w', encoding='utf-8') as f:
                if compact:
                    json.dump(n, f, ensure_ascii=False, separators=(',', ':'))
                else:
                    json.dump(n, f, ensure_ascii=False, indent=2)
                if raw.endswith('\n'):
                    f.write('\n')
    print(stats, 'still visible:', left)
    if check and any(stats.values()):
        sys.exit(1)


if __name__ == '__main__':
    main()
