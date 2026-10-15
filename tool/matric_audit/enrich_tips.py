#!/usr/bin/env python3
"""Give EVERY matric / model question a 'How to answer' tip (`tips`) and 1-2 `similar_questions`.

Order (idempotent; never overwrites what a question already has):
  1. copy from another copy of the same question (same stem) in the current packs;
  2. copy from tips_history.json (copies that existed in git history, e.g. dropped by dedupe);
  3. generate: plain-English tips from the question's form + subject, and 1-2 REAL questions with keyed answers
     from the same subject that share the most (rare) words, so every similar question has a checked answer.
Generated tips are marked `"tips_source": "generated"`; similar questions picked from the bank carry `"from": <id>`.
Run by run_all.sh after apply_fixes.py, so later pipeline runs keep these fields.
"""
import json, os, re, sys
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '..', '..', 'assets', 'high', 'exams')
STOP = set('the of a an and or to in is are was were be by for on with as at from that this which what who whom whose when where why how it its his her their they he she we you your our not no yes all any each some one two three four five above below following these those than then into about between will would can could should may might must has have had do does did if so such only also other more most less least very'.split())


def norm(s):
    return re.sub(r'[^a-z0-9]', '', (s or '').lower())[:200]


def words(s):
    return {w for w in re.findall(r'[a-z][a-z]{2,}', (s or '').lower()) if w not in STOP}


NEG = re.compile(r'\b(not|except|incorrect|false|least|wrong|untrue)\b', re.I)
BLANK = re.compile(r'_{2,}|\.\.\.\.|…|\bblank\b', re.I)
DEF = re.compile(r'\b(is called|are called|is known as|refers to|is defined as|is termed|the term)\b', re.I)
BEST = re.compile(r'\b(best|most|main|major|primary)\b', re.I)
CONTEXT = re.compile(r'\b(item|items|blank|blanks|passage|paragraph|conversation|dialogue|underlined|above|below|figure|diagram|table|graph|text|column)\b', re.I)
CALC_SUBJ = {'Mathematics', 'Physics', 'Chemistry'}

SUBJECT_TIP = {
    'Mathematics': 'If you are stuck, put each option back into the question and see which one works.',
    'Physics': 'Write the formula first, put in the numbers with their units, then work it out step by step.',
    'Chemistry': 'Write the formula or the balanced equation first. Check charges, moles and units before you choose.',
    'Biology': 'Think about what the part or process does (its function). The right option matches that function.',
    'Agriculture': 'Link the question to a farm practice you studied: what it is for and what problem it solves.',
    'Business and Economics': 'Use the textbook meaning of the key term (for example demand, cost, profit) to test each option.',
    'English': 'Read the whole sentence, not only the gap. Check tense, subject-verb agreement and meaning.',
    'Geography': 'Think of the place, the climate or the map fact. Remove options that do not fit the region.',
    'History': 'Put the event in time order: who, when and why. Remove options from the wrong period or place.',
    'General Knowledge': 'Use what you know first, then remove options that are clearly wrong.',
    'General Science': 'Name the science idea behind the question, then test each option against it.',
    'Social Studies': 'Find the key idea (rights, government, culture, economy) and match it to the option.',
}


def gen_tips(q, subject):
    stem = q.get('stem') or ''
    opts = q.get('options') if isinstance(q.get('options'), dict) else {}
    ov = ' '.join(str(v) for v in opts.values())
    tips = []
    if q.get('type') == 'workout' or not opts:
        tips.append('Show every step. Marks are given for the method, not only the final answer.')
    elif NEG.search(stem):
        tips.append('This question asks for the one that is NOT true. Check every option, cross out the true ones, and choose the one left.')
    elif BLANK.search(stem) and subject == 'English':
        tips.append('Try each option in the gap and read the full sentence. Choose the one that is correct in grammar and meaning.')
    elif DEF.search(stem):
        tips.append('Find the key words in the question and match them to the textbook definition.')
    elif BEST.search(stem):
        tips.append('More than one option may look right. Choose the most complete and most correct one.')
    elif re.search(r'\b(all of the above|none of the above|both)\b', ov, re.I):
        tips.append('Check every option. If two or more are true, "all of the above" may be the answer; if none is true, choose "none".')
    elif subject in CALC_SUBJ and re.search(r'\d', stem + ov):
        tips.append('Work it out on paper first, then compare your result with the options. Check units and signs.')
    else:
        tips.append('Read the question twice and underline the key words. Remove the options that are clearly wrong first.')
    st = SUBJECT_TIP.get(subject)
    if st and st not in tips:
        tips.append(st)
    return tips


def usable(q):
    """a bank question we may show as a similar question: stands on its own (no passage, list, figure or 'item 12'
    reference) and has a keyed answer that matches its options"""
    stem = q.get('stem') or ''
    if q.get('review_flag') or not stem or not q.get('answer') or len(stem) < 25:
        return False
    if q.get('passage_id') or q.get('match_list_id') or q.get('image') or q.get('subparts') or CONTEXT.search(stem):
        return False
    if q.get('type') == 'mcq':
        o = q.get('options')
        return isinstance(o, dict) and len(o) > 1 and q['answer'] in o
    return q.get('type') == 'workout' and bool(q.get('explanation_steps'))


def as_similar(q):
    s = {'stem': q['stem']}
    if q.get('stem_tex'):
        s['stem_tex'] = q['stem_tex']
    if isinstance(q.get('options'), dict):
        s['options'] = q['options']
    s['answer'] = q['answer']
    if q.get('explanation_steps'):
        s['explanation_steps'] = q['explanation_steps']
    s['from'] = q['id']
    return s


def qwords(q):
    return words(q.get('stem')) | words(' '.join(map(str, (q.get('options') or {}).values())))


def main():
    idx = json.load(open(os.path.join(ROOT, 'index.json')))
    hist = {k: v for k, v in json.load(open(os.path.join(HERE, 'tips_history.json'))).items() if not k.startswith('_')}
    packs = []
    for f in idx['exams']:
        p = os.path.join(ROOT, f)
        raw = open(p, encoding='utf-8').read()
        packs.append((p, json.loads(raw), raw))
    rich = {}  # 1. hand-written copies in the current packs
    for _, d, _r in packs:
        for q in d.get('questions') or []:
            k = norm(q.get('stem'))
            if len(k) > 15:
                if q.get('tips') and q.get('tips_source') != 'generated':
                    rich.setdefault(k, {}).setdefault('tips', q['tips'])
                if q.get('similar_questions') and not any('from' in s for s in q['similar_questions']):
                    rich.setdefault(k, {}).setdefault('similar_questions', q['similar_questions'])
    pool = defaultdict(list)
    for _, d, _r in packs:
        subj = d['exam'].get('subject', '')
        for q in d.get('questions') or []:
            if usable(q):
                pool[subj].append((q, qwords(q)))
    inv = {s: defaultdict(list) for s in pool}
    for s, lst in pool.items():
        for i, (_, w) in enumerate(lst):
            for x in w:
                inv[s][x].append(i)
    st = defaultdict(int)
    for p, d, raw in packs:
        subj = d['exam'].get('subject', '')
        ch = False
        for q in d.get('questions') or []:
            k = norm(q.get('stem'))
            need_t, need_s = not q.get('tips'), not q.get('similar_questions')
            if not (need_t or need_s):
                continue
            src = rich.get(k) if len(k) > 15 else None
            h = hist.get(k)
            if need_t:
                if src and src.get('tips'):
                    q['tips'] = src['tips']; st['tips_copied'] += 1
                elif h and h.get('tips'):
                    q['tips'] = h['tips']; st['tips_history'] += 1
                else:
                    q['tips'] = gen_tips(q, subj); q['tips_source'] = 'generated'; st['tips_generated'] += 1
                ch = True
            if need_s:
                if src and src.get('similar_questions'):
                    q['similar_questions'] = src['similar_questions']; st['similar_copied'] += 1; ch = True
                elif h and h.get('similar_questions'):
                    q['similar_questions'] = h['similar_questions']; st['similar_history'] += 1; ch = True
                else:
                    lst, ix = pool.get(subj, []), inv.get(subj, {})
                    score = defaultdict(float)
                    for x in qwords(q):
                        cand = ix.get(x, ())
                        if not cand or len(cand) > 400:  # very common word: not informative
                            continue
                        wgt = 1.0 / (1 + len(cand)) ** 0.5  # rarer shared words count more
                        for i in cand:
                            score[i] += wgt
                    want = 'workout' if q.get('type') == 'workout' else 'mcq'
                    picks, seen = [], {k}
                    for i, sc in sorted(score.items(), key=lambda t: (-t[1], lst[t[0]][0]['id'])):
                        c = lst[i][0]
                        ck = norm(c.get('stem'))
                        if c['id'] == q['id'] or ck in seen or sc < 0.25 or c.get('type') != want:
                            continue
                        seen.add(ck)
                        picks.append(as_similar(c))
                        if len(picks) == 2 or (len(picks) == 1 and len(c['stem']) > 220):
                            break
                    if not picks:  # nothing shares words: same type from the same subject, deterministic
                        for c, _ in lst:
                            if c['id'] != q['id'] and c.get('type') == want and norm(c.get('stem')) != k:
                                picks.append(as_similar(c))
                                break
                    if picks:
                        q['similar_questions'] = picks; st['similar_generated'] += 1; ch = True
                    else:
                        st['similar_none'] += 1
        if ch:
            m = re.match(r'\{\n( +)', raw)
            out = json.dumps(d, ensure_ascii=False, indent=len(m.group(1)) if m else None, separators=None if m else (',', ':'))
            with open(p, 'w', encoding='utf-8') as fh:
                fh.write(out + ('\n' if raw.endswith('\n') else ''))
    print(json.dumps(dict(st)))


if __name__ == '__main__':
    sys.exit(main())
