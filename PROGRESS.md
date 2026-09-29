# High — progress

## M1 — theme + clay + Home + Exams list + Settings ✅ (2026-09-29 11:58 EAT)

**Built** (all under `lib/high/`, assets under `assets/high/`, prefs key `high:v1`, fonts `HighNunito`):
- `theme/` — Warsay Prep palette (light + dark) as generated tokens, the Junior 3D clay painter (`clay.dart`,
  multi-layer fills + outer/inset shadows) and `deco.dart`: every High 3D surface (puffy cards/tiles, raised keys with
  thickness edges, pressed-in wells, nav keys, badges, knobs, bars, chart bars). Chrome's `line-height: normal`
  and fractional line boxes are emulated so stacked text doesn't drift against the web.
- `widgets/` — icons + illustrations generated from the web (`tool/gen_art.py` → `art_data.dart`), clay kit
  (Press with pressed-in animation + spring release, Btn, CBtn, PlayBtn, Avatar, Chip, Pill, Seg/catseg, Bar,
  Badge, Knob, Panel, Field), page scaffold (top bar, CSS margin collapsing, floating 5-key nav).
- Screens: shell (Home / Exams / Notes / Mistakes / Settings, per-tab stack, sheets, system back, onboarding
  sheet), **Home** (hero, Matriculation / Model / Grade 9–12 Notes category cards, 4 stat tiles with count-up,
  weekly chart, practice-mix donut, daily quiz, recently practised, weak-topics + tutor banners), **Exams**
  (sticky category segment + year chips, category header, search, subject tiles, all exams grouped by subject),
  **Settings** (profile + name, appearance light/dark/auto, progress + content summaries, 2-tap reset).
  Notes / Mistakes are placeholders until M2/M3; exam rows etc. open a "coming soon" page until M2.
- Data: 54 exams / 4,640 questions copied unchanged (`tool/sync_assets.sh`), repository + state are line-by-line
  ports of the web (stats, streak, daily quiz PRNG, weak topics…).
- Entry points: `HighApp` (standalone), `HighScreen` (embeddable), `High.init()`.

**Design reference**: `/workspace/high/design/reference.html` = the Warsay Prep web preview + High's 3D clay layer
(`design/clay3d.css`, `tool/build_reference.py`). Web shots: `tool/shoot_web.py` (fixed clock, 390×844 @2x);
Flutter shots: `test/screenshots_test.dart` (same clock + the web-generated progress seed); side-by-side:
`tool/compose_compare.py` → `compare/<scene>.png`.

| scene | mean px diff (light / dark) |
|---|---|
| home_fresh | 4.96 / 5.43 |
| home | 4.84 / 5.26 |
| home_mid | 3.86 / 4.01 |
| home_end | 5.16 / 5.36 |
| exams | 4.52 / 4.57 |
| exams_list | 4.46 / 4.80 |
| exams_rows | 4.34 / 4.20 |
| exams_model | 3.64 / 3.80 |
| settings | 2.72 / 2.59 |

Layout offsets are within ~1 CSS px down each page (`tool/band_shift.py`). Remaining diff = glyph rasterisation
(Chrome rounds glyph advances), blur falloff of shadows, emoji (no emoji font in the test renderer), and the Kokob
float animation phase.

Tests: `flutter analyze` clean; `test/screenshots_test.dart` (18 scenes), `test/m1_flow_test.dart` (onboarding,
nav, category cards, filters, search, settings, embed in a host route + system back).

## M2 — exam player, results, mistakes, stats — next
## M3 — notes + concept map + matric questions per unit — pending (PILOT_READY has appeared)
## M4 — full tests, README, zip — pending

## M2/M3 in progress – snapshot 2026-09-29 12:08 (UTC+3)
Budget is nearly spent; this section says exactly where things stand so anyone can continue.

Done since M1 (code present, not yet compiled together):
- `tool/build_symbols.py` -> `assets/high/fonts/HighSymbols-{Noto,DejaVu,Math}.ttf` (families HighSymbols/2/3, registered in
  pubspec); `ts()` uses them as `fontFamilyFallback` (Greek, arrows incl. ⇌, super/subscripts, math operators …).
- `HighState.dailyQuiz()` now returns the stored map (daily results persist).
- Notes renderer ported from Junior: `tool/port_junior_notes.py` copies it into `lib/high/notes/jr/` (Junior folder layout,
  High fonts, High palette, type × 0.82). Hand-written glue: `jr/state/app_state.dart` (AppState backed by HighState.notes),
  `jr/screens/shell.dart` (Shell shim -> HighNav/showSheet), `jr/data/repository.dart` (NotesRepo over
  assets/high/notes/notes/index.json + unit_questions.json, unitMap + card-id index), `jr/data/subjects.dart` (Grade 9-12).
  `jr/screens/unit_page.dart` has new Map and Matric sections. `lib/high/notes/concept_map.dart` = pannable concept map.
- `theme/deco.dart`: exam-player decorations (opt states, verdict, palette keys, chat bubbles …).

Still to do (in order):
1. app.dart: HighTab {home, notes, exercise, matric, tutor}; nav Home/Notes/Exercise/Matric/Tutor; Settings pushed from the
   avatar; Mistakes pushed from a Home card; `showSheet(..., bare: true)` for Junior sheets; put `AppScope(AppState(high, notesRepo))`
   above the shell; `NoNav` mixin in widgets/page.dart and used by UnitPage (`with NoNavPage` -> High NoNav).
2. High.init(): also `NotesRepo().init()`.
3. routes.dart: `Routes.unitQuestionIds(ctx, unitId)` (unit_questions.json ids present in ExamRepo) and `UnitMatricCard`
   (button -> quiz page with those ids, kind 'unit').
4. Exam player (lib/high/exam/): question card (MCQ/written/subparts/marking points/passages/stem+answer tables/figures),
   matching card, practice page, quiz page, timed setup/run/score, subject page, Mistakes page, weak topics, tutor (BM25 as in
   reference.html lines 1620-1690). Web behaviour notes are in this file's M1 section and design/reference.html.
5. Home: 2x2 grade tiles (Grade 9-12) under the greeting -> GradePage (subjects -> units -> UnitPage; practice questions per unit).
6. Exercise tab: `HighExerciseSource` extension point (default empty -> "Exercises coming soon"), README section.
7. `flutter analyze`, README, zip (`python3 tool/zip_project.py`).

## Snapshot 2026-09-29 12:20 (UTC+3) — minimum path done, compiles, smoke-tested
`flutter analyze`: no issues. `test/m2_smoke_test.dart` (tabs, grade tiles → Grade page, notes subject + unit page,
practice, quiz, mistakes, weak, exam subject page, exercise empty state, tutor question) and `test/notes_parse_test.dart`
(all 29 books parse) pass. Old M1 tests had only HighTab renames; not re-run (budget).

Works:
- Nav Home / Notes / Exercise / Matric / Tutor; Settings from the avatar; Mistakes card on Home + buttons on Matric.
- Home 2×2 Grade 9–12 tiles (number, subject count, progress) → `GradePage` (screens/notes_home.dart).
- Notes tab (grade chips → subject → units → UnitPage with lessons/games/quiz/concept map/matric questions).
  Junior JSON helpers made lenient (missing objects/lists/strings default; string lists joined) for High content.
- Exam player `lib/high/exam/`: cards.dart (all question types) + pages.dart (PracticePage with filters and focus,
  QuizPage with result card, ExamSubjectPage, MistakesPage, WeakPage, UnitMatricCard). routes.dart wired to them.
- Tutor tab (screens/tutor.dart): BM25 (k1 1.4, b .72), web tokenizer/synonyms/refusal thresholds, question links, quiz.
- Exercise extension point: `exercise/source.dart` + screens/exercise.dart; README "Plugging in exercises".

Left / next steps:
1. Timed exam mode (setup / run / score) — not built; Practice covers all questions.
2. No new compare screenshots (skipped for budget); M1 ones in `compare/`. Visual QA of the new screens vs the web.
3. Re-run and update `test/m1_flow_test.dart`, `test/screenshots_test.dart` for the new nav (Settings/Mistakes are
   pushed pages now, not tabs).
4. Stats page beyond Home widgets; tutor subject filter chips; curated suggestions per subject.

## Exercise bank — 2026-09-29 12:52 (UTC+3)
- `tools/clean_exercises.py`: 22 raw files / 9,585 MCQs in `/workspace/exercises_src` → **4956 kept**, in
  `assets/high/exercises/` (19 grade+subject files + index.json, about 2 MB). Keys were re-verified against the explanations, and
  unverifiable/malformed/duplicate items were dropped. Per-file table, drop reasons and unit coverage are in `docs/exercises_report.md`.
- The app loads the bank into `ExamRepo` as one synthetic `isExercise` exam per grade+subject. These exams don't appear on Matric
  and don't touch "recent". The Exercise tab lists Grade → Subject (notes subjects + English) → units + General. A unit opens the
  quiz player with a set of 20. Answers feed stats, Mistakes (a mistake row opens a one-question quiz) and "Retry wrong".
  `HighExercises` extension point kept (see README).
- Tests: `flutter test` all green (27), incl. new `exercises_parse_test.dart` and an exercise flow test in
  `m2_smoke_test.dart`. `m1_flow_test.dart` updated for the new nav. `test/exercise_shots_test.dart` →
  `compare/exercise_units.png`, `compare/exercise_question.png`.
- Next: better unit mapping for math/agriculture (many land in General). The source's unit hints (`-u6-`) use a different
  numbering from the textbooks. Optionally re-run with a manual unit alias table.

## Cross links + navigation — 2026-09-29 13:06 (UTC+3)
- `state/links.dart` `UnitLinks` (lazy, built once from the loaded content, via `HighState.links`) maps each unit to its
  matric ids and exercise ids, each question id to its unit, and each book to its matric ids and exercise count. All
  "Exercises (N)" / "Matric questions (N)" / "Study this unit" counts come from it.
- `Routes.unitNotes / unitExercises / unitMatric / notesBook / exerciseSubject / bookMatric` plus the `UnitLinkBar` widget (screens/routes.dart).
- Where the links appear:
  - Unit page: Exercises + Matric buttons under the title; the Matric section further down is unchanged.
  - Notes and Grade unit rows: Exercises + Matric chips.
  - Grade page subject rows: Notes / Exercises / Matric chips.
  - Exercise unit rows: Read the notes / Matric chips.
  - Quiz results for an exercise or unit-matric set: Read the notes plus the other set.
  - Matric/model explanations: "Study this unit" when the question is mapped.
- Shell (app.dart): visited tabs and every stacked page stay mounted offstage, so state and scroll survive both back and
  tab switches (re-tapping the open tab resets it). `HighNav.open(key, build)` pops back to a page that is already open instead of stacking a copy.
- Unit page jump bar: labels scale down instead of being cut ("M…").
- Tests: new `test/nav_links_test.dart`; `test/exercise_shots_test.dart` also writes `compare/unit_links.png`.
