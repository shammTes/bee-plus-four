# 4 — Highschool offline curriculum + controlled study coach

Flutter. Same security posture as BEE PLUS. **No Junior track** (G9–G12).

## Matric / model exams

- **Catalogue:** Drive-verified paper index (`assets/content/exam_catalog.json`)
- **Extracted bank:** OCR of official ESECE 2023 papers (Physics, Math/Algebra&Geometry, Chemistry) with:
  - step-by-step explanations
  - **similar practice** variants (same skill; not claimed as past papers)
  - **unit note links** so each question sits with the matching curriculum unit
- UI: **Exams → Matric questions** and **Notes → unit → Matric & model for this unit**

Full wiring pack (Dart + JSON):
[bee_plus_four_matric_full_pack.tar.gz](https://drive.google.com/file/d/1hpsCdNjkZDOngEdWm-C0nOeI-K2R2-tT/view)

## Accuracy policy

Stems from OCR of official papers. Answers explained from standard secondary curriculum reasoning. Similar questions are training variants only.

## Coach

Offline intent bot: quiz, **exam practice**, catalogue summary — curriculum packs only.

## Unlock

HMAC QR, device-bound, single-use.
