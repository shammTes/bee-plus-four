// TV / Smart View presenter: landscape, full screen, large type, one step at a time.
//   • question: stem (+ figure, options) -> each solution step -> the answer
//   • notes unit: one note card per step (lesson title above), cards scaled to fill the screen
// Controls: tap right/left half, big ‹ › buttons, or a keyboard / TV remote (→ ← space enter PgUp PgDn, Esc = exit).
import 'package:flutter/services.dart';
import 'package:flutter/widgets.dart';

import '../data/models.dart';
import '../exam/cards.dart' show Fig, TableView, tablesOf, texOpts, texStem;
import '../notes/jr/data/notes_models.dart';
import '../notes/jr/notes/cards.dart' show NoteCardView, UnitCtx;
import '../theme/tokens.dart';
import '../widgets/art.dart' show Ic;
import '../widgets/kit.dart';
import '../widgets/page.dart';
import '../widgets/rich.dart';

/// one presentable thing with [steps] reveal steps (>= 1)
abstract class Slide {
  int get steps;
  String get title;
  Widget build(BuildContext context, int step, double u);
}

class QuestionSlide extends Slide {
  QuestionSlide(this.q, {this.n});
  final Question q;
  final int? n;
  @override
  int get steps => 1 + q.steps.length + (q.isScored ? 1 : 0);
  @override
  String get title => '${n != null ? 'Question $n · ' : ''}${q.exam.name} ${yearShort(q.exam.year)}';

  @override
  Widget build(BuildContext context, int step, double u) {
    final k = Kit.of(context), p = k.p;
    final showAns = q.isScored && step == steps - 1;
    final shownSteps = (step).clamp(0, q.steps.length);
    final tx = texOpts(q);
    final opts = q.isMatch ? q.matchList!.choices : (q.options ?? const <String, String>{});
    // fit: long stems / many options shrink the type; short options go in two columns
    final plain = [texStem(q), ...opts.values].join();
    final f = plain.length > 520 ? .7 : (plain.length > 300 ? .8 : (opts.length > 4 ? .88 : 1.0));
    final two = opts.length >= 4 && opts.values.every((v) => v.length <= 48);
    Widget opt(MapEntry<String, String> e) => Container(
      margin: EdgeInsets.only(top: 10 * u * f),
      padding: EdgeInsets.symmetric(horizontal: 18 * u * f, vertical: 12 * u * f),
      decoration: k.d.raisedSoft(showAns && q.isCorrect(e.key) ? p.sage.tile : p.surface2, radius: 18 * u),
      child: Row(
        spacing: 14 * u * f,
        children: [
          Text(e.key, style: ts(26 * u * f, w900, showAns && q.isCorrect(e.key) ? p.sage.deep : p.ink2)),
          Expanded(child: RichTx(tx?[e.key] ?? e.value, tex: tx?[e.key] != null, style: ts(25 * u * f, w700, p.ink, height: 1.3))),
          if (showAns && q.isCorrect(e.key)) Ic('check', size: 30 * u * f, color: p.sage.deep),
        ],
      ),
    );
    final es = opts.entries.toList();
    final left = Column(
      crossAxisAlignment: CrossAxisAlignment.stretch,
      children: [
        RichTx(q.isMatch ? q.matchPrompt : texStem(q), tex: q.stemTex != null, style: ts(30 * u * f, w800, p.ink, height: 1.35)),
        for (final t in tablesOf(q.j['stem_tables'])) Padding(padding: EdgeInsets.only(top: 12 * u), child: TableView(t)),
        if (!two) for (final e in es) opt(e),
        if (two)
          for (var i = 0; i < es.length; i += 2)
            Row(
              crossAxisAlignment: CrossAxisAlignment.start,
              spacing: 12 * u,
              children: [Expanded(child: opt(es[i])), Expanded(child: i + 1 < es.length ? opt(es[i + 1]) : const SizedBox.shrink())],
            ),
      ],
    );
    final stepsW = [
      for (var i = 0; i < shownSteps; i++)
        Container(
          margin: EdgeInsets.only(top: 10 * u),
          padding: EdgeInsets.all(14 * u),
          decoration: k.d.raisedSoft(i == shownSteps - 1 && !showAns ? p.butter.tile : p.surface, radius: 16 * u),
          child: Row(
            crossAxisAlignment: CrossAxisAlignment.start,
            spacing: 12 * u,
            children: [
              Text('${i + 1}', style: ts(24 * u, w900, p.blue.deep)),
              Expanded(child: RichTx(q.steps[i], style: ts(24 * u, w700, p.ink, height: 1.35))),
            ],
          ),
        ),
      if (showAns)
        Container(
          margin: EdgeInsets.only(top: 12 * u),
          padding: EdgeInsets.all(14 * u),
          decoration: k.d.raisedSoft(p.sage.tile, radius: 16 * u),
          child: RichTx('Answer: ${q.answerText}', style: ts(27 * u, w900, p.sage.deep)),
        ),
    ];
    final fig = q.image != null ? Fig(path: q.image!, alt: q.imageAlt, exam: q.exam) : null;
    return Row(
      crossAxisAlignment: CrossAxisAlignment.start,
      spacing: 28 * u,
      children: [
        Expanded(flex: 11, child: SingleChildScrollView(child: Column(crossAxisAlignment: CrossAxisAlignment.stretch, children: [left, ...stepsW]))),
        if (fig != null) Expanded(flex: 9, child: Center(child: SingleChildScrollView(child: fig))),
      ],
    );
  }
}

class NotesSlide extends Slide {
  NotesSlide(this.u, this.bookId, this.svgPath);
  final Unit u;
  final String bookId;
  final String Function(String) svgPath;
  late final List<(Lesson, NoteCard, int)> cards = [
    for (final l in u.lessons)
      for (final (i, c) in l.cards.indexed) (l, c, i),
  ];
  @override
  int get steps => cards.isEmpty ? 1 : cards.length;
  @override
  String get title => 'Unit ${u.number} · ${u.title}';
  @override
  Widget build(BuildContext context, int step, double uu) {
    final p = Kit.of(context).p;
    if (cards.isEmpty) return Center(child: Text(u.title, style: ts(40 * uu, w900, p.ink)));
    final (l, c, i) = cards[step];
    return Column(
      crossAxisAlignment: CrossAxisAlignment.stretch,
      children: [
        Text('${l.number}  ${l.title}', style: ts(26 * uu, w900, p.ink2)),
        SizedBox(height: 10 * uu),
        Expanded(
          child: LayoutBuilder(
            builder: (c2, box) {
              // lay the phone-designed card out at a readable width, then scale it up to the TV
              const w = 640.0;
              final sc = (box.maxWidth / w).clamp(1.0, 2.2);
              return SingleChildScrollView(
                child: Center(
                  child: SizedBox(
                    width: w * sc,
                    child: FittedBox(
                      fit: BoxFit.fitWidth,
                      child: SizedBox(width: w, child: NoteCardView(key: ValueKey('${l.id}~$i'), ctx: UnitCtx(u, bookId, svgPath), card: c, ckey: '${l.id}~$i')),
                    ),
                  ),
                ),
              );
            },
          ),
        ),
      ],
    );
  }
}

class PresenterPage extends StatefulWidget with NoNav {
  const PresenterPage({super.key, required this.slides, this.lockLandscape = true});
  final List<Slide> slides;
  final bool lockLandscape;
  @override
  State<PresenterPage> createState() => _PresenterPageState();
}

class _PresenterPageState extends State<PresenterPage> {
  int _s = 0, _step = 0;
  final _focus = FocusNode();

  @override
  void initState() {
    super.initState();
    if (widget.lockLandscape) {
      SystemChrome.setPreferredOrientations(const [DeviceOrientation.landscapeLeft, DeviceOrientation.landscapeRight]);
      SystemChrome.setEnabledSystemUIMode(SystemUiMode.immersiveSticky);
    }
  }

  @override
  void dispose() {
    if (widget.lockLandscape) {
      SystemChrome.setPreferredOrientations(const []);
      SystemChrome.setEnabledSystemUIMode(SystemUiMode.edgeToEdge);
    }
    _focus.dispose();
    super.dispose();
  }

  void _next() => setState(() {
    if (_step < widget.slides[_s].steps - 1) {
      _step++;
    } else if (_s < widget.slides.length - 1) {
      _s++;
      _step = 0;
    }
  });

  void _prev() => setState(() {
    if (_step > 0) {
      _step--;
    } else if (_s > 0) {
      _s--;
      _step = widget.slides[_s].steps - 1;
    }
  });

  KeyEventResult _key(FocusNode n, KeyEvent e) {
    if (e is! KeyDownEvent && e is! KeyRepeatEvent) return KeyEventResult.ignored;
    final k = e.logicalKey;
    if ({LogicalKeyboardKey.arrowRight, LogicalKeyboardKey.arrowDown, LogicalKeyboardKey.space, LogicalKeyboardKey.enter, LogicalKeyboardKey.pageDown, LogicalKeyboardKey.select}.contains(k)) {
      _next();
    } else if ({LogicalKeyboardKey.arrowLeft, LogicalKeyboardKey.arrowUp, LogicalKeyboardKey.pageUp}.contains(k)) {
      _prev();
    } else if (k == LogicalKeyboardKey.escape) {
      HighNav.of(context).back();
    } else {
      return KeyEventResult.ignored;
    }
    return KeyEventResult.handled;
  }

  @override
  Widget build(BuildContext context) {
    final k = Kit.of(context), p = k.p, sz = MediaQuery.sizeOf(context);
    final u = (sz.shortestSide / 540).clamp(.6, 2.4); // 1.0 at 960×540 logical
    final sl = widget.slides[_s];
    final total = widget.slides.fold<int>(0, (a, x) => a + x.steps), done = widget.slides.take(_s).fold<int>(0, (a, x) => a + x.steps) + _step + 1;
    return Focus(
      focusNode: _focus,
      autofocus: true,
      onKeyEvent: _key,
      child: ColoredBox(
        color: p.bg,
        child: Padding(
          padding: EdgeInsets.fromLTRB(28 * u, 18 * u, 28 * u, 14 * u),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              Row(
                children: [
                  Expanded(child: Text(sl.title, maxLines: 1, overflow: TextOverflow.ellipsis, style: ts(22 * u, w900, p.ink2))),
                  Text('$done / $total', style: ts(20 * u, w900, p.ink3)),
                ],
              ),
              SizedBox(height: 14 * u),
              Expanded(
                child: GestureDetector(
                  behavior: HitTestBehavior.translucent,
                  onTapUp: (d) => d.localPosition.dx > sz.width * .35 ? _next() : _prev(),
                  child: sl.build(context, _step, u),
                ),
              ),
              SizedBox(height: 10 * u),
              Row(
                spacing: 14 * u,
                children: [
                  Btn('Exit', icon: 'x', kind: BtnKind.soft, fontSize: 16 * u, onTap: HighNav.of(context).back),
                  Expanded(child: ClipRRect(borderRadius: BorderRadius.circular(8), child: Bar((100 * done / total).round(), tone: 'sage', height: 10 * u))),
                  Btn('Back', icon: 'left', kind: BtnKind.soft, fontSize: 18 * u, padding: EdgeInsets.symmetric(horizontal: 22 * u, vertical: 14 * u), onTap: _prev),
                  Btn(_step < sl.steps - 1 ? 'Reveal' : 'Next', icon: 'right', trailing: true, fontSize: 18 * u, padding: EdgeInsets.symmetric(horizontal: 26 * u, vertical: 14 * u), onTap: _next),
                ],
              ),
            ],
          ),
        ),
      ),
    );
  }
}
