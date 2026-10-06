// Hidden pages must not rebuild on state changes; they catch up once when shown again.
import 'package:flutter/widgets.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:high/high/data/repository.dart';
import 'package:high/high/state/app_state.dart';
import 'package:high/high/state/page_gate.dart';

class _Reader extends StatelessWidget {
  const _Reader(this.builds);
  final List<int> builds;
  @override
  Widget build(BuildContext context) {
    HighScope.of(context);
    builds[0]++;
    return const SizedBox();
  }
}

/// like HighShell: the page widgets are the same instances on every shell rebuild
class _Host extends StatelessWidget {
  const _Host(this.s, this.top, this.a, this.b, this.outside);
  final HighState s;
  final int top;
  final Widget a, b, outside;
  @override
  Widget build(BuildContext context) => HighScope(
    state: s,
    child: Column(
      children: [
        PageGate(key: const ValueKey('a'), active: top == 0, child: a),
        PageGate(key: const ValueKey('b'), active: top == 1, child: b),
        outside,
      ],
    ),
  );
}

void main() {
  testWidgets('only the page on top rebuilds; a hidden page catches up once when shown', (t) async {
    final s = HighState(ExamRepo());
    final a = [0], b = [0], out = [0];
    final ra = _Reader(a), rb = _Reader(b), ro = _Reader(out);
    await t.pumpWidget(_Host(s, 0, ra, rb, ro));
    expect((a[0], b[0], out[0]), (1, 1, 1));

    for (var i = 0; i < 3; i++) {
      s.contentChanged();
      await t.pump();
    }
    expect(a[0], 4); // visible page: every change, as before
    expect(b[0], 1); // hidden page: none
    expect(out[0], 4); // readers outside any page (shell, nav bar) unchanged

    await t.pumpWidget(_Host(s, 1, ra, rb, ro)); // b comes on top
    expect(b[0], 2); // one catch-up rebuild
    s.contentChanged();
    await t.pump();
    expect(b[0], 3);
    expect(a[0], 4); // a is hidden now

    await t.pumpWidget(_Host(s, 0, ra, rb, ro));
    expect(a[0], 5);
    await t.pumpWidget(_Host(s, 1, ra, rb, ro)); // nothing changed while b was hidden: no rebuild
    expect(b[0], 3);
  });
}
