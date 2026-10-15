// 'Track my GPA' (Grades 11-12): Home card + page. Off by default. Predicts each subject's letter grade from the
// student's recent matric answers, or uses marks the student sets (manual mode), and shows the GPA out of 4.0.
import 'package:flutter/widgets.dart';

import '../state/app_state.dart';
import '../theme/tokens.dart';
import '../widgets/art.dart';
import '../widgets/kit.dart';
import '../widgets/page.dart';
import 'gpa.dart';
import 'gpa_config.dart';

/// grades from the student's answers (cached per number of answers, so Home stays fast on low-end phones)
class GpaData {
  static int _len = -1;
  static Object? _repo;
  static ({Map<String, double> pct, Map<String, int> n}) _cache = (pct: const {}, n: const {});

  static ({Map<String, double> pct, Map<String, int> n}) predicted(HighState s) {
    if (_len == s.ev.length && identical(_repo, s.repo)) return _cache;
    _len = s.ev.length;
    _repo = s.repo;
    final byId = s.repo.byId;
    return _cache = estimateFromAnswers(s.ev, (id) {
      final q = byId[id];
      if (q == null || q.exam.isExercise) return null;
      return q.exam.subject;
    });
  }

  static String stream(HighState s) => s.gpa['stream'] == 'social' ? 'social' : 'natural';
  static bool manual(HighState s) => s.gpa['manual'] == true;

  static Map<String, double> manualMarks(HighState s) => {
    for (final e in (s.gpa['marks'] as Map? ?? const {}).entries)
      if (e.value is num) e.key.toString(): (e.value as num).toDouble(),
  };

  static GpaResult result(HighState s) {
    if (manual(s)) return computeGpa(manualMarks(s), stream(s));
    final p = predicted(s);
    return computeGpa(p.pct, stream(s), answers: p.n);
  }
}

String fmtGpa(double? g) => g == null ? '–' : g.toStringAsFixed(2);

class GpaCard extends StatelessWidget implements Spaced {
  const GpaCard({super.key});
  @override
  EdgeInsets get blockMargin => const EdgeInsets.symmetric(vertical: 14);
  @override
  Widget build(BuildContext context) {
    final k = Kit.of(context), p = k.p, s = k.s;
    final on = s.gpaOn;
    final r = on ? GpaData.result(s) : null;
    return KeyedSubtree(
      key: const ValueKey('gpa-card'),
      child: Panel(
        tone: 'butter',
        margin: bareM(context, this, blockMargin),
        padding: const EdgeInsets.all(14),
        onTap: () => HighNav.of(context).push(const GpaPage()),
        label: 'Matric GPA',
        child: Row(
          spacing: 12,
          children: [
            const Badge('butter', 'trophy', s: 42),
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(on ? 'My matric GPA' : 'Track my GPA', style: ts(15, w900, p.ink)),
                  Text(
                    !on
                        ? 'Grades 11–12 · see your predicted GPA out of 4.0'
                        : r!.gpa == null
                        ? 'Answer ${GpaConfig.minAnswers}+ matric questions in a subject, or enter your marks'
                        : '${GpaData.manual(s) ? 'From your marks' : 'Predicted'} · ${r.used.length} of ${GpaConfig.counted} subjects',
                    style: ts(12.5, w700, p.ink2),
                  ),
                ],
              ),
            ),
            if (on && r!.gpa != null) Text('${fmtGpa(r.gpa)}/4', key: const ValueKey('gpa-value'), style: ts(20, w900, p.ink)),
            Ic('right', size: 20, color: p.ink3),
          ],
        ),
      ),
    );
  }
}

class GpaPage extends StatelessWidget {
  const GpaPage({super.key});
  @override
  Widget build(BuildContext context) {
    final k = Kit.of(context), p = k.p, s = k.s;
    final on = s.gpaOn, manual = GpaData.manual(s), stream = GpaData.stream(s);
    final r = GpaData.result(s);
    final subjects = [...GpaConfig.compulsory, ...GpaConfig.streams[stream]!];
    final pred = GpaData.predicted(s);
    final marks = GpaData.manualMarks(s);
    Widget row(String subj) {
      final v = manual ? marks[subj] : pred.pct[subj];
      final used = r.used.any((g) => g.subject == subj);
      return Container(
        key: ValueKey('gpa-row-$subj'),
        padding: const EdgeInsets.symmetric(vertical: 8),
        decoration: BoxDecoration(border: Border(top: BorderSide(color: p.line))),
        child: Row(
          spacing: 8,
          children: [
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(subj, style: ts(14, w900, p.ink)),
                  Text(
                    v == null
                        ? (manual ? 'No mark yet' : 'Not enough answers yet')
                        : '${v.round()}% · grade ${bandFor(v).letter}${manual ? '' : ' · ${pred.n[subj]} answers'}${used ? ' · counted' : ''}',
                    style: ts(12, w700, used ? p.ink2 : p.ink3),
                  ),
                ],
              ),
            ),
            if (manual) ...[
              ChipX('−5', small: true, onTap: () => s.gpaMark(subj, (v ?? 50) - 5)),
              ChipX('+5', small: true, onTap: () => s.gpaMark(subj, (v ?? 50) + 5)),
              if (v != null) ChipX('Clear', small: true, onTap: () => s.gpaMark(subj, null)),
            ] else
              Text(v == null ? '–' : bandFor(v).letter, style: ts(18, w900, p.ink)),
          ],
        ),
      );
    }

    return PageShell(
      top: TopBar(title: 'Matric GPA', sub: 'Grades 11–12 · out of 4.0', onBack: HighNav.of(context).back, tab: false),
      body: ScreenList(
        children: [
          Panel(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.stretch,
              spacing: 10,
              children: [
                Text('Track my GPA', style: ts(16, w900, p.ink)),
                Text('4 is named after 4.0, the top matric GPA. Turn this on to see your GPA as you practise.', style: ts(13, w700, p.ink2)),
                Wrap(
                  spacing: 8,
                  runSpacing: 8,
                  children: [
                    ChipX('Off', on: !on, onTap: () => s.gpaSet('on', false)),
                    ChipX('On', key: const ValueKey('gpa-on'), on: on, onTap: () => s.gpaSet('on', true)),
                  ],
                ),
              ],
            ),
          ),
          if (on) ...[
            Panel(
              tone: 'butter',
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                spacing: 4,
                children: [
                  Text(manual ? 'GPA from your marks' : 'Predicted GPA', style: ts(13, w900, p.ink2)),
                  Text('${fmtGpa(r.gpa)} / 4.0', key: const ValueKey('gpa-big'), style: ts(30, w900, p.ink)),
                  Text(
                    r.gpa == null
                        ? 'No grades yet.'
                        : !r.complete
                        ? 'Based on ${r.used.length} of ${GpaConfig.counted} subjects. Still needed: ${r.missing.join(', ')}.'
                        : r.gpa! >= GpaConfig.passGpa
                        ? 'At or above ${GpaConfig.passGpa.toStringAsFixed(1)}, the minimum for college.'
                        : 'Below ${GpaConfig.passGpa.toStringAsFixed(1)}, the minimum for college. Keep practising!',
                    style: ts(12.5, w700, p.ink2),
                  ),
                ],
              ),
            ),
            const SectionLabel('Stream'),
            Wrap(spacing: 8, children: [for (final e in GpaConfig.streamNames.entries) ChipX(e.value, on: stream == e.key, onTap: () => s.gpaSet('stream', e.key))]),
            const SectionLabel('Grades from'),
            Wrap(
              spacing: 8,
              children: [
                ChipX('My answers in 4', on: !manual, onTap: () => s.gpaSet('manual', false)),
                ChipX('My own marks', key: const ValueKey('gpa-manual'), on: manual, onTap: () => s.gpaSet('manual', true)),
              ],
            ),
            Panel(child: Column(crossAxisAlignment: CrossAxisAlignment.stretch, children: [for (final subj in subjects) row(subj)])),
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 8),
              child: Text(
                'How it works: A (75% and up) = 4, B (65%+) = 3, C (50%+) = 2, D (40%+) = 1, F = 0. '
                'Your GPA uses Maths, English and your best 3 other subjects. '
                '${manual ? '' : 'Each subject uses your last ${GpaConfig.recentAnswers} matric answers. '}'
                'This is a guide only; the real exam may be graded differently.',
                style: ts(12, w700, p.ink3, height: 1.4),
              ),
            ),
          ],
        ],
      ),
    );
  }
}
