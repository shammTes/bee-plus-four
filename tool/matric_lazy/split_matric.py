#!/usr/bin/env python3
"""Regenerate matric_lazy packs + missing eager banks from Matric_Questions.json.
Expects SRC at /workspace/tmp-sync/drive/Matric_Questions.json (or pass path as argv[1]).
See README.md for size tradeoff."""
import json, re, sys
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).resolve().parents[2]
SRC = Path(sys.argv[1] if len(sys.argv) > 1 else '/workspace/tmp-sync/drive/Matric_Questions.json')
EXAMS = ROOT / 'assets/high/exams'
LAZY = EXAMS / 'matric_lazy'
LAZY_SUB = LAZY / 'subjects'
SUBJ_MAP = {
  'english language': 'English',
  'business & economics': 'Business and Economics',
  'algebra and geometry': 'Mathematics',
}

def map_subj(s): return SUBJ_MAP.get((s or '').lower(), s)
def slug(s): return re.sub(r'[^a-z0-9]+', '_', (s or '').lower()).strip('_')

def to_options(opts):
  out = {}
  if isinstance(opts, dict):
    return {str(k): str(v) for k, v in opts.items()}
  for i, o in enumerate(opts or []):
    m = re.match(r'^([A-E])[.)]\s*(.*)$', str(o).strip())
    out[m.group(1) if m else chr(ord('A') + i)] = m.group(2) if m else str(o)
  return out

def convert_paper(paper):
  subj = map_subj(paper['subject'])
  year = str(paper['year'])
  typ = 'matriculation' if paper['category'] == 'Matric' else 'model'
  eid = f"drive-{slug(paper['paper_id'])}"
  questions = []
  for i, q in enumerate(paper.get('questions') or [], 1):
    opts = to_options(q.get('options'))
    ans = str(q.get('correct_answer') or '').strip()
    if opts and ans not in opts:
      for k, v in opts.items():
        if v.lower() == ans.lower() or ans.lower() in v.lower():
          ans = k
          break
      if len(ans) == 1: ans = ans.upper()
    qt = 'mcq' if (q.get('type') or 'MC').upper() in ('MC', 'MCQ') and len(opts) >= 2 else 'workout'
    expl = (q.get('explanation') or q.get('sample_answer') or '').strip()[:800]
    stem = q.get('question') or ''
    if q.get('context'): stem = f"{q['context']}\n\n{stem}"
    questions.append({
      'id': f'{eid}-q{i:03d}', 'exam_id': eid, 'part': 1 if qt == 'mcq' else 2,
      'number': q.get('number') or i, 'type': qt, 'marks': 1, 'stem': stem,
      'options': opts or None, 'answer': ans, 'accepted_answers': [ans] if ans else [],
      'explanation_steps': [expl] if expl else [], 'topic': q.get('topic') or subj,
    })
  exam = {
    'id': eid, 'year': year, 'subject': subj, 'grade': 12,
    'school': 'Eritrean Secondary Education Certificate Examination (national)' if typ == 'matriculation' else 'Model Examination',
    'type': typ, 'semester': None, 'title': paper.get('title') or f'{subj} {paper["category"]} {year}',
    'exam_code': paper['paper_id'], 'duration': None, 'total_points': len(questions),
  }
  return {'schema_version': '1.0', 'exam': exam, 'match_lists': {}, 'questions': questions}, eid

def main():
  m = json.loads(SRC.read_text())
  idx = json.loads((EXAMS / 'index.json').read_text())
  for paper in m['papers']:
    if paper['subject'] not in ('English Language', 'Algebra and Geometry'):
      continue
    bank, _ = convert_paper(paper)
    fname = f"bank_drive_{slug(paper['paper_id'])}.json"
    (EXAMS / fname).write_text(json.dumps(bank, ensure_ascii=False, separators=(',', ':')))
    if fname not in idx['exams']:
      idx['exams'].append(fname)
  (EXAMS / 'index.json').write_text(json.dumps(idx, indent=2) + '\n')
  LAZY.mkdir(parents=True, exist_ok=True)
  LAZY_SUB.mkdir(parents=True, exist_ok=True)
  by_subj = defaultdict(list)
  catalog = []
  for paper in m['papers']:
    bank, eid = convert_paper(paper)
    year = int(str(paper['year'])[:4])
    catalog.append({
      'paper_id': paper['paper_id'], 'exam_id': eid, 'subject': bank['exam']['subject'],
      'year': str(paper['year']), 'category': paper['category'], 'title': paper['title'],
      'questions': len(bank['questions']), 'lazy': year >= 2020,
      'file': f"subjects/{slug(bank['exam']['subject'])}.json" if year >= 2020 else None,
    })
    if year >= 2020:
      by_subj[bank['exam']['subject']].append(bank)
  for subj, banks in by_subj.items():
    seen, unique = set(), []
    for b in banks:
      if b['exam']['id'] in seen: continue
      seen.add(b['exam']['id']); unique.append(b)
    (LAZY_SUB / f'{slug(subj)}.json').write_text(json.dumps({'subject': subj, 'schema_version': '1.0', 'papers': unique}, ensure_ascii=False, separators=(',', ':')))
  (LAZY / 'catalog.json').write_text(json.dumps({
    'source': 'Matric_Questions.json',
    'note': 'Eager = existing + missing English Language / Algebra. Lazy = slim 2020+ by subject.',
    'totals': m.get('totals'), 'lazy_root': 'assets/high/exams/matric_lazy',
    'subjects': sorted(by_subj.keys()), 'papers': catalog,
  }, ensure_ascii=False, indent=2) + '\n')
  print('done', 'lazy subjects', len(by_subj))

if __name__ == '__main__':
  main()
