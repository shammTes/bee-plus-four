// First-run coach marks: dark 60 % scrim with a circular spotlight cut around the real widget, a white tooltip
// bubble tethered below (or above) with a small pointer, "Step X of N" dots, accent Next and a quiet Skip.
// One CustomPaint + one tween per step change: cheap on low-end phones (no blur, no saveLayer).
import 'dart:math' as math;

import 'package:flutter/widgets.dart';

import '../state/app_state.dart';
import '../theme/tokens.dart';
import 'kit.dart';
import 'page.dart';

/// Keys on the real widgets the coach marks point at. Each is attached to exactly one mounted widget.
abstract final class CoachKeys {
  static final grade = GlobalKey(debugLabel: 'coach:grade');
  static final resources = GlobalKey(debugLabel: 'coach:resources');
  static final settings = GlobalKey(debugLabel: 'coach:settings');
  static final _tabs = <HighTab, GlobalKey>{};
  static GlobalKey tab(HighTab t) => _tabs[t] ??= GlobalKey(debugLabel: 'coach:${t.name}');
}

class CoachStep {
  const CoachStep(this.title, this.body, [this.target]);
  final String title, body;
  final GlobalKey Function()? target; // null = centred welcome card
}

final kCoachSteps = <CoachStep>[
  const CoachStep('Welcome to 4', 'Grade 9–12 notes, practice and matric prep. Everything works offline.'),
  CoachStep('Pick your grade', 'Each grade opens its subjects, units and notes.', () => CoachKeys.grade),
  CoachStep('Notes', 'Every textbook, unit by unit, with memory tricks and quick games.', () => CoachKeys.tab(HighTab.notes)),
  CoachStep('Exercise', 'Practice questions sorted by grade, subject and unit.', () => CoachKeys.tab(HighTab.exercise)),
  CoachStep('Matric', 'Past matric and model exams, each with answers and worked steps.', () => CoachKeys.tab(HighTab.matric)),
  CoachStep('Tutor', 'Ask about any topic and 4 explains it from the books on this phone.', () => CoachKeys.tab(HighTab.tutor)),
  CoachStep('Extra resources', 'PDFs, videos and reels from your teacher. Copy them in, then tap Refresh.', () => CoachKeys.resources),
  CoachStep('Settings', 'Your name, theme, updates, and this tour again.', () => CoachKeys.settings),
];

class CoachMarks extends StatefulWidget {
  const CoachMarks({super.key, this.steps});
  final List<CoachStep>? steps;
  @override
  State<CoachMarks> createState() => _CoachMarksState();
}

class _CoachMarksState extends State<CoachMarks> {
  List<CoachStep> get _all => widget.steps ?? kCoachSteps;
  Rect? _hole; // spotlight circle bounds in this widget's coordinates
  int _shownFor = -2;
  List<int> _live = const []; // steps whose target exists right now

  @override
  Widget build(BuildContext context) {
    final s = HighScope.of(context);
    final step = s.tourStep;
    if (step == null) return const SizedBox.shrink();
    if (step != _shownFor) {
      _shownFor = step;
      WidgetsBinding.instance.addPostFrameCallback((_) => _locate(s));
    }
    final p = Kit.of(context).p;
    final live = _live.isEmpty ? [for (var i = 0; i < _all.length; i++) i] : _live;
    final i = math.max(0, step), pos = live.indexOf(i).clamp(0, live.length - 1);
    final c = _all[i.clamp(0, _all.length - 1)];
    final last = pos == live.length - 1;
    return LayoutBuilder(
      builder: (context, box) {
        final size = box.biggest;
        final hole = c.target == null ? null : _hole;
        // circle centre/radius animate between steps (one tween, ~320 ms)
        return TweenAnimationBuilder<Rect?>(
          tween: RectTween(end: hole ?? Rect.fromCircle(center: size.center(Offset.zero), radius: 0)),
          duration: const Duration(milliseconds: 320),
          curve: Curves.easeOutCubic,
          builder: (context, r, _) {
            final rr = r ?? Rect.zero;
            return Stack(
              children: [
                // absorbs every tap: the tour is a guided look, not a gate on the real buttons
                Positioned.fill(
                  child: GestureDetector(
                    behavior: HitTestBehavior.opaque,
                    onTap: () {},
                    child: CustomPaint(painter: _ScrimPainter(rr)),
                  ),
                ),
                _Bubble(
                  size: size,
                  hole: hole == null ? null : rr,
                  title: c.title,
                  body: c.body,
                  index: pos,
                  count: live.length,
                  last: last,
                  p: p,
                  onNext: () => _next(s, live, pos),
                  onSkip: s.skipTour,
                ),
              ],
            );
          },
        );
      },
    );
  }

  void _next(HighState s, List<int> live, int pos) {
    if (pos >= live.length - 1) {
      s.skipTour(); // done
      return;
    }
    s.tourStep = live[pos + 1] - 1;
    s.coachNext(_all.length);
  }

  /// Finds the current target on screen (scrolling it into view first) and sizes the circle around it.
  Future<void> _locate(HighState s) async {
    if (!mounted) return;
    final nav = HighNav.of(context);
    if (nav.current != HighTab.home) nav.tab(HighTab.home);
    _live = [for (var i = 0; i < _all.length; i++) if (_all[i].target == null || _all[i].target!().currentContext != null) i];
    var step = math.max(0, s.tourStep ?? 0);
    if (!_live.contains(step)) {
      final nxt = _live.where((x) => x > step);
      if (nxt.isEmpty) return s.skipTour();
      s.tourStep = nxt.first;
      step = nxt.first;
      _shownFor = step;
    }
    final t = _all[step].target?.call();
    final ctx = t?.currentContext;
    if (ctx != null && ctx.mounted) {
      await Scrollable.ensureVisible(ctx, alignment: .35, duration: const Duration(milliseconds: 250));
      await Future<void>.delayed(const Duration(milliseconds: 16));
    }
    if (!mounted) return;
    final me = context.findRenderObject() as RenderBox?, ro = t?.currentContext?.findRenderObject() as RenderBox?;
    Rect? hole;
    if (me != null && ro != null && ro.hasSize && ro.attached) {
      final tl = ro.localToGlobal(Offset.zero, ancestor: me);
      final rect = tl & ro.size;
      // wide targets (cards) get a circle on their centre, capped so the scrim still frames it
      final r = math.min(rect.longestSide / 2 + 10, math.max(rect.shortestSide / 2 + 16, me.size.width * .3));
      hole = Rect.fromCircle(center: rect.center, radius: r);
    }
    setState(() => _hole = hole);
  }
}

class _ScrimPainter extends CustomPainter {
  _ScrimPainter(this.hole);
  final Rect hole;
  @override
  void paint(Canvas c, Size s) {
    final path = Path()
      ..fillType = PathFillType.evenOdd
      ..addRect(Offset.zero & s);
    if (hole.width > 1) path.addOval(hole);
    c.drawPath(path, Paint()..color = const Color(0x99000000)); // 60 %
    if (hole.width > 1) {
      c.drawCircle(
        hole.center,
        hole.width / 2,
        Paint()
          ..style = PaintingStyle.stroke
          ..strokeWidth = 2
          ..color = const Color(0x66FFFFFF),
      );
    }
  }

  @override
  bool shouldRepaint(_ScrimPainter o) => o.hole != hole;
}

class _Bubble extends StatelessWidget {
  const _Bubble({required this.size, required this.hole, required this.title, required this.body, required this.index, required this.count, required this.last, required this.p, required this.onNext, required this.onSkip});
  final Size size;
  final Rect? hole;
  final String title, body;
  final int index, count;
  final bool last;
  final Palette p;
  final VoidCallback onNext, onSkip;

  static const _w = 320.0, _gap = 14.0, _arrow = 9.0;

  @override
  Widget build(BuildContext context) {
    final w = math.min(_w, size.width - 32);
    final pad = MediaQuery.paddingOf(context);
    const ink = Color(0xFF1C1C1E), ink2 = Color(0xFF6B6B70), accent = Color(0xFFE2664A);
    final card = Container(
      width: w,
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: const Color(0xFFFFFFFF),
        borderRadius: BorderRadius.circular(18),
        boxShadow: const [BoxShadow(color: Color(0x33000000), blurRadius: 24, offset: Offset(0, 8))],
      ),
      child: Column(
        mainAxisSize: MainAxisSize.min,
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(title, style: ts(17, w900, ink, spacing: -.2)),
          const SizedBox(height: 4),
          Text(body, style: ts(14, w700, ink2, height: 1.35)),
          const SizedBox(height: 14),
          Row(
            children: [
              for (var i = 0; i < count; i++)
                AnimatedContainer(
                  duration: const Duration(milliseconds: 220),
                  margin: const EdgeInsets.only(right: 5),
                  width: i == index ? 16 : 6,
                  height: 6,
                  decoration: BoxDecoration(color: i == index ? accent : const Color(0x22000000), borderRadius: BorderRadius.circular(3)),
                ),
              const SizedBox(width: 6),
              Expanded(child: Text('Step ${index + 1} of $count', style: ts(12, w800, ink2))),
              if (!last)
                GestureDetector(
                  onTap: onSkip,
                  behavior: HitTestBehavior.opaque,
                  child: Padding(padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 8), child: Text('Skip', style: ts(13.5, w800, ink2))),
                ),
              GestureDetector(
                onTap: onNext,
                child: Container(
                  padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 9),
                  decoration: BoxDecoration(color: accent, borderRadius: BorderRadius.circular(99)),
                  child: Text(last ? 'Done' : 'Next', style: ts(14, w900, const Color(0xFFFFFFFF))),
                ),
              ),
            ],
          ),
        ],
      ),
    );
    final h = hole;
    if (h == null) return Positioned.fill(child: Center(child: card));
    // below the circle when there is room for ~190 px, else above; pointer aims at the circle centre
    final below = h.bottom + _gap + 190 < size.height - pad.bottom;
    final left = (h.center.dx - w / 2).clamp(16.0, size.width - w - 16);
    final ax = (h.center.dx - left).clamp(24.0, w - 24);
    final pointer = CustomPaint(size: const Size(2 * _arrow, _arrow), painter: _Arrow(up: below));
    return Positioned(
      left: left,
      top: below ? h.bottom + _gap : null,
      bottom: below ? null : size.height - h.top + _gap,
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        mainAxisSize: MainAxisSize.min,
        children: [
          if (below) Padding(padding: EdgeInsets.only(left: ax - _arrow), child: pointer),
          card,
          if (!below) Padding(padding: EdgeInsets.only(left: ax - _arrow), child: pointer),
        ],
      ),
    );
  }
}

class _Arrow extends CustomPainter {
  _Arrow({required this.up});
  final bool up;
  @override
  void paint(Canvas c, Size s) {
    final path = up
        ? (Path()..moveTo(0, s.height)..lineTo(s.width / 2, 0)..lineTo(s.width, s.height)..close())
        : (Path()..moveTo(0, 0)..lineTo(s.width / 2, s.height)..lineTo(s.width, 0)..close());
    c.drawPath(path, Paint()..color = const Color(0xFFFFFFFF));
  }

  @override
  bool shouldRepaint(_Arrow o) => o.up != up;
}
