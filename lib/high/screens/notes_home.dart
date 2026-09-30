// Notes tab: grade chips -> subject chips -> units on the same page.
import 'package:flutter/widgets.dart';

import '../notes/jr/data/repository.dart';
import '../notes/jr/data/subjects.dart';
import '../notes/jr/state/app_state.dart' as jr;
import '../theme/tokens.dart';
import '../widgets/kit.dart';
import '../widgets/page.dart';
import 'routes.dart';

int _grade = 9;
String? _subject;

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
    final repo = Kit.of(context).s.notesRepo;
    final gs = repo.grades;
    if (gs.isNotEmpty && !gs.contains(_grade)) _grade = gs.contains(9) ? 9 : gs.first;
    final all = repo.grade(_grade);
    if (all.isNotEmpty && (_subject == null || !all.any((b) => b.subject == _subject))) {
      _subject = all.first.subject;
    }
    final book = all.where((b) => b.subject == _subject).firstOrNull;
    return PageShell(
      top: TopBar(title: 'Notes', sub: 'Grade $_grade · tap a subject, then a unit'),
      body: ScreenList(
        children: [
          Blk(
            margin: const EdgeInsets.only(top: 6),
            child: Wrap(spacing: 8, runSpacing: 8, children: [
              for (final g in gs)
                ChipX('Grade $g', tone: gradeTone(g), on: g == _grade, onTap: () => setState(() {
                  _grade = g;
                  _subject = null;
                })),
            ]),
          ),
          if (all.isEmpty)
            const EmptyCard(title: 'No notes yet', text: 'Notes for this grade are on the way.')
          else ...[
            SectionLabel('Subjects', n: all.length, icon: 'book'),
            Blk(
              margin: const EdgeInsets.only(top: 8),
              child: Wrap(spacing: 8, runSpacing: 8, children: [
                for (final b in all)
                  ChipX(b.look.key, tone: b.look.tone, on: b.subject == _subject, onTap: () => setState(() => _subject = b.subject)),
              ]),
            ),
            if (book != null) ...[
              SectionLabel('Units', n: book.units.length, icon: 'book'),
              Panel(
                padding: const EdgeInsets.fromLTRB(16, 6, 16, 6),
                child: Column(children: [for (final (i, u) in book.units.indexed) _unitRow(context, book, u, i, practice: true)]),
              ),
            ],
          ],
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
    final b = Kit.of(context).s.notesRepo.byId(bookId)!;
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

class GradePage extends StatefulWidget {
  const GradePage({super.key, required this.grade});
  final int grade;
  @override
  State<GradePage> createState() => _GradePageState();
}

class _GradePageState extends State<GradePage> {
  String? _stream;
  String? _pick;

  @override
  Widget build(BuildContext context) {
    final s = Kit.of(context).s;
    final all = s.notesRepo.grade(widget.grade);
    final split = widget.grade >= 11;
    final books = !split || _stream == null
        ? all
        : all.where((b) => (_stream == 'science' ? kScienceSubjects : kArtSubjects).contains(b.subject)).toList();
    if (books.isNotEmpty && (_pick == null || !books.any((b) => b.id == _pick))) _pick = books.first.id;
    final book = books.where((b) => b.id == _pick).firstOrNull;
    final nq = {for (final b in books) ...?s.links.bookMatric[b.id]}.length;
    return PageShell(
      top: TopBar(
        title: split && _stream != null ? 'Grade ${widget.grade} · ${_stream == 'science' ? 'Science' : 'Art'}' : 'Grade ${widget.grade}',
        sub: split && _stream == null ? 'Choose Science or Art' : '${books.length} subjects · $nq matric questions',
        onBack: () {
          if (split && _stream != null) {
            setState(() {
              _stream = null;
              _pick = null;
            });
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
            Blk(
              margin: const EdgeInsets.only(top: 8),
              child: Wrap(spacing: 8, runSpacing: 8, children: [
                for (final b in books)
                  ChipX(b.look.key, tone: b.look.tone, on: b.id == _pick, onTap: () {
                    if (s.tourStep != null && !s.tourWants('subject')) return;
                    setState(() => _pick = b.id);
                    s.tourAct('subject');
                  }),
              ]),
            ),
            if (book != null) ...[
              SectionLabel('Units', n: book.units.length, icon: 'book'),
              Panel(
                padding: const EdgeInsets.fromLTRB(16, 6, 16, 6),
                child: Column(children: [for (final (i, u) in book.units.indexed) _unitRow(context, book, u, i, practice: true)]),
              ),
            ],
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
