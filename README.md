# 4 — Highschool offline curriculum + study coach

## Exam extraction status (live)

| Source | Parsed stems | Solved (step-by-step + unit links) |
|--------|-------------:|-----------------------------------:|
| Matriculation (ESECE OCR) | partial 2023 pages | 15 |
| School **model** 2017/18 (Warsay Yikealo) | 269 | 15 |
| School **semester** finals | ~100 | 7 |
| **Total in app bank** | | **~37** |

Each solved item includes:
- correct answer + numbered explanation
- unit note links (grade/subject/unit)
- similar practice variants where topic templates apply

### Full pack (JSON + Dart UI)
[bee_plus_four_exam_extraction_latest.tar.gz](https://drive.google.com/file/d/PLACEHOLDER)

Merge into `assets/content/` and `lib/`.

### Accuracy
- Text model/school PDFs: parsed by regex, answers only when curriculum-verified
- Scanned matric PDFs: OCR page batches; no invented stems
- Unsolved stems kept in extraction queue for continuation

### App entry points
- Exams → Matric questions / adaptive practice
- Notes → unit → Matric & model for this unit
- Coach → exam practice / catalogue
