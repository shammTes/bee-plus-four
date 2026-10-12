// Study Coach exercises: 4-7-8 breathing, study timer (Pomodoro), 2-minute start, "change the thought"
// worksheet, review planner (spaced repetition) and "my goal". Timers tick once a second (breathing: 10×/s, one
// small CustomPaint), and only while the page is open.
import 'dart:async';
import 'dart:math' as math;

import 'package:flutter/widgets.dart';

import '../l10n.dart';
import '../state/app_state.dart';
import '../theme/tokens.dart';
import '../widgets/art.dart';
import '../widgets/kit.dart';
import '../widgets/page.dart';

String _l(BuildContext c, String k, [Map<String, Object>? v]) => highLabel(Kit.of(c).s.lang, k, v);

const kTools = ['breath478', 'pomodoro', 'twomin', 'reframe', 'spaced', 'goal'];

String toolTitle(String k) => switch (k) {
  'breath478' => 'Calm breathing',
  'pomodoro' => 'Study timer',
  'twomin' => '2-minute start',
  'reframe' => 'Change the thought',
  'spaced' => 'Review planner',
  'goal' => 'My goal',
  _ => k,
};
String toolIcon(String k) => switch (k) {
  'breath478' => 'wind',
  'pomodoro' => 'timer',
  'twomin' => 'play',
  'reframe' => 'chat',
  'spaced' => 'cal',
  'goal' => 'target',
  _ => 'sparkle',
};
String toolTone(String k) => switch (k) {
  'breath478' => 'mint',
  'pomodoro' => 'peach',
  'twomin' => 'butter',
  'reframe' => 'rose',
  'spaced' => 'blue',
  'goal' => 'sage',
  _ => 'lilac',
};

void openTool(BuildContext c, String k) => HighNav.of(c).open(
  'tool:$k',
  () => switch (k) {
    'breath478' => const BreathPage(),
    'pomodoro' => const TimerPage(),
    'twomin' => const TimerPage(twoMin: true),
    'reframe' => const ReframePage(),
    'spaced' => const ReviewPlannerPage(),
    _ => const GoalPage(),
  },
);

Widget _page(BuildContext context, String kind, String sub, List<Widget> children) => PageShell(
  top: TopBar(title: toolTitle(kind), sub: sub, onBack: HighNav.of(context).back, tab: false),
  body: ScreenList(children: children),
);

String mmss(int s) => '${(s ~/ 60).toString().padLeft(2, '0')}:${(s % 60).toString().padLeft(2, '0')}';

/// ring + big text in the middle
class _Ring extends CustomPainter {
  _Ring(this.f, this.track, this.fill, {this.scale = 1});
  final double f, scale;
  final Color track, fill;
  @override
  void paint(Canvas c, Size s) {
    final o = s.center(Offset.zero), r = s.shortestSide / 2 - 8;
    c.drawCircle(o, r * .78 * scale, Paint()..color = fill.withValues(alpha: .18));
    final st = Paint()
      ..style = PaintingStyle.stroke
      ..strokeWidth = 12
      ..strokeCap = StrokeCap.round;
    c.drawCircle(o, r, st..color = track);
    c.drawArc(Rect.fromCircle(center: o, radius: r), -math.pi / 2, 2 * math.pi * f.clamp(0, 1), false, st..color = fill);
  }

  @override
  bool shouldRepaint(_Ring o) => o.f != f || o.scale != scale || o.fill != fill || o.track != track;
}

Widget _ringBox(BuildContext context, double f, Color fill, String big, String small, {double scale = 1}) {
  final p = Kit.of(context).p;
  return Center(
    child: SizedBox(
      width: 240,
      height: 240,
      child: CustomPaint(
        painter: _Ring(f, p.surface2, fill, scale: scale),
        child: Center(
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              Text(big, style: ts(40, w900, p.ink, spacing: -1)),
              Text(small, textAlign: TextAlign.center, style: ts(14, w800, p.ink2)),
            ],
          ),
        ),
      ),
    ),
  );
}

// ---------------------------------------------------------------- 4-7-8 breathing
class BreathPage extends StatefulWidget {
  const BreathPage({super.key});
  @override
  State<BreathPage> createState() => _BreathPageState();
}

class _BreathPageState extends State<BreathPage> {
  static const phases = [(4, 'Breathe in'), (7, 'Hold'), (8, 'Breathe out')];
  static const rounds = 4;
  Timer? _t;
  int _ticks = 0; // tenths of a second since start
  bool get _on => _t != null;
  int get _cycle => 190; // 19 s per round

  void _toggle() {
    if (_on) {
      _t!.cancel();
      setState(() => _t = null);
      return;
    }
    setState(() {
      _ticks = 0;
      _t = Timer.periodic(const Duration(milliseconds: 100), (_) {
        if (!mounted) return;
        setState(() => _ticks++);
        if (_ticks >= _cycle * rounds) {
          _t?.cancel();
          setState(() => _t = null);
        }
      });
    });
  }

  @override
  void dispose() {
    _t?.cancel();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final k = Kit.of(context), p = k.p, t = k.tone('mint');
    final done = !_on && _ticks >= _cycle * rounds;
    var inRound = _ticks % _cycle, ph = 0;
    while (ph < 2 && inRound >= phases[ph].$1 * 10) {
      inRound -= phases[ph].$1 * 10;
      ph++;
    }
    final len = phases[ph].$1 * 10, frac = inRound / len;
    final left = ((len - inRound) / 10).ceil();
    // circle grows while breathing in, stays while holding, shrinks while breathing out
    final scale = !_on
        ? .7
        : ph == 0
        ? .6 + .4 * frac
        : ph == 1
        ? 1.0
        : 1 - .4 * frac;
    final round = math.min(rounds, _ticks ~/ _cycle + 1);
    return _page(context, 'breath478', 'In 4 · hold 7 · out 8', [
      Panel(
        margin: const EdgeInsets.only(top: 8),
        child: Column(
          spacing: 14,
          children: [
            _ringBox(
              context,
              _on ? frac : (done ? 1 : 0),
              t.deep,
              _on ? '$left' : (done ? '✓' : '4-7-8'),
              _on ? '${phases[ph].$2}\nRound $round of $rounds' : (done ? _l(context, 'wellDone') : 'Sit up. Relax your shoulders.'),
              scale: scale,
            ),
            Btn(
              _on ? _l(context, 'stop') : (done ? _l(context, 'doAgain') : _l(context, 'startTool')),
              icon: _on ? 'x' : 'play',
              kind: BtnKind.tone,
              tone: 'mint',
              block: true,
              onTap: _toggle,
            ),
          ],
        ),
      ),
      Panel(
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          spacing: 6,
          children: [
            Text('How to do it', style: ts(15, w900, p.ink)),
            for (final x in const [
              'Breathe in through your nose. Count to 4.',
              'Hold your breath. Count to 7.',
              'Breathe out slowly through your mouth. Count to 8.',
              'Do this 4 times.',
              'Feel dizzy? Stop and breathe normally.',
            ])
              Text('• $x', style: ts(14, w700, p.ink2, height: 1.4)),
          ],
        ),
      ),
    ]);
  }
}

// ---------------------------------------------------------------- study timer / 2-minute start
class TimerPage extends StatefulWidget {
  const TimerPage({super.key, this.twoMin = false});
  final bool twoMin;
  @override
  State<TimerPage> createState() => _TimerPageState();
}

class _TimerPageState extends State<TimerPage> {
  static const modes = [('focus', 'Study', 25), ('short', 'Short break', 5), ('long', 'Long break', 15)];
  late int _mode = 0;
  late int _total = widget.twoMin ? 120 : 25 * 60;
  late int _left = _total;
  int _rounds = 0;
  Timer? _t;
  final _task = TextEditingController();

  void _set(int m) {
    _t?.cancel();
    setState(() {
      _t = null;
      _mode = m;
      _total = modes[m].$3 * 60;
      _left = _total;
    });
  }

  void _start() {
    if (_t != null) {
      _t!.cancel();
      setState(() => _t = null);
      return;
    }
    if (_left == 0) _left = _total;
    setState(() {
      _t = Timer.periodic(const Duration(seconds: 1), (_) {
        if (!mounted) return;
        setState(() => _left--);
        if (_left <= 0) {
          _t?.cancel();
          setState(() {
            _t = null;
            _left = 0;
            if (!widget.twoMin && _mode == 0) _rounds++;
          });
        }
      });
    });
  }

  @override
  void dispose() {
    _t?.cancel();
    _task.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final k = Kit.of(context), p = k.p, tone = widget.twoMin ? 'butter' : (_mode == 0 ? 'peach' : 'mint');
    final t = k.tone(tone), done = _left == 0;
    final kind = widget.twoMin ? 'twomin' : 'pomodoro';
    return _page(context, kind, widget.twoMin ? 'Just start. Only 2 minutes.' : '25 minutes study, 5 minutes rest', [
      if (widget.twoMin)
        Panel(
          margin: const EdgeInsets.only(top: 8, bottom: 4),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            spacing: 8,
            children: [
              Text('What will you start?', style: ts(15, w900, p.ink)),
              Field(controller: _task, placeholder: 'e.g. 5 maths questions', maxLength: 60),
            ],
          ),
        )
      else
        Blk(
          margin: const EdgeInsets.only(top: 8, bottom: 4),
          child: Row(
            spacing: 8,
            children: [
              for (var i = 0; i < modes.length; i++)
                Expanded(
                  child: ChipX(modes[i].$2, small: true, on: _mode == i, onTap: () => _set(i)),
                ),
            ],
          ),
        ),
      Panel(
        child: Column(
          spacing: 14,
          children: [
            _ringBox(
              context,
              1 - _left / _total,
              t.deep,
              done ? '✓' : mmss(_left),
              done
                  ? (widget.twoMin ? 'You started! Keep going?' : (_mode == 0 ? 'Time for a break.' : 'Ready to study again.'))
                  : (_t == null ? 'Phone away. Ready?' : (widget.twoMin || _mode == 0 ? 'Focus. One task only.' : 'Rest. Stand up, drink water.')),
            ),
            Btn(
              _t != null ? _l(context, 'pause') : (done ? _l(context, 'doAgain') : _l(context, 'startTool')),
              icon: _t != null ? 'x' : 'play',
              kind: BtnKind.tone,
              tone: tone,
              block: true,
              onTap: _start,
            ),
            if (widget.twoMin && done)
              Btn('Keep going: 25 minutes', icon: 'timer', kind: BtnKind.soft, block: true, onTap: () => openTool(context, 'pomodoro')),
            if (!widget.twoMin) Text('Study rounds today: $_rounds', style: ts(13, w800, p.ink3)),
          ],
        ),
      ),
      Panel(
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          spacing: 6,
          children: [
            Text(widget.twoMin ? 'Why 2 minutes?' : 'How it works', style: ts(15, w900, p.ink)),
            for (final x
                in widget.twoMin
                    ? const [
                        'Starting is the hardest part.',
                        'Two minutes feels easy.',
                        'When the time ends, you may stop.',
                        'Most days, you will want to go on.',
                      ]
                    : const [
                        'Study for 25 minutes. One task only.',
                        'Rest for 5 minutes.',
                        'After 4 rounds, rest for 15 minutes.',
                        'Keep this page open while the timer runs.',
                      ])
              Text('• $x', style: ts(14, w700, p.ink2, height: 1.4)),
          ],
        ),
      ),
    ]);
  }
}

// ---------------------------------------------------------------- change the thought (reframing)
class ReframePage extends StatefulWidget {
  const ReframePage({super.key});
  @override
  State<ReframePage> createState() => _ReframePageState();
}

class _ReframePageState extends State<ReframePage> {
  static const asks = [
    ('The bad thought', 'e.g. I am stupid at maths'),
    ('Is it 100% true? What shows it is not?', 'e.g. I got 7 out of 10 last week'),
    ('What would you tell a friend?', 'e.g. You can learn this with practice'),
    ('A fairer thought', 'e.g. Maths is hard for me, and I am getting better'),
  ];
  final _c = [for (final _ in asks) TextEditingController()];
  @override
  void dispose() {
    for (final c in _c) {
      c.dispose();
    }
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final k = Kit.of(context), p = k.p, s = k.s;
    final saved = [
      for (final x in s.coachGet<List>('reframe') ?? const [])
        if (x is Map) x,
    ];
    return _page(context, 'reframe', 'Catch it. Check it. Change it.', [
      Panel(
        margin: const EdgeInsets.only(top: 8),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          spacing: 8,
          children: [
            for (var i = 0; i < asks.length; i++) ...[
              Text('${i + 1}. ${asks[i].$1}', style: ts(14, w900, p.ink)),
              Field(controller: _c[i], placeholder: asks[i].$2, maxLength: 120),
              const SizedBox(height: 4),
            ],
            Btn(
              _l(context, 'saveIt'),
              icon: 'check',
              kind: BtnKind.tone,
              tone: 'rose',
              block: true,
              onTap: () {
                if (_c[0].text.trim().isEmpty || _c[3].text.trim().isEmpty) {
                  return;
                }
                s.coachSet(
                  'reframe',
                  [
                    {
                      't': nowMs(),
                      'a': [for (final c in _c) c.text.trim()],
                    },
                    ...saved,
                  ].take(20).toList(),
                );
                for (final c in _c) {
                  c.clear();
                }
                FocusScope.of(context).unfocus();
              },
            ),
            Text('Fill in 1 and 4 to save.', style: ts(12, w700, p.ink3)),
          ],
        ),
      ),
      if (saved.isNotEmpty) SectionLabel('My changed thoughts', n: saved.length),
      for (final x in saved)
        Panel(
          margin: const EdgeInsets.only(top: 10),
          padding: const EdgeInsets.all(14),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            spacing: 4,
            children: [
              Text((x['a'] as List)[0] as String, style: ts(13.5, w700, p.ink3, decoration: TextDecoration.lineThrough)),
              Row(
                spacing: 6,
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Ic('right', size: 16, color: p.sage.deep),
                  Expanded(child: Text((x['a'] as List)[3] as String, style: ts(14.5, w900, p.ink, height: 1.35))),
                ],
              ),
            ],
          ),
        ),
    ]);
  }
}

// ---------------------------------------------------------------- review planner (spaced repetition)
const kReviewGaps = [1, 3, 7, 14, 30];
const _wd = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];
const _mo = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
String shortDate(DateTime d) => '${_wd[d.weekday - 1]} ${d.day} ${_mo[d.month - 1]}';
DateTime _day(DateTime d) => DateTime(d.year, d.month, d.day);

class ReviewPlannerPage extends StatefulWidget {
  const ReviewPlannerPage({super.key});
  @override
  State<ReviewPlannerPage> createState() => _ReviewPlannerPageState();
}

class _ReviewPlannerPageState extends State<ReviewPlannerPage> {
  final _c = TextEditingController();
  @override
  void dispose() {
    _c.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final k = Kit.of(context), p = k.p, s = k.s;
    final plans = [
      for (final x in s.coachGet<List>('spaced') ?? const [])
        if (x is Map) Map<String, dynamic>.from(x),
    ];
    final today = _day(highNow());
    DateTime? next(Map<String, dynamic> x) {
      final n = (x['n'] as num).toInt();
      if (n >= kReviewGaps.length) return null;
      return _day(DateTime.fromMillisecondsSinceEpoch((x['d'] as num).toInt())).add(Duration(days: kReviewGaps[n]));
    }

    plans.sort((a, b) => (next(a) ?? DateTime(9999)).compareTo(next(b) ?? DateTime(9999)));
    void save(List<Map<String, dynamic>> l) => s.coachSet('spaced', l);
    return _page(context, 'spaced', 'Look again after 1, 3, 7, 14 and 30 days', [
      Panel(
        margin: const EdgeInsets.only(top: 8),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          spacing: 8,
          children: [
            Text('Spaced review means: look at it again, a few days apart. This makes it stick.', style: ts(13.5, w700, p.ink2, height: 1.4)),
            Text('What did you study today?', style: ts(14, w900, p.ink)),
            Field(controller: _c, placeholder: 'e.g. Biology unit 2: the cell', maxLength: 60),
            Btn(
              'Add to my plan',
              icon: 'cal',
              kind: BtnKind.tone,
              tone: 'blue',
              block: true,
              onTap: () {
                final t = _c.text.trim();
                if (t.isEmpty) return;
                save(
                  [
                    {'t': t, 'd': today.millisecondsSinceEpoch, 'n': 0},
                    ...plans,
                  ].take(40).toList(),
                );
                _c.clear();
                FocusScope.of(context).unfocus();
              },
            ),
          ],
        ),
      ),
      if (plans.isNotEmpty) SectionLabel('My reviews', n: plans.length),
      for (final x in plans)
        () {
          final nx = next(x), n = (x['n'] as num).toInt();
          final due = nx != null && !nx.isAfter(today);
          final when = nx == null
              ? 'Learned ✓'
              : due
              ? 'Review today'
              : 'Next: ${shortDate(nx)}';
          return Panel(
            tone: due ? 'blue' : null,
            margin: const EdgeInsets.only(top: 10),
            padding: const EdgeInsets.fromLTRB(14, 12, 10, 12),
            child: Row(
              spacing: 10,
              children: [
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(x['t'] as String, style: ts(14.5, w900, p.ink), maxLines: 2, overflow: TextOverflow.ellipsis),
                      Text('$when · $n of ${kReviewGaps.length} done', style: ts(12.5, w800, due ? p.blue.deep : p.ink3)),
                    ],
                  ),
                ),
                if (nx != null)
                  Btn(
                    'Done',
                    kind: due ? BtnKind.tone : BtnKind.soft,
                    tone: 'blue',
                    fontSize: 13,
                    padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
                    onTap: () {
                      save([
                        for (final y in plans) identical(y, x) ? {...y, 'n': n + 1, 'd': y['d']} : y,
                      ]);
                    },
                  ),
                CBtn(
                  'x',
                  size: 34,
                  label: 'Remove',
                  onTap: () => save([
                    for (final y in plans)
                      if (!identical(y, x)) y,
                  ]),
                ),
              ],
            ),
          );
        }(),
    ]);
  }
}

// ---------------------------------------------------------------- my goal
class GoalPage extends StatefulWidget {
  const GoalPage({super.key});
  @override
  State<GoalPage> createState() => _GoalPageState();
}

class _GoalPageState extends State<GoalPage> {
  static const asks = [
    ('why', 'Why do I study?', 'e.g. I want to be a nurse and help my village'),
    ('goal', 'My goal. What, and by when?', 'e.g. 70% in the next maths test, by 30 Nov'),
    ('step', 'My first small step', 'e.g. 10 questions from unit 3 today'),
  ];
  late final Map<String, TextEditingController> _c;
  @override
  void initState() {
    super.initState();
    final g = HighScope.read(context).coachGet<Map>('goal') ?? const {};
    _c = {for (final a in asks) a.$1: TextEditingController(text: (g[a.$1] as String?) ?? '')};
  }

  @override
  void dispose() {
    for (final c in _c.values) {
      c.dispose();
    }
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final k = Kit.of(context), p = k.p, s = k.s;
    final saved = s.coachGet<Map>('goal');
    return _page(context, 'goal', 'Small, clear, with a date', [
      Panel(
        margin: const EdgeInsets.only(top: 8),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          spacing: 8,
          children: [
            for (final a in asks) ...[
              Text(a.$2, style: ts(14, w900, p.ink)),
              Field(controller: _c[a.$1], placeholder: a.$3, maxLength: 100),
              const SizedBox(height: 4),
            ],
            Btn(
              _l(context, 'saveIt'),
              icon: 'check',
              kind: BtnKind.tone,
              tone: 'sage',
              block: true,
              onTap: () {
                s.coachSet('goal', {for (final e in _c.entries) e.key: e.value.text.trim(), 't': nowMs()});
                FocusScope.of(context).unfocus();
              },
            ),
            if (saved != null) Text('Saved. Look at it every Sunday.', style: ts(12.5, w800, p.sage.deep)),
          ],
        ),
      ),
      Panel(
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          spacing: 6,
          children: [
            Text('A good goal is…', style: ts(15, w900, p.ink)),
            for (final x in const [
              'Clear: "70% in maths", not "do better".',
              'Easy to check: a mark or a number.',
              'Hard, but possible.',
              'Important to you.',
              'With a date.',
            ])
              Text('• $x', style: ts(14, w700, p.ink2, height: 1.4)),
          ],
        ),
      ),
    ]);
  }
}
