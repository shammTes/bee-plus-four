import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:hive_flutter/hive_flutter.dart';

import 'core/licensing/unlock_store.dart';
import 'core/theme/four_theme.dart';
import 'features/onboarding/onboarding_walkthrough.dart';
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
      title: '4',
      debugShowCheckedModeBanner: false,
      theme: FourTheme.highschool,
      home: const _RootGate(),
    );
  }
}

class _RootGate extends StatefulWidget {
  const _RootGate();

  @override
  State<_RootGate> createState() => _RootGateState();
}

class _RootGateState extends State<_RootGate> {
  bool? _done;

  @override
  void initState() {
    super.initState();
    OnboardingWalkthrough.isDone().then((v) {
      if (mounted) setState(() => _done = v);
    });
  }

  @override
  Widget build(BuildContext context) {
    if (_done == null) {
      return const Scaffold(
        body: Center(child: CircularProgressIndicator()),
      );
    }
    if (!_done!) {
      return OnboardingWalkthrough(
        onFinished: () => setState(() => _done = true),
      );
    }
    return const AppShell();
  }
}
