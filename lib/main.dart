import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:hive_flutter/hive_flutter.dart';

import 'core/licensing/unlock_store.dart';
import 'core/progress/mastery_store.dart';
import 'core/progress/study_log.dart';
import 'core/settings/app_settings.dart';
import 'core/theme/four_theme.dart';
import 'features/shell/app_shell.dart';

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await Hive.initFlutter();
  await AppSettings.instance.init();
  await UnlockStore.instance.init();
  await MasteryStore.instance.init();
  await StudyLog.instance.init();
  SystemChrome.setSystemUIOverlayStyle(
    const SystemUiOverlayStyle(
      statusBarColor: Colors.transparent,
      statusBarIconBrightness: Brightness.light,
    ),
  );
  runApp(const FourApp());
}

class FourApp extends StatelessWidget {
  const FourApp({super.key});

  @override
  Widget build(BuildContext context) {
    return AnimatedBuilder(
      animation: AppSettings.instance,
      builder: (context, _) {
        final dark = AppSettings.instance.darkMode;
        return MaterialApp(
          title: '4',
          debugShowCheckedModeBanner: false,
          theme: FourTheme.highschool,
          darkTheme: FourTheme.highschoolDark,
          themeMode: dark ? ThemeMode.dark : ThemeMode.light,
          home: const AppShell(),
        );
      },
    );
  }
}
