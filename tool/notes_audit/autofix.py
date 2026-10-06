#!/usr/bin/env python3
"""Automatic, rule-based part of the notes audit (Task 1).

1. check cards / worked steps whose text was cut off at import (400-420 chars) get the full explanation back from
   the Study Notes source (tmp-sync/drive/Study_Notes.json, English only);
2. source citation markers like [103, 111] are removed (not meaningful to a student);
3. phrases that only send the student to the book ("According to page 43, ...", "(p.12)", "(Fig. 2.5b)",
   "Textbook (G10 p.110): ", "in Section 6.2", "Step 1: Check ... in the text") are rewritten so the sentence stands
   on its own. The fact itself is kept; page numbers stay as `page` metadata.
History and Physics books are never touched. Writes a log of every change to /tmp/autofix_log.txt.
usage: python3 tool/notes_audit/autofix.py [--sn PATH] [books...]"""
import glob, json, os, re, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
BASE = os.path.join(ROOT, 'assets/high/notes/notes')
SN = '/workspace/tmp-sync/drive/Study_Notes.json'
META = {'id', 'src', 'pdf', 'source', 'book', 'file', 'src_qid', 'why_src', 'answer_src', 'type', 'mode', 'tone', 'status',
        'svg', 'diagram', 'lesson', 'label', 'section', 'kind', 'style', 'reveal', 'show', 'color', '$schema', 'source_outline'}

PG = r'(?:p\.|pp\.|page|pages)\s*\d+(?:\s*(?:,|and|&|–|-)\s*(?:and\s+)?\d+)*'
SECT = r'(?:Section|section|sections)\s+\d+(?:\.\d+)+'
SUBS = [
    # "According to page 11, condensation is ..." / "According to page 100, "The spleen ...""
    (re.compile(r'According to ' + PG + r'(?:\s+(?:of the text(?:book)?|in the text(?:book)?))?,\s*["“]?'), ''),
    (re.compile(r'According to (?:the )?text(?:book)?\s*(?:\((?:' + SECT + r'|Table [\d\.]+)\))?,\s*'), ''),
    (re.compile(r'According to ' + SECT + r'(?: of the text(?:book)?)?,\s*'), ''),
    (re.compile(r'Looking at (Table [\d\.]+) on ' + PG + r','), r'Looking at \1,'),
    (re.compile(r'\s+(?:on|from|in|at)\s+' + PG + r'(?=[\s\*\.,;:)])'), ''),
    (re.compile(r'\s+(?:in|from)\s+' + SECT + r'(?:\s+of the text(?:book)?)?'), ''),
    (re.compile(r'\s*\((?:see\s+)?(?:' + PG + r'|' + SECT + r')\)'), ''),
    (re.compile(r'\s*\((?:see\s+)?(?:Fig(?:ure)?s?\.?|Activity|Plate)\s*[\d\.]+[a-z]?(?:\s*(?:and|&|,)\s*[\d\.]+[a-z]?)*\)'), ''),
    (re.compile(r'\s*\(compare text(?:book)? Figure [\d\.]+[^)]*\)'), ''),
    (re.compile(r'\s*\(text(?:book)? Figure [\d\.]+\)'), ''),
    (re.compile(r'\s*[—–-]?\s*Text(?:book)?\s*\(G\d+\s*p\.?\s*\d+\):\s*'), ' — '),
    (re.compile(r'Text(?:book)?\s*\(G\d+\s*p\.?\s*\d+\):\s*'), ''),
    (re.compile(r'\s*\(text(?:book)?\s*G\d+\s*p\.?\s*\d+\)'), ''),
    (re.compile(r'\s*[—–-]\s*text(?:book)?\s*\(G\d+\s*p\.?\s*\d+\)', re.I), ''),
    # step headings that tell the student to go and look something up
    (re.compile(r'(\*\*Step \d+: )(?:Refer to|Check|Verify|Compare with|Locate|Look up|Find)\s+the text(?:book)?\s+(?:description|definition|reference|details|statement)s?(\*\*)?', re.I), r'\1Recall the key facts\2'),
    (re.compile(r'(\*\*Step \d+: [^*\n]*?)\s+(?:in|from|based on|on) (?:the )?text(?:book)?(?: Table [\d\.]+)?(\*\*)'), r'\1\2'),
    (re.compile(r'(\*\*Step \d+: [^*\n]*?)\s+(?:in|from|on) (?:' + SECT + r'|' + PG + r')(\*\*)'), r'\1\2'),
    (re.compile(r'(\*\*Step \d+: )Compare with the (chemical equation)(?: provided)?(\*\*)'), r'\1Use the \2\3'),
    (re.compile(r'(\*\*Step \d+: [^*\n]*?)\s+based on (?:the )?text(?:book)? (Table [\d\.]+)(\*\*)'), r'\1\3'),
    # bare "(p.12)" / "(p. 12)" at the end of game feedback etc.
    (re.compile(r'\s*\(p\.\s*\d+(?:[–-]\d+)?\)'), ''),
    (re.compile(r'\s*\(pp?\.\s*\d+(?:[–-]\d+)?\)'), ''),
]
CITE = re.compile(r'\s*\[\d+(?:\s*[,–-]\s*\d+)*\]')


def T(s):
    return '\n'.join(s) if isinstance(s, list) else (s or '')


def norm(s):
    return re.sub(r'\W+', '', T(s).lower())[:120]


def cut(s):
    s = T(s).rstrip()
    return len(s) > 120 and bool(re.search(r'[A-Za-z0-9 ]$', s.rstrip('*')))


def tidy(s, math_book):
    o = s
    if not math_book:
        s = CITE.sub('', s)
    for rx, rep in SUBS:
        s = rx.sub(rep, s)
    if s != o:
        s = re.sub(r'^\s*["“]', '', s) if o.lstrip().startswith('According') else s
        s = re.sub(r'(^|\n|\. )([a-z])', lambda m: m.group(1) + m.group(2).upper(), s, count=1) if o.lstrip().startswith('According') else s
        s = re.sub(r'  +', ' ', s).replace(' ,', ',').replace(' .', '.').replace('( ', '(')
        if o.lstrip().startswith('According') and s.count('"') % 2:
            s = s.replace('"', '', 1) if s.endswith('."') or s.endswith('"') else s
    return s


def walk(o, f, path=''):
    if isinstance(o, dict):
        for k, v in list(o.items()):
            if k in META:
                continue
            if isinstance(v, str):
                n = f(v, f'{path}.{k}')
                if n != v:
                    o[k] = n
            else:
                walk(v, f, f'{path}.{k}')
    elif isinstance(o, list):
        for i, v in enumerate(o):
            if isinstance(v, str):
                n = f(v, f'{path}[{i}]')
                if n != v:
                    o[i] = n
            else:
                walk(v, f, f'{path}[{i}]')


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    sn = {}
    if os.path.exists(SN):
        for ch in json.load(open(SN))['chapter_notes']:
            for r in ch['review_exercises']:
                sn[norm(r['question'])] = r
    log = open('/tmp/autofix_log.txt', 'a')
    files = sorted(glob.glob(os.path.join(BASE, '*_*.json')))
    for f in files:
        b = os.path.basename(f)
        if 'index' in b or b.startswith(('history', 'physics', 'unit_')):
            continue
        if args and b[:-5] not in args:
            continue
        d = json.load(open(f))
        math_book = b.startswith('mathematics')
        n = 0
        for u in d['units']:
            for l in u['lessons']:
                for c in l['cards']:
                    if c['type'] == 'check' and cut(c.get('why')):
                        r = sn.get(norm(c['q']))
                        if r and r.get('explanation') and len(r['explanation']) > len(T(c['why'])):
                            c['why'] = r['explanation']
                            n += 1
                            log.write(f'{b} {c["id"]} why restored from Study Notes\n')
                    if c['type'] == 'worked' and any(cut(s.get('text', '')) for s in c.get('steps', [])):
                        r = sn.get(norm(c['problem']))
                        if r and r.get('explanation'):
                            parts = [p.strip() for p in re.split(r'\n\s*\n', r['explanation']) if p.strip()]
                            c['steps'] = [{'text': p} for p in parts]
                            n += 1
                            log.write(f'{b} {c["id"]} steps restored from Study Notes\n')

        def fx(s, p):
            nonlocal n
            t = tidy(s, math_book)
            if t != s:
                n += 1
                log.write(f'{b} {p}\n  - {s[:300]}\n  + {t[:300]}\n')
            return t
        walk(d, fx)
        open(f, 'w').write(json.dumps(d, indent=2, ensure_ascii=False) + '\n')
        print(b, n, 'changes')


if __name__ == '__main__':
    main()
