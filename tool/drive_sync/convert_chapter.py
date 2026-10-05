#!/usr/bin/env python3
"""Convert a Drive chapter JSON into High exercise-bank MCQs (append)."""
import json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EX = ROOT / 'assets/high/exercises'
SUBJ = {
  'Chemistry': 'chemistry', 'History': 'history', 'Biology': 'biology', 'Physics': 'physics',
  'Mathematics': 'mathematics', 'Geography': 'geography', 'English': 'english',
  'Agriculture': 'agriculture', 'Business and Economics': 'business_economics',
}

def steps_text(steps):
  return ' '.join(f"{s.get('title','')}: {s.get('detail','')}".strip() for s in (steps or []))

def convert(path: Path):
  d = json.loads(path.read_text())
  subj = SUBJ.get(d['subject'], d['subject'].lower().replace(' ', '_'))
  grade = int(d['grade'])
  unit = f"{subj[:4]}{grade}-u{d['chapter_number']}"  # best-effort
  out_file = EX / f'{subj}_{grade}.json'
  bank = json.loads(out_file.read_text()) if out_file.exists() else {'subject': subj, 'grade': grade, 'questions': []}
  existing = {q['id'] for q in bank['questions']}
  added = 0
  for q in d.get('questions', []):
    if q.get('type') != 'MC' or not q.get('options'):
      continue
    qid = f"drive_{q['question_id']}"
    if qid in existing:
      continue
    opts = []
    for o in q['options']:
      opts.append(re.sub(r'^[A-E]\.\s*', '', o).strip())
    ans_letter = (q.get('answer') or 'A')[0]
    ans_idx = 'ABCDE'.index(ans_letter) if ans_letter in 'ABCDE' else 0
    expl = steps_text(q.get('solution_steps')) or q.get('answer', '')
    bank['questions'].append({
      'id': qid, 'unit': unit, 'prompt': q['question'], 'options': opts,
      'answer': ans_idx, 'explanation': expl, 'verified': 'drive_chapter',
      'src': d.get('chapter_id'),
    })
    added += 1
  out_file.write_text(json.dumps(bank, ensure_ascii=False, indent=1) + '\n')
  # stash raw
  dest = EX / 'drive_chapters' / path.name
  dest.write_text(path.read_text())
  print(f'{path.name}: +{added} MCQs → {out_file.name} (total {len(bank["questions"])})')

if __name__ == '__main__':
  for a in sys.argv[1:]:
    convert(Path(a))
