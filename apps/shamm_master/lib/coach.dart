import 'package:flutter/material.dart';

import 'widgets.dart';

class CoachStep {
  const CoachStep({required this.target, required this.title, required this.text, this.tab});
  final GlobalKey target;
  final String title;
  final String text;

  /// Bottom tab to open before this step.
  final int? tab;
}

/// Step-by-step coach marks: dims the screen, cuts a hole around one thing, explains it. Next / Back / Skip.
class CoachTour extends StatefulWidget {
  const CoachTour({super.key, required this.steps, required this.onDone, required this.onTab});
  final List<CoachStep> steps;
  final VoidCallback onDone;
  final ValueChanged<int> onTab;

  @override
  State<CoachTour> createState() => _CoachTourState();
}

class _CoachTourState extends State<CoachTour> {
  int i = 0;
  Rect? hole;

  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addPostFrameCallback((_) => _go(0));
  }

  Future<void> _go(int n) async {
    final s = widget.steps[n];
    if (s.tab != null) widget.onTab(s.tab!);
    setState(() {
      i = n;
      hole = null;
    });
    // Let the tab build, then scroll the target into view and measure it.
    await Future<void>.delayed(const Duration(milliseconds: 60));
    final ctx = s.target.currentContext;
    if (ctx == null || !mounted) return;
    if (!ctx.mounted) return;
    await Scrollable.ensureVisible(ctx, alignment: 0.3, duration: const Duration(milliseconds: 200));
    if (!mounted || !ctx.mounted) return;
    final box = ctx.findRenderObject() as RenderBox?;
    final me = context.findRenderObject() as RenderBox?;
    if (box == null || me == null || !box.hasSize) return;
    final tl = box.localToGlobal(Offset.zero, ancestor: me);
    setState(() => hole = (tl & box.size).inflate(6));
  }

  void next() => i + 1 < widget.steps.length ? _go(i + 1) : widget.onDone();

  @override
  Widget build(BuildContext context) {
    final s = widget.steps[i];
    final size = MediaQuery.sizeOf(context);
    final h = hole;
    final below = h == null || h.center.dy < size.height / 2;
    final bubble = Card(
      key: const Key('coachBubble'),
      elevation: 6,
      child: Padding(
        padding: const EdgeInsets.fromLTRB(18, 16, 12, 8),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              'Step ${i + 1} of ${widget.steps.length}',
              style: const TextStyle(color: brand, fontWeight: FontWeight.w700, fontSize: 13),
            ),
            const SizedBox(height: 4),
            Text(
              s.title,
              style: const TextStyle(fontSize: 18, fontWeight: FontWeight.w800, color: ink),
            ),
            const SizedBox(height: 6),
            Text(s.text, style: const TextStyle(fontSize: 15, color: ink, height: 1.35)),
            const SizedBox(height: 6),
            Row(
              children: [
                TextButton(key: const Key('coachSkip'), onPressed: widget.onDone, child: const Text('Skip')),
                const Spacer(),
                if (i > 0) TextButton(onPressed: () => _go(i - 1), child: const Text('Back')),
                FilledButton(
                  key: const Key('coachNext'),
                  style: FilledButton.styleFrom(minimumSize: const Size(96, 44)),
                  onPressed: next,
                  child: Text(i + 1 == widget.steps.length ? 'Done' : 'Next'),
                ),
              ],
            ),
          ],
        ),
      ),
    );
    return Stack(
      children: [
        Positioned.fill(
          child: GestureDetector(
            onTap: next,
            child: CustomPaint(painter: _HolePainter(h)),
          ),
        ),
        Positioned(
          left: 16,
          right: 16,
          top: below ? ((h?.bottom ?? size.height * 0.3) + 12).clamp(0, size.height - 260) : null,
          bottom: below ? null : (size.height - h.top + 12).clamp(0, size.height - 260),
          child: bubble,
        ),
      ],
    );
  }
}

class _HolePainter extends CustomPainter {
  _HolePainter(this.hole);
  final Rect? hole;

  @override
  void paint(Canvas canvas, Size size) {
    final path = Path()
      ..fillType = PathFillType.evenOdd
      ..addRect(Offset.zero & size);
    if (hole != null) path.addRRect(RRect.fromRectAndRadius(hole!, const Radius.circular(16)));
    canvas.drawPath(path, Paint()..color = const Color(0xB3000000));
    if (hole != null) {
      canvas.drawRRect(
        RRect.fromRectAndRadius(hole!, const Radius.circular(16)),
        Paint()
          ..style = PaintingStyle.stroke
          ..strokeWidth = 3
          ..color = const Color(0xFFA5B4FC),
      );
    }
  }

  @override
  bool shouldRepaint(_HolePainter old) => old.hole != hole;
}
