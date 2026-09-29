// First-launch sheet (web onboarding()): Kokob asks for the student's name.
import 'package:flutter/widgets.dart';

import '../theme/tokens.dart';
import '../widgets/kit.dart';
import '../widgets/page.dart';

class Onboarding extends StatefulWidget {
  const Onboarding({super.key});
  @override
  State<Onboarding> createState() => _OnboardingState();
}

class _OnboardingState extends State<Onboarding> {
  final _c = TextEditingController();
  @override
  void dispose() {
    _c.dispose();
    super.dispose();
  }

  void _go() {
    final s = Kit.of(context).s;
    s.setName(_c.text.trim().isEmpty ? 'Student' : _c.text.trim());
    HighNav.of(context).back();
  }

  @override
  Widget build(BuildContext context) {
    final p = Kit.of(context).p;
    return Column(
      crossAxisAlignment: CrossAxisAlignment.stretch,
      children: [
        const Padding(padding: EdgeInsets.only(top: 4), child: Center(child: Kokob(width: 120))),
        Padding(
          padding: const EdgeInsets.fromLTRB(0, 4, 0, 6),
          child: Text('Selam! 👋', textAlign: TextAlign.center, style: ts(22, w900, p.ink)),
        ),
        Padding(
          padding: const EdgeInsets.only(bottom: 14),
          child: Text.rich(
            TextSpan(
              children: [
                const TextSpan(text: "I'm "),
                TextSpan(text: 'Kokob', style: ts(14, w900, p.ink2)),
                const TextSpan(text: ', your offline study buddy for Grade 9–12 and the matriculation exams. What should I call you?'),
              ],
            ),
            textAlign: TextAlign.center,
            style: ts(14, w700, p.ink2, height: 1.45),
          ),
        ),
        Padding(
          padding: const EdgeInsets.fromLTRB(0, 4, 0, 14),
          child: Field(controller: _c, placeholder: 'Student', maxLength: 24, onSubmitted: (_) => _go(), fieldKey: const ValueKey('obName')),
        ),
        Btn("Let's go", icon: 'play', block: true, onTap: _go),
        Padding(
          padding: const EdgeInsets.only(top: 12),
          child: Text('Everything stays on this phone — no internet needed.', textAlign: TextAlign.center, style: ts(12.5, w700, p.ink3)),
        ),
      ],
    );
  }
}
