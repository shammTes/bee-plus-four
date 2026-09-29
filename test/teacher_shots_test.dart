// Screenshots: teacher picker, board, homework sheet -> compare/teacher_*.png, compare/homework_sheet.png
import 'dart:convert';
import 'dart:io';
import 'dart:ui' as ui;

import 'package:flutter/rendering.dart';
import 'package:flutter/widgets.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:high/high/app.dart';
import 'package:high/high/data/repository.dart';
import 'package:high/high/notes/jr/data/repository.dart';
import 'package:high/high/state/app_state.dart';
import 'package:high/high/teacher/teacher.dart';
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
      final img = await ro.toImage(pixelRatio: 2);
      final bd = await img.toByteData(format: ui.ImageByteFormat.png);
      File('compare/$name.png').writeAsBytesSync(bd!.buffer.asUint8List());
    });
  }

  testWidgets('teacher shots', (t) async {
    t.view.physicalSize = const Size(780, 1688);
    t.view.devicePixelRatio = 2;
    addTearDown(t.view.reset);
    final e = repo.exams.firstWhere((e) => e.subject == 'Physics' && e.questions.any((q) => q.image != null), orElse: () => repo.exams.first);
    final pick = [...e.questions.where((q) => q.image != null).take(2), ...e.mcqs.take(6)].map((q) => q.id).toSet().toList();
    SharedPreferences.setMockInitialValues({HighState.key: jsonEncode({'v': 2, 'name': 'Hana', 'theme': 'light', 'teacher': true, 'basket': pick})});
    final s = HighState(repo, await SharedPreferences.getInstance(), notes);
    await s.load();
    await t.pumpWidget(RepaintBoundary(key: key, child: HighApp(state: s)));
    await t.pumpAndSettle();
    final nav = HighNav.of(t.element(find.byType(PageShell).first));
    nav.open('teacher', () => const TeacherPage());
    await save(t, 'teacher_pick');
    nav.push(BoardPage(ids: pick));
    await save(t, 'teacher_board');
    final code = repo.codes!.setCode(pick);
    // ignore: avoid_print
    print('set code for ${pick.length} questions: $code (${code.length} chars)');
    nav.open('hw', () => HomeworkPage(ids: repo.codes!.canonical(pick), code: code));
    await save(t, 'homework_sheet');
    await t.pump(const Duration(seconds: 5));
  });
}
