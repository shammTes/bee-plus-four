import 'package:flutter/material.dart';

import '../../core/licensing/unlock_store.dart';
import '../../core/theme/four_theme.dart';

/// First-install guided walkthrough — Tigrinya, animated, hands-on steps.
class OnboardingWalkthrough extends StatefulWidget {
  const OnboardingWalkthrough({super.key, required this.onFinished});

  final VoidCallback onFinished;

  /// True after user finishes or skips onboarding.
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
      emoji: '👋',
      title: 'Welcome to 4',
      body:
          'Offline highschool study (G9–G12).\nNotes · Practice · Matric · Coach.',
      tip: 'Tap Next',
      color: Color(0xFF0D9488),
      icon: Icons.school_rounded,
    ),
    _Step(
      emoji: '📚',
      title: 'Pick your grade',
      body: 'Choose G9–G12 on Home. Switch anytime.',
      tip: 'Grade chips on Home',
      color: Color(0xFF0284C7),
      icon: Icons.grid_view_rounded,
    ),
    _Step(
      emoji: '📝',
      title: 'Notes & illustrated',
      body: 'Open Units → notes, illustrated decks, textbook at unit.',
      tip: 'Notes tab',
      color: Color(0xFF0F766E),
      icon: Icons.auto_stories_rounded,
    ),
    _Step(
      emoji: '✅',
      title: 'Practice',
      body: 'MCQs with answers & explanations. List any question.',
      tip: 'Practice tab',
      color: Color(0xFF7C3AED),
      icon: Icons.quiz_rounded,
    ),
    _Step(
      emoji: '📋',
      title: 'Matric & model exams',
      body: 'Past papers + explanations + similar practice.',
      tip: 'Exams tab',
      color: Color(0xFF4F46E5),
      icon: Icons.assignment_rounded,
    ),
    _Step(
      emoji: '📱',
      title: 'Unlock with Bee Seller',
      body: 'Show Device ID or scan the seller QR to unlock.',
      tip: 'Unlock / Scan QR',
      color: Color(0xFFEA580C),
      icon: Icons.qr_code_2_rounded,
    ),
    _Step(
      emoji: '🚀',
      title: 'Ready — start!',
      body: 'Study offline. Good luck!',
      tip: 'Start',
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
                        'Skip',
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
                        child: const Text('Back',
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
                          last ? 'Start' : 'Next',
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
    required this.emoji,
    required this.title,
    required this.body,
    required this.tip,
    required this.color,
    required this.icon,
  });
  final String emoji;
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
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    Text(step.emoji, style: const TextStyle(fontSize: 36)),
                    const SizedBox(height: 4),
                    Icon(step.icon, color: Colors.white, size: 28),
                  ],
                ),
              ),
            ),
          ),
          const SizedBox(height: 28),
          Text(
            step.title,
            textAlign: TextAlign.center,
            style: const TextStyle(
              color: Colors.white,
              fontSize: 26,
              fontWeight: FontWeight.w900,
              height: 1.25,
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
