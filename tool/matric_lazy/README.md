# Matric lazy packs

Source: Drive `Matric_Questions.json` (~20 MB, 11 169 questions, 136 papers).

## Size tradeoff
- Eager exams already cover most papers (~24 MB under `assets/high/exams`).
- Full Drive JSON is **not** shipped (would roughly double exam assets).
- **Eager adds** (~0.4 MB): English Language matric 2017–2024 + Algebra/Geometry 2023 (were missing).
- **Lazy packs** (~2.2 MB source): slim English-only 2017+ papers under `assets/high/exams/matric_lazy/subjects/<subject>.json`, loaded via `ExamRepo.ensureLazySubject` when a Matric subject page opens. Dedupes by exam id against already-loaded papers.
- APK zip compresses JSON well; expect ~0.6–0.9 MB APK delta for lazy packs + eager banks.

Regenerate (needs `/workspace/tmp-sync/drive/Matric_Questions.json`):
`python3 tool/matric_lazy/split_matric.py`
