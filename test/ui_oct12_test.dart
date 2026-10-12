// Small-phone check (360×640 logical) of the main screens with the app's +10% text size: no overflow / layout
// exception on Home (incl. quote + Study Coach cards), Notes, Exercise, Matric (a question with maths), Tutor (an
// answer) and Settings/About. SHOT_DIR=dir writes a PNG per screen (used for the PR before/after screenshots).
import 'dart:convert';
import 'dart:io';
import 'dart:ui' as ui;

import 'package:flutter/rendering.dart';
import 'package:flutter/widgets.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:high/high/app.dart';
import 'package:high/high/data/repository.dart';
import 'package:high/high/exam/pages.dart';
import 'package:high/high/notes/jr/data/repository.dart';
import 'package:high/high/screens/settings.dart';
import 'package:high/high/state/app_state.dart';
import 'package:high/high/tutor/tutor_page.dart';
import 'package:high/high/widgets/page.dart';
import 'package:shared_preferences/shared_preferences.dart';

import 'helpers.dart';

void main() {
  HighState.tickStudy = false;
  highDecorAnimations = false;
  highNow = () => DateTime(2026, 10, 12, 10);
  final repo = ExamRepo(useIsolate: false), notes = NotesRepo(useIsolate: false);
  final key = GlobalKey();
  final dir = Platform.environment['SHOT_DIR'];
  setUpAll(() async {
    await loadFonts();
    await repo.init();
    await notes.init();
  });

  Future<void> settle(WidgetTester t) async {
    for (var i = 0; i < 4; i++) {
      await t.runAsync(() => Future<void>.delayed(const Duration(milliseconds: 60)));
      await t.pump(const Duration(milliseconds: 100));
    }
    await t.pumpAndSettle();
    expect(t.takeException(), isNull);
  }

  Future<void> shot(WidgetTester t, String name) async {
    await settle(t);
    if (dir == null) return;
    Directory(dir).createSync(recursive: true);
    final ro = t.renderObject<RenderRepaintBoundary>(find.byKey(key));
    await t.runAsync(() async {
      final img = await ro.toImage(pixelRatio: 2);
      final bd = await img.toByteData(format: ui.ImageByteFormat.png);
      File('$dir/$name.png').writeAsBytesSync(bd!.buffer.asUint8List());
    });
  }

  Future<HighState> app(WidgetTester t, HighTab tab) async {
    t.view.physicalSize = const Size(720, 1280);
    t.view.devicePixelRatio = 2;
    addTearDown(t.view.reset);
    SharedPreferences.setMockInitialValues({HighState.key: jsonEncode({'v': 2, 'name': 'Hana', 'theme': 'light', 'tourDone': true})});
    final s = HighState(repo, await SharedPreferences.getInstance(), notes);
    await s.load();
    await t.pumpWidget(RepaintBoundary(key: key, child: HighApp(state: s, initialTab: tab)));
    await t.pumpAndSettle();
    return s;
  }

  testWidgets('home 360x640', (t) async {
    await app(t, HighTab.home);
    await shot(t, 'home');
    expect(find.text('Start studying'), findsNothing);
    final list = find.byType(Scrollable).first;
    for (var i = 1; i <= 3; i++) {
      await t.drag(list, const Offset(0, -420));
      await shot(t, 'home_$i');
    }
  });

  for (final tab in [HighTab.notes, HighTab.exercise, HighTab.matric]) {
    testWidgets('${tab.name} tab 360x640', (t) async {
      await app(t, tab);
      await shot(t, tab.name);
    });
  }

  testWidgets('matric question with maths 360x640', (t) async {
    await app(t, HighTab.matric);
    await t.runAsync(() => repo.ensureAllExams());
    HighNav.of(t.element(find.byType(PageShell).first)).push(const PracticePage(examId: 'bank-physics-matric-2024', focus: 'bank-physics-matric-2024-q045'));
    await shot(t, 'matric_formula');
  });

  testWidgets('tutor answer 360x640', (t) async {
    resetTutorChat();
    await app(t, HighTab.home);
    await t.tap(find.text('Tutor').last);
    await t.pumpAndSettle();
    expect(find.byType(TutorPage), findsOneWidget);
    await t.enterText(find.byType(EditableText), 'quadratic formula');
    await t.testTextInput.receiveAction(TextInputAction.done);
    for (var i = 0; i < 60 && find.textContaining('Looking it up').evaluate().isNotEmpty || i < 3; i++) {
      await t.runAsync(() => Future<void>.delayed(const Duration(milliseconds: 200)));
      await t.pump(const Duration(milliseconds: 100));
    }
    await t.pump(const Duration(milliseconds: 400));
    await shot(t, 'tutor_answer');
    expect(find.textContaining('📘'), findsWidgets);
  });

  testWidgets('settings / about 360x640', (t) async {
    await app(t, HighTab.home);
    HighNav.of(t.element(find.byType(PageShell).first)).push(const SettingsPage());
    await settle(t);
    await t.drag(find.byType(Scrollable).first, const Offset(0, -3000));
    await shot(t, 'about');
    expect(find.textContaining('works fully offline'), findsNothing);
  });
}
