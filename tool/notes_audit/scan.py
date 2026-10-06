#!/usr/bin/env python3
"""High notes audit scanner.

Scans assets/high/notes/notes/<subject>_<grade>.json (+ unit_<id>.json overrides, which REPLACE the unit at
runtime) for: textbook-pointer / placeholder text, empty or title-only cards, empty tables, cut-off strings,
odd $$ counts, invalid answer keys, missing assets, thin lessons and missing practice.

usage: python3 tool/notes_audit/scan.py [--json report.json] [--subjects a,b] [--strict]
--strict exits 1 when a blocking problem (pointer, placeholder, bad key, missing asset, odd $$, empty) is found
outside history/physics.
"""
import glob, json, os, re, sys, argparse
from collections import Counter, defaultdict

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
BASE = os.path.join(ROOT, 'assets/high/notes/notes')
MEDIA = os.path.join(ROOT, 'assets/high/media')

POINTER = [
    r'\b(see|refer(?:ring)? to|look (?:at|in)|check|consult|read|use|open|turn to|study (?:from|in)?)\s+(?:your|the)\s+(?:text\s?book|student\s?book|book|teacher\'?s? guide)',
    r'\btext\s?book\b', r'\bstudent\s?book\b',
    r'\b(?:in|from) the book\b', r'\bthe book says\b',
    r'\bas (?:shown|given|described|explained|seen|discussed) in (?:the |your )?(?:text|book|fig|figure|table|activity|chapter)',
    r'\(\s*(?:see\s+)?p(?:p|g)?\.\s*\d+', r'\bpages?\s+\d+', r'\bon p\.?\s*\d+',
    r'\bfig(?:ure)?\.?\s*\d+(?:\.\d+)*', r'\bactivity\s+\d+(?:\.\d+)*', r'\bexercise\s+\d+\.\d+', r'\btable\s+\d+\.\d+',
    r'\bread (?:the|your) (?:chapter|unit|book|lesson)', r'\bstudy from\b',
    r'\bcoming soon\b', r'\bTODO\b', r'\bTBD\b', r'\bplaceholder\b', r'\blorem\b', r'\bFIXME\b', r'\bto be added\b',
]
POINTER_RE = re.compile('|'.join('(?:%s)' % p for p in POINTER), re.I)
# fields that are metadata, never shown as prose
META = {'id', 'src', 'pdf', 'source', 'book', 'file', 'src_qid', 'why_src', 'answer_src', 'type', 'mode', 'tone', 'status',
        'svg', 'diagram', 'lesson', 'label', 'section', 'kind', 'style', 'reveal', 'show', 'color', 'enriched', 'from_global',
        'exam_question', 'orig', 'fills', '$schema', 'source_outline', 'pins_meta'}
CUT_END = re.compile(r'(?:[,(\[{=+−\-×/÷:;]|\b(?:the|a|an|and|or|of|to|is|are|with|for|in|by|from|that|which))\s*$', re.I)


def walk_strings(o, path=''):
    if isinstance(o, str):
        yield path, o
    elif isinstance(o, list):
        for i, x in enumerate(o):
            yield from walk_strings(x, f'{path}[{i}]')
    elif isinstance(o, dict):
        for k, v in o.items():
            if k in META:
                continue
            yield from walk_strings(v, f'{path}.{k}' if path else k)


def card_text(c):
    return ' '.join(s for _, s in walk_strings(c))


def credits():
    try:
        return json.load(open(os.path.join(MEDIA, 'credits.json')))
    except Exception:
        return {}


def placements():
    out = defaultdict(list)
    for n in ['placements.json', 'taxonomy_extra.json', 'g11_extra.json', 'commons_extra.json']:
        p = os.path.join(MEDIA, n)
        if not os.path.exists(p):
            continue
        for x in json.load(open(p)).get('cards', []):
            out[x['lesson']].append((n, x['card']))
    return out


def pubspec_dirs():
    dirs = []
    for line in open(os.path.join(ROOT, 'pubspec.yaml')):
        m = re.match(r'\s*-\s+(assets/\S+/)\s*$', line)
        if m:
            dirs.append(m.group(1))
    return dirs


def effective_units(book_path):
    d = json.load(open(book_path))
    out = []
    for u in d.get('units', []):
        ov = os.path.join(BASE, f"unit_{u.get('id')}.json")
        if os.path.exists(ov):
            out.append((json.load(open(ov)), os.path.basename(ov), True))
        else:
            out.append((u, os.path.basename(book_path), False))
    return d, out


def scan(subjects=None):
    cr, pl, pdirs = credits(), placements(), pubspec_dirs()
    issues = []  # dicts: book, unit, lesson, card, kind, field, text
    stats = {}
    cur = {'filled': set()}  # ids / unit-level field prefixes that a later card explicitly fills (card key 'fills')

    def add(**k):
        if k.get('kind') in ('pointer', 'cut_off'):
            f = cur['filled']
            if k.get('card') in f or any(k.get('field', '').startswith(x) for x in f if '.' in x or '[' in x):
                k['kind'] += '_filled'  # still reported, in its own column: the content now follows in a new card
        issues.append(k)
    for bp in sorted(glob.glob(os.path.join(BASE, '*_*.json'))):
        name = os.path.basename(bp)
        if name.startswith('unit_') or 'index' in name:
            continue
        subj = name.rsplit('_', 1)[0]
        if subjects and subj not in subjects:
            continue
        book, units = effective_units(bp)
        bst = stats[name[:-5]] = {'units': 0, 'lessons': 0, 'cards': 0, 'thin': 0, 'few_checks': 0, 'no_worked': 0, 'ex_lt20': 0,
                                  'exq': 0, 'checks': 0, 'worked': 0, 'overrides': 0}
        para_count = Counter()
        for u, file, is_ov in units:
            uid = u.get('id')
            cur['filled'] = {x for l in u.get('lessons', []) for c in l.get('cards', []) for x in (c.get('fills') or [])}
            bst['units'] += 1
            bst['overrides'] += is_ov
            diagrams = u.get('diagrams') or {}
            for dk, dg in diagrams.items():
                svg = dg.get('svg', '')
                fp = os.path.join(BASE, svg)
                if not svg or not os.path.exists(fp):
                    add(book=name, file=file, unit=uid, kind='missing_asset', field=f'diagrams.{dk}', text=svg)
                elif not any((('assets/high/notes/notes/' + svg).startswith(dd) and '/' not in ('assets/high/notes/notes/' + svg)[len(dd):]) for dd in pdirs):
                    add(book=name, file=file, unit=uid, kind='asset_not_in_pubspec', field=f'diagrams.{dk}', text=svg)
            for p, s in walk_strings({k: v for k, v in u.items() if k != 'lessons'}):
                if POINTER_RE.search(s):
                    add(book=name, file=file, unit=uid, kind='pointer', field=p, text=s)
                if s.count('$$') % 2:
                    add(book=name, file=file, unit=uid, kind='odd_dollars', field=p, text=s)
            for lsn in u.get('lessons', []):
                lid = lsn.get('id')
                bst['lessons'] += 1
                chars = checks = worked = mnem = teach = 0
                for c in lsn.get('cards', []):
                    bst['cards'] += 1
                    t, cid = c.get('type'), c.get('id')
                    txt = card_text(c)
                    chars += len(txt)
                    if t in ('text', 'remember', 'table', 'mnemonic', 'grammar', 'reading', 'diagram', 'steps', 'states', 'graph', 'worked'):
                        teach += len(txt)
                    checks += t == 'check'
                    worked += t == 'worked'
                    mnem += t == 'mnemonic'
                    for p, s in walk_strings(c):
                        if POINTER_RE.search(s):
                            add(book=name, file=file, unit=uid, lesson=lid, card=cid, kind='pointer', field=p, text=s)
                        if s.count('$$') % 2:
                            add(book=name, file=file, unit=uid, lesson=lid, card=cid, kind='odd_dollars', field=p, text=s)
                        if len(s) > 25 and CUT_END.search(s) and not s.rstrip().endswith('...') and not (s.rstrip().endswith(':') and ('steps[' in p or '**' in s or p.split('.')[-1] in ('q', 'problem') or p.endswith('.q'))):
                            add(book=name, file=file, unit=uid, lesson=lid, card=cid, kind='cut_off', field=p, text=s)
                        if s.count('(') > s.count(')') and len(s) > 20:
                            add(book=name, file=file, unit=uid, lesson=lid, card=cid, kind='cut_off', field=p, text=s)
                        if len(s) > 70:
                            para_count[s.strip()] += 1
                    body = [b for b in c.get('body', []) if isinstance(b, str) and b.strip()] if isinstance(c.get('body'), list) else c.get('body')
                    if t in ('text', 'remember', 'mnemonic') and not body and not c.get('letters'):
                        add(book=name, file=file, unit=uid, lesson=lid, card=cid, kind='empty', field='body', text=c.get('title', ''))
                    if t in ('text', 'remember') and body and len(' '.join(body)) < 40:
                        add(book=name, file=file, unit=uid, lesson=lid, card=cid, kind='title_only', field='body', text=' | '.join(body))
                    if t in ('text', 'remember') and body and ' '.join(body).strip().rstrip('.:').lower() == (c.get('title') or '').strip().rstrip('.:').lower():
                        add(book=name, file=file, unit=uid, lesson=lid, card=cid, kind='title_only', field='body', text=' | '.join(body))
                    if t == 'table':
                        rows = c.get('rows') or []
                        if not rows or not c.get('head'):
                            add(book=name, file=file, unit=uid, lesson=lid, card=cid, kind='empty_table', field='rows', text=c.get('title', ''))
                        for r in rows:
                            if not isinstance(r, list) or any(not isinstance(x, str) for x in r):
                                add(book=name, file=file, unit=uid, lesson=lid, card=cid, kind='bad_table', field='rows', text=str(r)[:80])
                            elif c.get('head') and len(r) != len(c['head']):
                                add(book=name, file=file, unit=uid, lesson=lid, card=cid, kind='table_width', field='rows', text=str(r)[:80])
                            elif all(not x.strip() for x in r):
                                add(book=name, file=file, unit=uid, lesson=lid, card=cid, kind='empty_table', field='rows', text='blank row')
                    if t == 'check':
                        opts = c.get('options') or {}
                        if not c.get('q') or len(opts) < 2 or c.get('answer') not in opts or not c.get('why'):
                            add(book=name, file=file, unit=uid, lesson=lid, card=cid, kind='bad_key', field='check', text=f"{c.get('q')} -> {c.get('answer')} {list(opts)}")
                    if t == 'worked':
                        if not c.get('problem') or not c.get('steps') or not c.get('answer'):
                            add(book=name, file=file, unit=uid, lesson=lid, card=cid, kind='empty', field='worked', text=c.get('title', ''))
                    if t in ('diagram', 'steps', 'states') or (t == 'worked' and c.get('diagram')):
                        if c.get('diagram') not in diagrams:
                            add(book=name, file=file, unit=uid, lesson=lid, card=cid, kind='missing_asset', field='diagram', text=str(c.get('diagram')))
                for src, m in pl.get(lid, []):
                    k = m.get('kind')
                    if k in ('photo', 'model'):
                        c0 = cr.get(m.get('id'))
                        if not c0 or not os.path.exists(os.path.join(MEDIA, c0.get('file', '~'))):
                            add(book=name, file=src, unit=uid, lesson=lid, card=m.get('id'), kind='missing_asset', field='media', text=str(m.get('id')))
                    if k == 'label' and not os.path.exists(os.path.join(MEDIA, (cr.get(str(m.get('img'))) or {}).get('file', '~'))):
                        add(book=name, file=src, unit=uid, lesson=lid, card=m.get('id'), kind='missing_asset', field='media.img', text=str(m.get('img')))
                    for p, s in walk_strings(m):
                        if POINTER_RE.search(s):
                            add(book=name, file=src, unit=uid, lesson=lid, card=m.get('id'), kind='pointer', field='media.' + p, text=s)
                if teach < 1500:
                    bst['thin'] += 1
                    add(book=name, file=file, unit=uid, lesson=lid, kind='thin', field='teaching chars', text=f'{teach} ({lsn.get("title")})')
                if checks < 3:
                    bst['few_checks'] += 1
                    add(book=name, file=file, unit=uid, lesson=lid, kind='few_checks', field='check', text=str(checks))
                if worked < 1:
                    bst['no_worked'] += 1
                    add(book=name, file=file, unit=uid, lesson=lid, kind='no_worked', field='worked', text='0')
                bst['checks'] += checks
                bst['worked'] += worked
            qs = (u.get('exercise') or {}).get('questions') or []
            bst['exq'] += len(qs)
            if len(qs) < 20:
                bst['ex_lt20'] += 1
                add(book=name, file=file, unit=uid, kind='few_exercise', field='exercise', text=str(len(qs)))
            seen = set()
            for q in qs:
                t = q.get('type')
                bad = None
                if q.get('id') in seen:
                    bad = 'duplicate id'
                seen.add(q.get('id'))
                if t == 'mcq' and (q.get('answer') not in (q.get('options') or {}) or len(q.get('options') or {}) < 2):
                    bad = 'mcq answer not in options'
                if t == 'fill' and q.get('answer') not in (q.get('choices') or []):
                    bad = 'fill answer not in choices'
                if t == 'tf' and not isinstance(q.get('answer'), bool):
                    bad = 'tf answer not bool'
                if t == 'short' and not str(q.get('answer', '')).strip():
                    bad = 'short answer empty'
                if t not in ('mcq', 'tf', 'fill', 'short'):
                    bad = f'unknown type {t}'
                if not q.get('why') or not q.get('q'):
                    bad = 'missing q/why'
                if bad:
                    add(book=name, file=file, unit=uid, card=q.get('id'), kind='bad_key', field='exercise', text=f"{bad}: {str(q.get('q'))[:80]}")
            for g in u.get('games') or []:
                if g.get('type') == 'label' and g.get('diagram') not in diagrams:
                    add(book=name, file=file, unit=uid, card=g.get('id'), kind='missing_asset', field='games.label', text=str(g.get('diagram')))
        for s, n in para_count.items():
            if n >= 3:
                add(book=name, file='*', unit='*', kind='repeated_paragraph', field=str(n), text=s)
    return issues, stats


BLOCKING = {'pointer', 'empty', 'title_only', 'empty_table', 'bad_table', 'bad_key', 'missing_asset', 'odd_dollars', 'asset_not_in_pubspec'}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--json')
    ap.add_argument('--subjects')
    ap.add_argument('--strict', action='store_true')
    ap.add_argument('--show', default='')
    a = ap.parse_args()
    subs = set(a.subjects.split(',')) if a.subjects else None
    issues, stats = scan(subs)
    if a.json:
        json.dump({'issues': issues, 'stats': stats}, open(a.json, 'w'), indent=1, ensure_ascii=False)
    by = defaultdict(Counter)
    for i in issues:
        by[i['book']][i['kind']] += 1
    kinds = sorted({i['kind'] for i in issues})
    print('book'.ljust(26) + ' '.join(k[:9].rjust(9) for k in kinds))
    for b in sorted(by):
        print(b[:-5].ljust(26) + ' '.join(str(by[b][k]).rjust(9) for k in kinds))
    print()
    for b, s in stats.items():
        print(b.ljust(26), s)
    for i in issues:
        if a.show and i['kind'] in a.show.split(','):
            print(f"[{i['kind']}] {i['book']} {i.get('unit')} {i.get('lesson', '')} {i.get('card', '')} {i['field']}: {i['text'][:160]}")
    if a.strict:
        blk = [i for i in issues if i['kind'] in BLOCKING and not i['book'].startswith(('history_', 'physics_'))]
        if blk:
            print(f'\n{len(blk)} blocking issues')
            sys.exit(1)


if __name__ == '__main__':
    main()
