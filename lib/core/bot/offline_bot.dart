import 'dart:math';

import '../content/content_repository.dart';
import '../models/content_models.dart';

/// Controlled offline study bot — no network, curriculum packs only.
class OfflineBot {
  OfflineBot({ContentRepository? repo})
      : _repo = repo ?? ContentRepository.instance;
  final ContentRepository _repo;
  final _rng = Random();

  /// Bound from Coach UI selectors.
  String grade = 'G10';
  String subject = 'MATH';

  String? activeSubject;
  String? activeGrade;
  PracticeQuestion? currentQuestion;
  int correct = 0, answered = 0, hintLevel = 0;

  String get progressSummary {
    if (answered == 0) {
      return 'No questions answered yet. Pick grade/subject and start a quiz.';
    }
    final pct = ((correct / answered) * 100).round();
    return 'Session: $correct / $answered correct ($pct%). '
        'Subject: ${activeSubject ?? subject}. Grade: ${activeGrade ?? grade}.';
  }

  /// Short offline unit-note briefings for current grade/subject.
  Future<BotReply> notesBrief() async {
    activeGrade = grade;
    activeSubject = subject;
    final notes = await _repo.notesFor(grade, subject);
    if (notes.isEmpty) {
      final any = (await _repo.notes()).where((n) => n.grade == grade).toList();
      if (any.isEmpty) {
        return BotReply(
          'No unit notes found for $grade. Try another grade.',
          quick: _defaultQuick(),
        );
      }
      final buf = StringBuffer('Unit notes for $grade (all subjects):\n\n');
      for (final n in any.take(8)) {
        buf.writeln('• ${n.subject} U${n.unitNumber}: ${n.title}');
        if (n.summary.isNotEmpty) {
          final s = n.summary.length > 160
              ? '${n.summary.substring(0, 160)}…'
              : n.summary;
          buf.writeln('  $s');
        }
        buf.writeln();
      }
      buf.writeln('Open Notes tab for full text + textbooks.');
      return BotReply(buf.toString(), quick: [
        QuickAction('Start quiz', BotAction.start),
        QuickAction('Progress', BotAction.progress),
      ]);
    }
    final buf = StringBuffer('Unit notes · $grade · $subject\n\n');
    for (final n in notes.take(10)) {
      buf.writeln('Unit ${n.unitNumber}: ${n.title}');
      if (n.summary.isNotEmpty) {
        final s = n.summary.length > 220
            ? '${n.summary.substring(0, 220)}…'
            : n.summary;
        buf.writeln(s);
      }
      if (n.keyTerms.isNotEmpty) {
        buf.writeln('Terms: ${n.keyTerms.take(6).join(', ')}');
      }
      buf.writeln();
    }
    buf.writeln('Tip: open Notes → Unit notes for full cards, or start a quiz.');
    return BotReply(buf.toString(), quick: [
      QuickAction('Start quiz', BotAction.start),
      QuickAction('More subjects', BotAction.newTopic),
      QuickAction('Progress', BotAction.progress),
    ]);
  }

  Future<BotReply> handle(String raw) async {
    final text = raw.trim();
    if (text.isEmpty) {
      return BotReply('Type a message, or pick a quick action.',
          quick: _defaultQuick());
    }
    final lower = text.toLowerCase();
    if (lower == 'notes' || lower.contains('show notes') || lower == 'note') {
      return notesBrief();
    }

    final intent = BotNlp.analyze(text);
    if (intent.isGreeting) {
      return BotReply(
        'Hi — offline coach for G9–G12.\n'
        'Use the chips for grade + subject, then Start quiz or Notes.',
        quick: _subjectQuick(),
      );
    }
    if (intent.action == BotAction.help) {
      return BotReply(
        'Offline only:\n'
        '• Grade + subject chips\n'
        '• Quiz mode: practice MCQs with hints\n'
        '• Notes mode: unit summaries from packs\n'
        '• Answer with A/B/C/D\n',
        quick: _defaultQuick(),
      );
    }
    if (intent.action == BotAction.progress) {
      return BotReply(progressSummary, quick: _defaultQuick());
    }
    if (intent.subject != null) {
      activeSubject = intent.subject;
      subject = intent.subject!;
      return BotReply('Subject set to $activeSubject. Say “start quiz” or “notes”.',
          quick: [
            QuickAction('Start quiz', BotAction.start),
            QuickAction('Notes', BotAction.help),
            QuickAction('Progress', BotAction.progress),
          ]);
    }
    if (intent.action == BotAction.newTopic) {
      activeSubject = null;
      currentQuestion = null;
      return BotReply('Choose a subject:', quick: _subjectQuick());
    }
    if (intent.action == BotAction.hint) return _hint();
    if (intent.action == BotAction.explain) return _explain();
    if (intent.action == BotAction.skip || intent.action == BotAction.start) {
      return _askQuestion();
    }

    final letter = RegExp(r'^[A-Da-d]$').firstMatch(text);
    if (letter != null) {
      final idx = letter.group(0)!.toUpperCase().codeUnitAt(0) - 65;
      return _gradeAnswer(idx);
    }
    final numAns = int.tryParse(text);
    if (numAns != null && numAns >= 1 && numAns <= 4) {
      return _gradeAnswer(numAns - 1);
    }

    // Fallback: treat as soft start
    if (lower.contains('quiz') || lower.contains('practice')) {
      return _askQuestion();
    }
    return BotReply(
      'I can run quizzes or show unit notes from your packs.\n'
      'Try: start quiz · notes · hint · progress',
      quick: _defaultQuick(),
    );
  }

  Future<BotReply> _askQuestion() async {
    activeGrade = grade;
    activeSubject = subject;
    hintLevel = 0;
    final pool = await _repo.questionsFor(grade, subject);
    if (pool.isEmpty) {
      final any = await _repo.questions();
      if (any.isEmpty) {
        return BotReply(
          'No practice questions loaded. Content pack may be missing.',
          quick: _defaultQuick(),
        );
      }
      currentQuestion = any[_rng.nextInt(any.length)];
    } else {
      currentQuestion = pool[_rng.nextInt(pool.length)];
    }
    final q = currentQuestion!;
    final buf = StringBuffer()
      ..writeln('${q.grade} · ${q.subject}')
      ..writeln()
      ..writeln(q.prompt)
      ..writeln()
      ..writeln('Reply A/B/C/D or tap an option.');
    return BotReply(buf.toString(), question: q, quick: [
      QuickAction('Hint', BotAction.hint),
      QuickAction('Skip', BotAction.skip),
      QuickAction('Progress', BotAction.progress),
    ]);
  }

  Future<BotReply> _gradeAnswer(int index) async {
    final q = currentQuestion;
    if (q == null) {
      return BotReply('No active question. Start a quiz first.',
          quick: _defaultQuick());
    }
    answered++;
    final ok = index == q.correctIndex;
    if (ok) correct++;
    final msg = ok
        ? 'Correct!\n\n${q.explanation}'
        : 'Not quite. Correct: ${String.fromCharCode(65 + q.correctIndex)}. '
            '${q.options[q.correctIndex]}\n\n${q.explanation}';
    currentQuestion = null;
    return BotReply(msg, quick: [
      QuickAction('Next question', BotAction.start),
      QuickAction('Notes', BotAction.help),
      QuickAction('Progress', BotAction.progress),
    ]);
  }

  Future<BotReply> _hint() async {
    final q = currentQuestion;
    if (q == null) {
      return BotReply('No active question. Start a quiz first.',
          quick: _defaultQuick());
    }
    hintLevel = (hintLevel + 1).clamp(1, 3);
    const hints = [
      'Focus on the key idea in the question stem.',
      'Eliminate options that contradict the definition or formula.',
      'Check units, signs, and definitions carefully before choosing.',
    ];
    return BotReply('Hint $hintLevel/3: ${hints[hintLevel - 1]}', quick: [
      QuickAction('Another hint', BotAction.hint),
      QuickAction('Explain', BotAction.explain),
      QuickAction('Skip', BotAction.skip),
    ]);
  }

  Future<BotReply> _explain() async {
    final q = currentQuestion;
    if (q == null) {
      return BotReply('No active question. Start a quiz first.',
          quick: _defaultQuick());
    }
    return BotReply(
      'Full explanation:\n${q.explanation}\n\n'
      'Correct: ${String.fromCharCode(65 + q.correctIndex)}. ${q.options[q.correctIndex]}',
      quick: [
        QuickAction('Next question', BotAction.start),
        QuickAction('Progress', BotAction.progress),
      ],
    );
  }

  List<QuickAction> _defaultQuick() => [
        QuickAction('Start quiz', BotAction.start),
        QuickAction('Subjects', BotAction.newTopic),
        QuickAction('Progress', BotAction.progress),
        QuickAction('Help', BotAction.help),
      ];

  List<QuickAction> _subjectQuick() => [
        QuickAction('Math', BotAction.subject, value: 'MATH'),
        QuickAction('Physics', BotAction.subject, value: 'PHYSICS'),
        QuickAction('Chemistry', BotAction.subject, value: 'CHEMISTRY'),
        QuickAction('Biology', BotAction.subject, value: 'BIOLOGY'),
        QuickAction('English', BotAction.subject, value: 'ENGLISH'),
        QuickAction('Geography', BotAction.subject, value: 'GEOGRAPHY'),
        QuickAction('History', BotAction.subject, value: 'HISTORY'),
      ];
}

enum BotAction {
  hint,
  explain,
  skip,
  progress,
  newTopic,
  help,
  start,
  subject,
  none
}

class BotIntent {
  final String? subject;
  final BotAction action;
  final bool isGreeting;
  const BotIntent(
      {this.subject, this.action = BotAction.none, this.isGreeting = false});
}

class BotNlp {
  static const subjectKeywords = {
    'MATH': ['math', 'mathematics', 'algebra', 'geometry', 'calculus'],
    'PHYSICS': ['physics', 'mechanics', 'force', 'motion', 'energy'],
    'CHEMISTRY': ['chemistry', 'chemical', 'atom', 'acid', 'base'],
    'BIOLOGY': ['biology', 'bio', 'cell', 'genetics'],
    'ENGLISH': ['english', 'grammar', 'vocabulary'],
    'GEOGRAPHY': ['geography', 'map', 'climate'],
    'HISTORY': ['history', 'historical'],
  };
  static const actionKeywords = {
    BotAction.hint: ['hint', 'clue', 'stuck'],
    BotAction.explain: ['explain', 'explanation', 'why'],
    BotAction.skip: ['skip', 'next', 'pass'],
    BotAction.progress: ['progress', 'stats', 'score'],
    BotAction.newTopic: ['new topic', 'change subject', 'subjects'],
    BotAction.help: ['help', 'guide', 'what can you'],
    BotAction.start: ['start', 'begin', 'quiz', 'practice', 'test'],
  };
  static BotIntent analyze(String text) {
    final lower = text.toLowerCase();
    final greeting = RegExp(
            r'^(hi|hello|hey|greetings|good morning|good afternoon|good evening)\b')
        .hasMatch(lower);
    String? subject;
    for (final e in subjectKeywords.entries) {
      if (e.value.any((k) => lower.contains(k))) {
        subject = e.key;
        break;
      }
    }
    var action = BotAction.none;
    for (final e in actionKeywords.entries) {
      if (e.value.any((k) => lower.contains(k))) {
        action = e.key;
        break;
      }
    }
    return BotIntent(
        subject: subject, action: action, isGreeting: greeting);
  }
}

class QuickAction {
  final String label;
  final BotAction action;
  final String? value;
  const QuickAction(this.label, this.action, {this.value});
}

class BotReply {
  final String text;
  final List<QuickAction> quick;
  final PracticeQuestion? question;
  const BotReply(this.text, {this.quick = const [], this.question});
}
