#!/usr/bin/env bash
# Whole matric-audit pipeline, in order (each step is idempotent), then the derived files.
set -euo pipefail
cd "$(dirname "$0")/../.."
python3 tool/matric_audit/fix_tex.py
python3 tool/matric_audit/fix_typos.py
python3 tool/matric_audit/fix_images.py
python3 tool/matric_audit/dedupe.py
python3 tool/matric_audit/dedupe_within.py
python3 tool/matric_audit/renumber.py
python3 tool/matric_audit/attach_figures.py
python3 tool/matric_audit/apply_fixes.py
python3 tool/exam_summary.py
python3 tools/map_unit_questions.py
python3 tools/verify_unit_links.py --quiet
python3 tool/build_tutor_index.py
python3 tool/matric_audit/audit.py
