import 'package:flutter/widgets.dart';

import '../state/app_state.dart';
import '../theme/tokens.dart';
import '../widgets/kit.dart';
import '../widgets/page.dart';

/// First-run walkthrough in simple English. Tap the real button named in each step.
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
    if (step == null || step < 0 || step >= _copy.length) return const SizedBox.shrink();
    final p = Kit.of(context).p;
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
              Text(c.$1, style: ts(18, w900, p.ink)),
              const SizedBox(height: 6),
              Text(c.$2, style: ts(15, w700, const Color(0xFF5C4A3A))),
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

  void _saveName(HighState s) {
    s.setName(_name.text.trim().isEmpty ? 'Student' : _name.text.trim());
    s.tourAct('name');
  }
}

const _copy = <(String, String)>[
  ('Hello', 'This app is 4. It is for Grade 9 to 12. It works with no internet. Type your name, then tap Continue.'),
  ('Grades', 'These four buttons are Grade 9, 10, 11 and 12. Grade 11 and 12 split into Science and Art. Tap Grade 9.'),
  ('Subjects', 'This page lists the subjects. Tap one subject to open its units.'),
  ('Units', 'These are the units for that subject. Notes, practice and matric start here. Now tap the back button.'),
  ('Go back', 'Good. Tap back again to return to the home page.'),
  ('Notes', 'The Notes button at the bottom opens the textbooks. Tap Notes.'),
  ('Practice', 'This is practice. Questions are grouped by grade and subject. Now tap Exercise.'),
  ('Matric', 'This is matric and model exams. Each question has an answer and an explanation. Tap Matric.'),
  ('Tutor', '4 can explain a topic from the books on this phone. Tap Tutor.'),
  ('Home', 'Tap Home to go back to the first page.'),
  ('Settings', 'Tap the round picture at the top to open Settings and About.'),
  ('You are ready', 'Everything stays on this phone. No internet is needed. Tap Done.'),
];
