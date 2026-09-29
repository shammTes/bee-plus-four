// Home streak / XP / badge area + the Badges screen.
import 'package:flutter/widgets.dart';

import '../theme/tokens.dart';
import '../widgets/art.dart' show Ic;
import '../widgets/kit.dart';
import '../widgets/page.dart';

/// id -> (name, how to earn, tone, icon)
const kBadges = <String, (String, String, String, String)>{
  'first': ('First steps', 'Earn 10 XP', 'sage', 'sprout'),
  'xp100': ('Rising star', 'Earn 100 XP', 'butter', 'star'),
  'xp500': ('Scholar', 'Earn 500 XP', 'blue', 'book'),
  'xp1500': ('Master', 'Earn 1500 XP', 'lilac', 'trophy'),
  'streak3': ('On fire', 'Study 3 days in a row', 'peach', 'flame'),
  'streak7': ('Week warrior', 'Study 7 days in a row', 'peach', 'flame'),
  'streak30': ('Unstoppable', 'Study 30 days in a row', 'peach', 'flame'),
  'labeler': ('Labeller', 'Finish 5 label-the-diagram games', 'mint', 'target'),
  'matcher': ('Matchmaker', 'Finish 5 match-up games', 'mint', 'grid'),
  'explorer': ('Explorer', 'Try 10 interactive models', 'butter', 'bulb'),
  'checker': ('Sharp mind', 'Finish 10 quick checks', 'sage', 'check'),
  'stars15': ('Star collector', 'Collect 15 unit stars', 'butter', 'star'),
};

class GameCard extends StatelessWidget implements Spaced {
  const GameCard({super.key});
  @override
  EdgeInsets get blockMargin => const EdgeInsets.symmetric(vertical: 14);
  @override
  Widget build(BuildContext context) {
    final k = Kit.of(context), p = k.p, s = k.s, st = s.streak(), got = s.badges;
    final lv = s.level, need = 25 * lv * lv, prev = 25 * (lv - 1) * (lv - 1);
    return Panel(
      margin: bareM(context, this, blockMargin),
      padding: const EdgeInsets.all(14),
      onTap: () => HighNav.of(context).open('badges', () => const BadgesPage()),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        spacing: 10,
        children: [
          Row(
            spacing: 12,
            children: [
              const Badge('peach', 'flame', s: 42),
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text('${st.cur}-day streak · Level $lv', style: ts(15, w900, p.ink)),
                    Text('${s.xp} XP · ${s.totalStars} ★ · ${got.length}/${kBadges.length} badges', style: ts(12.5, w700, p.ink2)),
                  ],
                ),
              ),
              Ic('right', size: 20, color: p.ink3),
            ],
          ),
          Bar(need == prev ? 0 : (100 * (s.xp - prev) / (need - prev)).clamp(0, 100), tone: 'peach'),
          if (got.isNotEmpty)
            Wrap(spacing: 6, runSpacing: 6, children: [for (final b in kBadges.keys.where(got.contains).take(8)) Badge(kBadges[b]!.$3, kBadges[b]!.$4, s: 30)]),
        ],
      ),
    );
  }
}

class BadgesPage extends StatelessWidget {
  const BadgesPage({super.key});
  @override
  Widget build(BuildContext context) {
    final k = Kit.of(context), p = k.p, s = k.s, got = s.badges, st = s.streak();
    return PageShell(
      top: TopBar(title: 'Badges', sub: '${s.xp} XP · level ${s.level} · best streak ${st.best} days', onBack: HighNav.of(context).back, tab: false),
      body: ListView(
        padding: const EdgeInsets.fromLTRB(18, 12, 18, 40),
        children: [
          Text(
            'Earn XP by answering questions, finishing quick checks, labelling diagrams, matching words and trying the interactive models in the notes. Each unit gives up to 3 stars.',
            style: ts(14, w700, p.ink2, height: 1.4),
          ),
          for (final e in kBadges.entries)
            Panel(
              margin: const EdgeInsets.only(top: 10),
              padding: const EdgeInsets.all(12),
              child: Opacity(
                opacity: got.contains(e.key) ? 1 : .45,
                child: Row(
                  spacing: 12,
                  children: [
                    Badge(e.value.$3, e.value.$4, s: 40),
                    Expanded(
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text(e.value.$1, style: ts(15, w900, p.ink)),
                          Text(e.value.$2, style: ts(12.5, w700, p.ink2)),
                        ],
                      ),
                    ),
                    if (got.contains(e.key)) Ic('check', size: 22, color: p.sage.deep),
                  ],
                ),
              ),
            ),
        ],
      ),
    );
  }
}
