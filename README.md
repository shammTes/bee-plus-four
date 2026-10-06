# High — Grade 9–12 notes + Eritrean matriculation prep (native Flutter module)

Offline, no WebView. Tabs: **Home · Notes · Exercise · Matric · Tutor** (Settings from the avatar on Home, Mistakes from
the Home card or the Matric page).

- **Home**: greeting, 2×2 Grade 9–12 clay tiles (→ Grade page: subjects → units → notes, unit exercises, matric
  questions per unit), matric & notes cards, stats, weekly chart, daily quiz, mistakes, recent, weak topics, tutor.
- **Notes**: 29 textbook note books / 149 units (`assets/high/notes/notes`), rendered by the ported Junior notes stack
  (`lib/high/notes/jr`): lessons, cards, diagrams, games, unit quiz, concept map, and "Matric questions" mapped by
  `assets/high/notes/unit_questions.json`.
- **Matric**: Matriculation + Model exams (`assets/high/exams`), practice player (MCQ, matching, written with model
  answers / marking points, passages, stem/answer tables, figures), quizzes, subject page, mistakes & bookmarks, weak topics.
- **Tutor**: Kokob, an offline BM25 tutor over the exam packs' concepts and questions.

## Run
```
source /opt/sdk/env.sh       # Flutter 3.47.x
python3 tool/split_notes.py # after editing notes: regenerates the committed per-unit files (assets/high/notes/split)
python3 tool/exam_summary.py  # after editing exam packs / topic indexes: regenerates assets/high/exams/summary.json
python3 tool/school_units.py  # after editing school papers: per-unit counts in assets/high/exercises/school/index.json
flutter pub get && flutter run
flutter analyze
flutter test            # ~20 s; test/exercise_shots_test.dart writes compare/exercise_*.png
```
Content refresh: `bash tool/sync_assets.sh [exam_src] [notes_src]` (defaults /workspace/examprep/content,
/workspace/high/content). If new notes books add SVG folders, list each `assets/high/notes/notes/svg/<book>/` in pubspec.

## Performance notes
- **Flat look** (default; Settings → Look → Clay brings the soft 3D look back): clay decorations paint one solid colour,
  a 1px border or one hard offset ledge, no blurred shadows, no `saveLayer` (opacity is a colour veil, `Dim`).
- **No decorative animations**: page enter fades, staggered cards, count-ups and pulsing pins are off (`Perf.animations`).
- **Start-up**: the exam summary + the two exercise indexes + the notes index. Exam packs, exercise sets, notes units,
  unit questions, placements and board codes load later, off the UI thread. All generated files below are committed
  (CI needs no extra step); `flutter test` fails when one is stale, so re-run its script after editing the source and
  after a merge / rebase that touched it. Output is deterministic, so regenerating gives a clean diff.
- **Exam packs** (~19 MB + ~5 MB topic indexes) are not decoded at start-up: `assets/high/exams/summary.json`
  (`tool/exam_summary.py`, ~0.7 MB) holds each exam's header and per question only its id, MCQ / matching / review flags
  and topic ids, plus topic titles. `ExamRepo(lazyExams: true)` builds light question stubs from it, so Home, Matric,
  Mistakes and progress are exact at once; a pack is read the first time one of its questions is shown (practice, quiz,
  mistakes list, homework, presenter; "Opening the questions…" meanwhile), the tutor and the teacher's matric pool read
  them all on first use. A summary that does not match `index.json` is ignored (full load).
  `test/exam_summary_test.dart` compares it with a full load.
- **Notes units** open from `assets/high/notes/split/<unitId>.json` (built by `tool/split_notes.py`, which honours
  `unit_<id>.json` overrides; `--check` fails if they are stale; `test/notes_split_test.dart` checks every unit).
  Without them the app falls back to the full book file.
- **Exercise counts** per unit come from the bank and school-paper `index.json` files (`tool/school_units.py` writes
  the school ones), so unit rows show exact counts before a set is loaded (`test/lazy_load_test.dart`).
- **Rebuilds**: the shell keeps every tab page alive but wraps each in a `PageGate` (`lib/high/state/page_gate.dart`):
  only the visible page rebuilds on a state change; a hidden one rebuilds once when it is shown again.
- **No `IntrinsicHeight`**: equal-height rows (Home hero, grade / subject tiles, game bins, card grids) use
  `EqualHeightRow` (`lib/high/widgets/equal_row.dart`), a two-pass layout without intrinsic measuring.
- **Maths** is laid out once per formula with flutter_math off screen and drawn from a cached picture
  (`lib/high/notes/jr/notes/math_pic.dart`); TeX errors fall back to the live widget.

## Merge into a host app
1. Copy `lib/high/` → `<host>/lib/high/` and `assets/high/` → `<host>/assets/high/`.
2. pubspec: add deps `flutter_svg`, `flutter_math_fork`, `shared_preferences`; copy the `assets:` entries (all
   `assets/high/...` lines) and the `fonts:` families `HighNunito`, `HighSymbols`, `HighSymbols2`, `HighSymbols3`.
3. Open it:
   ```dart
   import 'package:<host>/high/high.dart';
   await High.init();   // optional pre-warm
   Navigator.push(context, PageRouteBuilder(pageBuilder: (_, _, _) => const HighScreen()));
   ```
   Saved progress lives in SharedPreferences key `high:v1`.

## Plugging in exercises (Exercise tab)
The Exercise tab is a Grade → Subject → Unit browser (subjects from the notes index plus bank-only subjects such as
English; each subject ends with a "General" row for questions without a confident unit). Two item sources feed it:

### 1. Bundled bank (`assets/high/exercises`)
Built from raw MCQ dumps by `python3 tools/clean_exercises.py [src_dir] [notes_dir]` (defaults `/workspace/exercises_src`,
`/workspace/high/content/notes`). The script strips `A) ` labels and `[G9 MATH U4]` prefixes, re-verifies every answer key
against its explanation (drops what it cannot verify, except in the trusted files), removes malformed and duplicate items,
maps each question to a notes unit, and writes `<subject>_<grade>.json` + `index.json` + `docs/exercises_report.md`.

File shape: `{"subject": "biology", "grade": 9, "questions": [{"id": "biology_9_practice_g9_biology_1", "unit": "bio9-u1" | null,
"prompt": "…", "options": ["…", "…", "…", "…"], "answer": 1, "explanation": "…", "verified": "explanation" | "trusted",
"src": "practice_g9_biology#12"}]}`; `index.json` has `grades.<g>.<subject> = {file, count, units: {unitId|general: n}}`.

`ExamRepo` turns the bank into one synthetic exam per grade+subject (`Exam.isExercise`, not listed on Matric). In the app
(`ExamRepo(lazyExercises: true)`) only the two `index.json` files are read at start-up; a grade+subject's files (bank +
school papers) are read and decoded in a background isolate, once, when that subject is opened in the Exercise tab, a
unit's exercises are asked for, or saved progress (mistakes, bookmarks, homework, daily quiz) refers to its questions.
Counts shown before that come from `index.json`, so keep `count` / `units` there in step with the files.
Tapping a unit opens the standard quiz player with a set of 20 (unanswered first, then wrong), so answers count in stats,
Mistakes and "Retry wrong". To add more, drop new raw files in the source folder and re-run the script (add a file stem
to `TRUSTED` only if its keys are known good); new grades/subjects need no code changes.

### 2. Host-provided source (`lib/high/exercise/source.dart`, exported by `high.dart`)
```dart
class MyExercises extends HighExerciseSource {
  @override
  Future<List<HighExercise>> exercisesFor({required int grade, required String subject, required String unitId}) async {
    final raw = jsonDecode(await rootBundle.loadString('assets/my_ex/$unitId.json')) as List;
    return [for (final j in raw) HighExercise.fromJson(j as Map<String, dynamic>)];
  }
  @override
  int? countFor({required int grade, required String subject, required String unitId}) => null; // optional badge
}

void main() {
  HighExercises.register(MyExercises());   // register once, before opening HighScreen
  runApp(...);
}
```
- `grade`: 9–12; `subject`: notes subject key (`biology`, `chemistry`, `physics`, `mathematics`, `agriculture`,
  `geography`, `history`, `business_economics`, `english`); `unitId`: unit id from `assets/high/notes/notes/index.json`
  (e.g. `bio9-u1`) or `general`.
- Item JSON for `HighExercise.fromJson`:
  `{"id": "x1", "prompt": "Text, $inline TeX$ ok", "options": {"A": "…", "B": "…"}, "answer": "A", "explanation": "…", "extra": {}}`
  (omit `options` for a written item; `answer` is then the model answer shown on "Show answer").
- Override `buildUnit(context, grade:, subject:, unitId:)` to return your own widget for a unit.
- With a host source registered, a unit opens a page with a "Practise N bundled questions" button followed by the host
  items; with none registered (default `EmptyExerciseSource`) bundled units open the quiz directly and units with nothing
  show "Exercises coming soon".
