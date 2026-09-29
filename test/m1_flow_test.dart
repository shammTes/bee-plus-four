// M1 interaction smoke test: onboarding, bottom nav, home category cards, exams filters/search, settings.
import 'package:flutter/widgets.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:high/high/app.dart';
import 'package:high/high/data/repository.dart';
import 'package:high/high/screens/exams.dart';
import 'package:high/high/screens/settings.dart';
import 'package:high/high/state/app_state.dart';
import 'package:high/high/widgets/page.dart';
import 'package:shared_preferences/shared_preferences.dart';

import 'helpers.dart';

void main() {
  HighState.tickStudy = false;
  highDecorAnimations = false;
  final repo = ExamRepo(useIsolate: false);
  setUpAll(loadFonts);

  Future<HighState> boot(WidgetTester t, {Map<String, Object> prefs = const {}}) async {
    t.view.physicalSize = const Size(780, 1688);
    t.view.devicePixelRatio = 2;
    addTearDown(t.view.reset);
    await t.runAsync(repo.init);
    SharedPreferences.setMockInitialValues(prefs);
    final s = HighState(repo, await SharedPreferences.getInstance());
    await s.load();
    await t.pumpWidget(HighApp(state: s));
    await t.pumpAndSettle();
    return s;
  }

  testWidgets('onboarding asks for a name', (t) async {
    final s = await boot(t);
    expect(find.text('Selam! 👋'), findsOneWidget);
    await t.enterText(find.byKey(const ValueKey('obName')), 'Selam');
    await t.tap(find.text("Let's go"));
    await t.pumpAndSettle();
    expect(s.name, 'Selam');
    expect(find.text('Selam! 👋'), findsNothing);
    expect(find.textContaining('Selam!'), findsOneWidget); // greeting
    await t.pump(const Duration(seconds: 1));
  });

  testWidgets('nav, category cards, exams filters, settings', (t) async {
    final s = await boot(t, prefs: {HighState.key: '{"v":2,"name":"Hana","theme":"light","cat":"matric"}'});
    // home -> Model card opens the Exams tab on the model category
    await t.ensureVisible(find.text('Model Exams'));
    await t.pumpAndSettle();
    await t.tap(find.text('Model Exams'));
    await t.pumpAndSettle();
    expect(s.cat, 'model');
    expect(find.byType(ExamsPage), findsOneWidget);
    expect(find.text('Model Exams '), findsNothing);
    // category segment back to matriculation, then a year chip
    await t.tap(find.text('Matriculation'));
    await t.pumpAndSettle();
    expect(s.cat, 'matric');
    await t.tap(find.text('2023').first);
    await t.pumpAndSettle();
    await t.scrollUntilVisible(find.textContaining('2023 Matriculation exams by subject'), 400, scrollable: find.byType(Scrollable).first);
    expect(find.textContaining('2023 Matriculation exams by subject'), findsOneWidget);
    HighNav.of(t.element(find.byType(ExamsPage))).tab(HighTab.matric);
    await t.pumpAndSettle();
    await t.tap(find.text('All years'));
    await t.pumpAndSettle();
    // search
    await t.enterText(find.byType(EditableText), 'bio');
    await t.pumpAndSettle();
    expect(find.text('Chemistry'), findsNothing);
    expect(find.text('Biology'), findsWidgets);
    await t.enterText(find.byType(EditableText), '');
    await t.pumpAndSettle();
    // every tab opens
    for (final l in ['Notes', 'Exercise', 'Tutor', 'Home', 'Matric']) {
      await t.tap(find.text(l).last);
      await t.pumpAndSettle();
      expect(tester(t).takeException(), isNull);
    }
    // settings (pushed from the Home avatar): theme + name + reset
    HighNav.of(t.element(find.byType(ExamsPage))).push(const SettingsPage());
    await t.pumpAndSettle();
    expect(find.byType(SettingsPage), findsOneWidget);
    await t.tap(find.text('Dark'));
    await t.pumpAndSettle();
    expect(s.dark, isTrue);
    await t.tap(find.text('Auto'));
    await t.pumpAndSettle();
    expect(s.theme, isNull);
    await t.enterText(find.byKey(const ValueKey('nameField')), 'Abeba');
    await t.tap(find.text('Save name'));
    await t.pumpAndSettle();
    expect(s.name, 'Abeba');
    s.answers['x'] = {'c': 'A', 'ok': true, 't': 1};
    await t.scrollUntilVisible(find.text('Reset'), 200, scrollable: find.byType(Scrollable).first);
    await t.tap(find.text('Reset'));
    await t.pumpAndSettle();
    await t.tap(find.text('Tap again'));
    await t.pumpAndSettle();
    expect(s.answers, isEmpty);
    // theme toggle in the top bar
    await t.tap(find.bySemanticsLabel('Toggle dark mode'));
    await t.pumpAndSettle();
    expect(s.theme, isNotNull);
    await t.pump(const Duration(seconds: 3));
  });

  testWidgets('HighScreen embeds in a host app route', (t) async {
    t.view.physicalSize = const Size(780, 1688);
    t.view.devicePixelRatio = 2;
    addTearDown(t.view.reset);
    await t.runAsync(repo.init);
    SharedPreferences.setMockInitialValues({HighState.key: '{"v":2,"name":"Host"}'});
    final s = HighState(repo, await SharedPreferences.getInstance());
    await s.load();
    await t.pumpWidget(
      WidgetsApp(
        color: const Color(0xFF000000),
        pageRouteBuilder: <T>(RouteSettings st, WidgetBuilder b) => PageRouteBuilder<T>(settings: st, pageBuilder: (c, _, _) => b(c)),
        home: Builder(
          builder: (c) => GestureDetector(
            onTap: () => Navigator.of(c).push(PageRouteBuilder<void>(pageBuilder: (_, _, _) => HighScreen(state: s, initialTab: HighTab.matric))),
            child: const Center(child: Text('Open High', textDirection: TextDirection.ltr)),
          ),
        ),
      ),
    );
    await t.tap(find.text('Open High'));
    await t.pumpAndSettle();
    expect(find.byType(ExamsPage), findsOneWidget);
    // system back: Exams -> Home -> pops back to the host
    await t.binding.handlePopRoute();
    await t.pumpAndSettle();
    expect(find.text('Matric & notes'), findsOneWidget);
    await t.binding.handlePopRoute();
    await t.pumpAndSettle();
    expect(find.text('Open High'), findsOneWidget);
    await t.pump(const Duration(seconds: 1));
  });
}

WidgetTester tester(WidgetTester t) => t;
