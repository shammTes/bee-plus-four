# Exam parse batch note (2026-09-13)

## Done this run
- Inventories: Matric Physics, Algebra/Geometry, Chemistry, Biology, Examinations 2023.
- Drive file `1998_Physics.pdf` (id `1tNk4wrUdKD6JYuh5-SODiZygInaMYy1e`) is **mislabelled** — it is ESECE **Biology 1998** (subject code 05, 70 MCQs).
- Parsed 26 MCQs from readable pages (q1-16, 23-27, 33-37) into `assets/content/matric_biology.json`.
- Keys: 24 verified; q5 and q6 left `correct_index = -1`.
- Paper has 5 options A–E.

## GitHub state observed
- `matric_questions.json` and subject split files were **missing** from main at start.
- Concurrent update added Physics 2001 to `exam_catalog.json` (34 claimed) but bank JSON still absent when this note was written.

## Next batch (priority)
1. Confirm whether `2000_Physics.pdf` / `2001_Physics.pdf` / `2002_Physics.pdf` are actually Physics (covers were often mis-stapled).
2. Parse remaining Biology 1998 items (q17-22, 28-32, 38-70) after rotating inverted pages.
3. Real Physics years still missing from Drive Physics folder as physics: 1998 (file is bio), no 2018 physics PDF in that folder; 2023 physics is in Examinations 2023 (`1koD6UECbC7iASW-jhGFaaFMhZqpnn3iF`).
4. Math/Algebra gaps: 1998, 2002, 2009, 2012-2017 commercial vs geometry tracks.
5. Chemistry gaps: 1998, 2000, 2001, 2002, 2010, 2017 (2023 already catalogued).
6. Merge any restored prior ~500-question bank if recovered; do not overwrite without merge.
