// Motivation quotes + Study Coach: content checks, interactions, and screenshots of the new screens.
//   flutter test test/motivation_coach_test.dart   → PNGs in /workspace/media4/new_features/ (or $NEW_FEATURE_SHOTS)
import 'dart:convert';
import 'dart:io';
import 'dart:ui' as ui;

import 'package:flutter/rendering.dart';
import 'package:flutter/widgets.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:high/high/app.dart';
import 'package:high/high/data/repository.dart';
import 'package:high/high/motivation/quote_art.dart';
import 'package:high/high/motivation/quotes.dart';
import 'package:high/high/screens/home.dart';
import 'package:high/high/state/app_state.dart';
import 'package:high/high/study_coach/coach_data.dart';
import 'package:high/high/study_coach/coach_pages.dart';
import 'package:high/high/study_coach/coach_tools.dart';
import 'package:high/high/study_coach/plan_data.dart';
import 'package:high/high/study_coach/plan_pages.dart';
import 'package:high/high/widgets/page.dart';
import 'package:shared_preferences/shared_preferences.dart';

import 'helpers.dart';

final _words = RegExp(r"[A-Za-z0-9'’%-]+");

/// every string a student reads in the coach file (ids, tones, icons and tool kinds left out)
List<String> coachTexts(Object? o) {
  final out = <String>[];
  void walk(Object? x) {
    if (x is String) {
      out.add(x);
    } else if (x is List) {
      x.forEach(walk);
    } else if (x is Map) {
      for (final e in x.entries) {
        if (!const {'id', 'type', 'tone', 'icon', 'tool', 'group'}.contains(e.key)) walk(e.value);
      }
    }
  }

  walk(o);
  return out;
}

void main() {
  group('content', () {
    final quotesRaw = File(QuoteBook.asset).readAsStringSync(), coachRaw = File(CoachBook.asset).readAsStringSync();
    final qb = QuoteBook.parse(quotesRaw), cb = CoachBook.parse(coachRaw);

    test('quotes load: about 60 cards, each with text, author, art and a known category', () {
      expect(qb.quotes.length, greaterThanOrEqualTo(60));
      final ids = <String>{}, cats = {for (final c in qb.cats) c.id};
      for (final q in qb.quotes) {
        expect(ids.add(q.id), isTrue, reason: 'duplicate ${q.id}');
        expect(q.text.trim(), isNotEmpty);
        expect(q.author.trim(), isNotEmpty, reason: '${q.id} has no author');
        expect(cats, contains(q.cat), reason: q.id);
        expect(kQuoteMotifs, contains(q.art), reason: '${q.id} art ${q.art}');
        expect(kQuoteTones.keys, contains(q.tone), reason: '${q.id} tone ${q.tone}');
        if (!q.original) expect(q.meaning, isNotNull, reason: '${q.id}: famous quotes carry a plain meaning');
      }
      // quote of the day changes daily and stays the same within a day
      expect(qb.ofDay(DateTime(2026, 10, 11, 8)).id, qb.ofDay(DateTime(2026, 10, 11, 22)).id);
      expect(qb.ofDay(DateTime(2026, 10, 11)).id, isNot(qb.ofDay(DateTime(2026, 10, 12)).id));
    });

    test('study coach loads: every topic has steps and at least one interactive part', () {
      expect(cb.topics.length, greaterThanOrEqualTo(20));
      final ids = <String>{};
      for (final t in cb.topics) {
        expect(ids.add(t.id), isTrue, reason: 'duplicate ${t.id}');
        expect(cb.groups, contains(t.group));
        expect(t.stepCount, greaterThan(0), reason: '${t.id} has no steps');
        expect(t.hasInteractive, isTrue, reason: '${t.id} has nothing to do');
        expect(t.blocks.where((b) => b['type'] == 'try'), isNotEmpty, reason: '${t.id} has no "Try this today"');
        for (final b in t.blocks) {
          switch (b['type']) {
            case 'quiz':
              final max = (b['questions'] as List).length * (b['scores'] as List).cast<num>().reduce((a, c) => a > c ? a : c);
              expect((b['bands'] as List).last['max'], greaterThanOrEqualTo(max), reason: '${b['id']} bands do not reach $max');
              expect((b['options'] as List).length, (b['scores'] as List).length);
            case 'mcq':
              for (final i in b['items'] as List) {
                expect(i['answer'], inInclusiveRange(0, (i['options'] as List).length - 1));
              }
            case 'tool':
              expect(kTools, contains(b['tool']));
            case 'steps' || 'check' || 'try':
              expect(b['items'] as List, isNotEmpty);
          }
        }
      }
      for (final must in [
        'exam_anxiety',
        'procrastination',
        'how_to_study',
        'remember_reading',
        'self_talk',
        'comparing',
        'self_esteem',
        'failure',
        'peer_pressure',
      ]) {
        expect(cb.byId(must), isNotNull, reason: must);
      }
      // the five exercises the brief asked for are all reachable from a lesson
      final tools = {for (final t in cb.topics) ...t.tools};
      expect(tools, containsAll(['breath478', 'pomodoro', 'twomin', 'reframe', 'spaced']));
    });

    test('plain English: short sentences in every coach text', () {
      final long = <String>[];
      for (final s in coachTexts(jsonDecode(coachRaw))) {
        for (final sen in s.split(RegExp(r'(?<=[.!?…]["”]?)\s+'))) {
          if (_words.allMatches(sen).length > 13) long.add(sen);
        }
      }
      expect(long, isEmpty, reason: 'sentences over 13 words:\n${long.join('\n')}');
    });

    final planRaw = File(PlanBook.asset).readAsStringSync(), pb = PlanBook.parse(planRaw);

    test('check-in and 30-day plan content', () {
      expect(pb.items, hasLength(14));
      expect(pb.areas, hasLength(6));
      for (final a in pb.areas) {
        expect(cb.byId(a['topic'] as String), isNotNull, reason: 'area ${a['id']} links to a missing topic');
        expect(kPlanTopics, contains(a['topic']));
        final ls = pb.lessons(a['id'] as String);
        expect(ls, hasLength(25));
        for (final l in ls) {
          for (final f in ['title', 'text', 'action', 'why', 'technique']) {
            expect((l[f] as String).trim(), isNotEmpty, reason: '${l['id']} $f');
          }
          expect((pb.raw['techniques'] as Map)[l['technique']]?['sources'], isNotEmpty, reason: '${l['id']} research kept in metadata');
          if (l['tool'] != null) expect(kTools, contains(l['tool']));
        }
      }
      final student = jsonEncode({...pb.raw}..remove('techniques'));
      for (final w in ['diagnos', 'disorder', 'depress', 'ADHD', 'symptom', 'addict', 'trauma', 'helpline', 'hotline']) {
        expect(student.toLowerCase(), isNot(contains(w.toLowerCase())), reason: 'no "$w" in what students read');
      }
      expect(RegExp(r'\d{3}[- ]?\d{3,}').hasMatch(student), isFalse, reason: 'no phone numbers');
      final long = <String>[];
      for (final t in coachTexts({...pb.raw}..remove('techniques'))) {
        for (final sen in t.split(RegExp(r'(?<=[.!?…]["”]?)\s+'))) {
          if (_words.allMatches(sen).length > 13) long.add(sen);
        }
      }
      expect(long, isEmpty, reason: long.join('\n'));
    });

    test('check-in scoring, profiles and plan days', () {
      final none = {for (final it in pb.items) it['id'] as String: 0};
      final sc0 = pb.score(none);
      // reverse items count "Never" as hard: rested, 25 minutes, sees the point
      expect(sc0['focus'], 50);
      expect(sc0['stress'], 0);
      expect(pb.profileFor({for (final a in pb.areas) a['id'] as String: 10}), 'steady_builder');
      expect(pb.profileFor({'stress': 80, 'procrastination': 60, 'focus': 10, 'sleep': 10, 'phone': 10, 'motivation': 10}), 'overwhelmed_planner');
      expect(pb.profileFor({'stress': 80, 'procrastination': 20, 'focus': 10, 'sleep': 10, 'phone': 10, 'motivation': 10}), 'overloaded_juggler');
      expect(pb.topTwo({'stress': 50, 'sleep': 50, 'focus': 50, 'procrastination': 0, 'phone': 0, 'motivation': 0}), ['stress', 'sleep']);
      final ids = <String>{for (final x in pb.raw['profiles'] as List) x['id'] as String};
      expect(ids, hasLength(10));
      // 30 days: reflect on 7/14/21/28, check-in again on 30, lessons alternate the two areas
      expect(pb.day(1, 'sleep', 'phone')['id'], 'sleep-01');
      expect(pb.day(2, 'sleep', 'phone')['id'], 'phone-01');
      expect(pb.day(7, 'sleep', 'phone')['type'], 'reflect');
      expect(pb.day(8, 'sleep', 'phone')['id'], 'sleep-04');
      expect(pb.day(30, 'sleep', 'phone')['type'], 'recheck');
      expect(pb.day(29, 'sleep', 'phone', single: true)['id'], 'sleep-25');
      final mix = {
        for (var d = 1; d <= 30; d++)
          if (pb.day(d, 'sleep', 'phone')['type'] == 'lesson') pb.day(d, 'sleep', 'phone')['id'],
      };
      expect(mix, hasLength(25));
      // one new day per calendar day; streak counts days in a row
      final run = PlanRun({
        'a': 'sleep',
        'b': 'phone',
        'done': {'1': '2026-10-09', '2': '2026-10-10'},
      });
      expect(run.next, 3);
      expect(run.unlocked(3, DateTime(2026, 10, 10, 20)), isFalse);
      expect(run.unlocked(3, DateTime(2026, 10, 11, 7)), isTrue);
      expect(run.unlocked(4, DateTime(2026, 10, 11, 7)), isFalse);
      expect(run.streak(DateTime(2026, 10, 11)), 2);
      expect(run.streak(DateTime(2026, 10, 13)), 0);
    });

    test('score bands', () {
      final q = cb.byId('exam_anxiety')!.blocks.firstWhere((b) => b['type'] == 'quiz');
      expect(bandFor(q, 0)['title'], 'Mostly calm');
      expect(bandFor(q, 24)['title'], 'Very worried');
    });
  });

  group('screens', () {
    TestWidgetsFlutterBinding.ensureInitialized();
    HighState.tickStudy = false;
    highDecorAnimations = false;
    highNow = () => DateTime(2026, 10, 11, 10);
    final repo = ExamRepo(useIsolate: false);
    final shotKey = GlobalKey();
    HighNav? nav;
    final out = Platform.environment['NEW_FEATURE_SHOTS'] ?? '/workspace/media4/new_features';

    setUpAll(() async {
      await loadFonts();
      await repo.init();
      QuoteBook.cached = QuoteBook.parse(File(QuoteBook.asset).readAsStringSync());
      CoachBook.cached = CoachBook.parse(File(CoachBook.asset).readAsStringSync());
      // big file: rootBundle would parse it on a helper isolate, which never finishes inside the test zone
      PlanBook.cached = PlanBook.parse(File(PlanBook.asset).readAsStringSync());
    });

    Future<HighState> boot(WidgetTester tester, {bool dark = false, Map<String, dynamic> extra = const {}}) async {
      tester.view.physicalSize = const Size(780, 1688);
      tester.view.devicePixelRatio = 2;
      addTearDown(tester.view.reset);
      SharedPreferences.setMockInitialValues({
        HighState.key: jsonEncode({'v': 2, 'name': 'Hana', 'theme': dark ? 'dark' : 'light', 'lang': 'en', 'tourDone': true, ...extra}),
      });
      final s = HighState(repo, await SharedPreferences.getInstance());
      await s.load();
      await tester.pumpWidget(
        RepaintBoundary(
          key: shotKey,
          child: HighApp(state: s, initialTab: HighTab.home),
        ),
      );
      await settle(tester);
      nav = null;
      return s;
    }

    Future<void> shot(WidgetTester tester, String name) async {
      final ro = tester.renderObject<RenderRepaintBoundary>(find.byKey(shotKey));
      await tester.runAsync(() async {
        final img = await ro.toImage(pixelRatio: 1.5);
        final bd = await img.toByteData(format: ui.ImageByteFormat.png);
        File('$out/$name.png')
          ..createSync(recursive: true)
          ..writeAsBytesSync(bd!.buffer.asUint8List());
      });
    }

    void push(WidgetTester tester, Widget page) => (nav ??= HighNav.of(tester.element(find.byType(HomePage)))).push(page);

    Future<void> scrollTo(WidgetTester tester, Finder f) async {
      await tester.scrollUntilVisible(f, 300, scrollable: find.byType(Scrollable).last);
      await tester.pumpAndSettle();
    }

    for (final dark in [false, true]) {
      testWidgets('home shows quote of the day and the Study Coach card${dark ? ' (dark)' : ''}', (tester) async {
        await boot(tester, dark: dark);
        final sc = tester.stateList<ScrollableState>(find.byType(Scrollable)).firstWhere((x) => x.position.axis == Axis.vertical);
        sc.position.jumpTo(520);
        await tester.pumpAndSettle();
        expect(find.text('Quote of the day'), findsOneWidget);
        expect(find.text('Study Coach'), findsOneWidget);
        await shot(tester, 'home_quote_coach${dark ? '_dark' : ''}');
      });
    }

    testWidgets('quote gallery, viewer and saving a favourite', (tester) async {
      final s = await boot(tester);
      push(tester, const QuotesPage());
      await settle(tester);
      expect(find.byType(QuoteCard), findsWidgets);
      await shot(tester, 'quotes_gallery');
      await tester.tap(find.byType(QuoteCard).first);
      await settle(tester);
      expect(find.textContaining('It means:', findRichText: true), findsOneWidget);
      await tester.tap(find.text('Save'));
      await tester.pumpAndSettle();
      expect(s.quoteFavs, hasLength(1));
      await shot(tester, 'quote_viewer');
      await tester.drag(find.byType(PageView), const Offset(-500, 0));
      await tester.pumpAndSettle();
      await shot(tester, 'quote_viewer_next');
    });

    testWidgets('every card, one sheet (artwork review)', (tester) async {
      tester.view.physicalSize = const Size(2400, 3300);
      tester.view.devicePixelRatio = 1;
      addTearDown(tester.view.reset);
      final qs = QuoteBook.cached!.quotes;
      await tester.pumpWidget(
        RepaintBoundary(
          key: shotKey,
          child: Directionality(
            textDirection: TextDirection.ltr,
            child: ColoredBox(
              color: const Color(0xFFF7F0E5),
              child: Padding(
                padding: const EdgeInsets.all(12),
                child: Wrap(
                  spacing: 10,
                  runSpacing: 10,
                  children: [
                    for (final q in qs)
                      SizedBox(
                        width: 284,
                        height: 284 / .74,
                        child: QuoteCard(q: q, compact: true),
                      ),
                  ],
                ),
              ),
            ),
          ),
        ),
      );
      await tester.pump();
      await shot(tester, 'quotes_all_cards');
    });

    testWidgets('quote gallery dark, saved filter', (tester) async {
      await boot(
        tester,
        dark: true,
        extra: {
          'quoteFavs': ['q05', 'q20', 'q38'],
        },
      );
      push(tester, const QuotesPage());
      await settle(tester);
      await shot(tester, 'quotes_gallery_dark');
      await tester.tap(find.text('Saved'));
      await tester.pumpAndSettle();
      expect(find.byType(QuoteCard), findsNWidgets(3));
    });

    testWidgets('study coach home and a lesson with a self-check', (tester) async {
      final s = await boot(tester);
      push(tester, const CoachHomePage());
      await settle(tester);
      expect(find.text('Quick tools'), findsOneWidget);
      await shot(tester, 'coach_home');
      expect(find.textContaining('very sad'), findsNothing);
      expect(find.textContaining('unsafe'), findsNothing);

      push(tester, const CoachTopicPage(id: 'exam_anxiety'));
      await settle(tester);
      await shot(tester, 'coach_topic_exam_anxiety');
      // answer the 8 questions: "Sometimes" each → 8 points → "Some nerves"
      for (var i = 0; i < 8; i++) {
        final f = find.text('Sometimes').at(i);
        await tester.ensureVisible(f);
        await tester.pumpAndSettle();
        await tester.tap(f);
        await tester.pump();
      }
      final see = find.text('See my result');
      await tester.ensureVisible(see);
      await tester.pumpAndSettle();
      await tester.tap(see);
      await tester.pumpAndSettle();
      expect(find.text('Some nerves'), findsOneWidget);
      expect(((s.coach['quiz'] as Map)['anx_quiz'] as Map)['s'], 8);
      await tester.ensureVisible(find.text('Some nerves'));
      await tester.pumpAndSettle();
      await shot(tester, 'coach_quiz_result');
      await scrollTo(tester, find.text('Try this today'));
      await tester.tap(find.text('Do calm breathing now, and again before bed.'));
      await tester.pumpAndSettle();
      await shot(tester, 'coach_try_today');
      expect(s.coach['seen'], contains('exam_anxiety'));
      await tester.pump(const Duration(seconds: 1)); // debounced save
    });

    testWidgets('check-in → profile → 30-day plan → day 30 check-in again', (tester) async {
      final s = await boot(tester);
      push(tester, const CoachHomePage());
      await settle(tester);
      expect(find.text('Study check-in'), findsOneWidget);
      await tester.tap(find.text('Start (3 minutes)'));
      await settle(tester);
      await shot(tester, 'plan_checkin_question');
      for (var i = 0; i < 14; i++) {
        await tester.tap(find.text(i < 7 ? 'Often' : 'Rarely'));
        await tester.pump();
      }
      await settle(tester); // the 14th answer opens the profile directly (no mood / crisis question)
      expect(find.text('One last private question'), findsNothing);
      expect(find.text('Talking to someone helps'), findsNothing);
      await shot(tester, 'plan_profile');
      await scrollTo(tester, find.textContaining('Start: '));
      await shot(tester, 'plan_profile_start');
      await tester.tap(find.textContaining('Start: '));
      await settle(tester);
      expect(find.text('30-day plan'), findsOneWidget);
      await shot(tester, 'plan_day1');
      await scrollTo(tester, find.text('I did it'));
      await tester.tap(find.text('I did it'));
      await tester.pumpAndSettle();
      expect(planOf(s)!.isDone(1), isTrue);
      final sc = tester.stateList<ScrollableState>(find.byType(Scrollable)).firstWhere((x) => x.position.axis == Axis.vertical);
      sc.position.jumpTo(0);
      await tester.pumpAndSettle();
      expect(find.textContaining('opens tomorrow'), findsWidgets);
      await shot(tester, 'plan_done_today');

      // next morning: Day 2 is open, streak goes on
      highNow = () => DateTime(2026, 10, 12, 8);
      addTearDown(() => highNow = () => DateTime(2026, 10, 11, 10));
      HighNav.of(tester.element(find.byType(PlanPage))).back();
      await settle(tester);
      openPlan(tester.element(find.byType(CoachHomePage)));
      await settle(tester);
      expect(find.text('Day 2 of 30'), findsOneWidget);

      // jump to a finished week and to Day 30
      final run = planOf(s)!;
      run.m['done'] = {for (var d = 1; d <= 6; d++) '$d': '2026-10-${(d + 5).toString().padLeft(2, '0')}'};
      highNow = () => DateTime(2026, 10, 12, 18);
      s.coachSet('plan', run.m);
      await settle(tester);
      expect(find.text('Week 1: look back'), findsOneWidget);
      await shot(tester, 'plan_week_lookback');
      run.m['done'] = {for (var d = 1; d <= 29; d++) '$d': dayOf(DateTime(2026, 9, 12).add(Duration(days: d)))};
      s.coachSet('plan', run.m);
      await settle(tester);
      await tester.tap(find.text('Take the check-in again'));
      await settle(tester);
      for (var i = 0; i < 14; i++) {
        await tester.tap(find.text(i < 7 ? 'Sometimes' : 'Rarely'));
        await tester.pump();
      }
      await settle(tester);
      expect(find.text('Day 30: your change'), findsOneWidget);
      await shot(tester, 'plan_day30_change');
      expect(planOf(s)!.isDone(30), isTrue);
      await tester.pump(const Duration(seconds: 1));
    });

    testWidgets('lesson with a knowledge check and checklist', (tester) async {
      await boot(tester, dark: true);
      push(tester, const CoachTopicPage(id: 'how_to_study'));
      await settle(tester);
      await scrollTo(tester, find.text('Quick check: which works best?'));
      await tester.tap(find.text('Read once, then test yourself with the book closed'));
      await tester.pumpAndSettle();
      expect(find.textContaining('Right!'), findsOneWidget);
      await shot(tester, 'coach_mcq_dark');
    });

    testWidgets('exercises: breathing, study timer, 2-minute start, change the thought, review planner, goal', (tester) async {
      final s = await boot(
        tester,
        extra: {
          'coach': {
            'spaced': [
              {'t': 'Biology unit 2: the cell', 'd': DateTime(2026, 10, 10).millisecondsSinceEpoch, 'n': 0},
              {'t': 'Physics: Newton\'s laws', 'd': DateTime(2026, 10, 4).millisecondsSinceEpoch, 'n': 2},
            ],
            'reframe': [
              {
                't': 0,
                'a': ['I am stupid at maths', 'I got 7 of 10 last week', 'You can learn this', 'Maths is hard for me, and I am getting better'],
              },
            ],
          },
        },
      );
      push(tester, const BreathPage());
      await settle(tester);
      await tester.tap(find.text('Start'));
      await tester.pump(const Duration(milliseconds: 2500));
      expect(find.text('Breathe in\nRound 1 of 4'), findsOneWidget);
      await shot(tester, 'tool_breathing');
      await tester.pump(const Duration(seconds: 3));
      expect(find.text('Hold\nRound 1 of 4'), findsOneWidget);
      await tester.tap(find.text('Stop'));
      await tester.pump();

      push(tester, const TimerPage());
      await settle(tester);
      await tester.tap(find.text('Start'));
      await tester.pump(const Duration(seconds: 61));
      expect(find.text('23:59'), findsOneWidget);
      await shot(tester, 'tool_study_timer');
      await tester.tap(find.text('Pause'));
      await tester.pump();

      push(tester, const TimerPage(twoMin: true));
      await settle(tester);
      await tester.tap(find.text('Start'));
      await tester.pump(const Duration(seconds: 121));
      expect(find.text('You started! Keep going?'), findsOneWidget);
      await shot(tester, 'tool_two_minute');

      push(tester, const ReframePage());
      await settle(tester);
      await shot(tester, 'tool_change_thought');

      push(tester, const ReviewPlannerPage());
      await settle(tester);
      expect(find.text('Review today · 0 of 5 done'), findsOneWidget); // studied yesterday → review 1 day later
      await shot(tester, 'tool_review_planner');
      await tester.tap(find.text('Done').first);
      await tester.pumpAndSettle();
      expect(((s.coach['spaced'] as List).firstWhere((x) => x['t'] == 'Biology unit 2: the cell') as Map)['n'], 1);

      push(tester, const GoalPage());
      await settle(tester);
      await shot(tester, 'tool_goal');
    });
  });
}

Future<void> settle(WidgetTester tester) async {
  for (var i = 0; i < 6; i++) {
    await tester.runAsync(() => Future<void>.delayed(const Duration(milliseconds: 40)));
    await tester.pump(const Duration(milliseconds: 120));
  }
  await tester.pumpAndSettle();
}
