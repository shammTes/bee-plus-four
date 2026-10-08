#!/usr/bin/env python3
"""Apply the Oct 2026 teacher-feedback patch to the English notes (Grades 9-12), keep the indexes and the Grade 11
exercise bank in sync. Idempotent: running it twice gives the same files.

  python3 tool/english/teacher_feedback/run.py
then regenerate: tool/split_notes.py, tool/build_tutor_index.py, tools/map_unit_questions.py, tools/verify_unit_links.py
"""
import collections
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import Book, load_json, save_json, NOTES, EXER, _walk_strings  # noqa: E402
import clean  # noqa: E402
import g9  # noqa: E402
import g10  # noqa: E402
import g11a  # noqa: E402
import g11b  # noqa: E402
import g11c  # noqa: E402
import g11d  # noqa: E402

# wrong keys found while checking every explanation against its options
ANSWER_FIX = {'eng10-u6-chkE1': 'B', 'eng12-u6-chkE1': 'B', 'eng11-u12-q03': 'B', 'eng11-u5-q08': 'C', 'eng11-u7-q02': 'B',
              'eng11-u25-q02': 'B', 'eng11-u8-q02': 'B', 'eng11-u11-q02': 'C', 'eng11-u13-q02': 'B', 'eng11-u14-q02': 'C',
              'eng11-u6-q09': 'B', 'eng11-u7-q09': 'B'}
# Grade 11 bank items about transitive verbs / objects (now Unit 8)
TV_ITEMS = ['english_11_practice_g11_english_47', 'english_11_practice_g11_english_66', 'english_11_practice_g11_english_94',
            'english_11_practice_g11_english_96', 'english_11_practice_g11_english_196', 'english_11_sn_5', 'english_11_sn_14']


def objs(b):
    for u in b.d['units']:
        for l in u['lessons']:
            for c in l['cards']:
                yield u, c
        for q in u['exercise']['questions']:
            yield u, q


def fix_keys(b, log):
    for u, o in objs(b):
        if o['id'] in ANSWER_FIX and o.get('answer') != ANSWER_FIX[o['id']]:
            log.append(f"{o['id']}: answer {o['answer']} -> {ANSWER_FIX[o['id']]}")
            o['answer'] = ANSWER_FIX[o['id']]
        if o['id'] == 'eng11-u7-q02':
            o['q'] = o['q'].replace('extremely looking forward', 'really looking forward')


def suspicious(b):
    """explanations that name another option as the correct one"""
    out = []
    for u, o in objs(b):
        if o.get('type') not in ('check', 'mcq') or not isinstance(o.get('answer'), str):
            continue
        w = o['why'] if isinstance(o['why'], str) else '\n'.join(o['why'])
        for m in re.finditer(r'Option ([A-E]) is (?:the )?correct|correct (?:answer|option|choice) is (?:option )?\(?([A-E])\b|\(Option ([A-E])\) (?:is|as) (?:the )?correct', w):
            x = next(g for g in m.groups() if g)
            if x != o['answer']:
                out.append(f"{o['id']}: key {o['answer']} but text says {x}")
    return out


def fix_pages(b):
    for u in b.d['units']:
        p0 = u['pages'][0]
        for q in u['exercise']['questions']:
            if q.get('page') == 1 and p0 != 1:
                q['page'] = p0
        for l in u['lessons']:
            for c in l['cards']:
                if c.get('page') == 1 and l['pages'][0] != 1:
                    c['page'] = l['pages'][0]


def index_units(b, old_units):
    old = {u['id']: u for u in old_units}
    out = []
    for u in b.d['units']:
        x = dict(old.get(u['id'], {}))
        x.update(id=u['id'], number=u['number'], title=u['title'], pages=list(u['pages']), questions=len(u['exercise']['questions']),
                 topics=[dict(id=l['id'], number=l['number'], title=l['title'], page=l['pages'][0], cards=[c['id'] for c in l['cards']]) for l in u['lessons']])
        out.append(x)
    return out


def update_indexes(books):
    for name in ('index.json', 'english_index.json'):
        path = os.path.join(NOTES, name)
        d, st = load_json(path)
        for g, b in books.items():
            e = d['grades'].get(str(g), {}).get('english')
            if e:
                e['units'] = index_units(b, e['units'])
        save_json(path, d, st)


def unit_bank_items(b, uid):
    """Exercise-tab items built from a unit's own notes questions and quick checks (Unit 8 is new, so the bank needs items)"""
    u = b.unit(uid)
    src = [c for l in u['lessons'] for c in l['cards'] if c['type'] == 'check'] + u['exercise']['questions']
    out = []
    for o in src:
        why = o['why'] if isinstance(o['why'], str) else '\n\n'.join(w for w in o['why'] if not w.startswith('Answer '))
        t = o.get('type')
        if t in ('check', 'mcq'):
            keys = sorted(o['options'])
            opts, ans = [o['options'][k] for k in keys], keys.index(o['answer'])
        elif t == 'fill':
            opts, ans = list(o['choices']), o['choices'].index(o['answer'])
        else:  # true/false and typed answers: the Exercise tab needs 3-5 options
            continue
        tip = o.get('tip')
        expl = why + (f'\n\n**Tip:** {tip}' if tip and 'Tip:' not in why else '')
        out.append(dict(id=f"english_11_au_{o['id'].replace('-', '_')}", unit=uid, prompt=o['q'], options=opts, answer=ans,
                        explanation=expl.strip(), verified='reviewed', src=f'authored#{uid}'))
    return out


def update_bank(log, b11=None):
    rules = g11a.COPULA_RULES + clean.HEAD + clean.WORDS + [(r'Predicate nominatives are nouns or pronouns\.', 'It is a noun or a pronoun.'), (r'\bcase concord\b', 'pronoun form'), (r'\bCase concord\b', 'Pronoun form'),
                                               (r'\bmorphological\b', 'word-form'), (r'\bconcatenative morphology\b', 'adding prefixes and suffixes')]
    ix, ixs = load_json(os.path.join(EXER, 'index.json'))
    for g in (9, 10, 11, 12):
        path = os.path.join(EXER, f'english_{g}.json')
        if not os.path.exists(path):
            continue
        d, st = load_json(path)
        items = d['questions']
        n = 0
        for it in items:
            for o, k in [(o, k) for o, k in _walk_strings(it) if not (o is it and k in ('unit', 'verified'))]:
                s = clean.delatex(o[k])
                for rx, rp in rules:
                    s = re.sub(rx, rp, s)
                if s != o[k]:
                    o[k] = s
                    n += 1
            if g == 11:
                if it['unit'] == 'eng11-u8' and it['id'] not in TV_ITEMS and not it['id'].startswith('english_11_au_eng11_u8_'):
                    it['unit'] = 'eng11-u25'
                if it['id'] in TV_ITEMS:
                    it['unit'] = 'eng11-u8'
        if g == 11 and b11 is not None:
            new = unit_bank_items(b11, 'eng11-u8')
            ids = {x['id'] for x in new}
            items[:] = [it for it in items if it['id'] not in ids and not it['id'].startswith('english_11_au_eng11_u8_')] + new
            log.append(f'exercises/english_11.json: {len(new)} Unit 8 items from the notes')
        log.append(f'exercises/english_{g}.json: {n} strings simplified')
        save_json(path, d, st)
        e = ix['grades'].get(str(g), {}).get('english')
        if e:
            cnt = collections.Counter(it['unit'] for it in items)
            e['count'] = len(items)
            e['units'] = {k: cnt[k] for k in sorted(cnt)}
    ix['total'] = sum(e.get('count', 0) for gr in ix['grades'].values() for e in gr.values() if isinstance(e, dict))
    save_json(os.path.join(EXER, 'index.json'), ix, ixs)


def main():
    log = []
    b10 = g10.apply()
    b9, b11, b12 = Book(9), Book(11), Book(12)
    g9.apply(b9)
    g11a.apply(b11)
    g11b.apply(b11)
    g11c.apply(b11)
    g11d.apply(b11)
    for b in (b9, b10, b12):
        b.sub_all(g11a.COPULA_RULES)
    books = {9: b9, 10: b10, 11: b11, 12: b12}
    for g, b in books.items():
        fix_keys(b, log)
        st = clean.clean_book(b)
        log.append(f'G{g} clean: {dict(st)}')
        fix_pages(b)
        for s in suspicious(b):
            log.append('CHECK ' + s)
        b.save()
    update_indexes(books)
    update_bank(log, b11)
    print('\n'.join(log))


if __name__ == '__main__':
    main()
