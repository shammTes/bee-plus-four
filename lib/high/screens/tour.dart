import 'package:flutter/widgets.dart';

import '../state/app_state.dart';
import '../theme/tokens.dart';
import '../widgets/kit.dart';
import '../widgets/page.dart';

/// First-run walkthrough. Optional: How to use or Skip.
/// Active steps point at the real control (orange ring on the button to tap).
class TourCard extends StatefulWidget {
  const TourCard({super.key});
  @override
  State<TourCard> createState() => _TourCardState();
}

class _TourCardState extends State<TourCard> {
  final _name = TextEditingController();

  @override
  void dispose() {
    _name.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final s = HighScope.of(context);
    final step = s.tourStep;
    if (step == null) return const SizedBox.shrink();
    final p = Kit.of(context).p;
    if (step < 0) return _chooser(s, p);
    if (step >= _copy.length) return const SizedBox.shrink();
    final c = _copy[step];
    final bottom = 14 + MediaQuery.paddingOf(context).bottom + (s.tourWants('name') || s.tourWants('finish') ? 12 : 92);
    return Padding(
      padding: EdgeInsets.only(bottom: bottom),
      child: DecoratedBox(
        decoration: BoxDecoration(color: const Color(0xFFFFFCF7), borderRadius: BorderRadius.circular(24), boxShadow: const [BoxShadow(color: Color(0x332A1A12), blurRadius: 18, offset: Offset(0, 8))]),
        child: Padding(
          padding: const EdgeInsets.fromLTRB(16, 14, 16, 14),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              Row(
                children: [
                  Expanded(child: Text(c.$1, style: ts(18, w900, p.ink))),
                  GestureDetector(
                    onTap: s.skipTour,
                    child: Text('Skip', style: ts(14, w900, p.coral)),
                  ),
                ],
              ),
              const SizedBox(height: 6),
              Text(c.$2, style: ts(15, w700, const Color(0xFF5C4A3A))),
              const SizedBox(height: 8),
              Text(
                c.$3,
                style: ts(13, w800, const Color(0xFFC24E32)),
              ),
              if (s.tourWants('name')) ...[
                const SizedBox(height: 10),
                Field(controller: _name, placeholder: 'Your name', maxLength: 24, onSubmitted: (_) => _saveName(s)),
                const SizedBox(height: 8),
                Btn('Continue', icon: 'play', block: true, onTap: () => _saveName(s)),
              ],
              if (s.tourWants('finish')) ...[
                const SizedBox(height: 8),
                Text('Developed by Shamm Tesfalem, 07162947', style: ts(12.5, w800, p.ink3)),
                const SizedBox(height: 8),
                Btn('Done', icon: 'check', block: true, onTap: () => s.tourAct('finish')),
              ],
            ],
          ),
        ),
      ),
    );
  }

  Widget _chooser(HighState s, Palette p) {
    final bottom = 14 + MediaQuery.paddingOf(context).bottom + 20;
    return Padding(
      padding: EdgeInsets.only(bottom: bottom),
      child: DecoratedBox(
        decoration: BoxDecoration(color: const Color(0xFFFFFCF7), borderRadius: BorderRadius.circular(24), boxShadow: const [BoxShadow(color: Color(0x332A1A12), blurRadius: 18, offset: Offset(0, 8))]),
        child: Padding(
          padding: const EdgeInsets.fromLTRB(16, 16, 16, 16),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              Text('Welcome to 4', style: ts(20, w900, p.ink)),
              const SizedBox(height: 6),
              const Text(
                'A short walkthrough can point at the buttons to tap. You can skip it and start studying.',
                style: TextStyle(fontFamily: kFont, fontSize: 15, fontWeight: FontWeight.w700, color: Color(0xFF5C4A3A), height: 1.35),
              ),
              const SizedBox(height: 14),
              Btn('How to use', icon: 'play', block: true, onTap: s.startTour),
              const SizedBox(height: 8),
              Btn('Skip', icon: 'check', kind: BtnKind.soft, block: true, onTap: s.skipTour),
            ],
          ),
        ),
      ),
    );
  }

  void _saveName(HighState s) {
    s.setName(_name.text.trim().isEmpty ? 'Student' : _name.text.trim());
    s.tourAct('name');
  }
}

/// title, body, pointer hint
const _copy = <(String, String, String)>[
  ('Hello', 'This app is 4. Grade 9 to 12. Works with no internet. Type your name, then tap Continue.', 'Type in the box on this card, then tap Continue.'),
  ('Grades', 'These four tiles are Grade 9, 10, 11 and 12. Grade 11 and 12 split into Science and Art.', '\u2191 Tap Grade 9 \u2014 the tile with the orange ring.'),
  ('Subjects', 'This page lists the subjects. Tap one subject to open its units.', 'Tap any subject card on this page.'),
  ('Units', 'Notes, practice and matric start from a unit. Now go back.', 'Tap the back arrow at the top.'),
  ('Go back', 'Good. Return to the home page.', 'Tap back again.'),
  ('Notes', 'Notes opens the textbooks.', '\u2193 Tap Notes on the bar below \u2014 orange ring.'),
  ('Practice', 'Exercise groups questions by grade and subject.', '\u2193 Tap Exercise on the bar below \u2014 orange ring.'),
  ('Matric', 'Matric and model exams. Each question has an answer and steps.', '\u2193 Tap Matric on the bar below \u2014 orange ring.'),
  ('Tutor', '4 can explain a topic from the books on this phone.', '\u2193 Tap Tutor on the bar below \u2014 orange ring.'),
  ('Home', 'Home is the first page.', '\u2193 Tap Home on the bar below \u2014 orange ring.'),
  ('Settings', 'The round picture at the top opens Settings and About.', '\u2191 Tap the round picture at the top right.'),
  ('You are ready', 'Everything stays on this phone. No internet is needed.', 'Tap Done on this card.'),
];
