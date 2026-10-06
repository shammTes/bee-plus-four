// Exams library (web renderSubjects): sticky category segment + year chips, category header, search,
// subject tiles, and every exam grouped by subject.
import 'package:flutter/widgets.dart';

import '../data/models.dart';
import '../data/repository.dart';
import '../theme/tokens.dart';
import '../widgets/kit.dart';
import '../widgets/page.dart';
import 'home.dart' show ListRow, Stagger;
import 'routes.dart';

class ExamsPage extends StatefulWidget {
  const ExamsPage({super.key, this.controller});
  final ScrollController? controller;
  @override
  State<ExamsPage> createState() => _ExamsPageState();
}

/// the web keeps `lib = {year, q}` across visits
String? _libYear;
String _libQ = '';

class _ExamsPageState extends State<ExamsPage> {
  late final ScrollController _sc = widget.controller ?? ScrollController();
  late final TextEditingController _q = TextEditingController(text: _libQ);

  @override
  void dispose() {
    if (widget.controller == null) _sc.dispose();
    _q.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final k = Kit.of(context), p = k.p, s = k.s, r = s.repo;
    final nM = r.catExams('matric').length, nD = r.catExams('model').length;
    final cat = s.cat, c = catById(cat), ce = r.catExams(cat)..sort(byYear), cp = s.catProgress(cat);
    final years = {for (final e in ce) e.year}.toList()..sort((a, b) => yearKey(b) - yearKey(a));
    if (_libYear != null && !years.contains(_libYear)) _libYear = null;
    bool inYear(Exam e) => _libYear == null || e.year == _libYear;
    final subs = r.subjects.where((x) => ce.any((e) => e.subject == x && inYear(e)) && x.toLowerCase().contains(_libQ.toLowerCase())).toList();
    final exs = ce.where((e) => inYear(e) && subs.contains(e.subject)).toList();
    final ct = k.tone(c.tone);
    final catLong = c.long.toLowerCase().replaceFirstMapped(RegExp('^.'), (m) => m[0]!.toUpperCase());

    final sticky = DecoratedBox(
      decoration: BoxDecoration(
        gradient: LinearGradient(begin: Alignment.topCenter, end: Alignment.bottomCenter, colors: [p.bg, withA(p.bg, 0)], stops: const [.78, 1]),
      ),
      child: Padding(
        padding: const EdgeInsets.fromLTRB(4, 8, 4, 6),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            Padding(
              padding: const EdgeInsets.only(top: 2, bottom: 10),
              child: Seg(
                cat: true,
                current: cat,
                items: [for (final x in kCats) (id: x.id, label: x.label, icon: x.icon, count: x.id == 'matric' ? nM : nD, tone: x.tone, enabled: (x.id == 'matric' ? nM : nD) > 0)],
                onPick: (id) {
                  if (id == s.cat) return;
                  _libYear = null;
                  s.setCat(id);
                  if (_sc.hasClients) _sc.jumpTo(0);
                },
              ),
            ),
            if (years.length > 1)
              SingleChildScrollView(
                scrollDirection: Axis.horizontal,
                clipBehavior: Clip.none,
                padding: const EdgeInsets.fromLTRB(2, 4, 2, 12),
                child: Row(
                  spacing: 8,
                  children: [
                    ChipX('All years', count: ce.length, on: _libYear == null, onTap: () => setState(() => _libYear = null)),
                    for (final y in years) ChipX(yearShort(y), count: ce.where((e) => e.year == y).length, on: _libYear == y, onTap: () => setState(() => _libYear = y)),
                  ],
                ),
              ),
          ],
        ),
      ),
    );

    final body = <Widget>[
      Blk(
        margin: const EdgeInsets.only(top: 8),
        child: Row(spacing: 10, children: [
          Expanded(child: Btn('Mistakes', icon: 'repeat', kind: BtnKind.soft, block: true, onTap: () => Routes.mistakes(context))),
          Expanded(child: Btn('Weak topics', icon: 'target', kind: BtnKind.soft, block: true, onTap: () => Routes.weak(context))),
        ]),
      ),
      // .cathead
      Panel(
        tone: c.tone,
        margin: const EdgeInsets.fromLTRB(0, 4, 0, 12),
        padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 12),
        child: Row(
          spacing: 12,
          children: [
            Badge(c.tone, c.icon, s: 42),
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.stretch,
                children: [
                  Text.rich(
                    TextSpan(text: '${c.long} ', children: [TextSpan(text: '(${cp.exams})', style: ts(12, w900, p.ink))]),
                    style: ts(15, w900, p.ink),
                  ),
                  const SizedBox(height: 1),
                  OneLine(
                    '${c.blurb} · ${cp.subjects} subject${cp.subjects == 1 ? '' : 's'} · ${cp.years}',
                    style: ts(12, w800, mix(ct.deep, .75, p.ink2)),
                  ),
                  const SizedBox(height: 7),
                  Bar(cp.p.pct, tone: c.tone, height: 7, onTile: true),
                  const SizedBox(height: 1),
                  Text(cp.p.done > 0 ? '${cp.p.pct}% done · ${cp.p.acc}% right' : 'Not started yet', style: ts(12, w800, mix(ct.deep, .75, p.ink2))),
                ],
              ),
            ),
          ],
        ),
      ),
      if (subs.length > 4 || _libQ.isNotEmpty)
        Blk(
          margin: const EdgeInsets.fromLTRB(0, 4, 0, 10),
          child: Field(
            search: true,
            controller: _q,
            placeholder: 'Search ${c.label.toLowerCase()} subjects',
            onChanged: (v) => setState(() => _libQ = v),
          ),
        ),
      Blk(
        margin: const EdgeInsets.only(top: 6),
        child: Column(
          spacing: 12,
          children: [
            for (var i = 0; i < subs.length; i += 2)
              IntrinsicHeight(
                child: Row(
                  crossAxisAlignment: CrossAxisAlignment.stretch,
                  spacing: 12,
                  children: [
                    Expanded(child: Stagger(i: i, child: _SubjTile(subs[i], ce.where((e) => e.subject == subs[i] && inYear(e)).toList(), _libYear, cat))),
                    Expanded(child: i + 1 < subs.length ? Stagger(i: i + 1, child: _SubjTile(subs[i + 1], ce.where((e) => e.subject == subs[i + 1] && inYear(e)).toList(), _libYear, cat)) : const SizedBox()),
                  ],
                ),
              ),
          ],
        ),
      ),
      if (subs.isEmpty) const EmptyCard(title: 'No match', text: 'Try another year or search term.'),
      if (exs.isNotEmpty) ...[
        SectionLabel('${_libYear != null ? '$_libYear ' : ''}$catLong by subject', n: exs.length, icon: 'pen'),
        Panel(
          padding: const EdgeInsets.fromLTRB(16, 6, 16, 8),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              for (final sj in subs.where((x) => exs.any((e) => e.subject == x))) ...() {
                final l = look(sj), se = exs.where((e) => e.subject == sj).toList(), t = k.tone(l.tone);
                return [
                  Padding(
                    padding: const EdgeInsets.fromLTRB(0, 10, 0, 4),
                    child: Row(
                      spacing: 10,
                      children: [
                        Badge(l.tone, l.icon, s: 26),
                        Expanded(child: Text(sj, style: ts(14, w900, p.ink))),
                        Text('${se.length} exam${se.length > 1 ? 's' : ''}', style: ts(11.5, w800, p.ink3)),
                      ],
                    ),
                  ),
                  for (var i = 0; i < se.length; i++)
                    () {
                      final e = se[i], ep = s.examProgress(e);
                      return ListRow(
                        border: i > 0,
                        lead: Knob(
                          tone: l.tone,
                          size: 40,
                          radius: 13,
                          child: Text(yearShort(e.year).replaceFirst('/', '/\u200b'), textAlign: TextAlign.center, style: ts(11.5, w900, t.deep)),
                        ),
                        title: '${e.name} · ${yearShort(e.year)}',
                        sub: '${e.questions.length} questions · ${ep.done > 0 ? '${ep.pct}% done · ${ep.acc}% right' : 'not started'}',
                        trailing: PlayBtn(tone: l.tone, onTap: () => Routes.resume(context, e.id), label: 'Practice'),
                      );
                    }(),
                ];
              }(),
            ],
          ),
        ),
      ],
    ];

    return PageShell(
      top: TopBar(title: 'Matric', sub: '${r.exams.length} exam${r.exams.length == 1 ? '' : 's'} · $nM matriculation · $nD model'),
      body: ScrollConfiguration(
        behavior: const NoGlow(),
        child: CustomScrollView(
          controller: _sc,
          slivers: [
            const SliverToBoxAdapter(child: SizedBox(height: 4)),
            SliverPadding(padding: const EdgeInsets.symmetric(horizontal: 12), sliver: PinnedHeaderSliver(child: sticky)),
            SliverPadding(
              padding: EdgeInsets.fromLTRB(16, 0, 16, screenBottom(context)),
              sliver: SliverList.list(children: collapse(body)),
            ),
          ],
        ),
      ),
    );
  }
}

class _SubjTile extends StatelessWidget {
  const _SubjTile(this.s, this.ex, this.year, this.cat);
  final String s;
  final List<Exam> ex;
  final String? year;
  final String cat;
  @override
  Widget build(BuildContext context) {
    final k = Kit.of(context), p = k.p, l = look(s), t = k.tone(l.tone);
    final pr = k.s.subjectProgress(s, year, cat);
    return Panel(
      tone: l.tone,
      margin: EdgeInsets.zero,
      padding: const EdgeInsets.all(14),
      onTap: () => Routes.subject(context, s, year: year, cat: cat),
      label: s,
      child: ConstrainedBox(
        constraints: const BoxConstraints(minHeight: 150 - 28),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Badge(l.tone, l.icon, s: 44),
            const SizedBox(height: 6 + 8),
            Tx(s, style: ts(15.5, w900, p.ink, height: 1.2)),
            const SizedBox(height: 6),
            Text('${ex.length} exam${ex.length > 1 ? 's' : ''} · ${pr.total} ${ex.any((e) => e.matches.isNotEmpty) ? 'auto-marked' : 'MCQs'}', style: ts(12.5, w700, mix(t.deep, .7, p.ink2))),
            const Spacer(),
            const SizedBox(height: 6),
            Bar(pr.pct, tone: l.tone, onTile: true),
            const SizedBox(height: 6),
            Text(pr.done > 0 ? '${pr.pct}% done${pr.acc != null ? ' · ${pr.acc}% right' : ''}' : 'Not started', style: ts(11.5, w900, t.deep)),
          ],
        ),
      ),
    );
  }
}

