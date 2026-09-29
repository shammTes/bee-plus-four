import 'package:flutter/widgets.dart';

import 'high/high.dart';
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
    if (_open) return const HighApp();
    return WidgetsApp(
      title: '4',
      color: const Color(0xFFE88A6E),
      debugShowCheckedModeBanner: false,
      builder: (_, _) => LockScreen(
        unlock: widget.unlock,
        onUnlocked: () {
          if (mounted) setState(() => _open = true);
        },
      ),
    );
  }
}
