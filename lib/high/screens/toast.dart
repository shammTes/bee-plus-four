// `.toast`: small dark pill above the nav for 1.8 s.
import 'dart:async';

import 'package:flutter/widgets.dart';

import '../theme/tokens.dart';
import '../widgets/kit.dart';

void toast(BuildContext context, String msg) {
  final ov = Overlay.maybeOf(context);
  if (ov == null) return;
  final p = Kit.of(context).p;
  late OverlayEntry e;
  e = OverlayEntry(builder: (_) => _Toast(msg: msg, p: p, onDone: () => e.remove()));
  ov.insert(e);
}

class _Toast extends StatefulWidget {
  const _Toast({required this.msg, required this.p, required this.onDone});
  final String msg;
  final Palette p;
  final VoidCallback onDone;
  @override
  State<_Toast> createState() => _ToastState();
}

class _ToastState extends State<_Toast> {
  // shown as is for 2.2 s (no fade: nothing animates while the student scrolls underneath)
  late final Timer _t = Timer(const Duration(milliseconds: 2200), () => widget.onDone());
  @override
  void initState() {
    super.initState();
    _t;
  }

  @override
  void dispose() {
    _t.cancel();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) => Positioned(
    left: 0,
    right: 0,
    bottom: 100 + MediaQuery.paddingOf(context).bottom,
    child: IgnorePointer(
      child: Center(
        child: DecoratedBox(
          decoration: BoxDecoration(
            color: widget.p.ink,
            borderRadius: BorderRadius.circular(99),
            boxShadow: const [BoxShadow(color: Color.fromRGBO(0, 0, 0, .18), offset: Offset(0, 3))],
          ),
          child: Padding(
            padding: const EdgeInsets.symmetric(horizontal: 18, vertical: 11),
            child: Text(widget.msg, style: ts(13.5, w900, widget.p.bg), textDirection: TextDirection.ltr),
          ),
        ),
      ),
    ),
  );
}
