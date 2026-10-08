# Matric paper audit (2026-10)

User report: "a lot of blank matric papers, especially physics and math". What was actually wrong and the tools that fix it:

| step | script | what |
|---|---|---|
| audit | `audit.py [ROOT] [--json out]` | per paper / subject counts, read the way `ExamRepo` reads the packs (eager index + lazy Drive packs) |
| exact render check | `test/papers_render_test.dart` | loads every paper through `ExamRepo` (summary stubs, `ensureLazySubject`, `ensureAllExams`) and parses every maths segment with flutter_math_fork; fails on blank papers / stems, MCQ without options or key, TeX parse errors, over-escaped TeX, unshipped picture links, a paper listed twice. `PAPER_REPORT=x.json` writes the per-paper report |
| 1 | `fix_tex.py [--check]` | `\\frac` (over-escaped) -> `\frac` etc., `$` amounts inside `$$..$$`, `\text{___}`, `\text{ \Omega}` |
| 2 | `dedupe.py` | lazy `drive-*` packs repeated 128 eager papers under other ids (so each showed twice; the PR #34 removals came back through them), plus 4 eager pairs; keeps the more complete copy, merges copy-only questions (`dedupe_log.json`) |
| 3 | `dedupe_within.py` | the same question 2x inside one pack (overlapping Drive batches) (`dedupe_within_log.json`) |
| 4 | `renumber.py` | bank packs numbered Part I by batch slot, so Part II items left holes (Q4, Q6 ...) |
| 5 | `fix_images.py` | `![..](file:///android_asset/exam_images/..)` links to pictures that were never shipped (source APK keeps them encrypted) were shown as raw text -> visible "[Figure: .. (not available)]" + review flag |
| 6 | `apply_fixes.py` + `answer_fixes.json` | hand-solved key fixes / flags; identical printed options both accepted |
| 7 | `fix_typos.py` | leading copied question numbers, °c, wave length, focus length, it's, db |

Then: `python3 tool/exam_summary.py && python3 tools/map_unit_questions.py && python3 tools/verify_unit_links.py && python3 tool/build_tutor_index.py`.
