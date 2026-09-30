import 'package:flutter/widgets.dart';

import 'high/app.dart';
import 'high/high.dart';
import 'high/state/app_state.dart';
import 'licensing/lock_screen.dart';
import 'licensing/unlock_store.dart';

/// 4. Locked until Bee Seller issues a HIGHSCHOOL code for this phone.
Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();
  final unlock = UnlockStore();
  await unlock.init();
  // Load notes + exams while the lock screen is up so unlock is not a blank cream frame.
  final loading = _warm();
  runApp(FourRoot(unlock: unlock, loading: loading));
}

Future<HighState> _warm() async {
  try {
    return await High.init(useIsolate: true);
  } catch (_) {
    High.reset();
    return High.init(useIsolate: false);
  }
}

class FourRoot extends StatefulWidget {
  const FourRoot({super.key, required this.unlock, required this.loading});
  final UnlockStore unlock;
  final Future<HighState> loading;

  @override
  State<FourRoot> createState() => _FourRootState();
}

class _FourRootState extends State<FourRoot> {
  late bool _open = widget.unlock.isUnlocked;
  HighState? _state;
  Object? _err;

  @override
  void initState() {
    super.initState();
    widget.loading.then((s) {
      if (mounted) setState(() => _state = s);
    }, onError: (Object e) {
      if (mounted) setState(() => _err = e);
    });
  }

  Future<void> _unlocked() async {
    // Let MobileScanner unmount before swapping to HighScreen (avoids a black frame).
    await Future<void>.delayed(const Duration(milliseconds: 200));
    if (mounted) setState(() => _open = true);
  }

  @override
  Widget build(BuildContext context) {
    return WidgetsApp(
      title: '4',
      color: const Color(0xFFE88A6E),
      debugShowCheckedModeBanner: false,
      pageRouteBuilder: <T>(RouteSettings s, WidgetBuilder b) => PageRouteBuilder<T>(settings: s, pageBuilder: (c, _, _) => b(c)),
      home: !_open
          ? LockScreen(unlock: widget.unlock, onUnlocked: _unlocked)
          : _state != null
              ? HighScreen(state: _state)
              : OpeningPane(err: _err, onRetry: _err == null ? null : _retry),
    );
  }

  void _retry() {
    setState(() => _err = null);
    High.reset();
    High.init(useIsolate: false).then((s) {
      if (mounted) setState(() => _state = s);
    }, onError: (Object e) {
      if (mounted) setState(() => _err = e);
    });
  }
}

/// Visible stand-in for the cream HighScreen loading box (looked blank on low-end phones).
class OpeningPane extends StatelessWidget {
  const OpeningPane({super.key, this.err, this.onRetry});
  final Object? err;
  final VoidCallback? onRetry;

  @override
  Widget build(BuildContext context) {
    const ink = Color(0xFF3E3129);
    const coral = Color(0xFFC24E32);
    return ColoredBox(
      color: const Color(0xFFFFFCF7),
      child: Directionality(
        textDirection: TextDirection.ltr,
        child: Center(
          child: Padding(
            padding: const EdgeInsets.all(28),
            child: Column(
              mainAxisSize: MainAxisSize.min,
              children: [
                const Text('4', textAlign: TextAlign.center, style: TextStyle(fontFamily: 'HighNunito', fontSize: 56, fontWeight: FontWeight.w900, color: coral)),
                const SizedBox(height: 14),
                Text(
                  err != null ? 'Could not open 4.\n$err' : 'Loading notes and exams\u2026',
                  textAlign: TextAlign.center,
                  style: const TextStyle(fontFamily: 'HighNunito', fontSize: 16, fontWeight: FontWeight.w800, color: ink, height: 1.35),
                ),
                if (onRetry != null) ...[
                  const SizedBox(height: 18),
                  GestureDetector(
                    onTap: onRetry,
                    child: const DecoratedBox(
                      decoration: BoxDecoration(color: coral, borderRadius: BorderRadius.all(Radius.circular(999))),
                      child: Padding(
                        padding: EdgeInsets.symmetric(horizontal: 22, vertical: 12),
                        child: Text('Try again', style: TextStyle(fontFamily: 'HighNunito', fontSize: 15, fontWeight: FontWeight.w900, color: Color(0xFFFFFFFF))),
                      ),
                    ),
                  ),
                ],
              ],
            ),
          ),
        ),
      ),
    );
  }
}
