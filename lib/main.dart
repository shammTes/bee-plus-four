import 'package:flutter/widgets.dart';

import 'high/app.dart';
import 'licensing/lock_screen.dart';
import 'licensing/unlock_store.dart';

/// 4. Locked until Bee Seller issues a HIGHSCHOOL code for this phone.
Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();
  final unlock = UnlockStore();
  await unlock.init();
  runApp(FourRoot(unlock: unlock));
}

class FourRoot extends StatefulWidget {
  const FourRoot({super.key, required this.unlock});
  final UnlockStore unlock;

  @override
  State<FourRoot> createState() => _FourRootState();
}

class _FourRootState extends State<FourRoot> {
  late bool _open = widget.unlock.isUnlocked;

  @override
  Widget build(BuildContext context) {
    return WidgetsApp(
      title: '4',
      color: const Color(0xFFE88A6E),
      debugShowCheckedModeBanner: false,
      pageRouteBuilder: <T>(RouteSettings s, WidgetBuilder b) => PageRouteBuilder<T>(settings: s, pageBuilder: (c, _, _) => b(c)),
      home: _open
          ? const HighScreen()
          : LockScreen(
              unlock: widget.unlock,
              onUnlocked: () {
                if (mounted) setState(() => _open = true);
              },
            ),
    );
  }
}
