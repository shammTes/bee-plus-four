// Navigation helpers shared by screens (web: go(), resume(), topicQuiz()...).
import 'package:flutter/widgets.dart';

import '../state/app_state.dart';
import '../theme/tokens.dart';
import '../widgets/art.dart';
import '../widgets/kit.dart';
import '../widgets/page.dart';
import '../data/repository.dart' show exerciseSubjectLabel;
import '../exam/pages.dart';
import '../notes/jr/screens/unit_page.dart';
import 'exercise.dart';
import 'notes_home.dart';
export '../exam/pages.dart' show UnitMatricCard, MistakesPage, QuizPage, PracticePage;

abstract final class Routes {
  static HighState _s(BuildContext c) => HighScope.read(c);

  static void examsTab(BuildContext c) => HighNav.of(c).tab(HighTab.matric);

  /// web #cta: resume the most recent exam, else the library
  static void continueStudying(BuildContext c) {
    final s = _s(c);
    final r = s.recent.where((x) => s.repo.exam.containsKey(x['id'])).firstOrNull;
    if (r != null) {
      resume(c, r['id'] as String);
    } else {
      examsTab(c);
    }
  }

  /// open an exam in practice mode focused on the first unanswered scored question
  static void resume(BuildContext c, String examId) {
    final s = _s(c), e = s.repo.exam[examId];
    if (e == null) return;
    s.touchRecent(examId);
    final f = e.scored.where((q) => !s.answered(q.id)).firstOrNull;
    HighNav.of(c).push(PracticePage(examId: examId, focus: f?.id));
  }

  static Future<void> dailyQuiz(BuildContext c) async {
    final s = _s(c), d = s.dailyQuiz();
    d['res'] ??= <String, dynamic>{};
    // today's quiz may hold exercise questions whose set is not read in yet
    await s.needQuestions([for (final x in d['ids'] as List) '$x']);
    if (!c.mounted) return;
    HighNav.of(c).push(QuizPage(ids: [for (final x in d['ids'] as List) x as String], title: 'Daily Quiz', sub: '10 questions · mixed subjects', kind: 'daily'));
  }

  static void topicQuiz(BuildContext c, String subject, String topic) {
    final s = _s(c);
    final ids = (s.repo.topicQs['$subject|$topic'] ?? const <String>[]).where((id) => s.repo.byId[id]?.isScored ?? false).toList();
    int rank(String id) => !s.answered(id) ? 0 : (s.ansOk(id) ? 2 : 1);
    ids.sort((a, b) => rank(a) - rank(b));
    HighNav.of(c).push(QuizPage(ids: ids.take(10).toList(), title: s.repo.topicTitle(subject, topic), sub: '$subject · topic quiz'));
  }

  static void weak(BuildContext c) => HighNav.of(c).push(const WeakPage());
  static void mistakes(BuildContext c) => HighNav.of(c).push(const MistakesPage());
  static void tutor(BuildContext c) => HighNav.of(c).tab(HighTab.tutor);
  static void subject(BuildContext c, String subject, {String? year, String? cat}) => HighNav.of(c).push(ExamSubjectPage(subject: subject, cat: cat));

  /// matric questions mapped to a notes unit (unit_questions.json), auto-marked first — from the shared link index
  static List<String> unitQuestionIds(BuildContext c, String unitId) => _s(c).links.matricFor(unitId);

  // ---------------------------------------------------------------- cross links (deduped: an open page is popped back to)
  static void unitNotes(BuildContext c, String unitId, {String? section}) {
    final u = _s(c).notesRepo.unitById(unitId);
    if (u == null) return;
    HighNav.of(c).open('unit:$unitId', () => UnitPage(bookId: u.book.id, unitId: unitId, section: section));
  }

  static void unitExercises(BuildContext c, String unitId) {
    final u = _s(c).notesRepo.unitById(unitId);
    if (u == null) return;
    openExercises(c, grade: u.book.grade, subject: u.book.subject, unitId: unitId, title: 'Unit ${u.unit.number} · ${u.unit.title}');
  }

  static void unitMatric(BuildContext c, String unitId) {
    final s = _s(c), u = s.notesRepo.unitById(unitId), ids = s.links.matricFor(unitId);
    if (u == null || ids.isEmpty) return;
    HighNav.of(c).open('matric:$unitId', () => QuizPage(ids: ids, title: 'Matric questions', sub: 'Unit ${u.unit.number} · ${u.unit.title}', kind: 'unit', unitId: unitId));
  }

  static void notesBook(BuildContext c, String bookId) => HighNav.of(c).open('book:$bookId', () => NotesSubjectPage(bookId: bookId));
  static void exerciseSubject(BuildContext c, int grade, String subject) =>
      HighNav.of(c).open('exsub:$grade|$subject', () => ExerciseSubjectPage(grade: grade, subject: subject));

  /// matric for a notes subject: the exam subject page when the packs have that subject, else a quiz of the mapped questions
  static void bookMatric(BuildContext c, String bookId) {
    final s = _s(c), b = s.notesRepo.byId(bookId);
    if (b == null) return;
    final label = exerciseSubjectLabel(b.subject);
    if (s.repo.subjects.contains(label)) {
      HighNav.of(c).open('exam-subject:$label', () => ExamSubjectPage(subject: label));
    } else {
      final ids = s.links.bookMatric[bookId] ?? const [];
      if (ids.isNotEmpty) HighNav.of(c).open('bookmatric:$bookId', () => QuizPage(ids: ids.take(20).toList(), title: 'Matric questions', sub: b.title, kind: 'unit'));
    }
  }
}

/// "Exercises (N)" + "Matric questions (N)" (+ optional "Read the notes") clay buttons for one notes unit.
/// Buttons with nothing behind them are hidden.
class UnitLinkBar extends StatelessWidget {
  const UnitLinkBar({super.key, required this.unitId, this.notes = false, this.exercises = true, this.matric = true, this.small = false});
  final String unitId;
  final bool notes, exercises, matric, small;
  @override
  Widget build(BuildContext context) {
    final s = Kit.of(context).s, l = s.links;
    final ne = l.exerciseCountFor(unitId), nm = l.matricFor(unitId).length;
    final items = <(String, String, BtnKind, VoidCallback)>[
      if (notes) ('Read the notes', 'book', BtnKind.soft, () => Routes.unitNotes(context, unitId)),
      if (exercises && ne > 0) ('Exercises ($ne)', 'pen', BtnKind.tone, () => Routes.unitExercises(context, unitId)),
      if (matric && nm > 0) ('Matric questions ($nm)', 'trophy', BtnKind.soft, () => Routes.unitMatric(context, unitId)),
    ];
    if (items.isEmpty) return const SizedBox.shrink();
    if (small) {
      return Wrap(spacing: 8, runSpacing: 8, children: [for (final x in items) ChipX(x.$1, small: true, icon: x.$2, tone: x.$3 == BtnKind.tone ? 'blue' : null, onTap: x.$4)]);
    }
    Widget btn((String, String, BtnKind, VoidCallback) x) =>
        Btn(x.$1, icon: x.$2, kind: x.$3, tone: 'blue', block: true, fontSize: 13.5, padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 12), onTap: x.$4);
    return Column(crossAxisAlignment: CrossAxisAlignment.stretch, spacing: 10, children: [for (final x in items) btn(x)]);
  }
}

/// `.card.empty` with the sprout illustration
class EmptyCard extends StatelessWidget implements Spaced {
  const EmptyCard({super.key, required this.title, required this.text, this.art = 'sprout'});
  final String title, text, art;
  @override
  EdgeInsets get blockMargin => const EdgeInsets.symmetric(vertical: 14);
  @override
  Widget build(BuildContext context) {
    final p = Kit.of(context).p;
    return Panel(
      margin: bareM(context, this, blockMargin),
      padding: const EdgeInsets.fromLTRB(22, 26, 22, 22),
      child: Column(
        children: [
          Padding(padding: const EdgeInsets.only(bottom: 6), child: Art(art, palette: p, width: 130)),
          Padding(padding: const EdgeInsets.only(bottom: 4), child: Text(title, textAlign: TextAlign.center, style: ts(17, w900, p.ink))),
          Text(text, textAlign: TextAlign.center, style: ts(14, w700, p.ink2)),
        ],
      ),
    );
  }
}
