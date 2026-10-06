# Exercise tab: per-unit fill (tools/fill_exercises.py)

Every notes unit now has at least 25 MCQs (main bank + school papers). Grade 12 (all subjects) and English (all grades) were rebuilt unit by unit; other units under 30 were topped up.

Re-run: `python3 tools/fill_exercises.py && python3 tools/verify_exercises.py`. The fill tool removes the items it added before (ids with `_sn_`, `_au_`, `_ms_`, `_nx_`) and rebuilds them, so it is safe to re-run.

Sources, in order: Study_Notes review exercises (`study_notes#…`, English 11-12 Tigrinya step removed), hand-written items in `tool/exercises_fill/<subject>_<grade>.txt` (`authored#…`), similar questions of mapped matric items (`matric_similar#…`, only with a worked explanation of 45+ characters and no figure), and the notes unit exercise MCQs (`notes#…`) when a unit is still short. Source key errors found while checking answers are corrected in `tool/exercises_fill/fixes.json`.

Only MCQs: the loader (`lib/high/data/repository.dart`) needs a list of options and an answer index for every item.

| grade | subject | units | items in units (main + school) | min per unit | added by fill tool |
|---|---|---|---|---|---|
| 9 | biology | 4 | 1038 | 149 | 0 |
| 9 | chemistry | 4 | 466 | 27 | 27 |
| 9 | english | 10 | 424 | 25 | 269 |
| 9 | geography | 6 | 311 | 25 | 56 |
| 9 | history | 6 | 205 | 25 | 125 |
| 9 | mathematics | 8 | 484 | 28 | 120 |
| 9 | physics | 4 | 577 | 80 | 0 |
| 10 | biology | 8 | 854 | 43 | 0 |
| 10 | business_economics | 3 | 292 | 48 | 0 |
| 10 | chemistry | 5 | 626 | 48 | 0 |
| 10 | english | 10 | 261 | 25 | 261 |
| 10 | geography | 5 | 192 | 28 | 46 |
| 10 | history | 12 | 362 | 25 | 213 |
| 10 | mathematics | 5 | 408 | 49 | 16 |
| 10 | physics | 5 | 677 | 49 | 0 |
| 11 | agriculture | 3 | 605 | 147 | 0 |
| 11 | biology | 6 | 737 | 45 | 20 |
| 11 | business_economics | 2 | 164 | 45 | 20 |
| 11 | chemistry | 5 | 552 | 73 | 0 |
| 11 | english | 24 | 1145 | 30 | 743 |
| 11 | geography | 8 | 521 | 26 | 46 |
| 11 | history | 12 | 1066 | 30 | 59 |
| 11 | mathematics | 6 | 325 | 26 | 88 |
| 11 | physics | 3 | 292 | 76 | 0 |
| 12 | agriculture | 4 | 313 | 46 | 175 |
| 12 | biology | 3 | 123 | 34 | 103 |
| 12 | business_economics | 2 | 86 | 42 | 86 |
| 12 | chemistry | 3 | 168 | 30 | 111 |
| 12 | english | 5 | 134 | 25 | 134 |
| 12 | geography | 7 | 227 | 29 | 227 |
| 12 | history | 5 | 156 | 30 | 156 |
| 12 | mathematics | 4 | 204 | 32 | 133 |
| 12 | physics | 2 | 62 | 30 | 62 |

Total added by the fill tool: 3296.

Counts include the former "General" items tagged by `tools/tag_general_exercises.py` (see docs/matric_unit_links.md, "Tagging the General exercise items"); an item counts under the unit it is tagged to, which can be a unit of another grade of the same subject (e.g. sequence items of the Grade 10 file count under mathematics 12 u1).

## Per unit

- **biology 9**: u1 267, u2 428, u3 149, u4 194
- **chemistry 9**: u1 157, u2 137, u3 145, u4 27
- **english 9**: u1 105, u2 46, u3 47, u4 31, u5 49, u6 27, u7 30, u8 38, u9 25, u10 26
- **geography 9**: u1 33, u2 56, u3 137, u4 25, u5 33, u6 27
- **history 9**: u1 26, u2 26, u3 25, u4 43, u5 44, u6 41
- **mathematics 9**: u1 40, u2 37, u3 47, u4 29, u5 28, u6 148, u7 97, u8 58
- **physics 9**: u1 141, u2 124, u3 232, u4 80
- **biology 10**: u1 209, u2 188, u3 43, u4 61, u5 66, u6 58, u7 132, u8 97
- **business_economics 10**: u1 155, u2 89, u3 48
- **chemistry 10**: u1 144, u2 48, u3 125, u4 240, u5 69
- **english 10**: u1 27, u2 27, u3 25, u4 26, u5 27, u6 25, u7 26, u8 25, u9 26, u10 27
- **geography 10**: u1 54, u2 36, u3 39, u4 28, u5 35
- **history 10**: u1 49, u2 36, u3 30, u4 36, u5 30, u6 29, u7 25, u8 25, u9 26, u10 25, u11 25, u12 26
- **mathematics 10**: u1 95, u2 92, u3 83, u4 89, u5 49
- **physics 10**: u1 161, u2 171, u3 49, u4 150, u5 146
- **agriculture 11**: u1 147, u2 169, u3 289
- **biology 11**: u1 158, u2 201, u3 137, u4 95, u5 45, u6 101
- **business_economics 11**: u1 119, u2 45
- **chemistry 11**: u1 116, u2 176, u3 108, u4 73, u5 79
- **english 11**: u1 158, u2 34, u3 36, u4 44, u5 140, u6 31, u7 53, u8 66, u9 53, u10 40, u11 40, u12 30, u13 30, u14 34, u15 30, u16 62, u17 30, u18 37, u19 30, u20 30, u21 30, u22 33, u23 30, u24 44
- **geography 11**: u1 80, u2 101, u3 45, u4 26, u5 70, u6 87, u7 27, u8 85
- **history 11**: u1 95, u2 94, u3 140, u4 48, u5 150, u6 95, u7 73, u8 34, u9 49, u10 30, u11 111, u12 147
- **mathematics 11**: u1 106, u2 73, u3 27, u4 26, u5 66, u6 27
- **physics 11**: u1 132, u2 84, u3 76
- **agriculture 12**: u1 108, u2 46, u3 55, u4 104
- **biology 12**: u1 55, u2 34, u3 34
- **business_economics 12**: u1 44, u2 42
- **chemistry 12**: u1 36, u2 102, u3 30
- **english 12**: u1 25, u2 27, u3 26, u4 27, u5 29
- **geography 12**: u1 33, u2 29, u3 31, u4 30, u5 31, u6 41, u7 32
- **history 12**: u1 31, u2 32, u3 30, u4 32, u5 31
- **mathematics 12**: u1 106, u2 33, u3 32, u4 33
- **physics 12**: u1 30, u2 32
