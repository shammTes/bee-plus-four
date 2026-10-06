# Exercise tab: per-unit fill (tools/fill_exercises.py)

Every notes unit now has at least 25 MCQs (main bank + school papers). Grade 12 (all subjects) and English (all grades) were rebuilt unit by unit; other units under 30 were topped up.

Re-run: `python3 tools/fill_exercises.py && python3 tools/verify_exercises.py`. The fill tool removes the items it added before (ids with `_sn_`, `_au_`, `_ms_`, `_nx_`) and rebuilds them, so it is safe to re-run.

Sources, in order: Study_Notes review exercises (`study_notes#…`, English 11-12 Tigrinya step removed), hand-written items in `tool/exercises_fill/<subject>_<grade>.txt` (`authored#…`), similar questions of mapped matric items (`matric_similar#…`, only with a worked explanation of 45+ characters and no figure), and the notes unit exercise MCQs (`notes#…`) when a unit is still short. Source key errors found while checking answers are corrected in `tool/exercises_fill/fixes.json`.

Only MCQs: the loader (`lib/high/data/repository.dart`) needs a list of options and an answer index for every item.

| grade | subject | units | items in units (main + school) | min per unit | added by fill tool |
|---|---|---|---|---|---|
| 9 | biology | 4 | 880 | 83 | 0 |
| 9 | chemistry | 4 | 439 | 27 | 27 |
| 9 | english | 10 | 269 | 25 | 269 |
| 9 | geography | 6 | 276 | 25 | 56 |
| 9 | history | 6 | 205 | 25 | 125 |
| 9 | mathematics | 8 | 359 | 28 | 120 |
| 9 | physics | 4 | 520 | 64 | 0 |
| 10 | biology | 8 | 827 | 43 | 0 |
| 10 | business_economics | 3 | 246 | 48 | 0 |
| 10 | chemistry | 5 | 577 | 47 | 0 |
| 10 | english | 10 | 261 | 25 | 261 |
| 10 | geography | 5 | 192 | 28 | 46 |
| 10 | history | 12 | 362 | 25 | 213 |
| 10 | mathematics | 5 | 325 | 45 | 16 |
| 10 | physics | 5 | 636 | 49 | 0 |
| 11 | agriculture | 3 | 513 | 130 | 0 |
| 11 | biology | 6 | 679 | 45 | 20 |
| 11 | business_economics | 2 | 160 | 45 | 20 |
| 11 | chemistry | 5 | 519 | 70 | 0 |
| 11 | english | 24 | 743 | 30 | 743 |
| 11 | geography | 8 | 423 | 26 | 46 |
| 11 | history | 12 | 659 | 25 | 59 |
| 11 | mathematics | 6 | 275 | 26 | 88 |
| 11 | physics | 3 | 285 | 76 | 0 |
| 12 | agriculture | 4 | 180 | 45 | 175 |
| 12 | biology | 3 | 103 | 32 | 103 |
| 12 | business_economics | 2 | 86 | 42 | 86 |
| 12 | chemistry | 3 | 111 | 30 | 111 |
| 12 | english | 5 | 134 | 25 | 134 |
| 12 | geography | 7 | 227 | 29 | 227 |
| 12 | history | 5 | 156 | 30 | 156 |
| 12 | mathematics | 4 | 133 | 32 | 133 |
| 12 | physics | 2 | 62 | 30 | 62 |

Total added by the fill tool: 3296.

## Per unit

- **biology 9**: u1 248, u2 375, u3 83, u4 174
- **chemistry 9**: u1 156, u2 136, u3 120, u4 27
- **english 9**: u1 29, u2 28, u3 27, u4 25, u5 26, u6 27, u7 30, u8 26, u9 25, u10 26
- **geography 9**: u1 32, u2 48, u3 112, u4 25, u5 33, u6 26
- **history 9**: u1 26, u2 26, u3 25, u4 43, u5 44, u6 41
- **mathematics 9**: u1 40, u2 30, u3 47, u4 29, u5 28, u6 69, u7 79, u8 37
- **physics 9**: u1 136, u2 118, u3 202, u4 64
- **biology 10**: u1 199, u2 183, u3 43, u4 60, u5 66, u6 58, u7 128, u8 90
- **business_economics 10**: u1 120, u2 78, u3 48
- **chemistry 10**: u1 135, u2 47, u3 125, u4 201, u5 69
- **english 10**: u1 27, u2 27, u3 25, u4 26, u5 27, u6 25, u7 26, u8 25, u9 26, u10 27
- **geography 10**: u1 54, u2 36, u3 39, u4 28, u5 35
- **history 10**: u1 49, u2 36, u3 30, u4 36, u5 30, u6 29, u7 25, u8 25, u9 26, u10 25, u11 25, u12 26
- **mathematics 10**: u1 83, u2 93, u3 59, u4 45, u5 45
- **physics 10**: u1 138, u2 167, u3 49, u4 139, u5 143
- **agriculture 11**: u1 130, u2 144, u3 239
- **biology 11**: u1 146, u2 193, u3 113, u4 81, u5 45, u6 101
- **business_economics 11**: u1 115, u2 45
- **chemistry 11**: u1 107, u2 159, u3 106, u4 70, u5 77
- **english 11**: u1 31, u2 31, u3 31, u4 41, u5 32, u6 31, u7 30, u8 31, u9 30, u10 30, u11 30, u12 30, u13 30, u14 30, u15 30, u16 30, u17 30, u18 30, u19 30, u20 30, u21 30, u22 33, u23 30, u24 32
- **geography 11**: u1 80, u2 91, u3 35, u4 26, u5 40, u6 45, u7 26, u8 80
- **history 11**: u1 70, u2 52, u3 93, u4 48, u5 61, u6 47, u7 38, u8 27, u9 25, u10 27, u11 57, u12 114
- **mathematics 11**: u1 104, u2 30, u3 27, u4 26, u5 61, u6 27
- **physics 11**: u1 125, u2 84, u3 76
- **agriculture 12**: u1 45, u2 45, u3 45, u4 45
- **biology 12**: u1 37, u2 32, u3 34
- **business_economics 12**: u1 44, u2 42
- **chemistry 12**: u1 36, u2 45, u3 30
- **english 12**: u1 25, u2 27, u3 26, u4 27, u5 29
- **geography 12**: u1 33, u2 29, u3 31, u4 30, u5 31, u6 41, u7 32
- **history 12**: u1 31, u2 32, u3 30, u4 32, u5 31
- **mathematics 12**: u1 35, u2 33, u3 32, u4 33
- **physics 12**: u1 30, u2 32
