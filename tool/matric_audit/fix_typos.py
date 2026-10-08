#!/usr/bin/env python3
"""Small, safe text fixes in exam stems / options:
  * a leading "18. " copied from the paper into a bank_* stem (the app prints its own Q-label, and after
    renumber.py the copied number is often wrong)
  * °c -> °C, "wave length" -> wavelength, "focus length" -> focal length, "it's <noun>" -> its, " ," -> ",",
    "70 db" -> "70 dB" (Physics / Mathematics only for the wording fixes)
Usage: fix_typos.py [--dry]"""
import json, os, re, sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'assets', 'high', 'exams')
LEAD = re.compile(r'^\s*\d{1,3}\s*[.)]\s+(?=[A-Z*_(])')
WORD = [
    (re.compile(r'°c\b'), '°C'),
    (re.compile(r'\b([Ww])ave length'), r'\1avelength'),
    (re.compile(r'\bfocus length'), 'focal length'),
    (re.compile(r'\b([Ii])t[’\']s (gondola|velocity|speed|mass|weight|graph|image|period|frequency|vertex|radius|length)\b'), r'\1ts \2'),
    (re.compile(r'(?<=\w) +,'), ','),
    (re.compile(r'(?<=\d) ?db\b'), ' dB'),
]


def fix_text(s, sci):
    n = 0
    if sci:
        for p, r in WORD:
            s, k = p.subn(r, s)
            n += k
    return s, n


def main():
    dry = '--dry' in sys.argv
    idx = json.load(open(os.path.join(ROOT, 'index.json')))
    tot = {}
    for f in idx['exams']:
        p = os.path.join(ROOT, f)
        raw = open(p, encoding='utf-8').read()
        d = json.loads(raw)
        sci = d['exam'].get('subject') in ('Physics', 'Mathematics')
        n = 0
        for q in d.get('questions', []):
            s = q.get('stem')
            if isinstance(s, str):
                if f.startswith('bank_') and LEAD.match(s):
                    s = LEAD.sub('', s, 1)
                    n += 1
                s, k = fix_text(s, sci)
                n += k
                q['stem'] = s
            if isinstance(q.get('options'), dict):
                for kk, v in q['options'].items():
                    if isinstance(v, str):
                        q['options'][kk], k = fix_text(v, sci)
                        n += k
        if n:
            tot[f] = n
            if not dry:
                with open(p, 'w', encoding='utf-8') as fh:
                    if raw.startswith('{"'):
                        json.dump(d, fh, ensure_ascii=False, separators=(',', ':'))
                    else:
                        json.dump(d, fh, ensure_ascii=False, indent=2)
                    if raw.endswith('\n'):
                        fh.write('\n')
    for k, v in tot.items():
        print(k, v)
    print('total', sum(tot.values()))


if __name__ == '__main__':
    main()
