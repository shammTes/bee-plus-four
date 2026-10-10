#!/usr/bin/env python3
"""Chemistry tutor notes, Oct 2026 pass (sections checked against the Grade 9-11 textbooks):

  G9   2.1.5 electrical neutrality · 3.2.3 significance of symbols and formulas · 3.4.2 writing and balancing equations ·
       3.4.3 meaning of a balanced equation
  G10  1.4.5 patterns of formulas (valency) · 2.2.5 metallic bonding · 4.3.3 indicators in titration · 4.4.4 preparing salts ·
       4.5.1 measuring pH · 5.1.4 enthalpy of reaction
  G11  2.2.4 (concentration, nature of the electrode) · 2.2.5 applications of electrolysis · 2.2.6 Faraday's laws with
       balanced equations · 3.2 carbon cycle · 3.3 nitrogen cycle · 3.4.1 extraction of sulphur (Frasch) and allotropes ·
       3.4.3 Contact process, sulphuric acid and sulphates

    python3 tool/enrich/chem_oct10/build.py

Idempotent: everything it adds carries a "-co-" id (diagram keys "co_"); those are removed and re-inserted on every run.
FIXES in g9/g10/g11.py correct factual or garbled text in existing cards (set to a fixed value, so re-runs are no-ops).
Writes the SVGs to assets/high/notes/notes/svg/chemistry_<g>/ and the topic card lists in index.json.
Afterwards run tool/split_notes.py, tool/build_tutor_index.py, tools/map_unit_questions.py, tools/verify_unit_links.py.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
ROOT = os.path.normpath(os.path.join(HERE, '..', '..', '..'))
NOTES = os.path.join(ROOT, 'assets', 'high', 'notes', 'notes')

import co_g9 as g9  # noqa: E402
import co_g10 as g10  # noqa: E402
import co_g11 as g11  # noqa: E402
import svg_co  # noqa: E402

MODS = {9: g9, 10: g10, 11: g11}
TOPIC_TYPES = {'text', 'table', 'steps', 'states', 'diagram'}
OURS = {(t, m) for mod in MODS.values() for v in mod.GLOSSARY.values() for t, m, _ in v}


def load(p):
    with open(p, encoding='utf-8') as f:
        return json.load(f)


def save(p, d):
    with open(p, 'w', encoding='utf-8') as f:
        json.dump(d, f, ensure_ascii=False, indent=2)
        f.write('\n')


def is_co(i):
    return '-co-' in i


def unit_of(book, uid):
    return next(u for u in book['units'] if u['id'] == uid)


def lesson_of(book, lid):
    for u in book['units']:
        for l in u['lessons']:
            if l['id'] == lid:
                return u, l
    raise KeyError(lid)


def clean(book):
    for u in book['units']:
        for l in u['lessons']:
            l['cards'] = [c for c in l['cards'] if not is_co(c['id'])]
        if 'exercise' in u:
            u['exercise']['questions'] = [q for q in u['exercise']['questions'] if not is_co(q['id'])]
        if 'games' in u:
            u['games'] = [g for g in u['games'] if not is_co(g['id'])]
        if 'glossary' in u:
            u['glossary'] = [g for g in u['glossary'] if (g['term'], g['meaning']) not in OURS]
        for k in [k for k in u.get('diagrams', {}) if k.startswith('co_')]:
            del u['diagrams'][k]


def write_diagrams(book, uid, keys):
    u = unit_of(book, uid)
    folder = f"svg/chemistry_{uid.split('-')[0][4:]}"
    os.makedirs(os.path.join(NOTES, folder), exist_ok=True)
    short = uid.replace('-', '_')
    for key, sk in keys.items():
        fn, title, page = svg_co.ALL[sk]
        rel = f'{folder}/{short}_{key}.svg'
        with open(os.path.join(NOTES, rel), 'w', encoding='utf-8') as f:
            f.write(fn())
        u.setdefault('diagrams', {})[key] = {'svg': rel, 'title': title, 'page': page, 'pins': []}


def insert(book, blocks):
    for lid, after, cards in blocks:
        u, l = lesson_of(book, lid)
        ids = [c['id'] for c in l['cards']]
        at = ids.index(after) + 1 if after else len(ids)
        while at < len(ids) and is_co(ids[at]):
            at += 1
        l['cards'][at:at] = cards
        for c in cards:
            if 'diagram' in c:
                assert c['diagram'] in u.get('diagrams', {}), (lid, c['id'], c['diagram'])


def add_unit_extras(book, uid, qs, gloss):
    u = unit_of(book, uid)
    u.setdefault('exercise', {'questions': []})['questions'].extend(qs)
    have = {g['term'].lower() for g in u.get('glossary', [])}
    for term, meaning, page in gloss:
        if term.lower() not in have:
            u.setdefault('glossary', []).append({'term': term, 'meaning': meaning, 'page': page, 'src': 'notes'})


def apply_fixes(book, fixes):
    cards = {c['id']: c for u in book['units'] for l in u['lessons'] for c in l['cards']}
    for cid, field, value in fixes:
        c = cards[cid]
        if callable(value):
            c[field] = value(c[field])
        else:
            c[field] = value


def check_ids(book):
    seen = set()
    for u in book['units']:
        for i in [c['id'] for l in u['lessons'] for c in l['cards']] + [q['id'] for q in u.get('exercise', {}).get('questions', [])] + [g['id'] for g in u.get('games', [])]:
            assert i not in seen, i
            seen.add(i)


def update_index(books):
    ip = os.path.join(NOTES, 'index.json')
    idx = load(ip)
    lessons = {l['id']: l for b in books.values() for u in b['units'] for l in u['lessons']}
    for g in idx['grades'].values():
        for subj in g.values():
            if not subj.get('book', '').startswith('chemistry_'):
                continue
            for un in subj['units']:
                for t in un.get('topics', []):
                    l = lessons.get(t['id'])
                    if not l:
                        continue
                    t['cards'] = [c for c in t['cards'] if not is_co(c)]
                    t['cards'] += [c['id'] for c in l['cards'] if is_co(c['id']) and c['type'] in TOPIC_TYPES]
    save(ip, idx)


def main():
    books = {g: load(os.path.join(NOTES, f'chemistry_{g}.json')) for g in MODS}
    for g, b in books.items():
        mod = MODS[g]
        clean(b)
        apply_fixes(b, mod.FIXES)
        for uid, (unit, keys) in mod.U.items():
            write_diagrams(b, uid, keys)
        insert(b, mod.BLOCKS)
        for uid, (unit, keys) in mod.U.items():
            add_unit_extras(b, uid, unit.qs, mod.GLOSSARY.get(uid, []))
        check_ids(b)
        save(os.path.join(NOTES, f'chemistry_{g}.json'), b)
    update_index(books)
    n = sum(1 for b in books.values() for u in b['units'] for l in u['lessons'] for c in l['cards'] if is_co(c['id']))
    q = sum(1 for b in books.values() for u in b['units'] for x in u.get('exercise', {}).get('questions', []) if is_co(x['id']))
    d = sum(1 for b in books.values() for u in b['units'] for k in u.get('diagrams', {}) if k.startswith('co_'))
    print(f'chem oct10: {n} cards, {q} exercise questions, {d} diagrams')


if __name__ == '__main__':
    main()
