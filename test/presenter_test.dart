// Presenter (TV) mode at 1920×1080: step reveal via keys/buttons, notes + question slides; screenshots.
import 'dart:convert';
import 'dart:io';
import 'dart:ui' as ui;

import 'package:flutter/rendering.dart';
import 'package:flutter/services.dart';
import 'package:flutter/widgets.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:high/high/app.dart';
import 'package:high/high/data/repository.dart';
import 'package:high/high/notes/jr/data/repository.dart';
import 'package:high/high/notes/jr/screens/unit_page.dart';
import 'package:high/high/state/app_state.dart';
import 'package:high/high/teacher/presenter.dart';
import 'package:high/high/widgets/page.dart';
import 'package:shared_preferences/shared_preferences.dart';

import 'helpers.dart';

void main() {
  HighState.tickStudy = false;
  highDecorAnimations = false;
  highNow = () => DateTime(2026, 9, 29, 10);
  final repo = ExamRepo(useIsolate: false), notes = NotesRepo(useIsolate: false);
  final key = GlobalKey();
  setUpAll(() async {
    await loadFonts();
    await repo.init();
    await notes.init();
  });

  Future<void> save(WidgetTester t, String name) async {
    for (var i = 0; i < 4; i++) {
      await t.runAsync(() => Future<void>.delayed(const Duration(milliseconds: 80)));
      await t.pump(const Duration(milliseconds: 100));
    }
    await t.pumpAndSettle();
    final ro = t.renderObject<RenderRepaintBoundary>(find.byKey(key));
    await t.runAsync(() async {
      final img = await ro.toImage(pixelRatio: 1);
      final bd = await img.toByteData(format: ui.ImageByteFormat.png);
      File('compare/$name.png').writeAsBytesSync(bd!.buffer.asUint8List());
    });
  }

  testWidgets('presenter at 1920x1080', (t) async {
    t.view.physicalSize = const Size(1920, 1080);
    t.view.devicePixelRatio = 1;
    addTearDown(t.view.reset);
    SharedPreferences.setMockInitialValues({HighState.key: jsonEncode({'v': 2, 'name': 'Hana', 'theme': 'light'})});
    final s = HighState(repo, await SharedPreferences.getInstance(), notes);
    await s.load();
    await t.pumpWidget(RepaintBoundary(key: key, child: HighApp(state: s)));
    await t.pumpAndSettle();
    expect(t.takeException(), isNull);
    final nav = HighNav.of(t.element(find.byType(PageShell).first));

    // notes unit page scaled for the TV
    final b = notes.grade(10).firstWhere((b) => b.subject == 'physics');
    nav.push(UnitPage(bookId: b.id, unitId: b.units.first.id));
    await t.runAsync(() => notes.book(b.id));
    await t.pumpAndSettle();
    await save(t, 'tv_unit_page');
    expect(t.takeException(), isNull);

    // present the unit notes
    await t.tap(find.bySemanticsLabel('Present').first);
    await t.pumpAndSettle();
    expect(find.byType(PresenterPage), findsOneWidget);
    await t.sendKeyEvent(LogicalKeyboardKey.arrowRight);
    await t.pumpAndSettle();
    expect(find.textContaining('2 / '), findsOneWidget);
    await save(t, 'tv_present_notes');
    nav.back();
    await t.pumpAndSettle();

    // a question with a figure and steps: reveal steps then the answer
    final q = [for (final e in repo.exams) ...e.mcqs].firstWhere((q) => q.image != null && q.steps.length >= 2);
    nav.push(PresenterPage(slides: [QuestionSlide(q, n: 1)]));
    await t.pumpAndSettle();
    expect(find.textContaining('Answer:', findRichText: true), findsNothing);
    for (var i = 0; i < q.steps.length; i++) {
      await t.tap(find.text('Reveal'));
      await t.pumpAndSettle();
    }
    expect(find.textContaining('Answer:', findRichText: true), findsOneWidget);
    await save(t, 'tv_present_question');
    expect(t.takeException(), isNull);
    nav.back();
    await t.pumpAndSettle();
    await t.pump(const Duration(seconds: 5));
  });
}
