// Home dashboard (web renderHome): hero, category cards (+ Notes), stat tiles, weekly chart, practice-mix donut,
// daily quiz, recently practised, weak-topics + tutor banners.
import 'dart:math' as math;

import 'package:flutter/widgets.dart';

import '../data/models.dart';
import '../state/app_state.dart';
import '../theme/clay.dart';
import '../theme/tokens.dart';
import '../widgets/art.dart';
import '../widgets/kit.dart';
import '../widgets/page.dart';
import '../notes/jr/data/subjects.dart';
import '../notes/jr/state/app_state.dart' as jr;
import 'notes_home.dart';
import 'routes.dart';

/// descent of the 16px Nunito strut under an inline `<svg>` (web line box)
const kSvgDescent = 16 * .353;

/// the body's 16px Nunito line box (inline text inside a block without its own font-size)
const kBodyStrut = StrutStyle(fontFamily: kFont, fontSize: 16);

String greeting() {
  final h = highNow().hour;
  return h < 12 ? 'Good Morning' : h < 17 ? 'Good Afternoon' : 'Good Evening';
}

int niceMax(int m) {
  final step = m <= 10 ? 5 : m <= 40 ? 10 : m <= 100 ? 25 : m <= 200 ? 50 : 100;
  return math.max(step, (m / step).ceil() * step);
}

class HomePage extends StatelessWidget {
  const HomePage({super.key, this.controller});
  final ScrollController? controller;
  @override
  Widget build(BuildContext context) {
    final k = Kit.of(context), s = k.s, r = s.repo;
    final st = s.stats();
    final name = s.name ?? 'Student';
    final nQ = r.exams.fold(0, (a, e) => a + e.questions.length);
    final sub = st.fresh
        ? '${thousands(nQ)} questions from ${r.subjects.length} subject${r.subjects.length > 1 ? 's' : ''} are ready — offline.'
        : st.cur > 1
        ? "You're on a ${st.cur}-day streak. Keep it glowing!"
        : "Let's make today count.";
    return PageShell(
      top: const TopBar(title: 'High', sub: 'Grade 9–12 · matric prep & notes'),
      body: ScreenList(
        controller: controller,
        children: Stagger.wrap([
          _Hero(name: name, sub: sub, cta: st.fresh ? 'Start studying' : 'Continue studying'),
          const _Grades(),
          const _Cats(),
          _StatGrid(st: st),
          _Weekly(st: st),
          _Donut(st: st),
          const SectionLabel('Daily mix'),
          const _Daily(),
          const _MistakesCard(),
          const _Recent(),
          const _WeakBanner(),
          const _TutorBanner(),
        ]),
      ),
    );
  }
}

/// `.stagger > *` entrance (.5s, 40 ms steps, max .28 s)
class Stagger extends StatefulWidget implements Delegating {
  const Stagger({super.key, required this.i, required this.child});
  final int i;
  final Widget child;
  @override
  Widget get inner => child;
  static List<Widget> wrap(List<Widget> l) => [for (var i = 0; i < l.length; i++) Stagger(i: i, child: l[i])];
  @override
  State<Stagger> createState() => _StaggerState();
}

class _StaggerState extends State<Stagger> with SingleTickerProviderStateMixin {
  late final AnimationController _c;
  late final double _d = math.min(widget.i, 7) * 40.0;
  @override
  void initState() {
    super.initState();
    _c = AnimationController(vsync: this, duration: Duration(milliseconds: 500 + _d.round()))..forward();
  }

  @override
  void dispose() {
    _c.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) => AnimatedBuilder(
    animation: _c,
    child: widget.child,
    builder: (_, child) {
      final ms = _c.value * (500 + _d) - _d;
      final t = const Cubic(.2, .8, .2, 1).transform((ms / 500).clamp(0.0, 1.0));
      if (t >= 1) return child!;
      return Opacity(opacity: t, child: Transform.translate(offset: Offset(0, 12 * (1 - t)), child: child));
    },
  );
}

/// number that counts up over 800 ms (ease-out cubic), like the web countUp()
class CountUp extends StatefulWidget {
  const CountUp(this.to, {super.key, this.dec = 0, required this.style});
  final num to;
  final int dec;
  final TextStyle style;
  @override
  State<CountUp> createState() => _CountUpState();
}

class _CountUpState extends State<CountUp> with SingleTickerProviderStateMixin {
  late final AnimationController _c = AnimationController(vsync: this, duration: const Duration(milliseconds: 800))..forward();
  @override
  void dispose() {
    _c.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) => AnimatedBuilder(
    animation: _c,
    builder: (_, _) {
      final e = 1 - math.pow(1 - _c.value, 3);
      return Text((widget.to * e).toStringAsFixed(widget.dec), style: widget.style);
    },
  );
}

class _Hero extends StatelessWidget {
  const _Hero({required this.name, required this.sub, required this.cta});
  final String name, sub, cta;
  @override
  Widget build(BuildContext context) {
    final k = Kit.of(context), p = k.p;
    return Padding(
      padding: const EdgeInsets.only(top: 0),
      child: DecoratedBox(
        decoration: k.d.tileWith(p.peach, k.d.heroFill()),
        child: ClipRRect(
          borderRadius: BorderRadius.circular(R.lg),
          child: Stack(
            children: [
              ConstrainedBox(
                constraints: const BoxConstraints(minHeight: 150),
                child: Padding(
                  padding: const EdgeInsets.fromLTRB(6, 10, 16, 0),
                  child: IntrinsicHeight(
                    child: Row(
                      crossAxisAlignment: CrossAxisAlignment.stretch,
                      children: [
                        SizedBox(
                          width: 126,
                          child: Align(
                            alignment: Alignment.bottomLeft,
                            // inline <svg> in a div: the line box adds the font descent (16px Nunito: 5.65) under it
                            child: SizedBox(
                              width: 126,
                              height: 136 + kSvgDescent - 2,
                              child: OverflowBox(
                                alignment: Alignment.topLeft,
                                minWidth: 136,
                                maxWidth: 136,
                                minHeight: 136,
                                maxHeight: 136,
                                child: Transform.translate(offset: const Offset(-4, 0), child: Art('student', palette: p, width: 136, height: 136)),
                              ),
                            ),
                          ),
                        ),
                        const SizedBox(width: 4),
                        Expanded(
                          child: Center(
                            child: Padding(
                              padding: const EdgeInsets.only(bottom: 16),
                              child: Column(
                                mainAxisSize: MainAxisSize.min,
                                crossAxisAlignment: CrossAxisAlignment.start,
                                children: [
                                  const SizedBox(height: 6),
                                  Tx('${greeting()}, $name!', style: ts(20, w900, p.ink, height: 1.2, spacing: -.2)),
                                  const SizedBox(height: 4),
                                  Tx(sub, style: ts(13.5, w700, p.ink2, height: 1.4)),
                                  const SizedBox(height: 11),
                                  Btn(cta, icon: 'play', onTap: () => Routes.continueStudying(context)),
                                ],
                              ),
                            ),
                          ),
                        ),
                      ],
                    ),
                  ),
                ),
              ),
              Positioned(left: 0, right: 0, bottom: 0, height: 12, child: IgnorePointer(child: ColoredBox(color: withA(p.peach.mid, .35)))),
            ],
          ),
        ),
      ),
    );
  }
}

class _Cats extends StatelessWidget implements Spaced {
  const _Cats();
  @override
  EdgeInsets get blockMargin => const EdgeInsets.only(top: 18, bottom: 4);
  @override
  Widget build(BuildContext context) {
    final k = Kit.of(context), p = k.p, s = k.s;
    return Column(
      crossAxisAlignment: CrossAxisAlignment.stretch,
      children: [
        Padding(
          padding: EdgeInsets.fromLTRB(6, bareM(context, this, blockMargin).top, 6, 0),
          child: Row(
            crossAxisAlignment: CrossAxisAlignment.baseline,
            textBaseline: TextBaseline.alphabetic,
            children: [
              Expanded(child: Text('Matric & notes', style: ts(17, w900, p.ink, spacing: -.17))),
              Text('Choose where to study', style: ts(12, w800, p.ink3)),
            ],
          ),
        ),
        // .cats margin 14 0 4 minus the header's -4 bottom margin
        const SizedBox(height: 10),
        for (final c in kCats) ...[
          () {
            final cp = s.catProgress(c.id);
            return CatCard(
              tone: c.tone,
              icon: c.icon,
              title: c.long,
              sub: '${c.blurb}${cp.years.isNotEmpty ? ' · ${cp.years}' : ''}',
              counts: ['${cp.exams} exam${cp.exams == 1 ? '' : 's'}', '${cp.subjects} subject${cp.subjects == 1 ? '' : 's'}', '${thousands(cp.questions)} questions'],
              pct: cp.p.pct,
              status: cp.p.done > 0 ? '${cp.p.pct}% done · ${cp.p.acc}% right' : 'Not started',
              onTap: cp.exams == 0
                  ? null
                  : () {
                      s.setCat(c.id);
                      Routes.examsTab(context);
                    },
            );
          }(),
          const SizedBox(height: 14),
        ],
        CatCard(
          tone: 'blue',
          icon: 'book',
          title: 'Grade 9–12 Notes',
          sub: 'Textbook notes · concept maps · games',
          counts: const ['4 grades', '8 subjects', '29 books'],
          pct: s.notesPct(),
          status: s.notesPct() > 0 ? '${s.notesPct()}% read' : 'Not started',
          onTap: () => HighNav.of(context).tab(HighTab.notes),
        ),
        SizedBox(height: bareM(context, this, blockMargin).bottom),
      ],
    );
  }
}

/// `.tile.cat` big category card
class CatCard extends StatelessWidget {
  const CatCard({super.key, required this.tone, required this.icon, required this.title, required this.sub, required this.counts, required this.pct, required this.status, this.onTap});
  final String tone, icon, title, sub, status;
  final List<String> counts;
  final int pct;
  final VoidCallback? onTap;
  @override
  Widget build(BuildContext context) {
    final k = Kit.of(context), p = k.p, t = k.tone(tone);
    final subC = mix(t.deep, .72, p.ink2);
    return Panel(
      tone: tone,
      radius: R.xl,
      margin: EdgeInsets.zero,
      padding: EdgeInsets.zero,
      clip: true,
      onTap: onTap ?? () {},
      label: 'Open $title',
      child: Stack(
        children: [
          Positioned(
            right: -36,
            top: -44,
            width: 130,
            height: 130,
            child: DecoratedBox(decoration: BoxDecoration(shape: BoxShape.circle, color: Color.fromRGBO(255, 255, 255, p.dark ? .05 : .22))),
          ),
          ConstrainedBox(
            constraints: const BoxConstraints(minHeight: 146),
            child: Padding(
              padding: const EdgeInsets.fromLTRB(16, 16, 16, 14),
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                crossAxisAlignment: CrossAxisAlignment.stretch,
                children: [
                  Row(
                    spacing: 14,
                    children: [
                      Badge(tone, icon, s: 56),
                      Expanded(
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Tx(title, style: ts(21, w900, p.ink, height: 1.15, spacing: -.315), ellipsis: true),
                            const SizedBox(height: 3),
                            Tx(sub, style: ts(12.5, w800, subC, height: 1.35), ellipsis: true),
                          ],
                        ),
                      ),
                    ],
                  ),
                  const SizedBox(height: 11),
                  Wrap(
                    spacing: 6,
                    runSpacing: 6,
                    children: [
                      for (final c in counts)
                        DecoratedBox(
                          decoration: k.d.cnt(t),
                          child: Padding(padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 3), child: Text(c, style: ts(12, w900, t.deep))),
                        ),
                    ],
                  ),
                  const SizedBox(height: 10),
                  Row(
                    spacing: 10,
                    children: [
                      Expanded(child: Bar(pct, tone: tone, height: 10, onTile: true)),
                      Text(status, style: ts(12, w900, t.deep)),
                      DecoratedBox(
                        decoration: k.d.goBtn(t),
                        child: SizedBox(
                          height: 34,
                          child: Padding(
                            padding: const EdgeInsets.fromLTRB(14, 0, 8, 0),
                            child: Row(
                              mainAxisSize: MainAxisSize.min,
                              spacing: 2,
                              children: [Text('Open', style: ts(13.5, w900, t.deep)), Ic('right', size: 18, color: t.deep)],
                            ),
                          ),
                        ),
                      ),
                    ],
                  ),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }
}

class _StatGrid extends StatelessWidget implements Spaced {
  const _StatGrid({required this.st});
  final Stats st;
  @override
  EdgeInsets get blockMargin => const EdgeInsets.symmetric(vertical: 14);
  @override
  Widget build(BuildContext context) {
    final int? accDelta = st.nW >= 5 && st.nP >= 5 ? st.accW! - st.accP! : null;
    final studyH = st.studyAll >= 3600;
    final tiles = <(String, String, String, Object, String, int, String, String)>[
      ('sage', 'check', 'Questions answered', st.answered, '', 0, st.newW > 0 ? '+${st.newW} this week' : st.fresh ? 'Your first one awaits' : 'None yet this week', st.newW > 0 ? '' : 'flat'),
      (
        'peach',
        'target',
        'Accuracy',
        st.acc ?? '—',
        st.acc == null ? '' : '%',
        0,
        accDelta != null ? '${accDelta >= 0 ? '+' : ''}$accDelta pts vs last week' : st.accW != null ? '${st.accW}% this week' : 'Shows after 1 answer',
        accDelta != null && accDelta < 0 ? 'neg' : st.accW == null ? 'flat' : '',
      ),
      ('butter', 'clock', 'Study time', studyH ? st.studyAll / 3600 : jsRound(st.studyAll / 60), studyH ? 'h' : 'm', studyH ? 1 : 0, st.studyW >= 60 ? '+${fmtDur(st.studyW)} this week' : 'Tracked while you practise', st.studyW >= 60 ? '' : 'flat'),
      ('blue', 'flame', 'Current streak', st.cur, st.cur == 1 ? 'day' : 'days', 0, st.cur > 0 ? (st.best > st.cur ? 'in a row · best ${st.best}' : 'in a row · personal best!') : 'Study today to start one', st.cur > 0 ? '' : 'flat'),
    ];
    Widget tile((String, String, String, Object, String, int, String, String) x) {
      final (tone, icon, lbl, v, unit, dec, delta, dc) = x;
      final k = Kit.of(context), p = k.p, t = k.tone(tone);
      final vs = ts(28, w900, p.ink, height: 1.1, spacing: -.56);
      return Panel(
        tone: tone,
        margin: EdgeInsets.zero,
        padding: const EdgeInsets.fromLTRB(14, 14, 14, 13),
        child: ConstrainedBox(
          constraints: const BoxConstraints(minHeight: 132 - 27),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Badge(tone, icon, s: 40),
              const SizedBox(height: 10),
              Text(lbl, style: ts(13, w800, p.ink2)),
              const SizedBox(height: 2),
              Row(
                crossAxisAlignment: CrossAxisAlignment.baseline,
                textBaseline: TextBaseline.alphabetic,
                children: [
                  if (v is num && v != 0) CountUp(v, dec: dec, style: vs) else Text('$v', style: vs, strutStyle: strutOf(vs)),
                  if (unit.isNotEmpty) Padding(padding: const EdgeInsets.only(left: 2), child: Text(unit, style: ts(14, w800, p.ink2))),
                ],
              ),
              const Spacer(),
              Padding(
                padding: const EdgeInsets.only(top: 4),
                child: Text(delta, style: ts(12, w800, dc == 'neg' ? p.peach.deep : dc == 'flat' ? p.ink3 : t.deep)),
              ),
            ],
          ),
        ),
      );
    }

    return Padding(
      padding: bareM(context, this, blockMargin),
      child: Column(
        spacing: 12,
        children: [
          for (var r = 0; r < 2; r++)
            IntrinsicHeight(
              child: Row(
                crossAxisAlignment: CrossAxisAlignment.stretch,
                spacing: 12,
                children: [Expanded(child: tile(tiles[r * 2])), Expanded(child: tile(tiles[r * 2 + 1]))],
              ),
            ),
        ],
      ),
    );
  }
}

class _Weekly extends StatelessWidget implements Spaced {
  const _Weekly({required this.st});
  final Stats st;
  @override
  EdgeInsets get blockMargin => const EdgeInsets.symmetric(vertical: 14);
  static const barT = ['peach', 'butter', 'sage', 'rose', 'blue', 'mint', 'lilac'];
  static const ghost = [34, 58, 42, 74, 48, 64, 38];
  @override
  Widget build(BuildContext context) {
    final k = Kit.of(context), p = k.p;
    final max = niceMax(math.max(st.days.map((d) => d.n).reduce(math.max), 5));
    final lbl = ts(10.5, w800, p.ink3);
    return Panel(
      margin: bareM(context, this, blockMargin),
      child: Stack(
        clipBehavior: Clip.none,
        children: [
          Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              CardHead('Weekly activity', small: 'Questions answered per day', trailing: const PillX('This week', icon: 'cal')),
              SizedBox(
                height: 132,
                child: Stack(
                  clipBehavior: Clip.none,
                  children: [
                    for (final f in const [1.0, .5, 0.0])
                      Positioned(
                        left: 0,
                        right: 0,
                        top: (1 - f) * 132,
                        child: SizedBox(
                          height: 1,
                          child: CustomPaint(painter: DashPainter(p.line)),
                        ),
                      ),
                    for (final f in const [1.0, .5, 0.0])
                      Positioned(
                        left: 0,
                        width: 20,
                        top: (1 - f) * 132 - 8 + 1,
                        child: Text(st.fresh ? '' : '${jsRound(max * f)}', style: lbl, textAlign: TextAlign.right),
                      ),
                    Padding(
                      padding: const EdgeInsets.fromLTRB(26, 0, 2, 0),
                      child: Row(
                        crossAxisAlignment: CrossAxisAlignment.end,
                        spacing: 10,
                        children: [
                          for (var i = 0; i < 7; i++)
                            Expanded(
                              child: () {
                                final d = st.days[i], t = k.tone(barT[i]);
                                final zero = st.fresh || d.n == 0;
                                final pct = st.fresh ? ghost[i] / 100 : d.n > 0 ? math.max(6, 100 * d.n / max) / 100 : .04;
                                return Column(
                                  mainAxisAlignment: MainAxisAlignment.end,
                                  children: [
                                    if (!st.fresh && d.n > 0) Padding(padding: const EdgeInsets.only(bottom: 3), child: Text('${d.n}', style: ts(10.5, w900, p.ink2))),
                                    GrowBar(
                                      i: i,
                                      child: SizedBox(
                                        width: 26,
                                        height: math.max(6, 132 * pct),
                                        child: DecoratedBox(decoration: zero ? k.d.chartBarZero() : k.d.chartBar(t)),
                                      ),
                                    ),
                                  ],
                                );
                              }(),
                            ),
                        ],
                      ),
                    ),
                  ],
                ),
              ),
              Padding(
                padding: const EdgeInsets.fromLTRB(26, 6, 2, 0),
                child: Row(
                  spacing: 10,
                  children: [
                    for (final d in st.days)
                      Expanded(
                        child: Text(d.today ? 'Today' : d.label, textAlign: TextAlign.center, maxLines: 1, softWrap: false, overflow: TextOverflow.visible, style: ts(11.5, w800, d.today ? p.ink : p.ink3)),
                      ),
                  ],
                ),
              ),
            ],
          ),
          if (st.fresh)
            Positioned(
              left: -16,
              right: -16,
              top: -16,
              bottom: -16,
              child: ClipRRect(
                borderRadius: BorderRadius.circular(R.lg),
                child: DecoratedBox(
                  decoration: BoxDecoration(
                    gradient: LinearGradient(
                      begin: Alignment.topCenter,
                      end: Alignment.bottomCenter,
                      colors: [withA(p.surface, 0), withA(p.surface, .88)],
                      stops: const [0, .3],
                    ),
                  ),
                  child: Padding(
                    padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 10),
                    child: Column(
                      mainAxisAlignment: MainAxisAlignment.center,
                      spacing: 4,
                      children: [
                        Text('Your week will bloom here 🌱', textAlign: TextAlign.center, style: ts(14.5, w900, p.ink)),
                        ConstrainedBox(
                          constraints: const BoxConstraints(maxWidth: 260),
                          child: Text("Answer a few questions and each day's activity grows a bar.", textAlign: TextAlign.center, style: ts(12.5, w700, p.ink3)),
                        ),
                      ],
                    ),
                  ),
                ),
              ),
            ),
        ],
      ),
    );
  }
}

/// `.chart .b` grow animation (.8s spring from scaleY 0, 50 ms stagger)
class GrowBar extends StatefulWidget {
  const GrowBar({super.key, required this.i, required this.child});
  final int i;
  final Widget child;
  @override
  State<GrowBar> createState() => _GrowBarState();
}

class _GrowBarState extends State<GrowBar> with SingleTickerProviderStateMixin {
  late final AnimationController _c = AnimationController(vsync: this, duration: Duration(milliseconds: 800 + widget.i * 50))..forward();
  @override
  void dispose() {
    _c.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) => AnimatedBuilder(
    animation: _c,
    child: widget.child,
    builder: (_, child) {
      final d = widget.i * 50.0, ms = _c.value * (800 + d) - d;
      final v = springCurve.transform((ms / 800).clamp(0.0, 1.0));
      if (_c.isCompleted) return child!;
      return Transform(alignment: Alignment.bottomCenter, transform: Matrix4.diagonal3Values(1, v, 1), child: child);
    },
  );
}

/// CSS `border-top: 1.5px dashed` as Chrome draws it at 2x (1px line, ~3px dashes)
class DashPainter extends CustomPainter {
  DashPainter(this.c);
  final Color c;
  @override
  void paint(Canvas canvas, Size size) {
    final pt = Paint()..color = c;
    const dash = 3.2, gap = 1.8;
    for (double x = 0; x < size.width; x += dash + gap) {
      canvas.drawRect(Rect.fromLTWH(x, 0, math.min(dash, size.width - x), 1), pt);
    }
  }

  @override
  bool shouldRepaint(DashPainter o) => o.c != c;
}

class _Donut extends StatelessWidget implements Spaced {
  const _Donut({required this.st});
  final Stats st;
  @override
  EdgeInsets get blockMargin => const EdgeInsets.symmetric(vertical: 14);
  @override
  Widget build(BuildContext context) {
    final k = Kit.of(context), p = k.p, s = k.s, r = s.repo;
    final ansIds = s.answers.keys.where((id) => r.byId.containsKey(id)).toList();
    final bySub = <String, List<String>>{};
    for (final id in ansIds) {
      (bySub[r.byId[id]!.exam.subject] ??= []).add(id);
    }
    var segs = <({String name, int n, String tone})>[];
    var donutSub = '';
    if (bySub.length >= 2) {
      donutSub = 'by subject';
      final l = bySub.entries.toList()..sort((a, b) => b.value.length - a.value.length);
      segs = [for (final e in l) (name: e.key, n: e.value.length, tone: look(e.key).tone)];
    } else if (ansIds.isNotEmpty) {
      final subj = bySub.keys.first;
      donutSub = 'by topic · $subj';
      final g = <String, int>{};
      for (final id in ansIds) {
        final q = r.byId[id]!;
        final pt = r.primaryTopic(q);
        final t = q.topics.map((x) => r.topicParent['$subj|$x']).firstWhere((x) => x != null && x.isNotEmpty, orElse: () => null) ?? (pt != null ? r.topicTitle(subj, pt) : 'Other');
        g[t] = (g[t] ?? 0) + 1;
      }
      final arr = g.entries.toList()..sort((a, b) => b.value - a.value);
      const dT = ['peach', 'butter', 'sage', 'blue', 'lilac'];
      segs = [for (var i = 0; i < math.min(4, arr.length); i++) (name: arr[i].key, n: arr[i].value, tone: dT[i])];
      final rest = arr.skip(4).fold(0, (a, x) => a + x.value);
      if (rest > 0) segs.add((name: 'Other topics', n: rest, tone: 'lilac'));
    }
    if (segs.length > 5) {
      final rr = segs.skip(4).fold(0, (a, x) => a + x.n);
      segs = [...segs.take(4), (name: 'Other', n: rr, tone: 'lilac')];
    }
    final tot = segs.fold(0, (a, x) => a + x.n);
    final empty = ansIds.length < 5;
    final ctr = ts(20, w900, p.ink, height: 1);
    return Panel(
      margin: bareM(context, this, blockMargin),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          CardHead('Practice mix', small: empty ? 'Share of answered questions' : donutSub, trailing: empty ? null : PillX('${ansIds.length} answered')),
          Row(
            spacing: 14,
            children: [
              SizedBox(
                width: 128,
                height: 128,
                child: Stack(
                  children: [
                    Positioned.fill(
                      child: CustomPaint(
                        painter: DonutPainter(empty ? [(1.0, p.surface2)] : [for (final x in segs) (x.n / tot, k.tone(x.tone).mid)], gap: !empty && segs.length > 1),
                      ),
                    ),
                    Center(
                      child: Column(
                        mainAxisSize: MainAxisSize.min,
                        children: [
                          Text(empty ? '🍩' : '${st.acc ?? 0}%', style: ctr, strutStyle: strutOf(ctr)),
                          const SizedBox(height: 3),
                          Text(empty ? 'soon' : 'accuracy', style: ts(10.5, w800, p.ink3, height: 1)),
                        ],
                      ),
                    ),
                  ],
                ),
              ),
              Expanded(
                child: empty
                    ? Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text.rich(
                            TextSpan(
                              children: [
                                TextSpan(text: ansIds.isNotEmpty ? '${5 - ansIds.length} more to go' : 'Answer 5 questions', style: ts(15, w900, p.ink)),
                                const TextSpan(text: '\nto see which topics you practise most — and how you score in each.'),
                              ],
                            ),
                            style: ts(12.5, w800, p.ink2, height: 1.45),
                          ),
                          const SizedBox(height: 4),
                          Row(
                            spacing: 4,
                            children: [for (final t in const ['peach', 'butter', 'sage', 'blue', 'lilac']) _Dot(k.tone(t).mid)],
                          ),
                        ],
                      )
                    : Column(
                        spacing: 8,
                        children: [
                          for (final x in segs)
                            Row(
                              spacing: 8,
                              children: [
                                _Dot(k.tone(x.tone).mid),
                                Expanded(child: Text(x.name, maxLines: 1, softWrap: false, overflow: TextOverflow.ellipsis, style: ts(12.5, w800, p.ink2))),
                                Text('${jsRound(100 * x.n / tot)}%', style: ts(12.5, w900, p.ink)),
                              ],
                            ),
                        ],
                      ),
              ),
            ],
          ),
        ],
      ),
    );
  }
}

class _Dot extends StatelessWidget {
  const _Dot(this.c);
  final Color c;
  @override
  Widget build(BuildContext context) => SizedBox(
    width: 11,
    height: 11,
    child: DecoratedBox(
      decoration: ClayDecoration(
        radius: BorderRadius.circular(6),
        fills: [SolidFill(c)],
        shadows: const [Shadow3.inset(0, 1, 1, 0, Color.fromRGBO(255, 255, 255, .5))],
      ),
    ),
  );
}

/// SVG donut (r 44, stroke 20 in a 120 box, from 12 o'clock, 2.5 gap between segments)
class DonutPainter extends CustomPainter {
  DonutPainter(this.segs, {this.gap = false});
  final List<(double, Color)> segs;
  final bool gap;
  @override
  void paint(Canvas canvas, Size size) {
    final sc = size.width / 120;
    canvas.scale(sc);
    const r = 44.0, c = 2 * math.pi * r;
    final rect = Rect.fromCircle(center: const Offset(60, 60), radius: r);
    var off = 0.0;
    for (final (f, col) in segs) {
      final len = c * f;
      final l = math.max(.1, len - (gap ? 2.5 : 0));
      final pt = Paint()
        ..color = col
        ..style = PaintingStyle.stroke
        ..strokeWidth = 20;
      if (l >= c - .01) {
        canvas.drawCircle(const Offset(60, 60), r, pt);
      } else {
        canvas.drawArc(rect, -math.pi / 2 + off / r, l / r, false, pt);
      }
      off += len;
    }
  }

  @override
  bool shouldRepaint(DonutPainter o) => true;
}

class _Daily extends StatelessWidget implements Spaced {
  const _Daily();
  @override
  EdgeInsets get blockMargin => const EdgeInsets.symmetric(vertical: 14);
  @override
  Widget build(BuildContext context) {
    final k = Kit.of(context), p = k.p, s = k.s;
    final dq = s.dailyQuiz();
    final ids = (dq['ids'] as List).cast<String>();
    final res = (dq['res'] as Map?) ?? const {};
    final done = ids.where((id) => res[id] != null).length, right = ids.where((id) => res[id] == true).length;
    final all = done == ids.length;
    const sh1 = [Shadow(offset: Offset(0, 2), blurRadius: 6, color: Color.fromRGBO(80, 40, 20, .35))];
    const sh2 = [Shadow(offset: Offset(0, 1), blurRadius: 4, color: Color.fromRGBO(80, 40, 20, .4))];
    return Panel(
      margin: bareM(context, this, blockMargin),
      padding: EdgeInsets.zero,
      clip: true,
      onTap: () => Routes.dailyQuiz(context),
      label: 'Daily Quiz',
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          SizedBox(
            height: 156,
            child: Stack(
              children: [
                Positioned.fill(child: Art('desk', palette: p, fit: BoxFit.cover)),
                Positioned(
                  left: 16,
                  right: 16,
                  bottom: 14,
                  child: Row(
                    crossAxisAlignment: CrossAxisAlignment.end,
                    spacing: 10,
                    children: [
                      Expanded(
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Tx('Daily Quiz', style: ts(19, w900, white, height: 1.15).copyWith(shadows: sh1)),
                            const SizedBox(height: 2),
                            Text(
                              '${ids.length} mixed questions${s.repo.subjects.length > 1 ? ' · all subjects' : ' · ${s.repo.subjects.first}'}',
                              style: ts(12.5, w800, withA(white, .95)).copyWith(shadows: sh2),
                            ),
                          ],
                        ),
                      ),
                      PlayBtn(onTap: () => Routes.dailyQuiz(context), size: 46, onArt: true, color: p.coral, label: 'Start the daily quiz'),
                    ],
                  ),
                ),
              ],
            ),
          ),
          Padding(
            padding: const EdgeInsets.fromLTRB(16, 12, 16, 14),
            child: Row(
              spacing: 10,
              children: [
                Badge(all ? 'sage' : 'butter', all ? 'check' : 'shuffle', s: 34),
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      // inline <b> in a 16px block: the line box keeps the 16px strut
                      Text(
                        all ? 'Done today · $right/${ids.length} correct' : done > 0 ? '$done/${ids.length} done — finish your mix' : 'A fresh set every day',
                        style: ts(14, w900, p.ink),
                        strutStyle: kBodyStrut,
                      ),
                      Text(all ? 'A new mix unlocks tomorrow' : 'Your mistakes & unseen questions first', style: ts(12.5, w700, p.ink3)),
                    ],
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}

/// `.row` list row: thumb + two lines + trailing
class ListRow extends StatelessWidget {
  const ListRow({super.key, required this.lead, required this.title, required this.sub, this.trailing, this.border = false, this.onTap});
  final Widget lead;
  final String title, sub;
  final Widget? trailing;
  final bool border;
  final VoidCallback? onTap;
  @override
  Widget build(BuildContext context) {
    final p = Kit.of(context).p;
    Widget w = Padding(
      padding: const EdgeInsets.symmetric(vertical: 10),
      child: Row(
        spacing: 12,
        children: [
          lead,
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(title, maxLines: 1, softWrap: false, overflow: TextOverflow.ellipsis, style: ts(14.5, w900, p.ink)),
                const SizedBox(height: 1),
                Text(sub, maxLines: 1, softWrap: false, overflow: TextOverflow.ellipsis, style: ts(12, w700, p.ink3)),
              ],
            ),
          ),
          ?trailing,
        ],
      ),
    );
    if (onTap != null) w = GestureDetector(behavior: HitTestBehavior.opaque, onTap: onTap, child: w);
    if (!border) return w;
    return DecoratedBox(
      decoration: BoxDecoration(border: Border(top: BorderSide(color: p.line, width: 1))),
      child: Padding(padding: const EdgeInsets.only(top: 1), child: w),
    );
  }
}

class _Recent extends StatelessWidget implements Spaced {
  const _Recent();
  @override
  EdgeInsets get blockMargin => const EdgeInsets.symmetric(vertical: 14);
  @override
  Widget build(BuildContext context) {
    final k = Kit.of(context), s = k.s, r = s.repo;
    final rec = s.recent.where((x) => r.exam.containsKey(x['id'])).take(3).toList();
    return Panel(
      margin: bareM(context, this, blockMargin),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          CardHead('Recently practiced', trailing: PillX('See all', onTap: () => Routes.examsTab(context))),
          if (rec.isEmpty)
            ListRow(
              lead: const Knob(tone: 'lilac', child: Badge('lilac', 'sparkle', s: 34)),
              title: 'Nothing practised yet',
              sub: 'Pick a subject and your exams show up here',
              trailing: PlayBtn(tone: 'lilac', onTap: () => Routes.examsTab(context), label: 'Browse subjects'),
            )
          else
            for (var i = 0; i < rec.length; i++)
              () {
                final e = r.exam[rec[i]['id']]!, l = look(e.subject), pr = s.examProgress(e);
                return ListRow(
                  border: i > 0,
                  lead: Knob(tone: l.tone, child: Badge(l.tone, l.icon, s: 34)),
                  title: '${e.name} · ${yearShort(e.year)}',
                  sub: '${pr.done}/${pr.total} answered${pr.acc != null ? ' · ${pr.acc}% right' : ''} · ${ago((rec[i]['t'] as num?)?.toInt())}',
                  trailing: PlayBtn(tone: l.tone, onTap: () => Routes.resume(context, e.id), label: 'Resume'),
                );
              }(),
        ],
      ),
    );
  }
}

class Banner extends StatelessWidget implements Spaced {
  const Banner({super.key, required this.tone, required this.other, required this.title, required this.sub, required this.btn, required this.onTap, this.margin = const EdgeInsets.fromLTRB(0, 14, 0, 6)});
  final String tone, other, title, sub, btn;
  final VoidCallback onTap;
  final EdgeInsets margin;
  @override
  EdgeInsets get blockMargin => margin;
  @override
  Widget build(BuildContext context) {
    final k = Kit.of(context), p = k.p;
    return Panel(
      tone: tone,
      fills: k.d.bannerFill(k.tone(tone), k.tone(other)),
      margin: bareM(context, this, margin),
      padding: const EdgeInsets.fromLTRB(8, 12, 14, 12),
      onTap: onTap,
      label: title,
      child: Row(
        spacing: 10,
        children: [
          SizedBox(
            width: 62,
            height: 62 + kSvgDescent - 18,
            child: const Stack(clipBehavior: Clip.none, children: [Positioned(left: 0, top: -8, width: 62, height: 62, child: Kokob(width: 62))]),
          ),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Tx(title, style: ts(14, w800, p.ink, height: 1.3)),
                Tx(sub, style: ts(12, w700, p.ink2, height: 1.3)),
              ],
            ),
          ),
          Btn(btn, kind: BtnKind.tone, tone: tone, onTap: onTap, padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 10), fontSize: 13),
        ],
      ),
    );
  }
}

class _WeakBanner extends StatelessWidget implements Spaced {
  const _WeakBanner();
  @override
  EdgeInsets get blockMargin => const EdgeInsets.fromLTRB(0, 14, 0, 6);
  @override
  Widget build(BuildContext context) {
    final s = Kit.of(context).s;
    final n = s.weakTopics().where((t) => t.n >= 2 && t.acc < 70).length;
    return Banner(
      tone: 'sage',
      other: 'mint',
      title: 'Discover weak topics',
      sub: n > 0 ? '$n topic${n > 1 ? 's' : ''} need${n > 1 ? '' : 's'} some love' : 'Find where to focus next',
      btn: 'Explore now',
      onTap: () => Routes.weak(context),
      margin: bareM(context, this, blockMargin),
    );
  }
}

class _TutorBanner extends StatelessWidget implements Spaced {
  const _TutorBanner();
  @override
  EdgeInsets get blockMargin => const EdgeInsets.fromLTRB(0, 14, 0, 6);
  @override
  Widget build(BuildContext context) => Banner(
    tone: 'lilac',
    other: 'blue',
    title: 'Ask Kokob, your tutor',
    sub: 'Offline answers from your exam packs',
    btn: 'Ask now',
    onTap: () => Routes.tutor(context),
    margin: bareM(context, this, blockMargin),
  );
}

/// 2x2 Grade 9–12 puffy clay tiles right under the greeting -> GradePage
class _Grades extends StatelessWidget implements Spaced {
  const _Grades();
  @override
  EdgeInsets get blockMargin => const EdgeInsets.symmetric(vertical: 14);
  @override
  Widget build(BuildContext context) {
    final k = Kit.of(context), p = k.p, repo = k.s.notesRepo, a = jr.AppScope.of(context);
    Widget tile(int g) {
      final tone = gradeTone(g), t = k.tone(tone), books = repo.grade(g), pct = gradePct(a, books);
      return Panel(
        tone: tone,
        margin: EdgeInsets.zero,
        padding: const EdgeInsets.fromLTRB(16, 14, 16, 14),
        onTap: () => HighNav.of(context).open('grade:$g', () => GradePage(grade: g)),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              crossAxisAlignment: CrossAxisAlignment.baseline,
              textBaseline: TextBaseline.alphabetic,
              children: [
                Text('$g', style: ts(46, w900, t.deep, height: 1, spacing: -1.5)),
                const SizedBox(width: 6),
                Text('Grade', style: ts(14, w900, p.ink2)),
              ],
            ),
            const SizedBox(height: 6),
            Text('${books.length} subject${books.length == 1 ? '' : 's'} · $pct%', style: ts(12.5, w800, p.ink2)),
            Padding(padding: const EdgeInsets.only(top: 8), child: Bar(pct, tone: tone, height: 7, onTile: true)),
          ],
        ),
      );
    }

    return Padding(
      padding: bareM(context, this, blockMargin),
      child: Column(
        spacing: 12,
        children: [
          for (final r in const [[9, 10], [11, 12]])
            Row(spacing: 12, children: [for (final g in r) Expanded(child: tile(g))]),
        ],
      ),
    );
  }
}

class _MistakesCard extends StatelessWidget implements Spaced {
  const _MistakesCard();
  @override
  EdgeInsets get blockMargin => const EdgeInsets.symmetric(vertical: 14);
  @override
  Widget build(BuildContext context) {
    final k = Kit.of(context), p = k.p, s = k.s;
    final n = s.mistakes.where(s.repo.byId.containsKey).length, b = s.bookmarks.where(s.repo.byId.containsKey).length;
    return Panel(
      margin: bareM(context, this, blockMargin),
      padding: const EdgeInsets.all(14),
      onTap: () => Routes.mistakes(context),
      child: Row(
        spacing: 12,
        children: [
          const Badge('peach', 'repeat', s: 42),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text('Mistakes & bookmarks', style: ts(15, w900, p.ink)),
                Text('$n to retry · $b bookmarked', style: ts(12.5, w700, p.ink2)),
              ],
            ),
          ),
          Ic('right', size: 20, color: p.ink3),
        ],
      ),
    );
  }
}
