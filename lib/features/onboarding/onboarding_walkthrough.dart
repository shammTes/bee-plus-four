import 'package:flutter/material.dart';

import '../../core/licensing/unlock_store.dart';
import '../../core/theme/four_theme.dart';

/// First-install guided walkthrough — Tigrinya only, animated, hands-on steps.
class OnboardingWalkthrough extends StatefulWidget {
  const OnboardingWalkthrough({super.key, required this.onFinished});

  final VoidCallback onFinished;

  static Future<bool> isDone() async {
    try {
      await UnlockStore.instance.init();
      return UnlockStore.instance.seenOnboarding;
    } catch (_) {
      return false;
    }
  }

  static Future<void> markDone() async {
    try {
      await UnlockStore.instance.markOnboardingSeen();
    } catch (_) {}
  }

  @override
  State<OnboardingWalkthrough> createState() => _OnboardingWalkthroughState();
}

class _OnboardingWalkthroughState extends State<OnboardingWalkthrough>
    with TickerProviderStateMixin {
  final _page = PageController();
  int _index = 0;
  late final AnimationController _pulse;
  late final AnimationController _float;

  static const _steps = <_Step>[
    _Step(
      title: 'እንቋዕ ናብ 4 መጻእኩም',
      body:
          '4 ን ኤርትራዊ ልዕሊ ደረጃ ትምህርቲ (G9–G12) ንኽትመሃሩ ዝተዳለየ ኦፍላይን መተግበሪ እዩ።\n\n'
          'ኣብዚ ሓጺር መምርሒ ብኢድኩም ከመይ ከም እትጥቀሙሉ ንርእየኩም።',
      tip: 'ንቐጻሊ ጠውቁ',
      color: Color(0xFF0D9488),
      icon: Icons.school_rounded,
    ),
    _Step(
      title: '1) ክፍልኹም ምረጹ',
      body:
          'ኣብ መእተዊ ገጽ፡\n'
          '• G9 ወይ G10 ምረጹ\n'
          '• ን G11 / G12፡ 11 Science · 11 Arts · 12 Science · 12 Arts\n\n'
          'እቲ ጠውቒ ናብ ናይቲ ክፍሊ መዘኻኸሪ፣ መጽሓፍ፣ ምልምማድን ማትሪክን የብጽሓኩም።',
      tip: 'ክፍሊ ምረጽ → ክፍቱ ገጽ ይኸፍት',
      color: Color(0xFF0284C7),
      icon: Icons.grid_view_rounded,
    ),
    _Step(
      title: '2) መዘኻኸሪን ስእላዊን',
      body:
          'ኣብ ናይ ክፍሊ ገጽ «Notes» ጠውቁ።\n\n'
          '• ክፍለ-ትምህርቲ (Unit) ምረጹ\n'
          '• ጽሑፋዊ መዘኻኸሪ ኣንብቡ\n'
          '• Illustrated / slides እንተሃልዩ ክፈቱ\n'
          '• Textbooks ንሙሉእ መጽሓፍ PDF',
      tip: 'Unit → Notes / Slides',
      color: Color(0xFF0F766E),
      icon: Icons.auto_stories_rounded,
    ),
    _Step(
      title: '3) ምልምማድ (Practice)',
      body:
          '«Practice» ጠውቁ፣ ድሕሪኡ፡\n'
          '• ትምህርትን ክፍለ-ትምህርትን ምረጹ\n'
          '• ሕቶታት ብዝርዝር ትርእዩ\n'
          '• መልሲ ኣረጋግጹን ምስራሕኹም ተኸታተሉ\n\n'
          'ብቕዓት (mastery) ድኹም ክፍለ-ትምህርቲ የርእየኩም።',
      tip: 'Grade → Subject → Unit → ሕቶታት',
      color: Color(0xFF7C3AED),
      icon: Icons.quiz_rounded,
    ),
    _Step(
      title: '4) ማትሪኩሌሽን ፈተና',
      body:
          'ኣብ መእተዊ «Matriculation» ዓቢ ቁልፊ ጠውቁ።\n\n'
          '• ትምህርቲ + ዓመት ምረጹ (ኣብነት Chemistry 2018)\n'
          '• ሕቶታት ብዝርዝር ኣንብቡ\n'
          '• መግለጺን ተመሳሳሊ ሕቶታትን እንተሃልዩ ተጠቐሙ\n\n'
          'ማትሪክ ንሃገራዊ ፈተና እዩ — ምስ unit practice ይተሓሓዝ።',
      tip: 'Subject · Year → ሕቶ',
      color: Color(0xFF4F46E5),
      icon: Icons.assignment_rounded,
    ),
    _Step(
      title: '5) ላብ · ኣሰልጣኒ · መሳርሒ',
      body:
          '• Virtual labs — PhET ኦፍላይን (ፊዚክስ · ኬሚስትሪ · ባዮ)\n'
          '• Coach — ብክፍሊ/ትምህርቲ ሕቶ ወይ መዘኻኸሪ\n'
          '• Tools — ኣሃዚ፣ ሰዓት፣ ካርድ\n\n'
          'ኩሉ ብዘይ ኢንተርነት ይሰርሕ።',
      tip: 'Also / Labs / Coach ኣብ መእተዊ',
      color: Color(0xFF0EA5E9),
      icon: Icons.science_rounded,
    ),
    _Step(
      title: '6) መኽፈቲ QR (Bee Seller)',
      body:
          'ኣብ መእተዊ Device ID / QR ኣሎ።\n\n'
          '1) እቲ QR ን Bee Seller ኣርእዩ\n'
          '2) ሸጣኢ unlock QR የውጽእ\n'
          '3) ኣብ 4 እቲ ኮድ ስካን ወይ ለጥፉ\n\n'
          'ሓደ ግዜ ዝኽፈተ መሳርሒ ብቐጻሊ ይኽፈት።',
      tip: 'Home → QR → Bee Seller',
      color: Color(0xFFEA580C),
      icon: Icons.qr_code_2_rounded,
    ),
    _Step(
      title: 'ተዳልዩኹም — ጀምሩ!',
      body:
          'ሕጂ፡\n'
          '✓ ክፍልኹም ምረጹ\n'
          '✓ መዘኻኸሪ ኣንብቡ\n'
          '✓ ምልምማድ ስረሑ\n'
          '✓ ማትሪክ ለምምዱ\n\n'
          'ዕውት ይግበረልኩም!',
      tip: 'ጀምር → ናብ መእተዊ',
      color: Color(0xFF059669),
      icon: Icons.rocket_launch_rounded,
    ),
  ];

  @override
  void initState() {
    super.initState();
    _pulse = AnimationController(
      vsync: this,
      duration: const Duration(milliseconds: 1200),
    )..repeat(reverse: true);
    _float = AnimationController(
      vsync: this,
      duration: const Duration(milliseconds: 1800),
    )..repeat(reverse: true);
  }

  @override
  void dispose() {
    _page.dispose();
    _pulse.dispose();
    _float.dispose();
    super.dispose();
  }

  Future<void> _finish() async {
    await OnboardingWalkthrough.markDone();
    widget.onFinished();
  }

  void _next() {
    if (_index >= _steps.length - 1) {
      _finish();
      return;
    }
    _page.nextPage(
      duration: const Duration(milliseconds: 380),
      curve: Curves.easeOutCubic,
    );
  }

  void _back() {
    if (_index == 0) return;
    _page.previousPage(
      duration: const Duration(milliseconds: 320),
      curve: Curves.easeOutCubic,
    );
  }

  @override
  Widget build(BuildContext context) {
    final step = _steps[_index];
    final last = _index == _steps.length - 1;

    return Scaffold(
      body: AnimatedContainer(
        duration: const Duration(milliseconds: 450),
        curve: Curves.easeOutCubic,
        decoration: BoxDecoration(
          gradient: LinearGradient(
            begin: Alignment.topLeft,
            end: Alignment.bottomRight,
            colors: [
              step.color,
              Color.lerp(step.color, const Color(0xFF0F172A), 0.35)!,
            ],
          ),
        ),
        child: SafeArea(
          child: Column(
            children: [
              Padding(
                padding: const EdgeInsets.fromLTRB(8, 4, 8, 0),
                child: Row(
                  children: [
                    TextButton(
                      onPressed: _finish,
                      child: const Text(
                        'ዝለል',
                        style: TextStyle(
                          color: Colors.white70,
                          fontWeight: FontWeight.w800,
                        ),
                      ),
                    ),
                    const Spacer(),
                    Text(
                      '${_index + 1} / ${_steps.length}',
                      style: const TextStyle(
                        color: Colors.white70,
                        fontWeight: FontWeight.w800,
                      ),
                    ),
                    const SizedBox(width: 8),
                  ],
                ),
              ),
              Padding(
                padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 8),
                child: Row(
                  children: List.generate(_steps.length, (i) {
                    final active = i == _index;
                    final done = i < _index;
                    return Expanded(
                      child: AnimatedContainer(
                        duration: const Duration(milliseconds: 280),
                        margin: const EdgeInsets.symmetric(horizontal: 2),
                        height: 4,
                        decoration: BoxDecoration(
                          borderRadius: BorderRadius.circular(4),
                          color: active || done ? Colors.white : Colors.white24,
                        ),
                      ),
                    );
                  }),
                ),
              ),
              Expanded(
                child: PageView.builder(
                  controller: _page,
                  itemCount: _steps.length,
                  onPageChanged: (i) => setState(() => _index = i),
                  itemBuilder: (context, i) {
                    final s = _steps[i];
                    return _StepPage(
                      step: s,
                      pulse: _pulse,
                      float: _float,
                      isActive: i == _index,
                    );
                  },
                ),
              ),
              Padding(
                padding: const EdgeInsets.fromLTRB(20, 8, 20, 20),
                child: Row(
                  children: [
                    if (_index > 0)
                      OutlinedButton(
                        onPressed: _back,
                        style: OutlinedButton.styleFrom(
                          foregroundColor: Colors.white,
                          side: const BorderSide(color: Colors.white54),
                          padding: const EdgeInsets.symmetric(
                              horizontal: 18, vertical: 14),
                        ),
                        child: const Text('ዝሓለፈ',
                            style: TextStyle(fontWeight: FontWeight.w800)),
                      )
                    else
                      const SizedBox(width: 88),
                    const Spacer(),
                    ScaleTransition(
                      scale: Tween(begin: 1.0, end: 1.04).animate(
                        CurvedAnimation(
                            parent: _pulse, curve: Curves.easeInOut),
                      ),
                      child: FilledButton(
                        onPressed: _next,
                        style: FilledButton.styleFrom(
                          backgroundColor: Colors.white,
                          foregroundColor: step.color,
                          padding: const EdgeInsets.symmetric(
                              horizontal: 28, vertical: 14),
                          elevation: 4,
                        ),
                        child: Text(
                          last ? 'ጀምር' : 'ቐጻሊ',
                          style: const TextStyle(
                            fontWeight: FontWeight.w900,
                            fontSize: 16,
                          ),
                        ),
                      ),
                    ),
                  ],
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}

class _Step {
  const _Step({
    required this.title,
    required this.body,
    required this.tip,
    required this.color,
    required this.icon,
  });
  final String title;
  final String body;
  final String tip;
  final Color color;
  final IconData icon;
}

class _StepPage extends StatelessWidget {
  const _StepPage({
    required this.step,
    required this.pulse,
    required this.float,
    required this.isActive,
  });

  final _Step step;
  final AnimationController pulse;
  final AnimationController float;
  final bool isActive;

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 24),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          const SizedBox(height: 12),
          Center(
            child: AnimatedBuilder(
              animation: float,
              builder: (context, child) {
                final dy = isActive ? (float.value - 0.5) * 12 : 0.0;
                return Transform.translate(offset: Offset(0, dy), child: child);
              },
              child: Container(
                width: 110,
                height: 110,
                decoration: BoxDecoration(
                  color: Colors.white.withOpacity(0.18),
                  borderRadius: BorderRadius.circular(32),
                  border: Border.all(color: Colors.white30, width: 2),
                ),
                child: Icon(step.icon, color: Colors.white, size: 48),
              ),
            ),
          ),
          const SizedBox(height: 28),
          Text(
            step.title,
            textAlign: TextAlign.center,
            style: const TextStyle(
              color: Colors.white,
              fontSize: 24,
              fontWeight: FontWeight.w900,
              height: 1.3,
              fontFamily: 'NotoSansEthiopic',
            ),
          ),
          const SizedBox(height: 16),
          Expanded(
            child: SingleChildScrollView(
              child: Container(
                width: double.infinity,
                padding: const EdgeInsets.all(18),
                decoration: BoxDecoration(
                  color: Colors.white.withOpacity(0.12),
                  borderRadius: BorderRadius.circular(20),
                  border: Border.all(color: Colors.white24),
                ),
                child: Text(
                  step.body,
                  style: const TextStyle(
                    color: Colors.white,
                    fontSize: 16,
                    height: 1.55,
                    fontWeight: FontWeight.w600,
                    fontFamily: 'NotoSansEthiopic',
                  ),
                ),
              ),
            ),
          ),
          const SizedBox(height: 12),
          Container(
            padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 12),
            decoration: BoxDecoration(
              color: Colors.white,
              borderRadius: BorderRadius.circular(14),
            ),
            child: Row(
              children: [
                Icon(Icons.touch_app_rounded, color: step.color, size: 22),
                const SizedBox(width: 10),
                Expanded(
                  child: Text(
                    step.tip,
                    style: TextStyle(
                      color: step.color,
                      fontWeight: FontWeight.w900,
                      fontSize: 14,
                      fontFamily: 'NotoSansEthiopic',
                    ),
                  ),
                ),
              ],
            ),
          ),
          const SizedBox(height: 8),
        ],
      ),
    );
  }
}
