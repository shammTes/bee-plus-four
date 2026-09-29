// Notes tab: grade chips -> subjects -> units (textbook notes for Grade 9–12), plus the Grade page opened from Home's
// grade tiles (subjects -> units with notes + practice questions mapped from matric exams).
import 'package:flutter/widgets.dart';

import '../notes/jr/data/repository.dart';
import '../notes/jr/data/subjects.dart';
import '../notes/jr/state/app_state.dart' as jr;
import '../theme/tokens.dart';
import '../widgets/kit.dart';
import '../widgets/page.dart';
import 'routes.dart';

int _grade = 12;

int bookPct(jr.AppState a, IndexBook b) => b.units.isEmpty ? 0 : (b.units.fold<int>(0, (x, u) => x + a.unitPctIdx(u)) / b.units.length).round();
int gradePct(jr.AppState a, List<IndexBook> l) => l.isEmpty ? 0 : (l.fold<int>(0, (x, b) => x + bookPct(a, b)) / l.length).round();

class NotesHomePage extends StatefulWidget {
  const NotesHomePage({super.key});
  @override
  State<NotesHomePage> createState() => _NotesHomePageState();
}

class _NotesHomePageState extends State<NotesHomePage> {
  @override
  Widget build(BuildContext context) {
    final s = Kit.of(context).s, repo = s.notesRepo, a = jr.AppScope.of(context);
    final gs = repo.grades;
    if (gs.isNotEmpty && !gs.contains(_grade)) _grade = gs.last;
    final books = repo.grade(_grade);
    return PageShell(
      top: TopBar(title: 'Notes', sub: 'Grade 9–12 · ${repo.books.length} books · ${repo.totalUnits} units'),
      body: ScreenList(
        children: [
          Blk(
            margin: const EdgeInsets.only(top: 6),
            child: Wrap(spacing: 8, runSpacing: 8, children: [for (final g in gs) ChipX('Grade $g', tone: gradeTone(g), on: g == _grade, onTap: () => setState(() => _grade = g))]),
          ),
          SectionLabel('Grade $_grade subjects', n: books.length, icon: 'book'),
          for (final b in books) BookTile(book: b, pct: bookPct(a, b)),
          if (books.isEmpty) const EmptyCard(title: 'No notes yet', text: 'Notes for this grade are on the way.'),
        ],
      ),
    );
  }
}

class BookTile extends StatelessWidget {
  const BookTile({super.key, required this.book, required this.pct});
  final IndexBook book;
  final int pct;
  @override
  Widget build(BuildContext context) {
    final p = Kit.of(context).p, lk = book.look;
    return Panel(
      padding: const EdgeInsets.all(14),
      onTap: () => Routes.notesBook(context, book.id),
      child: Row(
        spacing: 12,
        children: [
          Badge(lk.tone, 'book', s: 44),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: [
                Text(lk.key, style: ts(16, w900, p.ink)),
                Text('Grade ${book.grade} · ${book.units.length} units · $pct%', style: ts(12.5, w700, p.ink3)),
                Padding(padding: const EdgeInsets.only(top: 6), child: Bar(pct, tone: lk.tone, height: 7)),
              ],
            ),
          ),
        ],
      ),
    );
  }
}

Widget _unitRow(BuildContext context, IndexBook b, IndexUnit u, int i, {bool practice = false}) {
  final k = Kit.of(context), p = k.p, a = jr.AppScope.of(context), pct = a.unitPctIdx(u), tone = b.look.tone;
  return Container(
    decoration: i == 0 ? null : BoxDecoration(border: Border(top: BorderSide(color: p.line))),
    padding: const EdgeInsets.symmetric(vertical: 10),
    child: Column(
      crossAxisAlignment: CrossAxisAlignment.stretch,
      children: [
        Press(
          onTap: () => Routes.unitNotes(context, u.id),
          child: Row(
            spacing: 12,
            children: [
              Knob(tone: tone, radius: 22, child: Text('${u.number}', style: ts(14, w900, k.tone(tone).deep))),
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.stretch,
                  children: [
                    Text(u.title, maxLines: 2, overflow: TextOverflow.ellipsis, style: ts(14.5, w900, p.ink)),
                    Text('${u.topics.length} topics · $pct% done', style: ts(12, w700, p.ink3)),
                    Padding(padding: const EdgeInsets.only(top: 6), child: Bar(pct, tone: tone, height: 6)),
                  ],
                ),
              ),
            ],
          ),
        ),
        if (practice) Padding(padding: const EdgeInsets.only(top: 8, left: 56), child: UnitLinkBar(unitId: u.id, small: true)),
      ],
    ),
  );
}

class NotesSubjectPage extends StatelessWidget {
  const NotesSubjectPage({super.key, required this.bookId});
  final String bookId;
  @override
  Widget build(BuildContext context) {
    final s = Kit.of(context).s, b = s.notesRepo.byId(bookId)!;
    return PageShell(
      top: TopBar(title: b.look.key, sub: 'Grade ${b.grade} · ${b.units.length} units', onBack: HighNav.of(context).back, tab: false),
      body: ScreenList(
        children: [
          SectionLabel('Units', n: b.units.length, icon: 'book'),
          Panel(padding: const EdgeInsets.fromLTRB(16, 6, 16, 6), child: Column(children: [for (final (i, u) in b.units.indexed) _unitRow(context, b, u, i, practice: true)])),
        ],
      ),
    );
  }
}

/// opened from the Grade tiles on Home: every subject of the grade with its units, notes and practice
class GradePage extends StatelessWidget {
  const GradePage({super.key, required this.grade});
  final int grade;
  @override
  Widget build(BuildContext context) {
    final k = Kit.of(context), p = k.p, s = k.s, a = jr.AppScope.of(context), books = s.notesRepo.grade(grade);
    final nq = {for (final b in books) ...?s.links.bookMatric[b.id]}.length;
    return PageShell(
      top: TopBar(title: 'Grade $grade', sub: '${books.length} subjects · $nq matric questions', onBack: HighNav.of(context).back, tab: false),
      body: ScreenList(
        children: [
          Panel(
            tone: gradeTone(grade),
            padding: const EdgeInsets.all(18),
            child: Row(
              spacing: 14,
              children: [
                Text('$grade', style: ts(52, w900, k.tone(gradeTone(grade)).deep, height: 1)),
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.stretch,
                    children: [
                      Text('Grade $grade', style: ts(20, w900, p.ink)),
                      Text('Notes, unit exercises and matric questions', style: ts(13, w700, p.ink2)),
                      Padding(padding: const EdgeInsets.only(top: 10), child: Bar(gradePct(a, books), tone: gradeTone(grade), onTile: true)),
                    ],
                  ),
                ),
              ],
            ),
          ),
          for (final b in books) ...[
            SectionLabel(b.look.key, n: '${b.units.length} units', icon: 'book'),
            Blk(
              margin: const EdgeInsets.only(top: 8),
              child: Wrap(
                spacing: 8,
                runSpacing: 8,
                children: [
                  ChipX('Notes', small: true, icon: 'book', tone: b.look.tone, onTap: () => Routes.notesBook(context, b.id)),
                  if ((s.links.bookExercises[b.id] ?? 0) > 0) ChipX('Exercises', small: true, icon: 'pen', count: s.links.bookExercises[b.id], onTap: () => Routes.exerciseSubject(context, grade, b.subject)),
                  if ((s.links.bookMatric[b.id] ?? const []).isNotEmpty) ChipX('Matric', small: true, icon: 'trophy', count: s.links.bookMatric[b.id]!.length, onTap: () => Routes.bookMatric(context, b.id)),
                ],
              ),
            ),
            Panel(padding: const EdgeInsets.fromLTRB(16, 6, 16, 6), child: Column(children: [for (final (i, u) in b.units.indexed) _unitRow(context, b, u, i, practice: true)])),
          ],
          if (books.isEmpty) const EmptyCard(title: 'No notes yet', text: 'Notes for this grade are on the way.'),
        ],
      ),
    );
  }
}
