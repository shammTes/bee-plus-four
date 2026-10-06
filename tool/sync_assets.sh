#!/usr/bin/env bash
# Copies exam content UNCHANGED from the Warsay Prep web app (/workspace/examprep/content) and the High notes content
# (/workspace/high/content, when present) into assets/high/. Writes assets/high/exams/index.json (Flutter cannot list
# asset folders) in the web preview's exam order (tools/build_preview.py sort_key).
#   bash tool/sync_assets.sh [exam_src] [notes_src]
set -euo pipefail
EX=${1:-/workspace/examprep/content}
NO=${2:-/workspace/high/content}
ROOT=$(cd "$(dirname "$0")/.." && pwd)
DST=$ROOT/assets/high
rm -rf "$DST/exams"; mkdir -p "$DST/exams/media"
python3 - "$EX" "$DST/exams" <<'PY'
import json, os, sys, shutil, glob
src, dst = sys.argv[1], sys.argv[2]
exams, topics = [], []
for p in sorted(glob.glob(os.path.join(src, '*.json'))):
    n = os.path.basename(p)
    if n in ('schema.json', 'catalog.json', 'summary.json') or n.startswith(('.', '_')) or n.endswith('.tmp.json'):
        continue
    if n == 'matric_phy_matric_2023.json':   # never used
        continue
    try:
        d = json.load(open(p, encoding='utf-8'))
    except Exception as e:
        print('skip', n, e); continue
    if isinstance(d.get('exam'), dict) and isinstance(d.get('questions'), list):
        exams.append((d['exam'], n))
    elif isinstance(d.get('topics'), list):
        topics.append(n)
    else:
        continue
    shutil.copyfile(p, os.path.join(dst, n))          # byte-for-byte copy
def key(t):
    x, n = t; y = str(x.get('year', ''))
    return (-int(y[:4]) if y[:4].isdigit() else 0, x.get('subject', ''), 0 if x.get('type') == 'matriculation' else 1, x.get('semester') or 0, x['id'])
exams.sort(key=key)
media = sorted(os.listdir(os.path.join(src, 'media'))) if os.path.isdir(os.path.join(src, 'media')) else []
for m in media:
    shutil.copyfile(os.path.join(src, 'media', m), os.path.join(dst, 'media', m))
json.dump({'exams': [n for _, n in exams], 'topics': topics, 'media': media}, open(os.path.join(dst, 'index.json'), 'w'), indent=1)
print(len(exams), 'exams,', len(topics), 'topic indexes,', len(media), 'media files')
PY
if [ -d "$NO" ]; then
  rm -rf "$DST/notes"; mkdir -p "$DST/notes"; touch "$DST/notes/.keep"
  cp -r "$NO"/. "$DST/notes/"
  echo "notes content copied from $NO"
fi
# the derived files the app reads at start-up (committed; see README → Performance notes)
python3 "$ROOT/tool/exam_summary.py"
if [ -f "$DST/notes/notes/index.json" ]; then python3 "$ROOT/tool/split_notes.py"; fi
