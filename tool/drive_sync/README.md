# Drive chapter sync

Source folder: https://drive.google.com/drive/folders/1k0yjHIKkeIlE_7QMhs5ph1XOF9FDGgjV

Listed (2026-10-05):
- `history_g10_c1/` → `history_g10_c1.json` (5 worked questions + similar)
- `chem_g10_c1.json` (5 worked questions + similar)
- `Study_Notes_markdown/` — 173 chapter notes by subject (Agriculture…Physics) + INDEX.md
- Matric_Questions.{csv,json,xlsx}, Practice_Questions.*, Study_Notes.*

Chapter JSON schema (Drive):
`chapter_id, subject, grade, chapter_number, chapter_title, questions[]`
Each question: `question_id, type (MC|FILL|WORKOUT|SHORT_ANSWER), difficulty, concepts, question, options, solution_steps[{step,title,detail}], answer, similar_questions[]`

Convert MC items into `assets/high/exercises/<subject>_<grade>.json` (prompt/options/answer index/explanation)
and keep full packs under `assets/high/exercises/drive_chapters/` for Tutor / step UI later.

Binary download of Drive files needs the `user-Google-drive` connector signed in (DownloadFile);
MCP `read_file` can pull text JSON for small chapters.
