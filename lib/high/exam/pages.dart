// Exam player pages: practice one exam (renderExam), quiz a list of questions (renderQuiz: daily / topic / mistakes /
// unit / tutor), the exam subject page (renderSubject), Mistakes & bookmarks (renderReview) and weak topics (renderWeak).
import 'package:flutter/widgets.dart';

import '../data/models.dart';
import '../data/repository.dart';
import '../screens/routes.dart';
import '../state/app_state.dart';
import '../theme/tokens.dart';
import '../widgets/kit.dart';
import '../widgets/page.dart';
import '../widgets/rich.dart';
import 'cards.dart';

/// fixed header strip (web `.sticky`) + scrolling blocks; scrolls to [focus] after the first frame
class _CardsScreen extends StatefulWidget {
  const _CardsScreen({required this.top, required this.header, required this.children, required this.keys, this.focus});
  final Widget top, header;
  final List<Widget> children;
  final Map<String, GlobalKey> keys;
  final String? focus;
  @override
  State<_CardsScreen> createState() => _CardsScreenState();
}

class _CardsScreenState extends State<_CardsScreen> {
  final _sc = ScrollController();
  @override
  void initState() {
    super.initState();
    if (widget.focus != null) {
      WidgetsBinding.instance.addPostFrameCallback((_) {
        final c = widget.keys[widget.focus]?.currentContext;
        if (c != null && c.mounted) Scrollable.ensureVisible(c, alignment: .02);
      });
    }
  }

  @override
  void dispose() {
    _sc.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) => PageShell(
    top: widget.top,
    body: Column(
      crossAxisAlignment: CrossAxisAlignment.stretch,
      children: [
        Padding(padding: const EdgeInsets.fromLTRB(16, 4, 16, 4), child: widget.header),
        Expanded(
          child: ScrollConfiguration(
            behavior: const NoGlow(),
            child: SingleChildScrollView(
              controller: _sc,
              padding: EdgeInsets.fromLTRB(16, 0, 16, kScreenBottom + MediaQuery.paddingOf(context).bottom),
              child: Column(crossAxisAlignment: CrossAxisAlignment.stretch, children: collapse(widget.children)),
            ),
          ),
        ),
      ],
    ),
  );
}

Widget _chips(List<Widget> c) => SingleChildScrollView(
  scrollDirection: Axis.horizontal,
  clipBehavior: Clip.none,
  padding: const EdgeInsets.fromLTRB(2, 4, 2, 10),
  child: Row(spacing: 8, children: c),
);

Widget progLine(BuildContext c, int pct, String label, String tone) {
  final t = Kit.of(c).tone(tone);
  return Row(spacing: 10, children: [Expanded(child: Bar(pct, tone: tone)), Text(label, style: ts(12.5, w900, t.deep))]);
}

// ---------------------------------------------------------------- practice one exam
String _filt = 'all';

class PracticePage extends StatefulWidget {
  const PracticePage({super.key, required this.examId, this.focus});
  final String examId;
  final String? focus;
  @override
  State<PracticePage> createState() => _PracticePageState();
}

class _PracticePageState extends State<PracticePage> {
  final _keys = <String, GlobalKey>{};
  @override
  Widget build(BuildContext context) {
    final k = Kit.of(context), s = k.s, e = s.repo.exam[widget.examId]!, l = look(e.subject);
    final parts = {for (final q in e.questions) q.part}.toList()..sort();
    const roman = ['', 'I', 'II', 'III', 'IV'];
    final f = [
      ('all', 'All', e.questions.length),
      for (final pt in parts) ('p$pt', 'Part ${pt < 5 ? roman[pt] : pt}', e.questions.where((q) => q.part == pt).length),
      ('todo', 'Unanswered', e.scored.where((q) => !s.answered(q.id)).length),
      ('wrong', 'Wrong', e.scored.where((q) => s.answered(q.id) && !s.ansOk(q.id)).length),
      ('flag', '⚑ Notes', e.questions.where((q) => q.reviewFlag != null).length),
    ].where((x) => x.$1 == 'all' || x.$3 > 0 || x.$1 == 'todo').toList();
    if (!f.any((x) => x.$1 == _filt)) _filt = 'all';
    final list = e.questions.where((q) =>
        _filt == 'all' ||
        _filt == 'p${q.part}' ||
        (_filt == 'todo' && q.isScored && !s.answered(q.id)) ||
        (_filt == 'wrong' && s.answered(q.id) && !s.ansOk(q.id)) ||
        (_filt == 'flag' && q.reviewFlag != null)).toList();
    final pr = s.examProgress(e);
    final o = CardOpts(graded: (id) => s.ans(id)?['c'] as String?);
    return _CardsScreen(
      keys: _keys,
      focus: widget.focus,
      top: TopBar(title: e.name, sub: '${yearShort(e.year)} · practice · instant feedback', onBack: HighNav.of(context).back, tab: false),
      header: Column(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          Padding(padding: const EdgeInsets.fromLTRB(4, 0, 4, 8), child: progLine(context, pr.pct, '${pr.done}/${pr.total}', l.tone)),
          _chips([for (final x in f) ChipX(x.$2, count: x.$3, on: _filt == x.$1, onTap: () => setState(() => _filt = x.$1))]),
        ],
      ),
      children: list.isEmpty ? [const EmptyCard(title: 'All clear!', text: 'Nothing left in this filter.')] : buildCards(list, o, _keys),
    );
  }
}

// ---------------------------------------------------------------- quiz
class QuizPage extends StatefulWidget {
  const QuizPage({super.key, required this.ids, required this.title, this.sub, this.kind = 'topic', this.unitId});
  final List<String> ids;

  /// notes unit this set belongs to (exercise / matric-by-unit): results offer the other two links
  final String? unitId;
  final String title;
  final String? sub;

  /// daily | mistakes | topic | unit | exercise
  final String kind;
  @override
  State<QuizPage> createState() => _QuizPageState();
}

class _QuizPageState extends State<QuizPage> {
  final _keys = <String, GlobalKey>{};
  late final Map<String, dynamic> _res;
  @override
  void initState() {
    super.initState();
    final s = HighScope.read(context);
    _res = widget.kind == 'daily' ? (s.dailyQuiz()['res'] as Map<String, dynamic>) : <String, dynamic>{};
  }

  @override
  Widget build(BuildContext context) {
    final k = Kit.of(context), p = k.p, s = k.s;
    final qs = [for (final id in widget.ids) ?s.repo.byId[id]];
    final mcq = qs.where((q) => q.isScored).map((q) => q.id).toList();
    final done = mcq.where((id) => _res[id] != null).toList(), right = done.where((id) => _res[id] == true).length;
    final o = CardOpts(
      mode: widget.kind == 'daily' ? 'daily' : 'quiz',
      showExam: true,
      graded: (id) => _res[id] != null ? (s.ans(id)?['c'] as String?) : null,
      onAnswer: (q, l, ok) {
        _res[q.id] = ok;
        if (widget.kind == 'daily') s.saveLater();
        setState(() {});
      },
    );
    final badge = switch (widget.kind) {
      'daily' => ('butter', 'shuffle'),
      'exercise' => ('blue', 'pen'),
      'mistakes' => ('peach', 'repeat'),
      _ => ('lilac', 'target'),
    };
    final kids = [...buildCards(qs, o, _keys)];
    if (mcq.isNotEmpty && done.length == mcq.length) {
      final pct = (100 * right / mcq.length).round();
      kids.add(
        Panel(
          tone: pct >= 80 ? 'sage' : (pct >= 50 ? 'butter' : 'peach'),
          padding: const EdgeInsets.fromLTRB(16, 22, 16, 18),
          child: Column(
            children: [
              const Kokob(width: 84),
              Padding(padding: const EdgeInsets.only(top: 6, bottom: 2), child: Text('$right/${mcq.length} correct', style: ts(22, w900, p.ink))),
              Text(
                pct == 100 ? 'Perfect score! 🎉' : (pct >= 80 ? 'Excellent work!' : (pct >= 50 ? 'Good effort — review the steps above' : 'Keep going — mistakes are how we learn')),
                textAlign: TextAlign.center,
                style: ts(14, w700, p.ink2),
              ),
              if (widget.unitId != null)
                Padding(
                  padding: const EdgeInsets.only(top: 14),
                  child: UnitLinkBar(unitId: widget.unitId!, notes: true, exercises: widget.kind != 'exercise', matric: widget.kind != 'unit'),
                ),
              Padding(
                padding: const EdgeInsets.only(top: 14),
                child: Row(
                  spacing: 10,
                  children: [
                    Expanded(child: Btn('Home', icon: 'home', kind: BtnKind.soft, block: true, onTap: () => HighNav.of(context).tab(HighTab.home))),
                    Expanded(
                      child: right < mcq.length
                          ? Btn('Retry wrong', icon: 'repeat', block: true, onTap: () => HighNav.of(context).push(QuizPage(ids: mcq.where((id) => _res[id] != true).toList(), title: 'Retry', sub: 'Your wrong answers', kind: 'mistakes')))
                          : Btn('More practice', icon: 'grid', block: true, onTap: () => widget.kind == 'exercise' ? HighNav.of(context).back() : HighNav.of(context).tab(HighTab.matric)),
                    ),
                  ],
                ),
              ),
            ],
          ),
        ),
      );
    }
    return _CardsScreen(
      keys: _keys,
      top: TopBar(title: widget.title, sub: widget.sub ?? '${qs.length} questions', onBack: HighNav.of(context).back, tab: false),
      header: Panel(
        margin: const EdgeInsets.only(top: 4, bottom: 6),
        padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 12),
        child: Row(
          spacing: 12,
          children: [
            Badge(badge.$1, badge.$2, s: 36),
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.stretch,
                children: [
                  progLine(context, mcq.isEmpty ? 0 : (100 * done.length / mcq.length).round(), '${done.length}/${mcq.length}', 'sage'),
                  Padding(padding: const EdgeInsets.only(top: 4), child: Text(done.isNotEmpty ? '$right correct so far' : 'Answer each question for instant feedback', style: ts(12.5, w700, p.ink3))),
                ],
              ),
            ),
          ],
        ),
      ),
      children: kids.isEmpty ? [const EmptyCard(title: 'Nothing to practise', text: 'No questions here yet.')] : kids,
    );
  }
}

// ---------------------------------------------------------------- exam subject page
class ExamSubjectPage extends StatefulWidget {
  const ExamSubjectPage({super.key, required this.subject, this.cat});
  final String subject;
  final String? cat;
  @override
  State<ExamSubjectPage> createState() => _ExamSubjectPageState();
}

class _ExamSubjectPageState extends State<ExamSubjectPage> {
  String? _cat;
  bool _allT = false;
  bool _lazyReady = false;
  bool _lazyLoading = false;

  @override
  void initState() {
    super.initState();
    _kickLazy();
  }

  @override
  void didUpdateWidget(covariant ExamSubjectPage oldWidget) {
    super.didUpdateWidget(oldWidget);
    if (oldWidget.subject != widget.subject) {
      _lazyReady = false;
      _kickLazy();
    }
  }

  void _kickLazy() {
    if (_lazyLoading) return;
    _lazyLoading = true;
    WidgetsBinding.instance.addPostFrameCallback((_) {
      if (!mounted) return;
      HighScope.read(context).repo.ensureLazySubject(widget.subject).whenComplete(() {
        if (!mounted) return;
        setState(() {
          _lazyLoading = false;
          _lazyReady = true;
        });
      });
    });
  }

  @override
  Widget build(BuildContext context) {
    final k = Kit.of(context), p = k.p, s = k.s, r = s.repo, sub = widget.subject, l = look(sub), t = k.tone(l.tone);
    // Touch flag so rebuild after lazy load refreshes paper list.
    final _ = _lazyReady;
    final all = r.exams.where((e) => e.subject == sub).toList();
    final counts = {for (final c in kCats) c.id: all.where((e) => e.cat == c.id).length};
    final cat = [_cat, widget.cat, s.cat].firstWhere((c) => c != null && (counts[c] ?? 0) > 0, orElse: () => kCats.firstWhere((c) => counts[c.id]! > 0, orElse: () => kCats.first).id)!;
    final exams = all.where((e) => e.cat == cat).toList()..sort(byYear);
    final pr = s.subjectProgress(sub, null, cat);
    final years = {for (final e in exams) e.year}.toList()..sort((a, b) => yearKey(b) - yearKey(a));
    final topics = [
      for (final e in r.topicQs.entries)
        if (e.key.startsWith('$sub|'))
          () {
            final ids = e.value.where((id) => r.byId[id]?.isScored ?? false).toList(), dn = ids.where(s.answered).toList();
            return (id: e.key.substring(sub.length + 1), ids: ids, n: dn.length, acc: dn.isEmpty ? null : (100 * dn.where(s.ansOk).length / dn.length).round());
          }(),
    ].where((x) => x.ids.isNotEmpty).toList()..sort((a, b) => b.ids.length - a.ids.length);
    return PageShell(
      top: TopBar(title: sub, sub: [for (final c in kCats) if (counts[c.id]! > 0) '${counts[c.id]} ${c.label.toLowerCase()}'].join(' · '), onBack: HighNav.of(context).back, tab: false),
      body: ScreenList(
        children: [
          Panel(
            tone: l.tone,
            padding: const EdgeInsets.all(18),
            child: Row(
              spacing: 14,
              children: [
                Badge(l.tone, l.icon, s: 58),
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.stretch,
                    children: [
                      Text(sub, style: ts(22, w900, p.ink)),
                      Text('${catById(cat).long} · ${scoredLabel(exams.expand((e) => e.scored).toList())} · ${pr.done > 0 ? '${pr.pct}% done · ${pr.acc}% right' : 'Not started yet'}', style: ts(13, w700, p.ink2)),
                      Padding(padding: const EdgeInsets.only(top: 10), child: Bar(pr.pct, tone: l.tone, onTile: true)),
                    ],
                  ),
                ),
              ],
            ),
          ),
          if (counts.values.where((n) => n > 0).length > 1)
            Blk(
              margin: const EdgeInsets.only(top: 14),
              child: Seg(
                cat: true,
                current: cat,
                items: [for (final c in kCats) (id: c.id, label: c.label, icon: c.icon, count: counts[c.id], tone: c.tone, enabled: counts[c.id]! > 0)],
                onPick: (id) => setState(() => _cat = id),
              ),
            ),
          for (final y in years) ...[
            SectionLabel('${catById(cat).label} · $y', n: '${exams.where((e) => e.year == y).length} exam(s)', icon: 'cal'),
            for (final e in exams.where((e) => e.year == y))
              () {
                final ep = s.examProgress(e), other = e.questions.length - e.scored.length, flags = e.questions.where((q) => q.reviewFlag != null).length;
                return Panel(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.stretch,
                    children: [
                      Row(
                        spacing: 12,
                        children: [
                          Knob(tone: l.tone, child: Badge(l.tone, 'pen', s: 34)),
                          Expanded(
                            child: Column(
                              crossAxisAlignment: CrossAxisAlignment.start,
                              children: [
                                Text(e.title.isEmpty ? e.name : e.title, style: ts(16, w900, p.ink, height: 1.25)),
                                Text(e.school.split(',').first, style: ts(12.5, w700, p.ink3)),
                              ],
                            ),
                          ),
                        ],
                      ),
                      Padding(
                        padding: const EdgeInsets.only(top: 8, bottom: 12),
                        child: Wrap(
                          spacing: 6,
                          runSpacing: 6,
                          children: [
                            Tag(e.short, tone: l.tone),
                            Tag('${e.mcqs.length} MCQ${e.matches.isNotEmpty ? ' + ${e.matches.length} matching' : ''}${other > 0 ? ' + $other written' : ''}'),
                            if (e.duration != null) Tag('⏱ ${e.duration}'),
                            if (flags > 0) Tag('⚑ $flags review notes'),
                          ],
                        ),
                      ),
                      progLine(context, ep.pct, '${ep.done}/${ep.total}', l.tone),
                      Padding(
                        padding: const EdgeInsets.only(top: 14),
                        child: Btn(ep.done > 0 ? 'Continue' : 'Practice', icon: 'play', kind: BtnKind.tone, tone: l.tone, block: true, onTap: () => Routes.resume(context, e.id)),
                      ),
                    ],
                  ),
                );
              }(),
          ],
          if (topics.isNotEmpty) ...[
            SectionLabel('Topics', n: topics.length, icon: 'steps'),
            Panel(
              padding: const EdgeInsets.fromLTRB(16, 6, 16, 6),
              child: Column(
                children: [
                  for (final (i, tp) in (_allT ? topics : topics.take(6)).indexed)
                    () {
                      final tone = tp.acc == null ? 'lilac' : (tp.acc! < 50 ? 'peach' : (tp.acc! < 75 ? 'butter' : 'sage'));
                      return Container(
                        decoration: i == 0 ? null : BoxDecoration(border: Border(top: BorderSide(color: p.line))),
                        padding: const EdgeInsets.symmetric(vertical: 10),
                        child: Row(
                          spacing: 12,
                          children: [
                            Expanded(
                              child: Column(
                                crossAxisAlignment: CrossAxisAlignment.stretch,
                                children: [
                                  Text(r.topicTitle(sub, tp.id), maxLines: 1, overflow: TextOverflow.ellipsis, style: ts(14.5, w900, p.ink)),
                                  Text('${tp.ids.length} questions${tp.n > 0 ? ' · ${tp.acc}% right (${tp.n} answered)' : ''}', style: ts(12, w700, p.ink3)),
                                  Padding(padding: const EdgeInsets.only(top: 6), child: Bar(tp.n > 0 ? tp.acc! : 0, tone: tone, height: 7)),
                                ],
                              ),
                            ),
                            PlayBtn(tone: tone, onTap: () => Routes.topicQuiz(context, sub, tp.id), label: 'Quiz'),
                          ],
                        ),
                      );
                    }(),
                  if (topics.length > 6 && !_allT)
                    Padding(
                      padding: const EdgeInsets.fromLTRB(0, 6, 0, 10),
                      child: Btn('Show all ${topics.length} topics', kind: BtnKind.soft, block: true, onTap: () => setState(() => _allT = true)),
                    ),
                ],
              ),
            ),
          ],
          if (t.deep == t.deep) const SizedBox.shrink(),
        ],
      ),
    );
  }
}

// ---------------------------------------------------------------- mistakes & bookmarks
String _rtab = 'mi', _rcat = 'all';

class MistakesPage extends StatefulWidget {
  const MistakesPage({super.key});
  @override
  State<MistakesPage> createState() => _MistakesPageState();
}

class _MistakesPageState extends State<MistakesPage> {
  @override
  Widget build(BuildContext context) {
    final k = Kit.of(context), p = k.p, s = k.s, r = s.repo;
    final bms = s.bookmarks.where(r.byId.containsKey).toList(), mis = s.mistakes.where(r.byId.containsKey).toList();
    final all = (_rtab == 'bm' ? bms : mis).reversed.toList();
    final rc = {for (final c in kCats) c.id: all.where((id) => r.byId[id]!.exam.cat == c.id).length};
    if (_rcat != 'all' && (rc[_rcat] ?? 0) == 0) _rcat = 'all';
    final ids = all.where((id) => _rcat == 'all' || r.byId[id]!.exam.cat == _rcat).toList();
    final multi = rc.values.where((n) => n > 0).length > 1;
    final groups = <String, List<String>>{};
    for (final id in ids) {
      (groups[r.byId[id]!.exam.id] ??= []).add(id);
    }
    return PageShell(
      top: TopBar(title: 'Mistakes', sub: 'Mistakes & bookmarks · all subjects', onBack: HighNav.of(context).back, tab: false),
      body: ScreenList(
        children: [
          Blk(
            margin: const EdgeInsets.only(top: 8),
            child: Seg(
              current: _rtab,
              items: [
                (id: 'mi', label: 'Mistakes', icon: 'x', count: mis.length, tone: 'sage', enabled: true),
                (id: 'bm', label: 'Bookmarks', icon: 'bookmark', count: bms.length, tone: 'sage', enabled: true),
              ],
              onPick: (id) => setState(() => _rtab = id),
            ),
          ),
          if (multi)
            Blk(
              margin: const EdgeInsets.only(top: 10),
              child: _chips([
                ChipX('All exams', small: true, count: all.length, on: _rcat == 'all', onTap: () => setState(() => _rcat = 'all')),
                for (final c in kCats) ChipX(c.long, small: true, count: rc[c.id], on: _rcat == c.id, onTap: () => setState(() => _rcat = c.id)),
              ]),
            ),
          if (_rtab == 'mi' && ids.isNotEmpty)
            Panel(
              tone: 'peach',
              padding: const EdgeInsets.all(14),
              child: Row(
                spacing: 12,
                children: [
                  const Badge('peach', 'repeat', s: 42),
                  Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text('Turn mistakes into points', style: ts(15, w900, p.ink)),
                        Text('${ids.length} question${ids.length > 1 ? 's' : ''} to retry', style: ts(12.5, w700, p.ink2)),
                      ],
                    ),
                  ),
                  Btn('Retry', onTap: () {
                    final l = mis.where((id) => r.byId[id]!.isScored && (_rcat == 'all' || r.byId[id]!.exam.cat == _rcat)).toList();
                    HighNav.of(context).push(QuizPage(ids: l.sublist(l.length > 20 ? l.length - 20 : 0), title: 'Retry mistakes', sub: 'Get them right this time', kind: 'mistakes'));
                  }),
                ],
              ),
            ),
          if (ids.isEmpty)
            _rtab == 'bm'
                ? const EmptyCard(title: 'No bookmarks yet', text: 'Tap the bookmark on any question to save it here for later.', art: 'kokob')
                : const EmptyCard(title: 'No mistakes — yet!', text: 'Wrong answers land here so you can retry them until they stick.'),
          for (final g in groups.entries) ...[
            SectionLabel('${r.exam[g.key]!.name} · ${yearShort(r.exam[g.key]!.year)}', n: g.value.length),
            for (final id in g.value)
              () {
                final q = r.byId[id]!, a = s.ans(id), lk = look(q.exam.subject), pt = r.primaryTopic(q);
                return Panel(
                  margin: const EdgeInsets.symmetric(vertical: 12),
                  padding: const EdgeInsets.all(14),
                  onTap: () => HighNav.of(context).push(q.exam.isExercise ? QuizPage(ids: [id], title: q.exam.name, sub: q.exam.year) : PracticePage(examId: q.exam.id, focus: id)),
                  child: Row(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    spacing: 12,
                    children: [
                      Knob(tone: lk.tone, size: 44, child: Badge(lk.tone, lk.icon, s: 30)),
                      Expanded(
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.stretch,
                          children: [
                            Text.rich(
                              TextSpan(children: [
                                TextSpan(text: q.label, style: ts(14, w900, k.tone(lk.tone).deep)),
                                TextSpan(text: ' · ${q.isMatch ? 'Match: ${q.matchPrompt}' : q.stem}'),
                              ]),
                              maxLines: 2,
                              overflow: TextOverflow.ellipsis,
                              style: ts(14, w700, p.ink, height: 1.45),
                            ),
                            Padding(
                              padding: const EdgeInsets.only(top: 8),
                              child: Wrap(
                                spacing: 6,
                                runSpacing: 6,
                                children: _rtab == 'mi' && a != null
                                    ? [Tag('You: ${a['c']}', tone: 'peach'), Tag('Answer: ${q.isMatch ? q.answerText : q.answer}', tone: 'sage')]
                                    : [Tag(pt != null ? r.topicTitle(q.exam.subject, pt) : q.exam.subject, tone: lk.tone), if (a != null) Tag(a['ok'] == true ? '✓ correct' : '✗ wrong', tone: a['ok'] == true ? 'sage' : 'peach')],
                              ),
                            ),
                          ],
                        ),
                      ),
                    ],
                  ),
                );
              }(),
          ],
        ],
      ),
    );
  }
}

// ---------------------------------------------------------------- weak topics
class WeakPage extends StatelessWidget {
  const WeakPage({super.key});
  @override
  Widget build(BuildContext context) {
    final k = Kit.of(context), p = k.p, s = k.s, r = s.repo;
    final w = s.weakTopics(), need = w.where((t) => t.n >= 2 && t.acc < 70).toList(), good = w.where((t) => !(t.n >= 2 && t.acc < 70)).toList();
    final untouched = r.topicQs.keys.where((key) => !w.any((x) => '${x.subject}|${x.id}' == key) && r.topicQs[key]!.any((id) => r.byId[id]?.isScored ?? false)).take(10).toList();
    Widget row(({String subject, String id, int n, int right, int acc}) t, int i) {
      final tone = t.acc < 50 ? 'peach' : (t.acc < 75 ? 'butter' : 'sage');
      return Container(
        decoration: i == 0 ? null : BoxDecoration(border: Border(top: BorderSide(color: p.line))),
        padding: const EdgeInsets.symmetric(vertical: 10),
        child: Row(
          spacing: 12,
          children: [
            Knob(tone: tone, radius: 24, child: Text('${t.acc}', style: ts(12.5, w900, k.tone(tone).deep))),
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.stretch,
                children: [
                  Text(r.topicTitle(t.subject, t.id), maxLines: 1, overflow: TextOverflow.ellipsis, style: ts(14.5, w900, p.ink)),
                  Text('${t.subject} · ${t.right} of ${t.n} correct', style: ts(12, w700, p.ink3)),
                ],
              ),
            ),
            PlayBtn(tone: tone, onTap: () => Routes.topicQuiz(context, t.subject, t.id), label: 'Practice topic'),
          ],
        ),
      );
    }

    return PageShell(
      top: TopBar(title: 'Weak topics', sub: 'Where to focus next', onBack: HighNav.of(context).back, tab: false),
      body: ScreenList(
        children: [
          Panel(
            tone: 'sage',
            padding: const EdgeInsets.fromLTRB(8, 12, 14, 12),
            child: Row(
              spacing: 10,
              children: [
                const Kokob(width: 62),
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(w.isEmpty ? 'Nothing to analyse yet' : (need.isNotEmpty ? '${need.length} topic${need.length > 1 ? 's' : ''} below 70%' : 'No weak spots right now!'), style: ts(14, w800, p.ink)),
                      Text(w.isEmpty ? 'Answer a few questions and I will spot patterns' : 'Based on every answer you have given', style: ts(12, w700, p.ink2)),
                    ],
                  ),
                ),
              ],
            ),
          ),
          if (need.isNotEmpty) ...[
            SectionLabel('Needs work', n: need.length),
            Panel(padding: const EdgeInsets.fromLTRB(16, 6, 16, 6), child: Column(children: [for (final (i, t) in need.indexed) row(t, i)])),
          ],
          if (good.isNotEmpty) ...[
            SectionLabel(need.isNotEmpty ? 'Other practised topics' : 'Practised topics', n: good.length),
            Panel(padding: const EdgeInsets.fromLTRB(16, 6, 16, 6), child: Column(children: [for (final (i, t) in good.take(12).indexed) row(t, i)])),
          ],
          if (untouched.isNotEmpty) ...[
            const SectionLabel('Not started yet'),
            Blk(
              margin: const EdgeInsets.only(top: 8),
              child: Wrap(
                spacing: 8,
                runSpacing: 8,
                children: [
                  for (final key in untouched)
                    () {
                      final i = key.indexOf('|'), sub = key.substring(0, i), id = key.substring(i + 1);
                      return ChipX(r.topicTitle(sub, id), tone: look(sub).tone, onTap: () => Routes.topicQuiz(context, sub, id));
                    }(),
                ],
              ),
            ),
          ],
          if (w.isEmpty) Blk(margin: const EdgeInsets.only(top: 8), child: Btn('Start the Daily Quiz', icon: 'play', block: true, onTap: () => Routes.dailyQuiz(context))),
        ],
      ),
    );
  }
}

/// "Matric questions for this unit" block on the notes unit page
class UnitMatricCard extends StatelessWidget {
  const UnitMatricCard({super.key, required this.unitId, required this.title, required this.ids});
  final String unitId, title;
  final List<String> ids;
  @override
  Widget build(BuildContext context) {
    final k = Kit.of(context), p = k.p, s = k.s;
    final scored = ids.where((id) => s.repo.byId[id]!.isScored).toList();
    final done = scored.where(s.answered).length, right = scored.where(s.ansOk).length;
    final preview = ids.take(3).map((id) => s.repo.byId[id]!).toList();
    return Panel(
      margin: EdgeInsets.zero,
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          Row(
            spacing: 12,
            children: [
              const Badge('peach', 'trophy', s: 42),
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text('${ids.length} exam question${ids.length == 1 ? '' : 's'} on this unit', style: ts(15, w900, p.ink)),
                    Text('Matriculation & model papers · ${done > 0 ? '$right of $done right' : '${scored.length} auto-marked'}', style: ts(12.5, w700, p.ink2)),
                  ],
                ),
              ),
            ],
          ),
          for (final q in preview)
            Container(
              margin: const EdgeInsets.only(top: 8),
              padding: const EdgeInsets.symmetric(horizontal: 11, vertical: 9),
              decoration: k.d.raised(p.surface2, radius: 14),
              child: RichTx('${q.exam.name} ${yearShort(q.exam.year)} · ${q.label}: ${q.stem}', maxLines: 2, style: ts(13, w700, p.ink, height: 1.4)),
            ),
          Padding(
            padding: const EdgeInsets.only(top: 14),
            child: Btn('Practise these questions', icon: 'play', block: true, onTap: () => Routes.unitMatric(context, unitId)),
          ),
        ],
      ),
    );
  }
}

extension on ExamRepo {
  // ignore: unused_element
  int get n => exams.length;
}
