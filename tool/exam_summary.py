#!/usr/bin/env python3
"""Build the exam-pack summary the app reads at start-up instead of every pack (assets/high/exams/summary.json).

    python3 tool/exam_summary.py            # writes assets/high/exams/summary.json
    python3 tool/exam_summary.py --check    # exit 1 if it is missing or out of date

The exam packs (assets/high/exams/*.json, ~19 MB, plus ~5 MB of topic indexes) used to be read and decoded before the
first screen, only for Home / Matric / Mistakes counts and stats. The summary holds just what those need: each kept
exam's "exam" block and, per question, its id, whether it is an auto-marked MCQ / matching question / has a review
flag, and its topic ids; plus each topic index's topic and subtopic titles (no concept texts, no question lists).
The app (ExamRepo with lazyExams) builds light question stubs from it and reads a whole pack only when that exam's
questions are shown; the tutor reads everything on first use.

Mirrors ExamRepo._load (lib/high/data/repository.dart) and Question.isMCQ / isMatch (models.dart): which exams and
questions are kept, in which order. test/exam_summary_test.dart checks the summary against a full load, so re-run this
after changing any exam pack or topic index (also after a rebase / merge that touched them). Deterministic output.

Format (v1): {"v":1,"exams":[{"file","exam","t":[topic ids used in this exam],"q":[[id,flags,[topic index…]],…]}],
"topics":[{"file","ix":{"exam_ids","subject"?,"topics":[{"id","title","subtopics":[{"id","title"}]}]}}]}
id is the question id without the exam id prefix when it has one ("-p1-q01"), else "=" + the full id.
flags: 1 = MCQ, 2 = matching (auto-marked), 4 = review flag.
"""
import argparse
import json
import os
import sys

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
EXAMS = os.path.join(ROOT, 'assets', 'high', 'exams')
OUT = os.path.join(EXAMS, 'summary.json')


def dart_str(v):
    """Dart toString of a JSON value (as strs() / str() use it)"""
    if v is True:
        return 'true'
    if v is False:
        return 'false'
    if v is None:
        return 'null'
    if isinstance(v, float):
        return repr(v) if v != int(v) or abs(v) >= 1e21 else f'{v:.1f}'
    if isinstance(v, (dict, list)):
        raise ValueError('unexpected JSON object/array in a string list')
    return str(v)


def strs(v):
    return [dart_str(x) for x in v if x is not None] if isinstance(v, list) else []


def opt_str(v):
    return v if isinstance(v, str) and v else None


def load(path):
    try:
        with open(path, encoding='utf-8') as f:
            return json.load(f)
    except (OSError, ValueError):
        return None


def build():
    idx = load(os.path.join(EXAMS, 'index.json'))
    exam_files = strs(idx.get('exams'))
    topic_files = strs(idx.get('topics'))
    seen, exams = set(), []
    for fn in exam_files:
        raw = load(os.path.join(EXAMS, fn))
        if not isinstance(raw, dict) or not isinstance(raw.get('exam'), dict):
            continue
        ex = raw['exam']
        eid = ex.get('id')
        if not isinstance(eid, str) or eid in seen:
            continue
        lists = {}
        ok = True
        for ml in raw.get('match_lists') or [] if isinstance(raw.get('match_lists'), list) else []:
            if isinstance(ml, dict) and ml.get('id') is not None and ml.get('choices') is not None:
                if not isinstance(ml['id'], str):
                    ok = False
                    break
                lists[ml['id']] = ml
        for ps in raw.get('passages') or [] if isinstance(raw.get('passages'), list) else []:
            if isinstance(ps, dict) and ps.get('id') is not None and not isinstance(ps['id'], str):
                ok = False
        qs = []
        for q in raw.get('questions') or [] if isinstance(raw.get('questions'), list) else []:
            if not isinstance(q, dict) or q.get('id') is None:
                continue
            if not isinstance(q['id'], str):
                ok = False
                break
            qs.append(q)
        if not ok:
            continue  # the app skips an exam whose ids are not strings
        seen.add(eid)
        topics, tix, out = [], {}, []
        for q in qs:
            opts = q.get('options')
            mcq = str(q.get('type') if q.get('type') is not None else '') == 'mcq' and isinstance(opts, dict) and len(opts) > 1
            ma, mid = opt_str(q.get('match_answer')), opt_str(q.get('match_list_id'))
            ml = lists.get(mid) if mid else None
            choices = ml.get('choices') if ml else None
            match = ma is not None and ml is not None and isinstance(choices, dict) and ma in {dart_str(k) for k in choices}
            flags = (1 if mcq else 0) | (2 if match else 0) | (4 if opt_str(q.get('review_flag')) else 0)
            ti = []
            for t in strs(q.get('topics')):
                if t not in tix:
                    tix[t] = len(topics)
                    topics.append(t)
                ti.append(tix[t])
            qid = q['id']
            out.append([qid[len(eid):] if qid.startswith(eid) and len(qid) > len(eid) else '=' + qid, flags, ti])
        exams.append({'file': fn, 'exam': ex, 't': topics, 'q': out})
    tops = []
    for fn in topic_files:
        ix = load(os.path.join(EXAMS, fn))
        if not isinstance(ix, dict):
            continue
        slim = {'exam_ids': ix.get('exam_ids')}
        if 'subject' in ix:
            slim['subject'] = ix['subject']
        st = []
        for t in ix.get('topics') or [] if isinstance(ix.get('topics'), list) else []:
            if not isinstance(t, dict):
                continue
            subs = [{'id': s.get('id'), 'title': s.get('title')} for s in (t.get('subtopics') or [] if isinstance(t.get('subtopics'), list) else []) if isinstance(s, dict) and s.get('id') is not None]
            st.append({'id': t.get('id'), 'title': t.get('title'), 'subtopics': subs})
        slim['topics'] = st
        tops.append({'file': fn, 'ix': slim})
    return json.dumps({'v': 1, 'exams': exams, 'topics': tops}, ensure_ascii=False, separators=(',', ':')) + '\n'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--check', action='store_true')
    a = ap.parse_args()
    text = build()
    if a.check:
        try:
            with open(OUT, encoding='utf-8', newline='') as f:
                cur = f.read()
        except OSError:
            cur = None
        if cur != text:
            sys.exit('exam summary out of date: run python3 tool/exam_summary.py')
        print('exam summary up to date')
        return
    with open(OUT, 'w', encoding='utf-8', newline='\n') as f:
        f.write(text)
    d = json.loads(text)
    print(f"wrote {os.path.relpath(OUT, ROOT)}: {len(d['exams'])} exams, {sum(len(e['q']) for e in d['exams'])} questions, {len(text.encode('utf-8')) // 1024} KB")


if __name__ == '__main__':
    main()
