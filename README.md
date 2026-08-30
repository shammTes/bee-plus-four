# 4 — Highschool offline curriculum + study coach

## Exam extraction status

| Source | Parsed stems | Solved (explanations + unit links) |
|--------|-------------:|-----------------------------------:|
| Matriculation ESECE 2023 (OCR) | pages batch | **15** |
| School model 2017/18 (Warsay Yikealo) | **269** | **15** |
| School semester finals | **~100** | **7** |
| **In-app bank** | | **37** |

Each solved item: answer, step-by-step, unit links, similar practice where applicable.

### Download full pack
[bee_plus_four_exam_extraction_latest.tar.gz](https://drive.google.com/file/d/1mDBolDyFbJmbPh5yy8UaA3nJ8nWlzb2a/view)

Contains `matric_questions.json`, `exam_catalog.json`, exam UI sources, parsed stem queues.

### Pipeline
1. **Text PDFs** (model + school) — full text extract + MCQ parse
2. **Scanned matric** — OCR page batches (Physics/Chem/Math/Bio 2023 underway)
3. Only curriculum-verified answers enter the solved bank
4. Unit index groups questions under notes for systematic practice

### App
- Exams → catalogue + matric bank + adaptive sessions
- Notes → unit → linked matric/model items
- Coach → exam practice (offline intents only)
