import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:hive_flutter/hive_flutter.dart';

import 'core/licensing/unlock_store.dart';
import 'core/theme/four_theme.dart';
import 'features/shell/app_shell.dart';

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await SystemChrome.setEnabledSystemUIMode(SystemUiMode.edgeToEdge);
  await Hive.initFlutter();
  await UnlockStore.instance.init();
  runApp(const FourApp());
}

/// App 4 — Highschool curriculum only + offline controlled bot.
class FourApp extends StatelessWidget {
  const FourApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'BEE PLUS 4',
      debugShowCheckedModeBanner: false,
      theme: FourTheme.highschool,
      home: const AppShell(),
    );
  }
}
