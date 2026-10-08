// Coach marks: walks every step on the real Home screen and saves a screenshot per step.
//   flutter test test/coach_marks_test.dart   → /workspace/shots/coach/ (or $COACH_SHOTS) + checks
import 'dart:convert';
import 'dart:io';
import 'dart:ui' as ui;

import 'package:flutter/rendering.dart';
import 'package:flutter/widgets.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:high/high/app.dart';
import 'package:high/high/data/repository.dart';
import 'package:high/high/state/app_state.dart';
import 'package:high/high/widgets/coach.dart';
import 'package:high/high/widgets/page.dart';
import 'package:high/licensing/unlock_store.dart';
import 'package:high/resources/gate.dart';
import 'package:shared_preferences/shared_preferences.dart';

import 'helpers.dart';

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();
  HighState.tickStudy = false;
  highDecorAnimations = false;
  highNow = () => DateTime(2026, 9, 29, 10);
  final repo = ExamRepo(useIsolate: false);
  final shotKey = GlobalKey();
  final out = Platform.environment['COACH_SHOTS'] ?? '/workspace/shots/coach';

  setUpAll(() async {
    await loadFonts();
    await repo.init();
  });

  for (final dark in [false, true]) {
    testWidgets('coach marks walk-through${dark ? ' (dark)' : ''}', (tester) async {
      tester.view.physicalSize = const Size(780, 1688);
      tester.view.devicePixelRatio = 2;
      addTearDown(tester.view.reset);
      // first install: no saved state → tour starts
      SharedPreferences.setMockInitialValues({
        HighState.key: jsonEncode({'v': 2, 'name': 'Hana', 'theme': dark ? 'dark' : 'light', 'tourStep': 0}),
        'four_device_id_v1': 'ABC234DEF567',
        'four_highschool_unlocked': true,
      });
      FlutterSecureStorage.setMockInitialValues({});
      final s = HighState(repo, await SharedPreferences.getInstance());
      await s.load();
      await tester.runAsync(() async {
        final u = UnlockStore();
        await u.init();
        ResourceGate.install(u); // shows the Extra resources card
      });
      await tester.pumpWidget(RepaintBoundary(key: shotKey, child: HighApp(state: s, initialTab: HighTab.home)));
      Future<void> settle() async {
        for (var i = 0; i < 8; i++) {
          await tester.runAsync(() => Future<void>.delayed(const Duration(milliseconds: 40)));
          await tester.pump(const Duration(milliseconds: 120));
        }
        await tester.pumpAndSettle();
      }

      Future<void> shot(String name) async {
        final ro = tester.renderObject<RenderRepaintBoundary>(find.byKey(shotKey));
        await tester.runAsync(() async {
          final img = await ro.toImage(pixelRatio: 2);
          final bd = await img.toByteData(format: ui.ImageByteFormat.png);
          File('$out/$name.png')
            ..createSync(recursive: true)
            ..writeAsBytesSync(bd!.buffer.asUint8List());
        });
      }

      await settle();
      final n = kCoachSteps.length;
      for (var i = 0; i < n; i++) {
        expect(find.text('Step ${i + 1} of $n'), findsOneWidget, reason: 'step ${i + 1}');
        expect(find.text(kCoachSteps[i].title), findsWidgets);
        await shot('coach_${i + 1}_${kCoachSteps[i].title.toLowerCase().replaceAll(RegExp('[^a-z]+'), '_')}${dark ? '_dark' : ''}');
        await tester.tap(find.text(i == n - 1 ? 'Done' : 'Next'));
        await settle();
      }
      expect(s.tourStep, isNull, reason: 'Done ends the tour');
      expect(find.textContaining('Step '), findsNothing);
      // replay from settings state
      s.replayTour();
      await settle();
      expect(find.text('Step 1 of $n'), findsOneWidget);
      await tester.tap(find.text('Skip'));
      await settle();
      expect(s.tourStep, isNull);
    });
  }
}
