// Study Coach ("Help me"): pick a problem, get a short lesson with step cards, self-checks, checklists, small
// exercises and "Try this today". Offline, content from assets/high/coach/topics.json. Lists are lazy (ScreenList).
import 'package:flutter/widgets.dart';

import '../l10n.dart';
import '../state/app_state.dart';
import '../theme/tokens.dart';
import '../widgets/art.dart';
import '../widgets/kit.dart';
import '../widgets/page.dart';
import 'coach_data.dart';
import 'coach_tools.dart';
import 'plan_pages.dart';

String _l(BuildContext c, String k, [Map<String, Object>? v]) => highLabel(Kit.of(c).s.lang, k, v);

/// topics shown as quick links on the Home card
const kCoachQuick = ['exam_anxiety', 'procrastination', 'how_to_study'];

/// topics linked to a check-in area: they also show the check-in / 30-day plan card
const kPlanTopics = {'how_to_study', 'procrastination', 'exam_anxiety', 'sleep_health', 'focus_phone', 'motivation'};

void openCoach(BuildContext c) => HighNav.of(c).open('coach', () => const CoachHomePage());
void openCoachTopic(BuildContext c, String id) => HighNav.of(c).open('coach:$id', () => CoachTopicPage(id: id));

Widget _loading() => const SizedBox.shrink();

/// Home block → Study Coach
class StudyCoachCard extends StatelessWidget implements Spaced {
  const StudyCoachCard({super.key});
  @override
  EdgeInsets get blockMargin => const EdgeInsets.symmetric(vertical: 14);
  @override
  Widget build(BuildContext context) {
    return FutureBuilder<CoachBook>(future: CoachBook.load(), initialData: CoachBook.cached, builder: (context, snap) => _card(context, snap.data));
  }

  Widget _card(BuildContext context, CoachBook? b) {
    final k = Kit.of(context), p = k.p, t = k.tone('lilac');
    return Panel(
      tone: 'lilac',
      margin: bareM(context, this, blockMargin),
      padding: const EdgeInsets.fromLTRB(16, 16, 16, 14),
      onTap: () => openCoach(context),
      label: _l(context, 'coachTitle'),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        spacing: 12,
        children: [
          Row(
            spacing: 12,
            children: [
              const Badge('lilac', 'help', s: 48),
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(_l(context, 'coachTitle'), style: ts(18, w900, p.ink, spacing: -.2)),
                    Text(_l(context, 'coachHomeSub', {'n': b?.topics.length ?? 21}), style: ts(12.5, w800, mix(t.deep, .72, p.ink2), height: 1.3)),
                  ],
                ),
              ),
              Ic('right', size: 20, color: t.deep),
            ],
          ),
          if (b != null)
            Wrap(
              spacing: 8,
              runSpacing: 8,
              children: [
                for (final id in kCoachQuick)
                  if (b.byId(id) case final tp?) ChipX(tp.title, small: true, tone: tp.tone, icon: tp.icon, onTap: () => openCoachTopic(context, id)),
              ],
            ),
        ],
      ),
    );
  }
}

class CoachHomePage extends StatelessWidget {
  const CoachHomePage({super.key});
  @override
  Widget build(BuildContext context) {
    final k = Kit.of(context), p = k.p, s = k.s;
    final seen = (s.coachGet<List>('seen') ?? const []).toSet();
    return PageShell(
      top: TopBar(title: _l(context, 'coachTitle'), sub: _l(context, 'coachPageSub'), onBack: HighNav.of(context).back, tab: false),
      body: FutureBuilder<CoachBook>(
        future: CoachBook.load(),
        initialData: CoachBook.cached,
        builder: (context, snap) {
          final b = snap.data;
          if (b == null) return _loading();
          return ScreenList(
            children: [
              Panel(
                tone: 'lilac',
                margin: const EdgeInsets.only(top: 6, bottom: 8),
                child: Row(
                  spacing: 12,
                  children: [
                    const Kokob(width: 54, float: false),
                    Expanded(child: Text(_l(context, 'coachIntro'), style: ts(14, w800, p.ink, height: 1.4))),
                  ],
                ),
              ),
              const PlanEntryCard(),
              SectionLabel(_l(context, 'quickTools'), icon: 'timer'),
              Blk(
                margin: const EdgeInsets.only(top: 6, bottom: 4),
                child: Wrap(
                  spacing: 8,
                  runSpacing: 8,
                  children: [
                    for (final t in const ['breath478', 'pomodoro', 'twomin', 'reframe', 'spaced', 'goal'])
                      ChipX(toolTitle(t), small: true, icon: toolIcon(t), tone: toolTone(t), onTap: () => openTool(context, t)),
                  ],
                ),
              ),
              for (final g in b.groups) ...[
                SectionLabel(g, n: b.topics.where((t) => t.group == g).length),
                for (final t in b.topics.where((t) => t.group == g)) _TopicRow(t: t, seen: seen.contains(t.id)),
              ],
              SafetyCard(title: b.safetyTitle, text: b.safetyText),
            ],
          );
        },
      ),
    );
  }
}

class _TopicRow extends StatelessWidget implements Spaced {
  const _TopicRow({required this.t, required this.seen});
  final CoachTopic t;
  final bool seen;
  @override
  EdgeInsets get blockMargin => const EdgeInsets.only(top: 10);
  @override
  Widget build(BuildContext context) {
    final p = Kit.of(context).p;
    return Panel(
      margin: bareM(context, this, blockMargin),
      padding: const EdgeInsets.fromLTRB(12, 12, 14, 12),
      onTap: () => openCoachTopic(context, t.id),
      label: t.title,
      child: Row(
        spacing: 12,
        children: [
          Badge(t.tone, t.icon, s: 42),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(t.title, style: ts(15, w900, p.ink), maxLines: 1, overflow: TextOverflow.ellipsis),
                Text(t.summary, style: ts(12.5, w700, p.ink2, height: 1.3), maxLines: 2, overflow: TextOverflow.ellipsis),
              ],
            ),
          ),
          if (seen) Ic('check', size: 18, color: p.sage.deep) else Ic('right', size: 18, color: p.ink3),
        ],
      ),
    );
  }
}

class SafetyCard extends StatelessWidget implements Spaced {
  const SafetyCard({super.key, required this.title, required this.text});
  final String title, text;
  @override
  EdgeInsets get blockMargin => const EdgeInsets.symmetric(vertical: 14);
  @override
  Widget build(BuildContext context) {
    final p = Kit.of(context).p;
    return Panel(
      tone: 'rose',
      margin: bareM(context, this, blockMargin),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        spacing: 12,
        children: [
          const Badge('rose', 'shield', s: 38),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              spacing: 4,
              children: [
                Text(title, style: ts(15, w900, p.ink)),
                Text(text, style: ts(13.5, w700, p.ink2, height: 1.4)),
              ],
            ),
          ),
        ],
      ),
    );
  }
}

/// One lesson
class CoachTopicPage extends StatefulWidget {
  const CoachTopicPage({super.key, required this.id});
  final String id;
  @override
  State<CoachTopicPage> createState() => _CoachTopicPageState();
}

class _CoachTopicPageState extends State<CoachTopicPage> {
  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addPostFrameCallback((_) {
      if (!mounted) return;
      final s = HighScope.read(context);
      final seen = [for (final x in s.coachGet<List>('seen') ?? const []) '$x'];
      if (!seen.contains(widget.id)) s.coachSet('seen', [...seen, widget.id]);
    });
  }

  @override
  Widget build(BuildContext context) {
    final k = Kit.of(context), p = k.p;
    return FutureBuilder<CoachBook>(
      future: CoachBook.load(),
      initialData: CoachBook.cached,
      builder: (context, snap) {
        final b = snap.data, t = b?.byId(widget.id);
        return PageShell(
          top: TopBar(title: t?.title ?? _l(context, 'coachTitle'), sub: t?.group, onBack: HighNav.of(context).back, tab: false),
          body: b == null || t == null
              ? _loading()
              : ScreenList(
                  children: [
                    Panel(
                      tone: t.tone,
                      margin: const EdgeInsets.only(top: 6, bottom: 6),
                      child: Row(
                        spacing: 14,
                        children: [
                          Badge(t.tone, t.icon, s: 52),
                          Expanded(child: Text(t.summary, style: ts(15, w800, p.ink, height: 1.4))),
                        ],
                      ),
                    ),
                    for (var i = 0; i < t.blocks.length; i++) blockWidget(t, t.blocks[i], b, i),
                    if (kPlanTopics.contains(t.id)) const PlanEntryCard(),
                  ],
                ),
        );
      },
    );
  }
}

/// the widget for one lesson block
Widget blockWidget(CoachTopic t, Map<String, dynamic> b, CoachBook book, int i) => switch (b['type']) {
  'note' => _NoteBlock(b: b),
  'steps' => _StepsBlock(b: b, tone: t.tone),
  'quiz' => QuizBlock(key: ValueKey('quiz:${b['id']}'), b: b),
  'mcq' => McqBlock(key: ValueKey('mcq:${b['id']}'), b: b),
  'check' => _CheckBlock(b: b),
  'tool' => _ToolBlock(b: b),
  'try' => _TryBlock(topic: t.id, b: b),
  'safety' => SafetyCard(title: book.safetyTitle, text: book.safetyText),
  _ => const SizedBox.shrink(),
};

class _NoteBlock extends StatelessWidget implements Spaced {
  const _NoteBlock({required this.b});
  final Map<String, dynamic> b;
  @override
  EdgeInsets get blockMargin => const EdgeInsets.symmetric(vertical: 10);
  @override
  Widget build(BuildContext context) {
    final p = Kit.of(context).p, tone = (b['tone'] as String?) ?? 'butter';
    return Panel(
      tone: tone,
      margin: bareM(context, this, blockMargin),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        spacing: 12,
        children: [
          Badge(tone, 'bulb', s: 36),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              spacing: 4,
              children: [
                Text(b['title'] as String, style: ts(15, w900, p.ink)),
                Text(b['text'] as String, style: ts(14, w700, p.ink2, height: 1.45)),
              ],
            ),
          ),
        ],
      ),
    );
  }
}

class _StepsBlock extends StatelessWidget implements Spaced {
  const _StepsBlock({required this.b, required this.tone});
  final Map<String, dynamic> b;
  final String tone;
  @override
  EdgeInsets get blockMargin => const EdgeInsets.symmetric(vertical: 10);
  @override
  Widget build(BuildContext context) {
    final k = Kit.of(context), p = k.p, t = k.tone(tone);
    final items = b['items'] as List;
    return Panel(
      margin: bareM(context, this, blockMargin),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          CardHead(b['title'] as String, small: _l(context, 'nSteps', {'n': items.length})),
          for (var i = 0; i < items.length; i++)
            Padding(
              padding: EdgeInsets.only(top: i == 0 ? 0 : 12),
              child: Row(
                crossAxisAlignment: CrossAxisAlignment.start,
                spacing: 12,
                children: [
                  SizedBox(
                    width: 30,
                    height: 30,
                    child: DecoratedBox(
                      decoration: BoxDecoration(
                        color: t.tile,
                        shape: BoxShape.circle,
                        border: Border.all(color: t.mid, width: 1.5),
                      ),
                      child: Center(child: Text('${i + 1}', style: ts(14, w900, t.deep))),
                    ),
                  ),
                  Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      spacing: 2,
                      children: [
                        Text(items[i]['t'] as String, style: ts(14.5, w900, p.ink, height: 1.3)),
                        Text(items[i]['x'] as String, style: ts(13.5, w700, p.ink2, height: 1.4)),
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

/// round tick box used by checklists and "Try this today"
class TickRow extends StatelessWidget {
  const TickRow({super.key, required this.text, required this.on, required this.onTap, this.tone = 'sage'});
  final String text, tone;
  final bool on;
  final VoidCallback onTap;
  @override
  Widget build(BuildContext context) {
    final k = Kit.of(context), p = k.p, t = k.tone(tone);
    return Semantics(
      checked: on,
      button: true,
      label: text,
      child: GestureDetector(
        behavior: HitTestBehavior.opaque,
        onTap: onTap,
        child: Padding(
          padding: const EdgeInsets.symmetric(vertical: 7),
          child: Row(
            crossAxisAlignment: CrossAxisAlignment.start,
            spacing: 12,
            children: [
              SizedBox(
                width: 26,
                height: 26,
                child: DecoratedBox(
                  decoration: BoxDecoration(
                    color: on ? t.deep : p.surface,
                    borderRadius: BorderRadius.circular(8),
                    border: Border.all(color: on ? t.deep : p.ink3, width: 1.6),
                  ),
                  child: on ? Center(child: Ic('check', size: 18, color: p.dark ? p.bg : white, strokeWidth: 3)) : null,
                ),
              ),
              Expanded(
                child: Padding(
                  padding: const EdgeInsets.only(top: 3),
                  child: Text(text, style: ts(14, w800, on ? p.ink3 : p.ink, height: 1.35, decoration: on ? TextDecoration.lineThrough : null)),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}

class _CheckBlock extends StatelessWidget implements Spaced {
  const _CheckBlock({required this.b});
  final Map<String, dynamic> b;
  @override
  EdgeInsets get blockMargin => const EdgeInsets.symmetric(vertical: 10);
  @override
  Widget build(BuildContext context) {
    final s = Kit.of(context).s, id = b['id'] as String, items = b['items'] as List;
    final chk = Map<String, dynamic>.from(s.coachGet<Map>('chk') ?? const {});
    final on = {for (final x in (chk[id] as List? ?? const [])) (x as num).toInt()};
    return Panel(
      margin: bareM(context, this, blockMargin),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          CardHead(b['title'] as String, small: _l(context, 'nDone', {'d': on.length, 'n': items.length}), trailing: const Badge('sage', 'list', s: 34)),
          for (var i = 0; i < items.length; i++)
            TickRow(
              text: items[i] as String,
              on: on.contains(i),
              onTap: () {
                final n = {...on};
                n.contains(i) ? n.remove(i) : n.add(i);
                s.coachSet('chk', {...chk, id: n.toList()..sort()});
              },
            ),
        ],
      ),
    );
  }
}

class _TryBlock extends StatelessWidget implements Spaced {
  const _TryBlock({required this.topic, required this.b});
  final String topic;
  final Map<String, dynamic> b;
  @override
  EdgeInsets get blockMargin => const EdgeInsets.symmetric(vertical: 10);
  @override
  Widget build(BuildContext context) {
    final p = Kit.of(context).p, s = Kit.of(context).s, items = b['items'] as List;
    final all = Map<String, dynamic>.from(s.coachGet<Map>('try') ?? const {});
    final today = dayKey(nowMs());
    final mine = all[topic] is Map && (all[topic] as Map)['d'] == today ? all[topic] as Map : null;
    final on = {for (final x in (mine?['done'] as List? ?? const [])) (x as num).toInt()};
    return Panel(
      tone: 'sage',
      margin: bareM(context, this, blockMargin),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          CardHead(
            _l(context, 'tryToday'),
            small: on.length == items.length ? _l(context, 'tryAllDone') : _l(context, 'tryPick'),
            trailing: const Badge('sage', 'flag', s: 34),
          ),
          for (var i = 0; i < items.length; i++)
            TickRow(
              text: items[i] as String,
              on: on.contains(i),
              onTap: () {
                final n = {...on};
                n.contains(i) ? n.remove(i) : n.add(i);
                s.coachSet('try', {
                  ...all,
                  topic: {'d': today, 'done': n.toList()..sort()},
                });
              },
            ),
          if (on.isNotEmpty)
            Padding(
              padding: const EdgeInsets.only(top: 6),
              child: Text(_l(context, 'tryWell'), style: ts(13, w800, p.sage.deep)),
            ),
        ],
      ),
    );
  }
}

class _ToolBlock extends StatelessWidget implements Spaced {
  const _ToolBlock({required this.b});
  final Map<String, dynamic> b;
  @override
  EdgeInsets get blockMargin => const EdgeInsets.symmetric(vertical: 10);
  @override
  Widget build(BuildContext context) {
    final p = Kit.of(context).p, kind = b['tool'] as String, tone = toolTone(kind);
    return Panel(
      tone: tone,
      margin: bareM(context, this, blockMargin),
      onTap: () => openTool(context, kind),
      label: b['title'] as String,
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        spacing: 10,
        children: [
          Row(
            spacing: 12,
            children: [
              Badge(tone, toolIcon(kind), s: 42),
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(_l(context, 'toolLabel'), style: ts(11.5, w900, p.ink3)),
                    Text(b['title'] as String, style: ts(15.5, w900, p.ink)),
                  ],
                ),
              ),
            ],
          ),
          Text(b['text'] as String, style: ts(13.5, w700, p.ink2, height: 1.4)),
          Align(
            alignment: Alignment.centerLeft,
            child: Btn(
              _l(context, 'startTool'),
              icon: 'play',
              kind: BtnKind.tone,
              tone: tone,
              onTap: () => openTool(context, kind),
              fontSize: 13.5,
              padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 10),
            ),
          ),
        ],
      ),
    );
  }
}

/// Self-check questionnaire: tap one answer per line, then see your score band and advice.
class QuizBlock extends StatefulWidget implements Spaced {
  const QuizBlock({super.key, required this.b});
  final Map<String, dynamic> b;
  @override
  EdgeInsets get blockMargin => const EdgeInsets.symmetric(vertical: 10);
  @override
  State<QuizBlock> createState() => _QuizBlockState();
}

class _QuizBlockState extends State<QuizBlock> {
  // kept for the session: lazy lists drop cards that scroll far away, the answers must survive that
  static final _answers = <String, Map<int, int>>{};
  static final _shown = <String>{};
  String get _id => widget.b['id'] as String;
  Map<int, int> get _ans => _answers[_id] ??= {};
  bool get _show => _shown.contains(_id);
  set _show(bool v) => v ? _shown.add(_id) : _shown.remove(_id);
  @override
  Widget build(BuildContext context) {
    final k = Kit.of(context), p = k.p, s = k.s, b = widget.b;
    final qs = b['questions'] as List, opts = b['options'] as List, scores = [for (final x in b['scores'] as List) (x as num).toInt()];
    final saved = (s.coachGet<Map>('quiz') ?? const {})[b['id']] as Map?;
    final all = _ans.length == qs.length;
    final score = _ans.values.fold(0, (a, i) => a + scores[i]);
    final last = saved == null ? null : bandFor(b, (saved['s'] as num).toInt());
    Widget result(Map<String, dynamic> band, int sc) {
      final t = k.tone(band['tone'] as String);
      return DecoratedBox(
        decoration: BoxDecoration(
          color: t.tile,
          borderRadius: BorderRadius.circular(R.md),
          border: Border.all(color: t.mid, width: 1.5),
        ),
        child: Padding(
          padding: const EdgeInsets.all(14),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            spacing: 4,
            children: [
              Text(_l(context, 'yourScore', {'s': sc, 'm': qs.length * scores.last}), style: ts(12, w900, t.deep)),
              Text(band['title'] as String, style: ts(17, w900, p.ink)),
              Text(band['advice'] as String, style: ts(14, w700, p.ink2, height: 1.45)),
            ],
          ),
        ),
      );
    }

    return Panel(
      margin: bareM(context, widget, widget.blockMargin),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          CardHead(b['title'] as String, small: b['intro'] as String?, trailing: const Badge('lilac', 'check', s: 34)),
          if (!_show && last != null) ...[
            Text(_l(context, 'lastTime'), style: ts(12.5, w800, p.ink3)),
            const SizedBox(height: 6),
            result(last, (saved!['s'] as num).toInt()),
            const SizedBox(height: 12),
          ],
          if (_show)
            result(bandFor(b, score), score)
          else
            for (var i = 0; i < qs.length; i++)
              Padding(
                padding: const EdgeInsets.only(bottom: 12),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  spacing: 6,
                  children: [
                    Text('${i + 1}. ${qs[i]}', style: ts(14, w800, p.ink, height: 1.35)),
                    Wrap(
                      spacing: 6,
                      runSpacing: 6,
                      children: [
                        for (var j = 0; j < opts.length; j++) ChipX(opts[j] as String, small: true, on: _ans[i] == j, onTap: () => setState(() => _ans[i] = j)),
                      ],
                    ),
                  ],
                ),
              ),
          const SizedBox(height: 4),
          if (_show)
            Padding(
              padding: const EdgeInsets.only(top: 12),
              child: Btn(
                _l(context, 'doAgain'),
                icon: 'repeat',
                kind: BtnKind.soft,
                onTap: () => setState(() {
                  _ans.clear();
                  _show = false;
                }),
              ),
            )
          else
            Btn(
              all ? _l(context, 'seeResult') : _l(context, 'answerAll', {'n': qs.length - _ans.length}),
              icon: 'check',
              enabled: all,
              block: true,
              onTap: () {
                s.coachSet('quiz', {
                  ...?s.coachGet<Map>('quiz')?.cast<String, dynamic>(),
                  b['id'] as String: {'s': score, 't': nowMs()},
                });
                // the card gets much shorter: jump to its top first so the result is in view
                Scrollable.ensureVisible(context);
                setState(() => _show = true);
              },
            ),
        ],
      ),
    );
  }
}

/// Knowledge check: tap an answer, see right / wrong and why.
class McqBlock extends StatefulWidget implements Spaced {
  const McqBlock({super.key, required this.b});
  final Map<String, dynamic> b;
  @override
  EdgeInsets get blockMargin => const EdgeInsets.symmetric(vertical: 10);
  @override
  State<McqBlock> createState() => _McqBlockState();
}

class _McqBlockState extends State<McqBlock> {
  final _pick = <int, int>{};
  @override
  Widget build(BuildContext context) {
    final k = Kit.of(context), p = k.p, items = widget.b['items'] as List;
    return Panel(
      margin: bareM(context, widget, widget.blockMargin),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          CardHead(widget.b['title'] as String, small: _l(context, 'tapAnswer'), trailing: const Badge('blue', 'target', s: 34)),
          for (var i = 0; i < items.length; i++)
            Padding(
              padding: EdgeInsets.only(top: i == 0 ? 0 : 16),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.stretch,
                spacing: 8,
                children: [
                  Text(items[i]['q'] as String, style: ts(14.5, w900, p.ink, height: 1.35)),
                  for (var j = 0; j < (items[i]['options'] as List).length; j++)
                    () {
                      final picked = _pick[i], right = (items[i]['answer'] as num).toInt();
                      final done = picked != null;
                      final good = done && j == right, bad = done && j == picked && j != right;
                      final t = good
                          ? p.sage
                          : bad
                          ? p.peach
                          : null;
                      return GestureDetector(
                        behavior: HitTestBehavior.opaque,
                        onTap: done ? null : () => setState(() => _pick[i] = j),
                        child: DecoratedBox(
                          decoration: BoxDecoration(
                            color: t?.tile ?? p.surface2,
                            borderRadius: BorderRadius.circular(R.md),
                            border: Border.all(color: t?.mid ?? p.line, width: 1.5),
                          ),
                          child: Padding(
                            padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 11),
                            child: Row(
                              spacing: 8,
                              children: [
                                Expanded(child: Text((items[i]['options'] as List)[j] as String, style: ts(14, w800, p.ink, height: 1.3))),
                                if (good) Ic('check', size: 18, color: p.sage.deep, strokeWidth: 3),
                                if (bad) Ic('x', size: 18, color: p.peach.deep, strokeWidth: 3),
                              ],
                            ),
                          ),
                        ),
                      );
                    }(),
                  if (_pick[i] != null)
                    Text(
                      '${_pick[i] == (items[i]['answer'] as num).toInt() ? _l(context, 'rightWord') : _l(context, 'notQuite')} ${items[i]['why']}',
                      style: ts(13.5, w700, p.ink2, height: 1.4),
                    ),
                ],
              ),
            ),
        ],
      ),
    );
  }
}
