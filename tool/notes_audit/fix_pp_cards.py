#!/usr/bin/env python3
"""Round 2: tidy the 'textbook pp.' text cards (sentences pulled from the textbook) so they read as clear notes.
- drop sentences that are exercise prompts or questions ("Explain…", "Find…", "Show that…", "…?")
- drop sentences that point at something the card does not contain (Fig./Table/Example N, "shaded region",
  "as shown…", "the example…", a trailing "the following:")
- drop exact repeats inside a lesson; fix OCR degree signs ("10 0C" -> "10 °C") and doubled spaces
- bold the defined term in definition sentences ("X is called Y" / "Y is the …")
History books are not touched. usage: python3 tool/notes_audit/fix_pp_cards.py [--dry]
"""
import json, glob, os, re, sys
BASE = os.path.join(os.path.dirname(__file__), '..', '..', 'assets/high/notes/notes')
dry = '--dry' in sys.argv
IMP = re.compile(r'^(Explain|Describe|Discuss|Find|Show that|Show|Calculate|Identify|Draw|Write|List|State|Compare|Prove|Determine|'
                 r'Mention|Name|Give|Construct|Complete|Sketch|Use|Solve|Evaluate|Simplify|Verify|Classify|Suggest|Define|Investigate|'
                 r'Observe|Measure|Record|Try|Look at|Refer to|Read|Answer|Consider the|Let us|Now)\b')
REF = re.compile(r'\b((Fig\.?|Figure|Table|Activity|Exercise|Example|Problem|Question)\s*\(?\d|shaded region|in problem|as shown|shown (above|below)|shown in (the )?(graph|figure|diagram|table)|'
                 r'the example (shows|above|below)|in the diagram|the diagram (above|below)|see (the )?(figure|table|grade)|following (figure|table|diagram))', re.I)
FIGP = re.compile(r'\s*[\(\[](?:see )?(?:Fig\.?|Figure|Table)\s*[\d\.]+\s?[a-z]?[\)\]]')
FIGC = re.compile(r',?\s*as (?:shown|illustrated|indicated) in (?:Fig\.?|Figure|Table)\s*[\d\.]+\s?[a-z]?,?|,?\s*as shown in the circular flow of income and expenditure|\s+in Fig\.\s*[\d\.]+[a-z]?')
DEF1 = re.compile(r'^((?:The |A |An )?)([A-Z][\w’\'\- ]{2,40}?) (is|are|refers to|means) (the|a|an|defined|called|known)\b')
NOTSUBJ = re.compile(r'^(Every|Inside|Outside|This|These|That|Those|It|They|There|Here|Each|All|Some|Most|Many|Such|One|Another|Its|Their|In|On|At|For|When|If|Since|However|Therefore|Thus)\b')
DEF2 = re.compile(r'\b(is|are) (called|known as|termed|referred to as) ((?:an? |the )?)([\w’\'\- ]{3,40}?)([.,;]|$)')


def bad(s):
    t = s.strip()
    return (len(t) < 25 or t.endswith('?') or bool(IMP.match(t)) or bool(REF.search(t)) or t[:1].islower()
            or t.rstrip().endswith(':') or re.match(r'^[\d\)\(•\-–]', t) is not None)


def tidy(s):
    s = re.sub(r'(\d)\s?0\s?C\b', r'\1 °C', s)
    s = FIGP.sub('', s)
    s = FIGC.sub(' ', s)
    s = re.sub(r'\s{2,}', ' ', s).strip()
    if '**' in s:
        return s
    m = DEF2.search(s)
    if m and len(s) < 260:
        return s[:m.start(4)] + '**' + m.group(4) + '**' + s[m.end(4):]
    m = DEF1.match(s)
    if (m and len(s) < 260 and len(m.group(2).split()) <= 4 and not NOTSUBJ.match(m.group(2))
            and not re.search(r'\b(then|also|thus|therefore|main|other|first|second|only)$', m.group(2), re.I)
            and not re.search(r'\b(good example|an example|a requirement|one of)\b', s, re.I)):
        return m.group(1) + '**' + m.group(2) + '**' + s[m.end(2):]
    return s


dropped, cards, bolded = [], 0, 0
for p in sorted(glob.glob(os.path.join(BASE, '*.json'))):
    b = os.path.basename(p)
    if b.startswith('history') or 'index' in b:
        continue
    raw = open(p, encoding='utf-8').read()
    d = json.loads(raw)
    ch = False
    for u in d.get('units') or [d]:
        for l in u.get('lessons', []):
            seen = set()
            for c in l['cards']:
                if not str(c.get('src', '')).startswith('textbook p') or c.get('type') not in ('text', 'remember'):
                    continue
                body = c.get('body')
                if not isinstance(body, list):
                    continue
                cards += 1
                new = []
                for s in body:
                    if not isinstance(s, str):
                        new.append(s); continue
                    key = re.sub(r'\W+', '', s.lower())
                    if bad(FIGC.sub(' ', FIGP.sub('', s))) or key in seen:
                        dropped.append(f'{b} {c["id"]}: {s[:150]}')
                        continue
                    seen.add(key)
                    t = tidy(s)
                    bolded += t != s
                    new.append(t)
                if not new:  # never empty a card; keep the first original sentence
                    new = [tidy(body[0])]
                if new != body:
                    c['body'] = new
                    ch = True
    if ch and not dry:
        compact = not raw.startswith('{\n')
        txt = json.dumps(d, ensure_ascii=False, separators=(',', ':')) if compact else json.dumps(d, ensure_ascii=False, indent=2)
        open(p, 'w', encoding='utf-8').write(txt + '\n')
print(f'cards {cards}, sentences dropped {len(dropped)}, sentences tidied/bolded {bolded}')
if dry:
    print('\n'.join(dropped))
