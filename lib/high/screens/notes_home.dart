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
  String? _stream;
  @override
  Widget build(BuildContext context) {
    final s = Kit.of(context).s, repo = s.notesRepo, a = jr.AppScope.of(context);
    final gs = repo.grades;
    if (gs.isNotEmpty && !gs.contains(_grade)) _grade = gs.last;
    final split = _grade >= 11;
    final all = repo.grade(_grade);
    final books = !split || _stream == null ? all : all.where((b) => (_stream == 'science' ? kScienceSubjects : kArtSubjects).contains(b.subject)).toList();
    return PageShell(
      top: TopBar(title: 'Notes', sub: split && _stream == null ? 'Grade $_grade · choose Science or Art' : 'Grade $_grade · ${books.length} subjects'),
      body: ScreenList(
        children: [
          Blk(
            margin: const EdgeInsets.only(top: 6),
            child: Wrap(spacing: 8, runSpacing: 8, children: [
              for (final g in gs)
                ChipX('Grade $g', tone: gradeTone(g), on: g == _grade, onTap: () => setState(() {
                  _grade = g;
                  _stream = null;
                })),
            ]),
          ),
          if (split && _stream == null) ...[
            _StreamCard(title: 'Science', ti: 'ሳይንስ', sub: 'Mathematics, Physics, Chemistry, Biology, Agriculture', tone: 'mint', onTap: () => setState(() => _stream = 'science')),
            _StreamCard(title: 'Art', ti: 'ኪነት', sub: 'Mathematics, History, Geography, Business, Agriculture', tone: 'butter', onTap: () => setState(() => _stream = 'art')),
          ] else ...[
            SectionLabel(split ? (_stream == 'science' ? 'Science' : 'Art') : 'Grade $_grade subjects', n: books.length, icon: 'book'),
            for (final b in books) BookTile(book: b, pct: bookPct(a, b)),
          ],
          if (!split && books.isEmpty) const EmptyCard(title: 'No notes yet', text: 'Notes for this grade are on the way.'),
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

/// opened from the Grade tiles on Home: subjects first. Grades 11 and 12 pick Science or Art.
class GradePage extends StatefulWidget {
  const GradePage({super.key, required this.grade});
  final int grade;
  @override
  State<GradePage> createState() => _GradePageState();
}

class _GradePageState extends State<GradePage> {
  String? _stream;

  @override
  Widget build(BuildContext context) {
    final k = Kit.of(context), p = k.p, s = k.s, a = jr.AppScope.of(context);
    final all = s.notesRepo.grade(widget.grade);
    final split = widget.grade >= 11;
    final books = !split || _stream == null
        ? all
        : all.where((b) => (_stream == 'science' ? kScienceSubjects : kArtSubjects).contains(b.subject)).toList();
    final nq = {for (final b in books) ...?s.links.bookMatric[b.id]}.length;
    return PageShell(
      top: TopBar(
        title: split && _stream != null ? 'Grade ${widget.grade} · ${_stream == 'science' ? 'Science' : 'Art'}' : 'Grade ${widget.grade}',
        sub: split && _stream == null ? 'Choose Science or Art' : '${books.length} subjects · $nq matric questions',
        onBack: () {
          if (split && _stream != null) {
            setState(() => _stream = null);
          } else {
            HighNav.of(context).back();
          }
        },
        tab: false,
      ),
      body: ScreenList(
        children: [
          if (split && _stream == null) ...[
            _StreamCard(title: 'Science', ti: 'ሳይንስ', sub: 'Mathematics, Physics, Chemistry, Biology, Agriculture', tone: 'mint', onTap: () => setState(() => _stream = 'science')),
            _StreamCard(title: 'Art', ti: 'ኪነት', sub: 'Mathematics, History, Geography, Business, Agriculture', tone: 'butter', onTap: () => setState(() => _stream = 'art')),
          ] else ...[
            Panel(
              tone: gradeTone(widget.grade),
              padding: const EdgeInsets.all(18),
              child: Row(
                spacing: 14,
                children: [
                  Text('${widget.grade}', style: ts(52, w900, k.tone(gradeTone(widget.grade)).deep, height: 1)),
                  Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.stretch,
                      children: [
                        Text(split ? (_stream == 'science' ? 'Science' : 'Art') : 'Grade ${widget.grade}', style: ts(20, w900, p.ink)),
                        Text('Pick a subject', style: ts(13, w700, p.ink2)),
                        Padding(padding: const EdgeInsets.only(top: 10), child: Bar(gradePct(a, books), tone: gradeTone(widget.grade), onTile: true)),
                      ],
                    ),
                  ),
                ],
              ),
            ),
            for (final b in books)
              Panel(
                margin: const EdgeInsets.only(bottom: 10),
                padding: const EdgeInsets.all(14),
                onTap: () {
                  if (s.tourStep != null && !s.tourWants('subject')) return;
                  Routes.notesBook(context, b.id);
                  s.tourAct('subject');
                },
                child: Row(
                  spacing: 12,
                  children: [
                    Badge(b.look.tone, 'book', s: 46),
                    Expanded(
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text(b.look.key, style: ts(17, w900, p.ink)),
                          Text('${b.units.length} units', style: ts(12.5, w700, p.ink3)),
                        ],
                      ),
                    ),
                  ],
                ),
              ),
            if (books.isEmpty) const EmptyCard(title: 'No notes yet', text: 'Notes for this grade are on the way.'),
          ],
        ],
      ),
    );
  }
}

class _StreamCard extends StatelessWidget {
  const _StreamCard({required this.title, required this.ti, required this.sub, required this.tone, required this.onTap});
  final String title, ti, sub, tone;
  final VoidCallback onTap;
  @override
  Widget build(BuildContext context) {
    final k = Kit.of(context), p = k.p;
    return Panel(
      tone: tone,
      margin: const EdgeInsets.only(bottom: 12),
      padding: const EdgeInsets.all(18),
      onTap: onTap,
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(title, style: ts(26, w900, k.tone(tone).deep)),
          Text(ti, style: const TextStyle(fontFamily: 'HighGeez', fontSize: 16, fontWeight: FontWeight.w700, color: Color(0xFF5C4A3A), height: 1.4)),
          const SizedBox(height: 6),
          Text(sub, style: ts(13, w700, p.ink2)),
        ],
      ),
    );
  }
}
