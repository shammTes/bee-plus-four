// Renders High at 390×844 logical px @2x with the bundled fonts, the web-generated progress seed
// (compare/seed_progress.json) and the same fixed clock as tool/shoot_web.py -> compare/flutter/<scene>.png
//   flutter test test/screenshots_test.dart
import 'dart:convert';
import 'dart:io';
import 'dart:ui' as ui;

import 'package:flutter/rendering.dart';
import 'package:flutter/widgets.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:high/high/app.dart';
import 'package:high/high/data/repository.dart';
import 'package:high/high/state/app_state.dart';
import 'package:high/high/widgets/page.dart';
import 'package:shared_preferences/shared_preferences.dart';

import 'helpers.dart';

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();
  HighState.tickStudy = false;
  highDecorAnimations = false;
  highNow = () => DateTime(2026, 9, 29, 10);
  final repo = ExamRepo(useIsolate: false);
  final shotKey = GlobalKey();
  final seed = jsonDecode(File('compare/seed_progress.json').readAsStringSync()) as Map<String, dynamic>;

  setUpAll(() async {
    await loadFonts();
    await repo.init();
  });

  Map<String, dynamic> fresh() => {'v': 2, 'name': 'Hana', 'theme': 'light', 'cat': 'matric', 'answers': {}, 'bookmarks': [], 'mistakes': [], 'ev': [], 'study': {}, 'recent': [], 'attempts': [], 'daily': {}};

  Future<void> shoot(WidgetTester tester, String name, {required Map<String, dynamic> state, bool dark = false, HighTab tab = HighTab.home, double scroll = 0}) async {
    tester.view.physicalSize = const Size(780, 1688);
    tester.view.devicePixelRatio = 2;
    addTearDown(tester.view.reset);
    final st = Map<String, dynamic>.from(state)..['theme'] = dark ? 'dark' : 'light';
    SharedPreferences.setMockInitialValues({HighState.key: jsonEncode(st)});
    final s = HighState(repo, await SharedPreferences.getInstance());
    await s.load();
    await tester.pumpWidget(
      RepaintBoundary(
        key: shotKey,
        child: HighApp(state: s, initialTab: tab),
      ),
    );
    for (var i = 0; i < 6; i++) {
      await tester.runAsync(() => Future<void>.delayed(const Duration(milliseconds: 60)));
      await tester.pump(const Duration(milliseconds: 100));
    }
    await tester.pumpAndSettle();
    if (scroll > 0) {
      final sc = tester.stateList<ScrollableState>(find.byType(Scrollable)).firstWhere((x) => x.position.axis == Axis.vertical);
      sc.position.jumpTo(scroll.clamp(0, sc.position.maxScrollExtent));
      await tester.pumpAndSettle();
    }
    final ro = tester.renderObject<RenderRepaintBoundary>(find.byKey(shotKey));
    await tester.runAsync(() async {
      final img = await ro.toImage(pixelRatio: 2);
      final bd = await img.toByteData(format: ui.ImageByteFormat.png);
      File('compare/flutter/$name.png')
        ..createSync(recursive: true)
        ..writeAsBytesSync(bd!.buffer.asUint8List());
    });
  }

  for (final dark in [false, true]) {
    final x = dark ? '_dark' : '';
    testWidgets('home_fresh$x', (t) => shoot(t, 'home_fresh$x', state: fresh(), dark: dark));
    testWidgets('home$x', (t) => shoot(t, 'home$x', state: seed, dark: dark));
    testWidgets('home_mid$x', (t) => shoot(t, 'home_mid$x', state: seed, dark: dark, scroll: 760));
    testWidgets('home_end$x', (t) => shoot(t, 'home_end$x', state: seed, dark: dark, scroll: 1500));
    testWidgets('exams$x', (t) => shoot(t, 'exams$x', state: seed, dark: dark, tab: HighTab.matric));
    testWidgets('exams_list$x', (t) => shoot(t, 'exams_list$x', state: seed, dark: dark, tab: HighTab.matric, scroll: 700));
    testWidgets('exams_rows$x', (t) => shoot(t, 'exams_rows$x', state: seed, dark: dark, tab: HighTab.matric, scroll: 1500));
    testWidgets('exams_model$x', (t) => shoot(t, 'exams_model$x', state: {...seed, 'cat': 'model'}, dark: dark, tab: HighTab.matric));
    testWidgets('settings$x', (t) => shoot(t, 'settings$x', state: seed, dark: dark, tab: HighTab.home));
  }
}
