#!/usr/bin/env python3
"""Agriculture deep tutor notes (Grades 11-12): full explanations, Eritrean examples, key-fact tables, comparisons, worked
examples, SVG figures and extra practice questions for every section of the textbook, merged into
assets/high/notes/notes/agriculture_<g>.json. Same pipeline as tool/enrich/math_deep/build.py (marker "-ad-", diagram keys
"ad_", figures in svg/agri_<g>/a<g>_u<n>_<key>.svg, checked by test/notes_agri_svg_test.dart).

    python3 tool/enrich/agri_deep/build.py            # all unit modules g<grade>_u<n>.py in this folder
    python3 tool/enrich/agri_deep/build.py 11         # only Grade 11

A unit module defines
    UID       'agri11-u1'
    LESSONS   {lesson id: [items]}  item = existing card id (kept, moved to this place) or a card dict (common.py helpers);
              a card dict with an existing id replaces that card. Existing cards not listed stay at the end of the lesson.
    DIAGRAMS  {key: (svg text, caption, textbook page)}  -> svg/agri_<g>/a<g>_u<n>_<key>.svg, unit diagram 'ad_<key>'
    QS        practice questions (common.QSet items) appended to the unit exercise
    DROP  [card ids]  thin / broken cards whose content is now covered by a new card (removed, also from the unit map)
    PATCH {card id: {field: value}}   GLOSSARY  [(term, meaning, page)]   TIPS [(text, page)]   IDEAS [(node id, label, topic node, card id)] (unit map)

Idempotent: everything it adds carries "-ad-" (diagram keys "ad_") and is removed and re-inserted on every run; stale
figure SVG files are deleted; DROP is applied again on every run. Also updates the lessons' topic card lists in index.json. Afterwards run tool/split_notes.py,
tools/map_unit_questions.py, tools/verify_unit_links.py and tool/build_tutor_index.py.
"""
import copy
import glob
import importlib
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(1, os.path.join(HERE, '..', 'math_deep'))  # svglib.py (shared SVG builder)
ROOT = os.path.normpath(os.path.join(HERE, '..', '..', '..'))
NOTES = os.path.join(ROOT, 'assets', 'high', 'notes', 'notes')


def md(i):
    return '-ad-' in i


def modules(grades):
    out = []
    for p in sorted(glob.glob(os.path.join(HERE, 'g*_u*.py')), key=lambda p: [int(x) for x in re.findall(r'\d+', os.path.basename(p))]):
        m = re.match(r'g(\d+)_u(\d+)\.py$', os.path.basename(p))
        if m and (not grades or m[1] in grades):
            out.append((int(m[1]), int(m[2]), importlib.import_module(os.path.basename(p)[:-3])))
    return out


def merge_unit(g, un, unit, mod):
    uid = unit['id']
    assert uid == mod.UID, (uid, mod.UID)
    svgdir = f'svg/agri_{g}'
    os.makedirs(os.path.join(NOTES, svgdir), exist_ok=True)
    # 0) remove what an earlier run added
    drop = set(getattr(mod, 'DROP', []))
    for l in unit['lessons']:
        l['cards'] = [c for c in l['cards'] if not md(c['id']) and c['id'] not in drop]
    ex = unit.setdefault('exercise', {}).setdefault('questions', [])
    unit['exercise']['questions'] = ex = [q for q in ex if not md(q['id'])]
    dg = unit.setdefault('diagrams', {})
    for k in [k for k in dg if k.startswith('ad_')]:
        del dg[k]
    for f in glob.glob(os.path.join(NOTES, svgdir, f'a{g}_u{un}_*.svg')):
        os.remove(f)
    # 1) diagrams
    svg_text = {}
    for k, (svg, title, page) in mod.DIAGRAMS.items():
        s = str(svg)
        rel = f'{svgdir}/a{g}_u{un}_{k}.svg'
        with open(os.path.join(NOTES, rel), 'w', encoding='utf-8') as f:
            f.write(s)
        dg['ad_' + k] = {'svg': rel, 'title': title, 'page': page, 'pins': []}
        svg_text['ad_' + k] = s
    # 2) lessons
    lessons = {l['id']: l for l in unit['lessons']}
    by_id = {c['id']: c for l in unit['lessons'] for c in l['cards']}
    used = set()
    new = {}
    for lid, items in mod.LESSONS.items():
        assert lid in lessons, lid
        out = []
        for it in items:
            if isinstance(it, str):
                assert it in by_id, f'{uid}: unknown card {it}'
                c = copy.deepcopy(by_id[it])
            else:
                c = copy.deepcopy(it)
                if not md(c['id']):
                    assert c['id'] in by_id, f'{uid}: replacement for unknown card {c["id"]}'
                    old = by_id[c['id']]
                    for k in ('enriched',):
                        if k in old:
                            c[k] = old[k]
            assert c['id'].startswith(uid + '-'), c['id']
            assert c['id'] not in used, f'{uid}: card used twice {c["id"]}'
            used.add(c['id'])
            out.append(c)
        new[lid] = out
    for lid, out in new.items():
        l = lessons[lid]
        left = [c for c in l['cards'] if c['id'] not in used]
        l['cards'] = out + left
    for l in unit['lessons']:
        if l['id'] not in new:
            l['cards'] = [c for c in l['cards'] if c['id'] not in used or c['id'] in {x['id'] for x in l['cards']}]
    # 2b) presentation patches for cards kept as they are: PATCH = {card id: {field: value}} (e.g. a table layout)
    #     '_inline': True turns display maths in table cells into inline maths (and drops ** around maths) so a
    #     cards / compare layout reads as running text
    for l in unit['lessons']:
        for c in l['cards']:
            p = dict(getattr(mod, 'PATCH', {}).get(c['id'], {}))
            if p.pop('_inline', False):
                fix = lambda s: s.replace('**', '').replace('$$', '$') if '$' in s else s
                c['head'] = [fix(h) for h in c['head']]
                c['rows'] = [[fix(x) for x in r] for r in c['rows']]
            c.update(p)
    unknown = set(getattr(mod, 'PATCH', {})) - {c['id'] for l in unit['lessons'] for c in l['cards']}
    assert not unknown, f'{uid}: PATCH for unknown cards {unknown}'
    # 3) checks
    ids = [c['id'] for l in unit['lessons'] for c in l['cards']]
    dup = {i for i in ids if ids.count(i) > 1}
    assert not dup, f'{uid}: duplicate card ids {dup}'
    for l in unit['lessons']:
        for c in l['cards']:
            if c.get('diagram'):
                assert c['diagram'] in dg, (c['id'], c['diagram'])
            if c['type'] == 'steps' and c['diagram'] in svg_text:
                for st in c['steps']:
                    if st.get('show'):
                        assert f'data-hl="{st["show"]}"' in svg_text[c['diagram']] or re.search(r'data-s="[^"]*\b%s\b' % re.escape(st['show']), svg_text[c['diagram']]), (c['id'], st['show'])
            if c['type'] == 'check':
                assert c['answer'] in c['options'], c['id']
            if c['type'] == 'table':
                assert all(len(r) == len(c['head']) for r in c['rows']), c['id']
    unused = set(svg_text) - {c.get('diagram') for l in unit['lessons'] for c in l['cards']}
    assert not unused, f'{uid}: diagrams never shown {unused}'
    # 4) exercise questions
    for q in mod.QS:
        if q['type'] == 'mcq':
            assert q['answer'] in q['options'], q['id']
        if q['type'] == 'fill':
            assert q['answer'] in q['choices'], q['id']
        assert q['why'] and q['tip'] and q['similar'], q['id']
        ex.append(q)
    qids = [q['id'] for q in ex]
    assert len(qids) == len(set(qids)), f'{uid}: duplicate question ids'
    assert not set(qids) & set(ids), f'{uid}: question id clashes with a card id'
    # 5) glossary and tips (merged by term / text)
    have = {x['term'].lower() for x in unit.get('glossary', [])}
    for t, m, p in getattr(mod, 'GLOSSARY', []):
        if t.lower() not in have:
            unit.setdefault('glossary', []).append({'term': t, 'meaning': m, 'page': p, 'src': 'notes'})
            have.add(t.lower())
    have = {x['text'] for x in unit.get('tips', [])}
    for t, p in getattr(mod, 'TIPS', []):
        if t not in have:
            unit.setdefault('tips', []).append({'text': t, 'page': p, 'src': 'notes'})
    # 6) unit map: key ideas
    um = unit.get('unitMap')
    if um:
        um['nodes'] = [x for x in um['nodes'] if not x['id'].startswith('ad_')]
        um['edges'] = [e for e in um.get('edges', []) if not e['to'].startswith('ad_')]
        live = set(ids)
        first = {l['id']: l['cards'][0]['id'] for l in unit['lessons'] if l['cards']}
        gone = set()
        for x in um['nodes']:
            if 'cards' in x:
                x['cards'] = [c for c in x['cards'] if c in live]
                if not x['cards']:  # every card of the node was dropped: point it at its lesson / the unit start
                    if x.get('lesson') in first:
                        x['cards'] = [first[x['lesson']]]
                    elif x['kind'] == 'unit':
                        x['cards'] = [unit['lessons'][0]['cards'][0]['id']]
                    else:
                        gone.add(x['id'])
        um['nodes'] = [x for x in um['nodes'] if x['id'] not in gone]
        um['edges'] = [e for e in um.get('edges', []) if e['from'] not in gone and e['to'] not in gone]
        nids = {x['id'] for x in um['nodes']}
        for nid, lab, frm, card in getattr(mod, 'IDEAS', []):
            assert card in ids, card
            if frm in nids:
                um['nodes'].append({'id': 'ad_' + nid, 'label': lab, 'kind': 'idea', 'cards': [card]})
                um['edges'].append({'from': frm, 'to': 'ad_' + nid, 'label': 'key idea'})
    return list(new)


def main():
    grades = set(sys.argv[1:])
    mods = modules(grades)
    by_grade = {}
    for g, un, m in mods:
        by_grade.setdefault(g, []).append((un, m))
    idx_p = os.path.join(NOTES, 'index.json')
    with open(idx_p, encoding='utf-8') as f:
        idx = json.load(f)
    for g, lst in by_grade.items():
        p = os.path.join(NOTES, f'agriculture_{g}.json')
        with open(p, encoding='utf-8') as f:
            book = json.load(f)
        units = {u['id']: u for u in book['units']}
        touched = {}
        drops = set()
        for un, m in lst:
            before = sum(len(l['cards']) for l in units[m.UID]['lessons']), len(units[m.UID]['exercise']['questions'])
            touched[m.UID] = merge_unit(g, un, units[m.UID], m)
            drops |= set(getattr(m, 'DROP', []))
            u = units[m.UID]
            after = sum(len(l['cards']) for l in u['lessons']), len(u['exercise']['questions'])
            print(f'{m.UID}: cards {before[0]} -> {after[0]}, questions {before[1]} -> {after[1]}, figures {len([k for k in u["diagrams"] if k.startswith("ad_")])}')
        with open(p, 'w', encoding='utf-8') as f:
            json.dump(book, f, ensure_ascii=False, indent=2)
            f.write('\n')
        lessons = {l['id']: l for u in book['units'] for l in u['lessons']}
        topics = idx['grades'][str(g)]['agriculture']['units']
        for tu in topics:
            if tu['id'] not in touched:
                continue
            for t in tu['topics']:
                if t['id'] in touched[tu['id']]:
                    old = {c for c in t.get('cards', []) if not md(c) and c not in drops}
                    t['cards'] = [c['id'] for c in lessons[t['id']]['cards'] if c['id'] in old or c['type'] == 'text']
    with open(idx_p, 'w', encoding='utf-8') as f:
        json.dump(idx, f, ensure_ascii=False, indent=2)
        f.write('\n')


if __name__ == '__main__':
    main()
