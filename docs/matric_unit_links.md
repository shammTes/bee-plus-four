# Notes units ↔ matric questions ↔ exercises

The "Matric questions" card on a notes unit and its "Exercises (N)" chip both read link files.
This branch rebuilt them from the current question banks. **It must merge after #21** (Exercise bank fill), because
it is based on that branch and re-tags and fixes items in the exercise files #21 wrote.

## Files and tools

| File | What it is |
|---|---|
| `assets/high/notes/unit_questions.json` | `units: {unitId: [{id, confidence, via, secondary?, copies?}]}`, compact. Read by `NotesRepo` → `UnitLinks` (`lib/high/state/links.dart`), which keeps ids found in the eager exam bank and puts auto-marked questions first. |
| `tools/map_unit_questions.py` | Rebuilds `unit_questions.json` from every paper in `assets/high/exams/index.json` (206 papers, 16 880 questions). ~20 s. `--calibrate` prints accuracy against the textbook-ref links. |
| `tools/unitmap_lib.py` | Shared loaders, subject families, tokenizer, TF-IDF and kNN. |
| `tools/verify_unit_links.py` | Checker (see below). Exits 1 on any error. |
| `test/unit_links_test.dart` | Flutter test: loads `ExamRepo` and checks every linked id resolves to a loaded question of an allowed subject, and every exercise unit key is a notes unit. |
| `tool/matric_unit_sync/overrides.json` | Questions dropped by hand, with the working. |
| `tool/matric_unit_sync/textbook_ref_links.json`, `prior_text_links.json`, `before_counts.json` | Snapshot of the previous `unit_questions.json`: textbook-ref links (kept as the strongest evidence), earlier text links (low-confidence fallback), and per-unit counts before this change. |
| `tool/matric_unit_sync/report.json` | Output: every dropped (broken) question with its reason, key conflicts between copies, every question that could not be placed, and counts before/after per unit. |
| `tools/fix_legacy_exercises.py` + `tool/matric_unit_sync/exercise_fixes.json` | Hand-checked key/explanation fixes and drops for older practice items, plus unit tags for the English 11 "General" items. Idempotent. Run it again after `tools/clean_exercises.py`. |

Re-run everything:

```
python3 tools/fix_legacy_exercises.py && python3 tools/verify_exercises.py
python3 tools/map_unit_questions.py && python3 tools/verify_unit_links.py
```

## How a question is placed

A question and its exact copies in other papers form one group: same subject family, same normalised stem, same options.
Each group is linked to a unit once. The representative copy is the curated paper's copy, or else the copy with the longest explanation.
The evidence is tried strongest first:

1. **Textbook-ref link** from the previous map: the question's `textbook_ref` unit and printed page (confidence high/medium).
2. **`textbook_ref`** ("Grade N, Unit M – title") of any copy, resolved against the notes units of the subject family.
3. **English rules**: each grammar or function point is linked to every unit whose lessons teach it, up to 5 units; the extra units are marked `secondary`. A reading question is linked to Reading Comprehension only when its passage is in the paper data.
4. **Text classifier** (for the other subjects): TF-IDF of the stem, options and topic against the notes unit titles, lesson titles and text, plus nearest neighbours among unit-tagged exercise items and textbook-ref links.
   - Checked against the textbook-ref links: "medium" was right 97% of the time and "low" 88%. Anything weaker is not linked.
   - When the classifier is unsure, an earlier text link is kept at low confidence if that unit is still in its top 3.
5. Chemistry / General Science lab, apparatus and scientific-method questions also go to `chem9-u4` (Capstone Review & Lab Guide).

Social Studies questions may link to History, Geography or Business & Economics units.
General Science may link to Biology, Chemistry or Physics. General Knowledge may link to any subject except English and Maths.

## Linked counts per subject / grade

"Before" = the old `unit_questions.json`, counting only ids the app could resolve. "Unit links" counts a question once per unit it is linked to.

| Subject | Grade | Units | Unit links before | after | Unique questions before | after | Units with <10 before → after |
|---|---|---|---|---|---|---|---|
| Agriculture | 11 | 3 | 219 | 502 | 216 | 499 | 0 → 0 |
| Agriculture | 12 | 4 | 235 | 603 | 234 | 602 | 0 → 0 |
| Biology | 9 | 4 | 152 | 341 | 151 | 340 | 0 → 0 |
| Biology | 10 | 8 | 199 | 491 | 187 | 480 | 0 → 0 |
| Biology | 11 | 6 | 131 | 326 | 128 | 323 | 0 → 0 |
| Biology | 12 | 3 | 103 | 247 | 102 | 246 | 0 → 0 |
| Business Economics | 10 | 3 | 238 | 666 | 238 | 666 | 0 → 0 |
| Business Economics | 11 | 2 | 181 | 594 | 181 | 594 | 0 → 0 |
| Business Economics | 12 | 2 | 176 | 536 | 176 | 536 | 0 → 0 |
| Chemistry | 9 | 4 | 131 | 426 | 131 | 417 | 1 → 0 |
| Chemistry | 10 | 5 | 206 | 575 | 203 | 572 | 0 → 0 |
| Chemistry | 11 | 5 | 173 | 566 | 170 | 563 | 0 → 0 |
| Chemistry | 12 | 3 | 100 | 309 | 100 | 309 | 0 → 0 |
| English | 9 | 10 | 88 | 561 | 88 | 419 | 5 → 0 |
| English | 10 | 10 | 52 | 491 | 52 | 403 | 9 → 2 |
| English | 11 | 24 | 89 | 1417 | 89 | 1044 | 22 → 2 |
| English | 12 | 5 | 25 | 162 | 25 | 130 | 4 → 0 |
| Geography | 9 | 6 | 162 | 390 | 160 | 388 | 1 → 0 |
| Geography | 10 | 5 | 167 | 374 | 167 | 374 | 0 → 0 |
| Geography | 11 | 8 | 194 | 406 | 192 | 404 | 1 → 0 |
| Geography | 12 | 7 | 148 | 347 | 144 | 343 | 1 → 0 |
| History | 9 | 6 | 119 | 281 | 115 | 277 | 1 → 0 |
| History | 10 | 12 | 176 | 471 | 175 | 470 | 6 → 0 |
| History | 11 | 12 | 175 | 480 | 174 | 479 | 1 → 0 |
| History | 12 | 5 | 119 | 362 | 117 | 360 | 0 → 0 |
| Mathematics | 9 | 8 | 83 | 194 | 83 | 194 | 4 → 0 |
| Mathematics | 10 | 5 | 62 | 151 | 62 | 151 | 2 → 1 |
| Mathematics | 11 | 6 | 68 | 235 | 63 | 232 | 3 → 0 |
| Mathematics | 12 | 4 | 47 | 199 | 47 | 199 | 1 → 0 |
| Physics | 9 | 4 | 81 | 333 | 78 | 330 | 0 → 0 |
| Physics | 10 | 5 | 79 | 342 | 79 | 342 | 0 → 0 |
| Physics | 11 | 3 | 79 | 307 | 78 | 306 | 0 → 0 |
| Physics | 12 | 2 | 50 | 174 | 50 | 174 | 0 → 0 |
| **All** | | 199 | 4307 | 13859 | 4049 | 12289 | 62 → 5 |

Per paper subject (unique questions): 12289 linked, 2353 not placed, 472 dropped.

| Paper subject | Linked | Not placed | Dropped (broken) |
|---|---|---|---|
| Agriculture | 1079 | 277 | 19 |
| Biology | 1052 | 136 | 38 |
| Business and Economics | 1543 | 74 | 11 |
| Chemistry | 1543 | 114 | 47 |
| English | 1249 | 329 | 14 |
| General Knowledge | 145 | 719 | 11 |
| General Science | 845 | 63 | 14 |
| Geography | 1172 | 155 | 115 |
| History | 1222 | 205 | 7 |
| Mathematics | 765 | 120 | 153 |
| Physics | 880 | 73 | 38 |
| Social Studies | 794 | 88 | 5 |

Units still under 10 links (the checker prints these with the reason):

- `eng10-u3` noun clauses (1): the bank has almost no noun-clause items.
- `eng10-u8` present continuous / confusing verbs (8).
- `eng11-u14` question formation (4): only a few "correct question for this answer" items exist.
- `eng11-u22` pronunciation (0): no paper has pronunciation items.
- `math10-u2` axiomatic geometry & proofs (3): few such items, and the figure-based ones are dropped.

## Broken questions (not linked; the exam papers are unchanged)

| Reason | Questions |
|---|---|
| figure not shipped | 318 |
| needs a map/figure that is not in the paper data | 46 |
| key differs from the textbook-checked copy | 29 |
| copies of this question have different keys | 25 |
| key text appears in two options | 24 |
| faulty item | 20 |
| key is an empty option | 2 |
| wrong key | 2 |
| wrong key and figure not shipped | 2 |
| garbled options | 1 |
| faulty stem | 1 |
| explanation is self-contradicting working | 1 |
| no correct option | 1 |

"Figure not shipped" means the stem points at a `file:///android_asset/…` image that is not in the app.
"Key differs from the textbook-checked copy" means a bank copy disagrees with the curated, textbook-checked copy of the same question. The curated copy is kept.
When copies disagree and none is curated, the whole group is dropped (39 conflicts in total).
Hand drops (`overrides.json`):

- `bank-math-matric-2023-q024`: wrong key: (x+3)^2+(y+2)^2=36 gives x^2+6x+y^2+4y-23=0, which is option D; key says A (=26)
- `drive-math_matric_2023-q024`: wrong key: (x+3)^2+(y+2)^2=36 gives x^2+6x+y^2+4y-23=0, which is option D; key says A (=26)
- `bank-math-matric-2023-q025`: wrong key and figure not shipped: AB = 12 sin30 = 6, DB = AB cos60 = 3 (option D); key says E (9)
- `drive-math_matric_2023-q025`: wrong key and figure not shipped: AB = 12 sin30 = 6, DB = AB cos60 = 3 (option D); key says E (9)
- `bank-agriculture-model-2016-q081`: garbled options: key D 'Cruling' and a sixth option 'F. Crutching' (the real answer)
- `bank-geography-model-2020-2021-q078`: faulty stem: asks which is NOT a problem, all of A-D are problems and the key is 'All'
- `chem-2017-18-model-p1-q75`: no correct option: E/c^2 = 4.7e-13/9e16 = 5.2e-30 kg; key 5.2e-29 kg
- `bank-gkn-matric-2023-q015`: explanation is self-contradicting working ('Wait, I/T conflict'); key B is right but the explanation is not usable

Not placed (still in the Matric tab, just not on a unit):

| Reason | Questions |
|---|---|
| no textbook ref and no clear match to a notes unit | 2024 |
| English reading question: its passage is not in the paper data | 314 |
| English item: no grammar point matched a unit lesson | 15 |

Most of the questions that are not placed are General Knowledge items, about current affairs, world facts and the like, which no textbook unit covers.

## Exercises

- The notes "Exercises (N)" chip and the Exercise tab unit tile read the same map, `ExamRepo.exerciseUnits` keyed by the item's `unit`. So the counts match and the chip opens that unit's items, as long as the `unit` is a real notes unit id. The checker verifies this for every main and school item.
  - Exception: 4 Grade 10 school items on torque are tagged `phys9-u3`. They show under that Grade 9 unit, both in the notes and in the Exercise tab.
- **English 11 "General"**: the 421 items with `unit: null` were tagged with keyword rules on the prompt and explanation (`ENG11_RULES` in `tools/fix_legacy_exercises.py`). 19 were dropped and 402 tagged. English 11 now has no General items: u1 158 · u2 34 · u3 36 · u4 44 · u5 140 · u6 31 · u7 53 · u8 66 · u9 53 · u10 40 · u11 40 · u12 30 · u13 30 · u14 34 · u15 30 · u16 62 · u17 30 · u18 37 · u19 30 · u20 30 · u21 30 · u22 33 · u23 30 · u24 44.
- **Key fixes**: 43 answers were corrected.
  - 40 are English 11 punctuation and reported-speech items that had been keyed to option A by default.
  - 3 are Physics 10 items: six cells with one reversed = 6 V; the TV uses more energy than the toaster; the 100 W bulb in series gets 82.5 V.
- 10 self-correcting "Wait, let me recalculate…" explanations were rewritten (their keys were right).
- 31 items were removed: 19 English 11 items that were ambiguous or had no single correct option, and these:

- `physics_9_practice_g9_physics_127`: friction is 9 N for the stated numbers; 9 N is not an option
- `physics_9_practice_g9_physics_131`: effort is about 52 N; no option matches
- `physics_9_practice_g9_physics_137`: unknown weight is 9 N; not an option
- `physics_9_practice_g9_physics_146`: depends on a previous question not shown
- `physics_9_practice_g9_physics_148`: balance point is the 70 cm mark; not an option
- `physics_10_practice_g10_physics_179`: "one diagonal connected" makes the circuit ambiguous
- `physics_10_practice_g10_physics_187`: current is 0.185 A; not an option
- `physics_10_practice_g10_physics_197`: "diagonal corners connected" makes the circuit ambiguous
- `chemistry_11_practice_g11_chemistry_151`: mass of Cl2 is 13.2 g; not an option
- `chemistry_10_practice_g10_chemistry_126`: needs 539 g of H2SO4; not an option
- `mathematics_10_practice_g10_math_325`: sum is 155; not an option
- `mathematics_10_practice_g10_math_333`: no term equals 1/27 for a = 1, r = 1/4

Exercise bank total: 8274 → 8243 items. Every unit still has ≥ 25 (`tools/verify_exercises.py`).

## Checker (`tools/verify_unit_links.py`)

Fails on any of these:
- `unit_questions.json` is not compact
- an unknown unit id
- a dangling question id (not in the eager exam bank)
- a question linked to a unit of a subject its paper cannot belong to
- a dropped (broken) question that is still linked
- a duplicate id in a unit
- an exercise `unit` that is not a notes unit of that subject
- duplicate exercise ids
- `exercises/index.json` counts that differ from the files

It reports units under `--min` (10) links with the reason, untagged exercise counts per book, and per-unit exercise counts.

## Known gaps

- 2353 questions are not placed. Most are General Knowledge, plus English reading questions whose passage is missing from the paper data.
- 318 questions point at figures that are not shipped.
- The lazy `matric_lazy` packs are not linked. They load on demand, and about 96% of them duplicate the eager bank.
- Other subjects still have untagged ("General") exercise items, for example History 11 (407), Agriculture 11 (225), Maths 10 (212) and English 9 (212). Only English 11 was in scope here.
- The loader maps an untagged exercise item to the unit `eng<grade>-practice` for every subject (`repository.dart`). It is harmless, because the item still shows under General.
- `unit_questions.json` is about 1.1 MB and is parsed on the main thread when the notes load.
