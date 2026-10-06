"""Import the Drive 'Practice Question Bank' (agriculture 11/12, biology 10/11) into unit exercises:
main MC questions -> mcq, other main questions and every similar question -> short answer, with worked-solution explanations."""
import sys, os, json, re
sys.path.insert(0, os.path.dirname(__file__))
from patch import Book, mcq, short
SRC = '/workspace/tmp-sync/drive/Practice_Questions.json'
BOOK = {'agri_g11': 'agriculture_11', 'agri_g12': 'agriculture_12', 'bio_g10': 'biology_10', 'bio_g11': 'biology_11'}

def clean(s):
    s = re.sub(r'\bChapter\b', 'Unit', s)
    s = re.sub(r'\bchapter\b', 'unit', s)
    return s.strip()

def why(steps):
    out = []
    for st in steps or []:
        t, dt = clean(st.get('title', '')), clean(st.get('detail', ''))
        out.append(f'**{t}.** {dt}' if t else dt)
    return out or ['See the unit notes.']

TIP_MC = 'Eliminate options that contradict the unit notes, then choose the one that matches every detail in the question.'
TIP_SH = 'Write your answer first, then open the worked solution and compare the key facts and numbers.'

d = json.load(open(SRC))
books = {}
for ch in d['chapters']:
    bk = BOOK[ch['chapter_id'].rsplit('_c', 1)[0]]
    B = books.setdefault(bk, Book(bk))
    uid = B.d['units'][ch['chapter_number'] - 1]['id']
    qs = []
    for q in ch['questions']:
        qid = q['question_id']
        base = qid.replace('_', '-')
        w = why(q.get('solution_steps'))
        done = False
        if q['type'] == 'MC' and q.get('options'):
            opts = {}
            for o in q['options']:
                m = re.match(r'\s*([A-E])[.)]\s*(.*)', o)
                if m:
                    opts[m.group(1)] = clean(m.group(2))
            m = re.match(r'\s*([A-E])[.)]', q['answer'])
            ans = m.group(1) if m else None
            if ans in opts and len(opts) >= 3:
                qs.append(mcq(base, clean(q['question']), opts, ans, w, TIP_MC, src_qid=qid, src='practice_bank'))
                done = True
        if not done:
            qs.append(short(base, clean(q['question']), clean(str(q['answer'])), w, TIP_SH, src_qid=qid, src='practice_bank'))
        for i, sq in enumerate(q.get('similar_questions') or []):
            qs.append(short(f'{base}-s{i+1}', clean(sq['question']), clean(str(sq['answer'])), why(sq.get('solution_steps')), TIP_SH, src_qid=qid, src='practice_bank'))
    B.ex(uid, qs)
for B in books.values():
    B.save()
