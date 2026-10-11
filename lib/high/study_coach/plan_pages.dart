// Study check-in → friendly profile (top 2 areas) → optional 30-day plan: one short lesson and one tiny action a
// day, "I did it", streak, weekly look-back, and the same check-in again on Day 30 to see the change.
// Everything stays on the phone (HighState.coach: 'checks', 'plan'). The "how do you feel" answer is never saved.
import 'package:flutter/widgets.dart';

import '../state/app_state.dart';
import '../theme/tokens.dart';
import '../widgets/art.dart';
import '../widgets/kit.dart';
import '../widgets/page.dart';
import 'coach_pages.dart';
import 'coach_tools.dart';
import 'plan_data.dart';

void openCheckIn(BuildContext c, {bool recheck = false}) => HighNav.of(c).push(CheckInPage(recheck: recheck));
void openPlan(BuildContext c) => HighNav.of(c).open('coach:plan', () => const PlanPage());

Map<String, int> _ints(Object? m) => {for (final e in (m as Map? ?? const {}).entries) '${e.key}': (e.value as num).toInt()};

/// the latest saved check-in scores, or null
Map<String, int>? lastCheck(HighState s) {
  final l = s.coachGet<List>('checks');
  return l == null || l.isEmpty ? null : _ints((l.first as Map)['sc']);
}

PlanRun? planOf(HighState s) {
  final m = s.coachGet<Map>('plan');
  return m == null ? null : PlanRun(Map<String, dynamic>.from(m));
}

void _savePlan(HighState s, PlanRun p) => s.coachSet('plan', p.m);

Widget _withBook(Widget Function(BuildContext, PlanBook) b) => FutureBuilder<PlanBook>(
  future: PlanBook.load(),
  initialData: PlanBook.cached,
  builder: (c, snap) => snap.data == null ? const SizedBox.shrink() : b(c, snap.data!),
);

/// Coach home: start the check-in, or continue the plan
class PlanEntryCard extends StatelessWidget implements Spaced {
  const PlanEntryCard({super.key});
  @override
  EdgeInsets get blockMargin => const EdgeInsets.symmetric(vertical: 8);
  @override
  Widget build(BuildContext context) => _withBook((context, b) {
    final k = Kit.of(context), p = k.p, s = k.s, run = planOf(s), last = lastCheck(s);
    final now = highNow();
    final String title, sub, cta;
    final VoidCallback go;
    if (run != null && run.next <= b.days) {
      final d = run.next, open = run.unlocked(d, now);
      title = '30-day plan · Day $d of ${b.days}';
      sub = open ? 'Today: ${b.day(d, run.a, run.b, single: run.single)['title']}' : 'Done for today. Day $d opens tomorrow.';
      cta = open ? 'Open today' : 'See my plan';
      go = () => openPlan(context);
    } else if (run != null) {
      title = '30-day plan done!';
      sub = 'Well done. Take a new check-in any time.';
      cta = 'See my plan';
      go = () => openPlan(context);
    } else {
      title = last == null ? 'Study check-in' : 'Your check-in result';
      sub = last == null
          ? '14 quick questions. Find your 2 focus areas. Get a 30-day plan.'
          : 'Your focus: ${b.topTwo(last).map((a) => b.area(a)['name']).join(' and ')}';
      cta = last == null ? 'Start (3 minutes)' : 'See my result';
      go = last == null ? () => openCheckIn(context) : () => HighNav.of(context).push(ProfilePage(scores: last));
    }
    final streak = run?.streak(now) ?? 0;
    return Panel(
      tone: 'blue',
      margin: bareM(context, this, blockMargin),
      onTap: go,
      label: title,
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        spacing: 12,
        children: [
          Row(
            spacing: 12,
            children: [
              const Badge('blue', 'cal', s: 46),
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(title, style: ts(16.5, w900, p.ink)),
                    Text(sub, style: ts(13, w700, p.ink2, height: 1.35), maxLines: 2, overflow: TextOverflow.ellipsis),
                  ],
                ),
              ),
            ],
          ),
          if (run != null) Bar((run.next - 1) / b.days * 100, tone: 'blue'),
          Row(
            children: [
              Btn(
                cta,
                icon: 'play',
                kind: BtnKind.tone,
                tone: 'blue',
                fontSize: 13.5,
                padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 10),
                onTap: go,
              ),
              const Spacer(),
              if (streak > 0) PillX('$streak-day streak', icon: 'flame'),
            ],
          ),
        ],
      ),
    );
  });
}

// ---------------------------------------------------------------- check-in, one question at a time
class CheckInPage extends StatefulWidget {
  const CheckInPage({super.key, this.recheck = false});
  final bool recheck;
  @override
  State<CheckInPage> createState() => _CheckInPageState();
}

class _CheckInPageState extends State<CheckInPage> {
  int _i = 0;
  final _ans = <String, int>{};

  void _finish(PlanBook b, int feel) {
    final s = HighScope.read(context), sc = b.score(_ans), now = nowMs();
    final old = s.coachGet<List>('checks') ?? const [];
    s.coachSet(
      'checks',
      [
        {'t': now, 'sc': sc},
        ...old,
      ].take(12).toList(),
    );
    final run = planOf(s);
    Map<String, int>? before;
    if (widget.recheck && run != null) {
      before = _ints(run.m['base']);
      run.m['done'] = {...run.done, '${b.recheckDay}': dayOf(highNow())};
      run.m['after'] = sc;
      _savePlan(s, run);
    }
    final nav = HighNav.of(context);
    nav.back();
    nav.push(ProfilePage(scores: sc, feelHigh: feel >= (b.feel['showSupportAtLeast'] as num), before: before));
  }

  @override
  Widget build(BuildContext context) => _withBook((context, b) {
    final p = Kit.of(context).p, items = b.items, n = items.length;
    final onFeel = _i >= n;
    final q = onFeel ? b.feel['text'] as String : items[_i]['text'] as String;
    return PageShell(
      top: TopBar(
        title: widget.recheck ? 'Day 30 check-in' : 'Study check-in',
        sub: onFeel ? 'One last private question' : 'Question ${_i + 1} of $n',
        onBack: HighNav.of(context).back,
        tab: false,
      ),
      body: ScreenList(
        children: [
          Blk(
            margin: const EdgeInsets.only(top: 8, bottom: 6),
            child: Bar((_i / n * 100).clamp(0, 100), tone: 'blue'),
          ),
          if (_i == 0)
            Blk(
              margin: const EdgeInsets.only(bottom: 4),
              child: Text(b.checkin['intro'] as String, style: ts(13.5, w700, p.ink2, height: 1.4)),
            ),
          Panel(
            margin: const EdgeInsets.only(top: 8),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.stretch,
              spacing: 10,
              children: [
                Text(q, style: ts(19, w900, p.ink, height: 1.35, spacing: -.2)),
                if (onFeel) Text(b.feel['note'] as String, style: ts(12.5, w700, p.ink3, height: 1.35)),
                const SizedBox(height: 4),
                for (var j = 0; j < b.scale.length; j++)
                  Btn(
                    b.scale[j],
                    kind: !onFeel && _ans[items[_i]['id']] == j ? BtnKind.tone : BtnKind.soft,
                    tone: 'blue',
                    block: true,
                    onTap: () {
                      if (onFeel) return _finish(b, j);
                      setState(() {
                        _ans[items[_i]['id'] as String] = j;
                        _i++;
                      });
                    },
                  ),
              ],
            ),
          ),
          if (_i > 0)
            Blk(
              margin: const EdgeInsets.only(top: 12),
              child: Align(
                alignment: Alignment.centerLeft,
                child: ChipX('Back', small: true, icon: 'left', onTap: () => setState(() => _i--)),
              ),
            ),
        ],
      ),
    );
  });
}

// ---------------------------------------------------------------- profile
class ProfilePage extends StatelessWidget {
  const ProfilePage({super.key, required this.scores, this.feelHigh = false, this.before});
  final Map<String, int> scores;
  final bool feelHigh;

  /// Day 1 scores when this is the Day 30 check-in
  final Map<String, int>? before;

  @override
  Widget build(BuildContext context) => _withBook((context, b) {
    final k = Kit.of(context), p = k.p, s = k.s;
    final top = b.topTwo(scores), pr = b.profile(b.profileFor(scores)), run = planOf(s);
    final betterBy = (b.checkin['betterBy'] as num).toInt();
    Widget areaRow(Map<String, dynamic> a) {
      final v = scores[a['id']] ?? 0, was = before?[a['id']];
      final t = k.tone(a['tone'] as String);
      return Padding(
        padding: const EdgeInsets.only(top: 10),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          spacing: 5,
          children: [
            Row(
              spacing: 8,
              children: [
                Ic(a['icon'] as String, size: 16, color: t.deep),
                Expanded(child: Text(a['name'] as String, style: ts(14, w900, p.ink))),
                Text(
                  was == null
                      ? b.band(v)
                      : (was - v >= betterBy
                            ? 'Much better'
                            : was > v
                            ? 'A bit better'
                            : was == v
                            ? 'Same'
                            : 'Harder now'),
                  style: ts(12.5, w800, was != null && was - v >= betterBy ? p.sage.deep : t.deep),
                ),
              ],
            ),
            if (was != null)
              ClipRRect(
                borderRadius: BorderRadius.circular(4),
                child: SizedBox(
                  height: 6,
                  child: Align(
                    alignment: Alignment.centerLeft,
                    child: FractionallySizedBox(
                      widthFactor: (was / 100).clamp(0.02, 1.0),
                      child: ColoredBox(color: p.ink3.withValues(alpha: .45), child: const SizedBox.expand()),
                    ),
                  ),
                ),
              ),
            Bar(v, tone: a['tone'] as String),
          ],
        ),
      );
    }

    return PageShell(
      top: TopBar(
        title: before != null ? 'Day 30: your change' : 'Your result',
        sub: 'Not a test. Just a picture of right now.',
        onBack: HighNav.of(context).back,
        tab: false,
      ),
      body: ScreenList(
        children: [
          if (feelHigh) SafetyCard(title: b.support['title'] as String, text: b.support['text'] as String),
          Panel(
            tone: b.area(top.first)['tone'] as String,
            margin: const EdgeInsets.only(top: 8),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              spacing: 6,
              children: [
                Text('You are…', style: ts(12.5, w900, p.ink3)),
                Text(pr['name'] as String, style: ts(23, w900, p.ink, spacing: -.4)),
                Text(pr['tagline'] as String, style: ts(15, w800, p.ink2, height: 1.35)),
                Text(pr['about'] as String, style: ts(14, w700, p.ink2, height: 1.45)),
              ],
            ),
          ),
          Panel(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: [
                CardHead(
                  before != null ? 'Day 1 (grey) and now' : 'Your 2 focus areas',
                  small: before != null ? 'Shorter bar = easier for you now' : top.map((a) => b.area(a)['name']).join(' and '),
                ),
                for (final a in b.areas) areaRow(a),
              ],
            ),
          ),
          Panel(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              spacing: 6,
              children: [
                Text('Your strengths', style: ts(15, w900, p.ink)),
                for (final x in pr['strengths'] as List) Text('• $x', style: ts(14, w700, p.ink2, height: 1.4)),
                const SizedBox(height: 6),
                Text('Watch out for', style: ts(15, w900, p.ink)),
                for (final x in pr['watch'] as List) Text('• $x', style: ts(14, w700, p.ink2, height: 1.4)),
                const SizedBox(height: 6),
                Text('Try this first', style: ts(15, w900, p.ink)),
                Text(pr['tip'] as String, style: ts(14, w700, p.ink2, height: 1.4)),
              ],
            ),
          ),
          SectionLabel('Lessons for you'),
          Blk(
            margin: const EdgeInsets.only(top: 6),
            child: Wrap(
              spacing: 8,
              runSpacing: 8,
              children: [
                for (final a in top)
                  ChipX(
                    '${b.area(a)['name']}: full lesson',
                    small: true,
                    icon: b.area(a)['icon'] as String,
                    tone: b.area(a)['tone'] as String,
                    onTap: () => openCoachTopic(context, b.area(a)['topic'] as String),
                  ),
              ],
            ),
          ),
          if (before == null && (run == null || run.next > b.days))
            Panel(
              tone: 'blue',
              margin: const EdgeInsets.only(top: 16),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.stretch,
                spacing: 10,
                children: [
                  Text('Your 30-day plan', style: ts(16, w900, p.ink)),
                  Text(b.plan['intro'] as String, style: ts(13.5, w700, p.ink2, height: 1.4)),
                  Btn(
                    'Start: ${b.area(top[0])['name']} + ${b.area(top[1])['name']}',
                    icon: 'play',
                    kind: BtnKind.tone,
                    tone: 'blue',
                    block: true,
                    onTap: () => _start(context, s, b, top, false),
                  ),
                  Btn('Only ${b.area(top[0])['name']}', kind: BtnKind.soft, block: true, onTap: () => _start(context, s, b, top, true)),
                ],
              ),
            )
          else if (before == null)
            Blk(
              margin: const EdgeInsets.only(top: 16),
              child: Btn('Back to my plan', icon: 'cal', kind: BtnKind.tone, tone: 'blue', block: true, onTap: () => openPlan(context)),
            ),
          if (before != null)
            Blk(
              margin: const EdgeInsets.only(top: 16),
              child: Text('Any change counts. So does showing up for 30 days. Well done!', style: ts(14.5, w800, p.sage.deep, height: 1.4)),
            ),
        ],
      ),
    );
  });

  void _start(BuildContext context, HighState s, PlanBook b, List<String> top, bool single) {
    _savePlan(s, PlanRun({'a': top[0], 'b': top[1], 'single': single, 'start': nowMs(), 'base': scores, 'done': <String, String>{}}));
    final nav = HighNav.of(context);
    nav.back();
    openPlan(context);
  }
}

// ---------------------------------------------------------------- the plan
class PlanPage extends StatefulWidget {
  const PlanPage({super.key});
  @override
  State<PlanPage> createState() => _PlanPageState();
}

class _PlanPageState extends State<PlanPage> {
  int? _view; // a past day the student tapped
  final _notes = <String, TextEditingController>{};
  int? _mood;

  @override
  void dispose() {
    for (final c in _notes.values) {
      c.dispose();
    }
    super.dispose();
  }

  @override
  Widget build(BuildContext context) => _withBook((context, b) {
    final k = Kit.of(context), p = k.p, s = k.s, run = planOf(s), now = highNow();
    if (run == null) {
      return PageShell(
        top: TopBar(title: '30-day plan', onBack: HighNav.of(context).back, tab: false),
        body: ScreenList(
          children: [
            Panel(
              margin: const EdgeInsets.only(top: 8),
              onTap: () => openCheckIn(context),
              child: Text('Take the check-in first.', style: ts(15, w800, p.ink)),
            ),
          ],
        ),
      );
    }
    final next = run.next, d = _view ?? (next > b.days ? b.days : next);
    final entry = b.day(d, run.a, run.b, single: run.single), open = run.unlocked(d, now), done = run.isDone(d);
    final streak = run.streak(now), best = run.m['best'] is num ? (run.m['best'] as num).toInt() : streak;
    final moods = [
      for (final r in (run.m['notes'] as Map? ?? const {}).values)
        if (r is Map && r['mood'] is num) (r['mood'] as num).toInt(),
    ];
    final lowMood = moods.isNotEmpty && (moods.last == 0 || (moods.length > 1 && moods[moods.length - 1] <= 1 && moods[moods.length - 2] <= 1));

    void complete([Map<String, dynamic>? note]) {
      run.m['done'] = {...run.done, '$d': dayOf(now)};
      if (note != null) run.m['notes'] = {...?(run.m['notes'] as Map?)?.cast<String, dynamic>(), '$d': note};
      final st = run.streak(now);
      if (st > best) run.m['best'] = st;
      _savePlan(s, run);
      setState(() => _view = null);
    }

    Widget grid() => Wrap(
      spacing: 6,
      runSpacing: 6,
      children: [
        for (var i = 1; i <= b.days; i++)
          GestureDetector(
            onTap: run.isDone(i) || i == next ? () => setState(() => _view = i == next ? null : i) : null,
            child: SizedBox(
              width: 38,
              height: 38,
              child: DecoratedBox(
                decoration: BoxDecoration(
                  color: run.isDone(i) ? p.blue.deep : (i == d ? p.blue.tile : p.surface2),
                  borderRadius: BorderRadius.circular(11),
                  border: Border.all(color: i == d ? p.blue.deep : p.line, width: i == d ? 2 : 1),
                ),
                child: Center(
                  child: run.isDone(i)
                      ? Ic('check', size: 16, color: p.dark ? p.bg : white, strokeWidth: 3)
                      : Text('$i', style: ts(12.5, w900, b.reflectDays.contains(i) || i == b.recheckDay ? p.peach.deep : p.ink2)),
                ),
              ),
            ),
          ),
      ],
    );

    final List<Widget> today;
    if (!open) {
      today = [
        Panel(
          tone: 'sage',
          child: Row(
            spacing: 12,
            children: [
              const Badge('sage', 'check', s: 40),
              Expanded(child: Text('Done for today! Day $d opens tomorrow. Rest well.', style: ts(14.5, w800, p.ink, height: 1.4))),
            ],
          ),
        ),
      ];
    } else if (entry['type'] == 'lesson') {
      final a = b.area(entry['area'] as String);
      today = [
        Panel(
          tone: a['tone'] as String,
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            spacing: 8,
            children: [
              Row(
                spacing: 10,
                children: [
                  Badge(a['tone'] as String, a['icon'] as String, s: 36),
                  Expanded(child: Text('Day $d · ${a['name']} · 5 minutes', style: ts(12.5, w900, p.ink3))),
                ],
              ),
              Text(entry['title'] as String, style: ts(20, w900, p.ink, spacing: -.3)),
              Text(entry['text'] as String, style: ts(15, w700, p.ink2, height: 1.45)),
              Text.rich(
                TextSpan(
                  children: [
                    TextSpan(text: 'Why this works: ', style: ts(13, w900, p.ink)),
                    TextSpan(text: entry['why'] as String),
                  ],
                ),
                style: ts(13, w700, p.ink3, height: 1.4),
              ),
            ],
          ),
        ),
        Panel(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            spacing: 6,
            children: [
              CardHead('Your tiny action', trailing: const Badge('sage', 'flag', s: 32)),
              Text(entry['action'] as String, style: ts(15, w800, p.ink, height: 1.4)),
              if (entry['tool'] != null)
                Padding(
                  padding: const EdgeInsets.only(top: 4),
                  child: Align(
                    alignment: Alignment.centerLeft,
                    child: ChipX(
                      toolTitle(entry['tool'] as String),
                      small: true,
                      icon: toolIcon(entry['tool'] as String),
                      tone: toolTone(entry['tool'] as String),
                      onTap: () => openTool(context, entry['tool'] as String),
                    ),
                  ),
                ),
              const SizedBox(height: 4),
              TickRow(text: done ? 'Done. Great work!' : 'I did it', on: done, onTap: done ? () {} : complete),
            ],
          ),
        ),
        Blk(
          margin: const EdgeInsets.only(top: 6),
          child: Align(
            alignment: Alignment.centerLeft,
            child: ChipX('More on ${a['name']}', small: true, icon: 'book', onTap: () => openCoachTopic(context, a['topic'] as String)),
          ),
        ),
      ];
    } else if (entry['type'] == 'reflect') {
      final saved = (run.m['notes'] as Map?)?['$d'] as Map?;
      final prompts = [for (final x in entry['prompts'] as List) x as Map<String, dynamic>];
      final labels = [for (final x in (entry['mood'] as Map)['labels'] as List) x as String];
      today = [
        Panel(
          tone: 'peach',
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            spacing: 8,
            children: [
              Text(entry['title'] as String, style: ts(19, w900, p.ink)),
              Text(entry['text'] as String, style: ts(14, w700, p.ink2, height: 1.4)),
              for (final q in prompts) ...[
                Text(q['text'] as String, style: ts(14, w900, p.ink)),
                if (saved != null)
                  Text('${saved[q['id']] ?? ''}', style: ts(14, w700, p.ink2))
                else
                  Field(controller: _notes.putIfAbsent(q['id'] as String, TextEditingController.new), placeholder: 'Write a few words', maxLength: 120),
              ],
              Text((entry['mood'] as Map)['text'] as String, style: ts(14, w900, p.ink)),
              Wrap(
                spacing: 6,
                runSpacing: 6,
                children: [
                  for (var i = 0; i < labels.length; i++)
                    ChipX(labels[i], small: true, on: (saved?['mood'] ?? _mood) == i, onTap: saved != null ? null : () => setState(() => _mood = i)),
                ],
              ),
              if (saved == null)
                Btn(
                  'Save my week',
                  icon: 'check',
                  kind: BtnKind.tone,
                  tone: 'peach',
                  block: true,
                  enabled: _mood != null,
                  onTap: () {
                    complete({for (final e in _notes.entries) e.key: e.value.text.trim(), 'mood': _mood});
                    _notes.clear();
                    _mood = null;
                    FocusScope.of(context).unfocus();
                  },
                ),
            ],
          ),
        ),
      ];
    } else {
      today = [
        Panel(
          tone: 'sage',
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            spacing: 10,
            children: [
              Text(entry['title'] as String, style: ts(19, w900, p.ink)),
              Text(entry['text'] as String, style: ts(14, w700, p.ink2, height: 1.4)),
              if (done)
                Btn(
                  'See my change',
                  icon: 'chart',
                  kind: BtnKind.tone,
                  tone: 'sage',
                  block: true,
                  onTap: () => HighNav.of(context).push(ProfilePage(scores: _ints(run.m['after']), before: _ints(run.m['base']))),
                )
              else
                Btn('Take the check-in again', icon: 'play', kind: BtnKind.tone, tone: 'sage', block: true, onTap: () => openCheckIn(context, recheck: true)),
            ],
          ),
        ),
      ];
    }

    return PageShell(
      top: TopBar(
        title: '30-day plan',
        sub: run.single ? b.area(run.a)['name'] as String : '${b.area(run.a)['name']} + ${b.area(run.b)['name']}',
        onBack: HighNav.of(context).back,
        tab: false,
      ),
      body: ScreenList(
        children: [
          Blk(
            margin: const EdgeInsets.only(top: 8),
            child: Row(
              spacing: 8,
              children: [
                PillX('Day ${next > b.days ? b.days : next} of ${b.days}', icon: 'cal'),
                PillX('$streak-day streak', icon: 'flame'),
                if (best > 1) PillX('Best $best'),
              ],
            ),
          ),
          if (lowMood) SafetyCard(title: b.support['title'] as String, text: b.support['text'] as String),
          ...today,
          SectionLabel('Your 30 days', n: run.done.length),
          Blk(margin: const EdgeInsets.only(top: 8), child: grid()),
          Blk(
            margin: const EdgeInsets.only(top: 10),
            child: Text('Missed a day? No problem. Just carry on where you stopped.', style: ts(12.5, w700, p.ink3, height: 1.4)),
          ),
          Blk(
            margin: const EdgeInsets.only(top: 18),
            child: Align(
              alignment: Alignment.centerLeft,
              child: ChipX(
                'Stop this plan',
                small: true,
                icon: 'x',
                onTap: () {
                  s.coachSet('plan', null);
                  HighNav.of(context).back();
                },
              ),
            ),
          ),
        ],
      ),
    );
  });
}
