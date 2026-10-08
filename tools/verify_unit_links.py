#!/usr/bin/env python3
"""Check the notes-unit <-> matric/model question links and the unit <-> exercise links.

  python3 tools/verify_unit_links.py            # exit 1 on any error
  python3 tools/verify_unit_links.py --min 10   # threshold for the "few links" report (default 10)

Errors (fail):
  * assets/high/notes/unit_questions.json is not compact JSON, or a unit id is not a notes unit
  * a linked id is not in the eager exam bank (assets/high/exams/index.json papers) = dangling
  * a linked question's paper subject cannot belong to the unit's subject (see FAMILY)
  * a linked id is listed as dropped (broken) in tool/matric_unit_sync/report.json
  * the same id twice in one unit, or an entry without id/confidence
  * an exercise item (main or school file) has a unit that is not a notes unit of the file's subject
    (another grade of the same subject is reported, not failed: the item then shows under that unit)
  * duplicate exercise ids, or index.json counts that differ from the files
Report (no fail):
  * units with fewer than --min matric links, with the reason (how many questions the bank has for that topic)
  * per-unit exercise counts: the notes "Exercises (N)" chip and the Exercise tab tile both read the same
    map (ExamRepo.exerciseUnits), built here exactly as the app builds it
"""
import argparse, collections, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from unitmap_lib import ROOT, EXER, UQ, FAMILY, load_units, load_exams

# known reasons for units under the threshold (checked by hand against the whole bank, Oct 2026)
FEW_WHY = {
    'eng10-u3': 'noun clauses: the bank has almost no noun-clause items',
    'eng10-u8': 'present continuous / confusing verbs: only a few cloze items test these',
    'eng11-u8': 'transitive / intransitive verbs and objects (Textbook Unit 8): only 2 items in all papers ("discuss ___ the matter", no preposition)',
    'eng11-u14': 'question formation: only ~4 "correct question for this answer" items in all papers',
    'eng11-u22': 'pronunciation / vowel sounds: no pronunciation items in any paper',
    'math10-u2': 'axiomatic geometry & proofs: few such items, and the figure-based ones are dropped (figure not shipped)',
}
REPORT = os.path.join(ROOT, 'tool/matric_unit_sync/report.json')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--min', type=int, default=10)
    ap.add_argument('--quiet', action='store_true')
    a = ap.parse_args()
    errs = []
    err = errs.append

    units = {u['id']: u for u in load_units()}
    raw = open(UQ, encoding='utf-8').read()
    uq = json.loads(raw)
    if raw != json.dumps(uq, ensure_ascii=False, separators=(',', ':')):
        err('unit_questions.json is not compact (json.dumps separators=(",",":"), ensure_ascii=False)')
    bank = {}
    for f, e, q in load_exams():
        bank.setdefault(q['id'], (f, e['subject']))
    rep = json.load(open(REPORT, encoding='utf-8')) if os.path.exists(REPORT) else {}
    dropped = {d['id'] for d in rep.get('dropped', [])}
    unmapped = collections.Counter(u['subject'] for u in rep.get('unmapped', []))

    linked = set()
    for uid, lst in uq['units'].items():
        if uid not in units:
            err(f'unit_questions: unknown unit {uid}')
            continue
        subj = units[uid]['subject']
        seen = set()
        for m in lst:
            i = m.get('id')
            if not i or m.get('confidence') not in ('high', 'medium', 'low'):
                err(f'{uid}: bad entry {m}')
                continue
            if i in seen:
                err(f'{uid}: duplicate {i}')
            seen.add(i)
            if i not in bank:
                err(f'{uid}: dangling id {i} (not in the eager exam bank)')
                continue
            if subj not in FAMILY.get(bank[i][1], []):
                err(f'{uid}: {i} is a {bank[i][1]} question, unit subject is {subj}')
            if i in dropped:
                err(f'{uid}: {i} is listed as dropped/broken')
            linked.add(i)

    # few-links report: unit -> count; the bank for its subject family
    few = []
    for uid, u in sorted(units.items(), key=lambda x: (x[1]['subject'], x[1]['grade'], x[1]['number'] or 0)):
        n = len(uq['units'].get(uid, []))
        if n < a.min:
            few.append((uid, n, u['title']))

    # exercises, built like ExamRepo._loadExercises + loadSchoolPapers
    ex_units = collections.defaultdict(list)
    ids = set()
    idx = json.load(open(os.path.join(EXER, 'index.json'), encoding='utf-8'))
    null_units = collections.Counter()
    cross = collections.Counter()
    files = []
    for g, subs in idx['grades'].items():
        for s, ent in subs.items():
            files.append((os.path.join(EXER, ent['file']), int(g), s, ent))
    sp = os.path.join(EXER, 'school/index.json')
    if os.path.exists(sp):
        for g, subs in json.load(open(sp, encoding='utf-8'))['grades'].items():
            for s, ent in subs.items():
                files.append((os.path.join(EXER, 'school', ent['file']), int(g), s, None))
    for path, g, s, ent in files:
        qs = json.load(open(path, encoding='utf-8'))['questions']
        school = ent is None
        if ent and (ent['count'] != len(qs) or ent['units'] != dict(sorted(collections.Counter(q.get('unit') or 'general' for q in qs).items()))):
            err(f'{path}: index.json counts differ from the file')
        for q in qs:
            if q['id'] in ids:
                if not school:
                    err(f'{path}: duplicate exercise id {q["id"]}')
                continue  # the app skips school ids already loaded
            ids.add(q['id'])
            u = q.get('unit')
            if not u:
                null_units[f'{s} {g}'] += 1
                continue
            nu = units.get(u)
            if not nu:
                err(f'{path}: {q["id"]} unit {u} is not a notes unit')
            elif nu['subject'] != s:
                err(f'{path}: {q["id"]} unit {u} belongs to {nu["subject"]}')
            elif nu['grade'] != g:
                cross[f'{s} {g} -> {u}'] += 1  # shown under that unit (both in notes and in the Exercise tab of its grade)
            ex_units[u].append(q['id'])
    no_ex = [uid for uid in units if not ex_units.get(uid)]

    print(f'{len(units)} notes units; {len(uq["units"])} with matric links; {len(linked)} unique linked questions '
          f'of {len(bank)} in the eager bank; {len(dropped)} dropped as broken')
    print(f'exercise items: {len(ids)}; {sum(len(v) for v in ex_units.values())} in a notes unit; '
          f'{len(no_ex)} units without exercises; untagged (General only): {dict(sorted(null_units.items()))}')
    if cross:
        print(f'exercise items tagged to a unit of another grade (same subject; allowed): {dict(cross)}')
    print(f'units with < {a.min} matric links: {len(few)}')
    by_subj_unmapped = dict(unmapped)
    for uid, n, title in few:
        fam = [k for k, v in FAMILY.items() if units[uid]['subject'] in v]
        why = FEW_WHY.get(uid) or 'not explained: check tools/map_unit_questions.py rules'
        print(f'  {uid:10} {n:3}  {title[:40]:40}  {why}  (unplaced {"/".join(fam)} questions in the bank: '
              f'{sum(by_subj_unmapped.get(k, 0) for k in fam)})')
    if not a.quiet:
        print('exercise items per unit (= notes "Exercises (N)" = Exercise tab tile):')
        for uid in sorted(ex_units):
            print(f'  {uid:10} {len(ex_units[uid])}')
    for e in errs[:200]:
        print('ERROR', e)
    print('OK' if not errs else f'{len(errs)} errors')
    sys.exit(1 if errs else 0)


if __name__ == '__main__':
    main()
