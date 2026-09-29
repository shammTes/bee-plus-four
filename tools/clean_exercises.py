#!/usr/bin/env python3
"""Clean + verify + unit-map the practice MCQ bank for the High Exercise tab.

  python3 tools/clean_exercises.py [src_dir] [notes_dir]
    src_dir   default /workspace/exercises_src      (*.json lists of {id, grade, subject, prompt, options[4], correct_index, explanation})
    notes_dir default /workspace/high/content/notes (index.json + <subject>_<grade>.json)
Writes assets/high/exercises/<subject>_<grade>.json, assets/high/exercises/index.json, docs/exercises_report.md.

Answer-key policy (many source keys are broken; 8 files key everything as A):
  1. explanation names exactly one option  -> key := that option ("verified": "explanation")
  2. else trusted file and the explanation does not contradict the key -> keep ("verified": "trusted")
  3. else drop.
"""
import collections, glob, json, math, os, re, sys, unicodedata

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = sys.argv[1] if len(sys.argv) > 1 else '/workspace/exercises_src'
NOTES = sys.argv[2] if len(sys.argv) > 2 else '/workspace/high/content/notes'
OUT = os.path.join(ROOT, 'assets/high/exercises')
REPORT = os.path.join(ROOT, 'docs/exercises_report.md')
TH = float(os.environ.get('EX_TH', 8.0)); MG = float(os.environ.get('EX_MG', 1.4))
TRUSTED = {'practice_g9_biology', 'practice_g11_agriculture', 'practice_g11_english', 'practice_g11_history_p5'}
SUBJ = {'MATH': 'mathematics', 'MATHEMATICS': 'mathematics', 'BIOLOGY': 'biology', 'CHEMISTRY': 'chemistry', 'PHYSICS': 'physics',
        'GEOGRAPHY': 'geography', 'HISTORY': 'history', 'AGRICULTURE': 'agriculture', 'ENGLISH': 'english',
        'BUSINESS_ECONOMICS': 'business_economics', 'ECONOMICS': 'business_economics'}

LABEL = re.compile(r'^\s*\(?([A-Ea-e])\s*[\).:]\s+')
PREFIX = re.compile(r'^\s*\[\s*G\d+[^\]]*\]\s*')
SUPMAP = str.maketrans('₀₁₂₃₄₅₆₇₈₉⁰¹²³⁴⁵⁶⁷⁸⁹⁻⁺−–—', '01234567890123456789-+---')


def norm(s):
    s = unicodedata.normalize('NFKC', str(s)).translate(SUPMAP).lower()
    s = re.sub(r"[^\w%.+\-/]+", ' ', s)
    s = re.sub(r'[.\-/+](?!\d)', ' ', s)   # keep 2.5, -3, 1/2; drop sentence punctuation
    return re.sub(r'\s+', ' ', s).strip()


def has_digit(s):
    return bool(re.search(r'\d', s))


def occurrences(opt, expl):
    """positions where option `opt` (normalized) appears in normalized explanation `expl`, or [] if not checkable/absent"""
    if not opt:
        return []
    if has_digit(opt):   # numbers / formulas: whole-token match (10 must not match 100 or 2.10)
        pat = r'(?<![\w.])' + re.escape(opt) + r'(?![\w]|\.\d)'
    elif len(opt) > 3:
        pat = r'(?<!\w)' + re.escape(opt) + r'(?!\w)'
    else:
        return []
    return [m.start() for m in re.finditer(pat, expl)]


def named_options(opts, expl):
    """indices of options the explanation names. Options contained in another named option are ignored
    ("cell" vs "cell wall"). Among several numeric options, the one stated as the result (after the last '=' / '≈'
    / 'is' / 'answer') wins."""
    e = norm(expl)
    no = [norm(o) for o in opts]
    hit = {i: occurrences(o, e) for i, o in enumerate(no)}
    hit = {i: p for i, p in hit.items() if p}
    hit = {i: p for i, p in hit.items() if not any(j != i and no[i] != no[j] and re.search(r'(?<!\w)' + re.escape(no[i]) + r'(?!\w)', no[j]) for j in hit)}
    if len(set(no[i] for i in hit)) < len(hit):   # two options normalize equal (punctuation-only difference): not decidable
        return sorted(hit) * 2
    if len(hit) > 1 and all(has_digit(no[i]) for i in hit):
        raw = unicodedata.normalize('NFKC', str(expl)).translate(SUPMAP).lower()
        marks = [m.end() for m in re.finditer(r'=|≈|\bis\b|\banswer\b|\btherefore\b|\bso\b', raw)]
        if marks:
            tail = norm(raw[marks[-1]:])
            fin = [i for i in hit if re.match(r'(?:about |approximately |approx |= )?' + re.escape(no[i]) + r'(?![\w]|\.\d)', tail)]
            if len(fin) == 1:
                return fin
    return sorted(hit)


STOP = set('''a an the of to in on for and or is are was were be been by with what which how why when where does do did can
it its this that these those as at from about into than then there their they them he she his her we you your our not no
yes all any each other such only also may might will would should could which who whom whose one two three four five
following true false correct incorrect statement statements best most least example called known used use using
answer question option options above below both none mainly usually because so if but more less many much very'''.split())


def stem(w):
    for suf in ('ational', 'ization', 'ations', 'ation', 'ities', 'ness', 'ment', 'ings', 'ing', 'ies', 'ied', 'es', 'ed', 's'):
        if len(w) > len(suf) + 3 and w.endswith(suf):
            return w[:-len(suf)] + ('y' if suf in ('ies', 'ied') else '')
    return w


def toks(s):
    return [stem(w) for w in re.findall(r'[a-z][a-z]+', norm(s)) if w not in STOP and len(w) > 2]


def strings(o):
    if isinstance(o, str):
        yield o
    elif isinstance(o, list):
        for x in o:
            yield from strings(x)
    elif isinstance(o, dict):
        for k, v in o.items():
            if k not in ('id', 'svg', 'type', 'src', 'tone', 'page', 'art', 'status'):
                yield from strings(v)


def load_units():
    idx = json.load(open(os.path.join(NOTES, 'index.json'), encoding='utf-8'))
    units = {}   # (subject, grade) -> [unit dict with bag]
    for g, subs in idx['grades'].items():
        for subj, b in subs.items():
            book = None
            p = os.path.join(NOTES, b['file'])
            if os.path.exists(p):
                book = {u['id']: u for u in json.load(open(p, encoding='utf-8')).get('units', [])}
            L = []
            for u in b['units']:
                bag = collections.Counter()
                for w in toks(u['title']):
                    bag[w] += 6
                for t in u.get('topics', []):
                    for w in toks(t['title']):
                        bag[w] += 3
                if book and u['id'] in book:
                    bu = book[u['id']]
                    for part in ('lessons', 'glossary', 'intro'):
                        for s in strings(bu.get(part)):
                            for w in toks(s):
                                bag[w] += 1
                L.append({'id': u['id'], 'number': u['number'], 'title': u['title'], 'bag': bag, 'len': sum(bag.values())})
            units[(subj, int(g))] = L
    return units


def mapper(units_list):
    n = len(units_list)
    df = collections.Counter()
    for u in units_list:
        df.update(set(u['bag']))

    def score(qt):
        out = []
        for u in units_list:
            s = 0.0
            for w, f in qt.items():
                tf = u['bag'].get(w)
                if tf:
                    s += f * math.log(1 + n / df[w]) * (1 + math.log(tf)) / (1 + math.log(1 + u['len'] / 2000))
            out.append((s, u))
        out.sort(key=lambda x: -x[0])
        return out
    return score


def main():
    units = load_units()
    mappers = {k: mapper(v) for k, v in units.items()}
    per_file = collections.OrderedDict()
    buckets = collections.defaultdict(list)    # (subject, grade) -> questions
    seen = set()
    hint_agree = hint_total = 0
    for path in sorted(glob.glob(os.path.join(SRC, '*.json'))):
        stemf = os.path.splitext(os.path.basename(path))[0]
        data = json.load(open(path, encoding='utf-8'))
        st = per_file[stemf] = collections.Counter()
        keys = [q.get('correct_index') for q in data if isinstance(q, dict)]
        all_a = bool(keys) and all(k == 0 for k in keys)
        st['_all_a'] = int(all_a)
        n = 0
        for q in data:
            st['in'] += 1
            try:
                subj = SUBJ[str(q['subject']).upper()]
                grade = int(str(q['grade']).upper().lstrip('G'))
                prompt_raw = str(q['prompt'])
                opts_raw = [str(o) for o in q['options']]
                key = int(q['correct_index'])
                expl = str(q.get('explanation') or '').strip()
            except Exception:
                st['drop: malformed'] += 1
                continue
            m = re.match(r'^\s*\[\s*G\d+\s+\w+\s+U(\d+)\s*\]', prompt_raw)
            hint = int(m.group(1)) if m else None
            m2 = re.search(r'-u(\d+)-', str(q.get('id', '')))
            hint = hint or (int(m2.group(1)) if m2 else None)
            prompt = PREFIX.sub('', prompt_raw).strip()
            letters = [LABEL.match(o) for o in opts_raw]
            if 3 <= len(opts_raw) <= 5 and all(lm and lm.group(1).upper() == 'ABCDE'[i] for i, lm in enumerate(letters)):
                opts = [LABEL.sub('', o, count=1).strip() for o in opts_raw]
            else:
                opts = [o.strip() for o in opts_raw]
            raw_key = lambda o: re.sub(r'\s+', ' ', o.strip().lower())
            if not 3 <= len(opts) <= 5 or not prompt or any(not o for o in opts) or len({raw_key(o) for o in opts}) < len(opts) or not 0 <= key < len(opts):
                st['drop: malformed'] += 1
                continue
            dkey = (subj, grade, norm(prompt), tuple(sorted(raw_key(o) for o in opts)))
            if dkey in seen:
                st['drop: duplicate'] += 1
                continue
            named = named_options(opts, expl) if expl and not expl.lower().startswith('see unit notes') else []
            if len(named) == 1:
                verified = 'explanation'
                if named[0] != key:
                    st['key fixed by explanation'] += 1
                key = named[0]
            elif stemf in TRUSTED and (not named or key in named):
                verified = 'trusted'
            else:
                if expl.lower().startswith('see unit notes') or not expl:
                    st['drop: no explanation ("See unit notes.")'] += 1
                elif all_a:
                    st['drop: all-A file, explanation does not confirm'] += 1
                elif len(named) > 1:
                    st['drop: explanation names several options'] += 1
                elif named:
                    st['drop: explanation contradicts key'] += 1
                else:
                    st['drop: explanation names no option'] += 1
                continue
            seen.add(dkey)
            # unit mapping
            unit = None
            sc = mappers.get((subj, grade))
            if sc:
                qt = collections.Counter(toks(prompt) * 2 + toks(' '.join(opts)) + toks(expl))
                res = sc(qt)
                if res and res[0][0] > 0:
                    top, second = res[0][0], (res[1][0] if len(res) > 1 else 0)
                    if top >= TH and top >= MG * second:
                        unit = res[0][1]
                if hint is not None:
                    hint_total += 1
                    if unit is not None and unit['number'] == hint:
                        hint_agree += 1
            n += 1
            st['kept'] += 1
            st['kept ' + verified] += 1
            st['mapped' if unit else 'general'] += 1
            buckets[(subj, grade)].append({
                'id': f'{subj}_{grade}_{stemf}_{n}', 'unit': unit['id'] if unit else None,
                'prompt': prompt, 'options': opts, 'answer': key, 'explanation': expl, 'verified': verified,
                'src': f'{stemf}#{q.get("id")}',
            })
    # write
    os.makedirs(OUT, exist_ok=True)
    for f in glob.glob(os.path.join(OUT, '*.json')):
        os.remove(f)
    index = {'about': 'Practice MCQs for the Exercise tab, generated by tools/clean_exercises.py (see docs/exercises_report.md).',
             'total': 0, 'grades': {}}
    for (subj, grade), qs in sorted(buckets.items(), key=lambda x: (x[0][1], x[0][0])):
        fn = f'{subj}_{grade}.json'
        json.dump({'subject': subj, 'grade': grade, 'questions': qs}, open(os.path.join(OUT, fn), 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
        uc = collections.Counter(q['unit'] or 'general' for q in qs)
        index['grades'].setdefault(str(grade), {})[subj] = {'file': fn, 'count': len(qs), 'units': dict(sorted(uc.items()))}
        index['total'] += len(qs)
    json.dump(index, open(os.path.join(OUT, 'index.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    # report
    tot = collections.Counter()
    for s in per_file.values():
        tot.update(s)
    reasons = sorted({k for s in per_file.values() for k in s if k.startswith('drop:')})
    L = ['# Exercise bank cleaning report', '', f'Generated by `tools/clean_exercises.py` from `{SRC}`.', '',
         f'**{tot["in"]} in → {tot["kept"]} kept, {tot["in"] - tot["kept"]} dropped.** '
         f'Kept: {tot["kept explanation"]} verified by explanation ({tot["key fixed by explanation"]} keys corrected), '
         f'{tot["kept trusted"]} kept from trusted files.', '',
         f'Trusted files: {", ".join(sorted(TRUSTED))}.', '',
         '| file | all-A | in | kept | verified | trusted | key fixed | dropped | ' + ' | '.join(r[6:] for r in reasons) + ' |',
         '|' + '---|' * (8 + len(reasons))]
    for f, s in per_file.items():
        L.append(f'| {f} | {"yes" if s["_all_a"] else ""} | {s["in"]} | {s["kept"]} | {s["kept explanation"]} | {s["kept trusted"]} | {s["key fixed by explanation"]} | {s["in"] - s["kept"]} | ' + ' | '.join(str(s[r]) for r in reasons) + ' |')
    L.append(f'| **total** | | {tot["in"]} | {tot["kept"]} | {tot["kept explanation"]} | {tot["kept trusted"]} | {tot["key fixed by explanation"]} | {tot["in"] - tot["kept"]} | ' + ' | '.join(str(tot[r]) for r in reasons) + ' |')
    L += ['', '## Unit mapping', '',
          f'{tot["mapped"]} of {tot["kept"]} kept questions ({100 * tot["mapped"] / max(1, tot["kept"]):.1f} %) mapped to a notes unit; '
          f'{tot["general"]} in the per-subject "General" bucket (unit: null). English has no notes book, so it is all General.', '',
          f'Sanity check: {hint_total} source questions carry a unit hint in their id/prefix (`-u6-`, `[G9 MATH U4]`, not used for mapping); '
          f'the keyword mapping lands on that unit number for {hint_agree} ({100 * hint_agree / max(1, hint_total):.0f} %). Source unit numbering can differ from the textbook, so this is a lower bound on accuracy.', '',
          '| grade | subject | kept | mapped | general | units with questions |', '|---|---|---|---|---|---|']
    for g, subs in sorted(index['grades'].items(), key=lambda x: int(x[0])):
        for subj, e in sorted(subs.items()):
            gen = e['units'].get('general', 0)
            nu = len(units.get((subj, int(g)), []))
            L.append(f'| {g} | {subj} | {e["count"]} | {e["count"] - gen} | {gen} | {len([u for u in e["units"] if u != "general"])}/{nu} |')
    L += ['', '## Rules', '', '- Leading `A) `/`A. ` option labels and `[G9 MATH U4]` prompt prefixes are stripped.',
          '- Explanation check: normalized whole-word match of each option (text options > 3 chars; options with digits match as whole tokens); '
          'an option contained in another matched option is ignored; among several numeric matches the one stated after the last `=`/`≈`/`is` wins.',
          '- Trusted files keep their key when the explanation names no option or names the key among others.',
          '- Dropped: malformed (not 3–5 distinct non-empty options, bad index), exact duplicates (same grade/subject/prompt/options), '
          'and everything that could not be verified.',
          '- Unit mapping: TF-IDF-style score of prompt (×2), options and explanation tokens against unit title (×6), topic titles (×3) and '
          'the unit\'s notes text (×1); confident when top ≥ 8 and ≥ 1.4 × runner-up (tuned on the questions whose source ids carry a unit hint), else General.']
    open(REPORT, 'w', encoding='utf-8').write('\n'.join(L) + '\n')
    print(f'{tot["in"]} in, {tot["kept"]} kept ({tot["kept explanation"]} explanation, {tot["kept trusted"]} trusted), '
          f'{tot["mapped"]} mapped, hint agreement {hint_agree}/{hint_total}')
    for f, s in per_file.items():
        print(f'  {f:40s} {s["in"]:4d} -> {s["kept"]:4d}  fixed {s["key fixed by explanation"]:3d} ' + ' '.join(f'{r[6:]}={s[r]}' for r in reasons if s[r]))


if __name__ == '__main__':
    main()
