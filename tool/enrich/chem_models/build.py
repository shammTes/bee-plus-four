#!/usr/bin/env python3
"""Chemistry models and tutor notes for Grades 9-11 (separation methods, polarity, London forces, concentration units,
colligative properties, acid-base theories, energy changes, equilibrium, carbon allotropes, carbonic acid, activity series,
ideal and real gases).

    python3 tool/enrich/chem_models/build.py

Idempotent: every card, question, game and diagram it adds carries a "-cm-" id (diagram keys "cm_"), and those are removed
and re-inserted on every run. It also removes the old Grade 9 3-D models and orphan diagrams (water V-shape, tetrahedron,
NaCl lattice, random-dots particle movie). Writes the SVGs to assets/high/notes/notes/svg/chemistry_<g>/ and the topic
card lists in index.json. Afterwards run tool/split_notes.py and tool/build_tutor_index.py.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
ROOT = os.path.normpath(os.path.join(HERE, '..', '..', '..'))
NOTES = os.path.join(ROOT, 'assets', 'high', 'notes', 'notes')
MEDIA = os.path.join(ROOT, 'assets', 'high', 'media')

import g9  # noqa: E402
import g10  # noqa: E402
import g11  # noqa: E402
import svg_g9  # noqa: E402
import svg_g10  # noqa: E402
import svg_g11  # noqa: E402

# old Grade 9 models: (unit, diagram key) whose SVG is deleted, cards removed, and 3-D model placements removed
OLD_DIAGRAMS = [('chem9-u1', 'f2'), ('chem9-u2', 'f4'), ('chem9-u2', 'f5'), ('chem9-u3', 'f7')]
OLD_CARDS = {'chem9-u1-c14', 'chem9-u1-c15'}
OLD_PLACEMENTS = {('chem9-u2-l2-2', 'm_water'), ('chem9-u2-l2-2', 'm_nacl')}
TOPIC_TYPES = {'text', 'table', 'steps', 'states', 'diagram'}
# glossary entries this tool adds (removed before re-adding, matched on term + meaning)
OURS = {(t, m) for t, m, _ in g9.GLOSSARY} | {(t, m) for mod in (g10, g11) for v in mod.GLOSSARY.values() for t, m, _ in v}


def load(p):
    with open(p, encoding='utf-8') as f:
        return json.load(f)


def save(p, d, indent=2, newline=True):
    with open(p, 'w', encoding='utf-8') as f:
        json.dump(d, f, ensure_ascii=False, indent=indent)
        if newline:
            f.write('\n')


def is_cm(i):
    return '-cm-' in i


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
            l['cards'] = [c for c in l['cards'] if not is_cm(c['id']) and c['id'] not in OLD_CARDS]
        if 'exercise' in u:
            u['exercise']['questions'] = [q for q in u['exercise']['questions'] if not is_cm(q['id'])]
        if 'games' in u:
            u['games'] = [g for g in u['games'] if not is_cm(g['id'])]
        if 'glossary' in u:
            u['glossary'] = [g for g in u['glossary'] if (g['term'], g['meaning']) not in OURS]
        for k in [k for k in u.get('diagrams', {}) if k.startswith('cm_')]:
            del u['diagrams'][k]


def remove_old(book):
    for uid, key in OLD_DIAGRAMS:
        u = unit_of(book, uid)
        used = [c['id'] for l in u['lessons'] for c in l['cards'] if c.get('diagram') == key]
        assert not used, (uid, key, used)
        d = u['diagrams'].pop(key, None)
        if d:
            p = os.path.join(NOTES, d['svg'])
            if os.path.exists(p):
                os.remove(p)
        if u.get('unitMap'):
            for n in u['unitMap'].get('nodes', []):
                n['cards'] = [c for c in n.get('cards', []) if c not in OLD_CARDS]


def write_diagrams(book, uid, keys, mod):
    u = unit_of(book, uid)
    folder = f"svg/chemistry_{uid.split('-')[0][4:]}"
    os.makedirs(os.path.join(NOTES, folder), exist_ok=True)
    short = uid.replace('-', '_')
    for key, sk in keys.items():
        fn, title, page = mod.ALL[sk]
        rel = f'{folder}/{short}_{key}.svg'
        with open(os.path.join(NOTES, rel), 'w', encoding='utf-8') as f:
            f.write(fn())
        u.setdefault('diagrams', {})[key] = {'svg': rel, 'title': title, 'page': page, 'pins': []}


def insert(book, blocks):
    for lid, after, cards in blocks:
        u, l = lesson_of(book, lid)
        ids = [c['id'] for c in l['cards']]
        at = ids.index(after) + 1 if after else len(ids)
        # keep several blocks after the same anchor in order
        while at < len(ids) and is_cm(ids[at]):
            at += 1
        l['cards'][at:at] = cards
        for c in cards:
            if 'diagram' in c:
                assert c['diagram'] in u.get('diagrams', {}), (lid, c['id'], c['diagram'])


def add_unit_extras(book, uid, qs, gloss, games=()):
    u = unit_of(book, uid)
    u.setdefault('exercise', {'questions': []})['questions'].extend(qs)
    have = {g['term'].lower() for g in u.get('glossary', [])}
    for term, meaning, page in gloss:
        if term.lower() not in have:
            u.setdefault('glossary', []).append({'term': term, 'meaning': meaning, 'page': page, 'src': 'notes'})
    u.setdefault('games', []).extend(games)


def check_ids(book):
    seen = set()
    for u in book['units']:
        for i in [c['id'] for l in u['lessons'] for c in l['cards']] + [q['id'] for q in u.get('exercise', {}).get('questions', [])] + [g['id'] for g in u.get('games', [])]:
            assert i not in seen, i
            seen.add(i)


def update_index(books):
    ip = os.path.join(NOTES, 'index.json')
    idx = load(ip)
    lessons = {}
    for b in books.values():
        for u in b['units']:
            for l in u['lessons']:
                lessons[l['id']] = l
    for g in idx['grades'].values():
        for subj in g.values():
            if not subj.get('book', '').startswith('chemistry_'):
                continue
            for un in subj['units']:
                for t in un.get('topics', []):
                    l = lessons.get(t['id'])
                    if not l:
                        continue
                    t['cards'] = [c for c in t['cards'] if not is_cm(c) and c not in OLD_CARDS]
                    t['cards'] += [c['id'] for c in l['cards'] if is_cm(c['id']) and c['type'] in TOPIC_TYPES]
    save(ip, idx)


def update_media():
    pp = os.path.join(MEDIA, 'placements.json')
    pl = load(pp)
    pl['cards'] = [x for x in pl['cards'] if (x.get('lesson'), x.get('card', {}).get('id')) not in OLD_PLACEMENTS]
    save(pp, pl, indent=1, newline=False)
    used = {x.get('card', {}).get('id') for x in pl['cards']}
    cp = os.path.join(MEDIA, 'credits.json')
    cr = load(cp)
    for mid in ('m_water', 'm_nacl'):
        if mid not in used and mid in cr:
            f = os.path.join(MEDIA, cr[mid]['file'])
            if os.path.exists(f):
                os.remove(f)
            del cr[mid]
    save(cp, cr, indent=1)


def main():
    books = {g: load(os.path.join(NOTES, f'chemistry_{g}.json')) for g in (9, 10, 11)}
    for b in books.values():
        clean(b)
    remove_old(books[9])

    write_diagrams(books[9], 'chem9-u1', g9.DIAGRAMS, svg_g9)
    insert(books[9], g9.BLOCKS)
    add_unit_extras(books[9], 'chem9-u1', g9.U.qs, g9.GLOSSARY, g9.GAMES)

    for mod, b, svgmod in ((g10, books[10], svg_g10), (g11, books[11], svg_g11)):
        for uid, (unit, keys) in mod.UNITS.items():
            write_diagrams(b, uid, keys, svgmod)
        insert(b, mod.BLOCKS)
        for uid, (unit, keys) in mod.UNITS.items():
            add_unit_extras(b, uid, unit.qs, mod.GLOSSARY.get(uid, []))

    for g, b in books.items():
        check_ids(b)
        save(os.path.join(NOTES, f'chemistry_{g}.json'), b)
    update_index(books)
    update_media()
    n = sum(1 for b in books.values() for u in b['units'] for l in u['lessons'] for c in l['cards'] if is_cm(c['id']))
    q = sum(1 for b in books.values() for u in b['units'] for x in u.get('exercise', {}).get('questions', []) if is_cm(x['id']))
    print(f'chem models: {n} cards, {q} exercise questions')


if __name__ == '__main__':
    main()
