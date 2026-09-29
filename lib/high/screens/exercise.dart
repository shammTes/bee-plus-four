// Exercise tab: Grade -> Subject -> Unit browser.
// Items: the bundled, answer-verified MCQ bank (assets/high/exercises, built by tools/clean_exercises.py; opened in the
// quiz player so answers feed Mistakes / "Retry wrong") plus anything a host registers via HighExercises (source.dart).
import 'package:flutter/widgets.dart';

import '../widgets/art.dart' show Ic;
import '../exam/cards.dart' show Tag;
import '../exercise/source.dart';
import '../notes/jr/data/repository.dart';
import '../notes/jr/data/subjects.dart';
import '../state/app_state.dart';
import '../theme/tokens.dart';
import '../widgets/kit.dart';
import '../widgets/page.dart';
import '../widgets/rich.dart';
import 'routes.dart';
import '../teacher/teacher.dart' show ClassCodeCard;

int _g = 9;
const kExerciseSet = 20;

bool get _pluginEmpty => HighExercises.source is EmptyExerciseSource;

/// subjects of a grade: notes books plus bank-only subjects (e.g. English)
List<({String subject, IndexBook? book})> exerciseSubjects(HighState s, int g) {
  final books = s.notesRepo.grade(g);
  final extra = s.repo.exerciseExams.keys.where((k) => k.startsWith('$g|')).map((k) => k.substring(k.indexOf('|') + 1)).where((sj) => !books.any((b) => b.subject == sj));
  return [for (final b in books) (subject: b.subject, book: b), for (final sj in extra) (subject: sj, book: null)];
}

int exerciseCount(HighState s, int g, String subject) => s.repo.exerciseExams['$g|$subject']?.questions.length ?? 0;

/// open a unit: bank only -> quiz of the next [kExerciseSet] questions (unanswered, then wrong, then right)
void openExercises(BuildContext c, {required int grade, required String subject, String? unitId, required String title}) {
  final s = HighScope.read(c);
  final ids = [...s.repo.exerciseIds(grade: grade, subject: subject, unitId: unitId)];
  if (ids.isNotEmpty && _pluginEmpty) {
    int rank(String id) => !s.answered(id) ? 0 : (s.ansOk(id) ? 2 : 1);
    ids.sort((a, b) => rank(a) - rank(b));
    final set = ids.take(kExerciseSet).toList();
    HighNav.of(c).open('ex:${unitId ?? 'general|$grade|$subject'}', () => QuizPage(ids: set, title: title, sub: 'Grade $grade · ${set.length} of ${ids.length} exercises', kind: 'exercise', unitId: unitId));
  } else {
    HighNav.of(c).open('ex:${unitId ?? 'general|$grade|$subject'}', () => ExerciseUnitPage(grade: grade, subject: subject, unitId: unitId, title: title));
  }
}

class ExercisePage extends StatefulWidget {
  const ExercisePage({super.key});
  @override
  State<ExercisePage> createState() => _ExercisePageState();
}

class _ExercisePageState extends State<ExercisePage> {
  @override
  Widget build(BuildContext context) {
    final k = Kit.of(context), p = k.p, s = k.s;
    final gs = {...s.notesRepo.grades, for (final e in s.repo.exerciseExams.keys) int.parse(e.split('|').first)}.toList()..sort();
    if (gs.isNotEmpty && !gs.contains(_g)) _g = gs.first;
    final subs = exerciseSubjects(s, _g);
    final total = subs.fold<int>(0, (a, x) => a + exerciseCount(s, _g, x.subject));
    return PageShell(
      top: const TopBar(title: 'Exercise', sub: 'Practice by grade, subject and unit'),
      body: ScreenList(
        children: [
          Blk(
            margin: const EdgeInsets.only(top: 6),
            child: Wrap(spacing: 8, runSpacing: 8, children: [for (final g in gs) ChipX('Grade $g', tone: gradeTone(g), on: g == _g, onTap: () => setState(() => _g = g))]),
          ),
          const ClassCodeCard(),
          SectionLabel('Grade $_g', n: total > 0 ? '$total questions' : '${subs.length} subjects', icon: 'pen'),
          for (final x in subs)
            () {
              final lk = notesSubject(x.subject), n = exerciseCount(s, _g, x.subject);
              return Panel(
                padding: const EdgeInsets.all(14),
                onTap: () => Routes.exerciseSubject(context, _g, x.subject),
                child: Row(
                  spacing: 12,
                  children: [
                    Badge(lk.tone, 'pen', s: 42),
                    Expanded(
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text(lk.key, style: ts(16, w900, p.ink)),
                          Text([if (x.book != null) '${x.book!.units.length} units', n > 0 ? '$n questions' : 'coming soon'].join(' · '), style: ts(12.5, w700, p.ink3)),
                        ],
                      ),
                    ),
                    Ic('right', size: 20, color: p.ink3),
                  ],
                ),
              );
            }(),
        ],
      ),
    );
  }
}

class ExerciseSubjectPage extends StatelessWidget {
  const ExerciseSubjectPage({super.key, required this.grade, required this.subject});
  final int grade;
  final String subject;
  @override
  Widget build(BuildContext context) {
    final k = Kit.of(context), p = k.p, s = k.s, lk = notesSubject(subject);
    final book = s.notesRepo.grade(grade).where((b) => b.subject == subject).firstOrNull;
    final gen = s.repo.exerciseIds(grade: grade, subject: subject);
    Widget row({required String badge, required String title, required String? unitId, required String openTitle}) {
      final ids = s.repo.exerciseIds(grade: grade, subject: subject, unitId: unitId);
      final extra = HighExercises.source.countFor(grade: grade, subject: subject, unitId: unitId ?? 'general');
      final n = ids.length + (extra ?? 0), done = ids.where(s.answered).length, right = ids.where(s.ansOk).length;
      return Panel(
        padding: const EdgeInsets.all(14),
        onTap: () => openExercises(context, grade: grade, subject: subject, unitId: unitId, title: openTitle),
        child: Row(
          spacing: 12,
          children: [
            Knob(tone: lk.tone, radius: 22, child: Text(badge, style: ts(14, w900, k.tone(lk.tone).deep))),
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.stretch,
                children: [
                  Text(title, maxLines: 2, overflow: TextOverflow.ellipsis, style: ts(14.5, w900, p.ink)),
                  Text(n == 0 ? 'Exercises coming soon' : '$n questions${done > 0 ? ' · $right of $done right' : ''}', style: ts(12, w700, p.ink3)),
                  if (ids.isNotEmpty) Padding(padding: const EdgeInsets.only(top: 6), child: Bar((100 * done / ids.length).round(), tone: lk.tone, height: 6)),
                  if (unitId != null) Padding(padding: const EdgeInsets.only(top: 10), child: UnitLinkBar(unitId: unitId, notes: true, exercises: false, small: true)),
                ],
              ),
            ),
            if (n > 0) Tag('$n', tone: lk.tone),
          ],
        ),
      );
    }

    return PageShell(
      top: TopBar(title: lk.key, sub: 'Grade $grade · exercises', onBack: HighNav.of(context).back, tab: false),
      body: ScreenList(
        children: [
          if (book != null)
            for (final u in book.units) row(badge: '${u.number}', title: u.title, unitId: u.id, openTitle: 'Unit ${u.number} · ${u.title}'),
          if (gen.isNotEmpty || book == null) row(badge: '★', title: 'General', unitId: null, openTitle: '${lk.key} · General'),
        ],
      ),
    );
  }
}

/// unit page used when a host source is registered (or the bank has nothing): bundled set button + host items
class ExerciseUnitPage extends StatefulWidget {
  const ExerciseUnitPage({super.key, required this.grade, required this.subject, required this.unitId, required this.title});
  final int grade;
  final String subject, title;

  /// null = the subject's "General" bucket
  final String? unitId;
  @override
  State<ExerciseUnitPage> createState() => _ExerciseUnitPageState();
}

class _ExerciseUnitPageState extends State<ExerciseUnitPage> {
  late final Future<List<HighExercise>> _f = HighExercises.source.exercisesFor(grade: widget.grade, subject: widget.subject, unitId: widget.unitId ?? 'general');
  final _picked = <String, String>{};
  @override
  Widget build(BuildContext context) {
    final w = widget, s = Kit.of(context).s;
    final bank = s.repo.exerciseIds(grade: w.grade, subject: w.subject, unitId: w.unitId);
    final custom = HighExercises.source.buildUnit(context, grade: w.grade, subject: w.subject, unitId: w.unitId ?? 'general');
    final top = TopBar(title: 'Exercises', sub: w.title, onBack: HighNav.of(context).back, tab: false);
    if (custom != null) return PageShell(top: top, body: custom);
    return PageShell(
      top: top,
      body: FutureBuilder<List<HighExercise>>(
        future: _f,
        builder: (c, snap) {
          final l = snap.data;
          if (l == null) return const SizedBox.shrink();
          return ScreenList(
            children: [
              if (bank.isNotEmpty)
                Blk(
                  margin: const EdgeInsets.only(top: 8),
                  child: Btn('Practise ${bank.length} bundled questions', icon: 'play', block: true, onTap: () {
                    HighNav.of(c).push(QuizPage(ids: bank.take(kExerciseSet).toList(), title: w.title, sub: 'Grade ${w.grade} · exercises', kind: 'exercise'));
                  }),
                ),
              if (l.isEmpty && bank.isEmpty) const EmptyCard(title: 'Exercises coming soon', text: 'Practice for this unit is on its way. Meanwhile, try the unit quiz in Notes.', art: 'kokob'),
              for (final (i, e) in l.indexed) _item(c, e, i),
            ],
          );
        },
      ),
    );
  }

  Widget _item(BuildContext c, HighExercise e, int i) {
    final k = Kit.of(c), p = k.p, pick = _picked[e.id];
    return Panel(
      padding: const EdgeInsets.all(14),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        spacing: 8,
        children: [
          RichTx('${i + 1}. ${e.prompt}', style: ts(15, w800, p.ink, height: 1.45)),
          if (e.options != null)
            for (final o in e.options!.entries)
              Press(
                onTap: pick != null ? null : () => setState(() => _picked[e.id] = o.key),
                child: Container(
                  padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 10),
                  decoration: k.d.raised(pick == null ? p.surface2 : (o.key == e.answer ? k.tone('sage').tile : (o.key == pick ? k.tone('peach').tile : p.surface2)), radius: 14),
                  child: RichTx('${o.key}. ${o.value}', style: ts(14, w700, p.ink)),
                ),
              )
          else if (pick == null)
            Btn('Show answer', kind: BtnKind.soft, onTap: () => setState(() => _picked[e.id] = '')),
          if (pick != null && e.options == null) RichTx(e.answer, style: ts(14, w700, p.ink)),
          if (pick != null && e.explanation != null) RichTx(e.explanation!, style: ts(13.5, w600, p.ink2)),
        ],
      ),
    );
  }
}
