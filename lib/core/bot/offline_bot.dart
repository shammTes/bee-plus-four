import 'dart:math';
import '../content/content_repository.dart';
import '../models/content_models.dart';

/// Controlled offline study bot — no network, no free-form LLM.
/// Intent keywords + curriculum pack answers only (Adaptive Exam Prep style).
class OfflineBot {
  OfflineBot({ContentRepository? repo}) : _repo = repo ?? ContentRepository.instance;
  final ContentRepository _repo;
  final _rng = Random();
  String? activeSubject;
  String? activeGrade;
  PracticeQuestion? currentQuestion;
  int correct = 0, answered = 0, hintLevel = 0;

  String get progressSummary {
    if (answered == 0) return 'No questions answered yet. Say “start quiz” to begin.';
    final pct = ((correct / answered) * 100).round();
    return 'Session: $correct / $answered correct ($pct%). Subject: ${activeSubject ?? "not set"}. Grade: ${activeGrade ?? "G10"}.';
  }

  Future<BotReply> handle(String raw) async {
    final text = raw.trim();
    if (text.isEmpty) return BotReply('Type a message, or pick a quick action.', quick: _defaultQuick());
    final intent = BotNlp.analyze(text);
    if (intent.isGreeting) {
      return BotReply(
        'Hi — offline study coach for highschool (G9–G12).\n'
        'I only answer from curriculum packs.\nChoose a subject or say “start quiz”.',
        quick: _subjectQuick(),
      );
    }
    if (intent.action == BotAction.help) {
      return BotReply(
        'Offline only:\n• Start a quiz\n• Hint / explain / skip\n• Session progress\n'
        'I will not invent topics outside your JSON content.',
        quick: _defaultQuick(),
      );
    }
    if (intent.action == BotAction.progress) return BotReply(progressSummary, quick: _defaultQuick());
    if (intent.subject != null) {
      activeSubject = intent.subject;
      return BotReply('Subject set to $activeSubject. Say “start quiz”.', quick: [
        QuickAction('Start quiz', BotAction.start),
        QuickAction('Change subject', BotAction.newTopic),
        QuickAction('Progress', BotAction.progress),
      ]);
    }
    if (intent.action == BotAction.newTopic) {
      activeSubject = null; currentQuestion = null;
      return BotReply('Choose a subject:', quick: _subjectQuick());
    }
    if (intent.action == BotAction.hint) return _hint();
    if (intent.action == BotAction.explain) return _explain();
    if (intent.action == BotAction.skip || intent.action == BotAction.start) return _askQuestion();
    final letter = RegExp(r'^[A-Da-d]$').firstMatch(text);
    if (letter != null && currentQuestion != null) {
      return _gradeAnswer(letter.group(0)!.toUpperCase().codeUnitAt(0) - 65);
    }
    final num = int.tryParse(text);
    if (num != null && currentQuestion != null && num >= 1 && num <= currentQuestion!.options.length) {
      return _gradeAnswer(num - 1);
    }
    return BotReply(
      'I only respond to study intents (subject, start quiz, hint, explain, skip, progress).\nTry: “physics”, “start quiz”, or “help”.',
      quick: _defaultQuick(),
    );
  }

  Future<BotReply> answerIndex(int index) => _gradeAnswer(index);

  Future<BotReply> _askQuestion() async {
    final grade = activeGrade ?? 'G10';
    final subject = activeSubject ?? 'MATH';
    var list = await _repo.questionsFor(grade, subject);
    if (list.isEmpty) {
      final all = await _repo.questions();
      list = all.where((q) => ['G9','G10','G11','G12'].contains(q.grade)).toList();
    }
    if (list.isEmpty) {
      return BotReply('No highschool practice questions in packs yet. Upload JSON and rebuild.', quick: _subjectQuick());
    }
    currentQuestion = list[_rng.nextInt(list.length)];
    hintLevel = 0;
    final q = currentQuestion!;
    final buf = StringBuffer()..writeln('**${q.subject} · ${q.grade}**')..writeln(q.prompt)..writeln();
    for (var i = 0; i < q.options.length; i++) {
      buf.writeln('${String.fromCharCode(65 + i)}. ${q.options[i]}');
    }
    buf.writeln('\nReply with A–D, or ask for a hint.');
    return BotReply(buf.toString(), question: q, quick: [
      QuickAction('Hint', BotAction.hint),
      QuickAction('Skip', BotAction.skip),
      QuickAction('Progress', BotAction.progress),
    ]);
  }

  Future<BotReply> _gradeAnswer(int index) async {
    final q = currentQuestion;
    if (q == null) return BotReply('No active question. Say “start quiz”.', quick: _defaultQuick());
    answered++;
    final ok = index == q.correctIndex;
    if (ok) correct++;
    final msg = ok
        ? 'Correct!\n\n${q.explanation}'
        : 'Not quite. Correct: ${String.fromCharCode(65 + q.correctIndex)}. ${q.options[q.correctIndex]}\n\n${q.explanation}';
    currentQuestion = null;
    return BotReply(msg, quick: [
      QuickAction('Next question', BotAction.start),
      QuickAction('Change subject', BotAction.newTopic),
      QuickAction('Progress', BotAction.progress),
    ]);
  }

  Future<BotReply> _hint() async {
    final q = currentQuestion;
    if (q == null) return BotReply('No active question. Start a quiz first.', quick: _defaultQuick());
    hintLevel = (hintLevel + 1).clamp(1, 3);
    const hints = [
      'Focus on the key idea in the question stem.',
      'Eliminate options that contradict the definition or formula.',
      'The pack explanation names the exact rule after you answer.',
    ];
    return BotReply('Hint $hintLevel/3: ${hints[hintLevel - 1]}', quick: [
      QuickAction('Another hint', BotAction.hint),
      QuickAction('Explain', BotAction.explain),
      QuickAction('Skip', BotAction.skip),
    ]);
  }

  Future<BotReply> _explain() async {
    final q = currentQuestion;
    if (q == null) return BotReply('No active question. Start a quiz first.', quick: _defaultQuick());
    return BotReply(
      'Full explanation (from pack):\n${q.explanation}\n\nCorrect: ${String.fromCharCode(65 + q.correctIndex)}. ${q.options[q.correctIndex]}',
      quick: [QuickAction('Next question', BotAction.start), QuickAction('Progress', BotAction.progress)],
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
  ];
}

enum BotAction { hint, explain, skip, progress, newTopic, help, start, subject, none }

class BotIntent {
  final String? subject;
  final BotAction action;
  final bool isGreeting;
  const BotIntent({this.subject, this.action = BotAction.none, this.isGreeting = false});
}

class BotNlp {
  static const subjectKeywords = {
    'MATH': ['math', 'mathematics', 'algebra', 'geometry', 'calculus', 'equation'],
    'PHYSICS': ['physics', 'mechanics', 'electricity', 'force', 'motion', 'energy', 'optics'],
    'CHEMISTRY': ['chemistry', 'chemical', 'atom', 'molecule', 'acid', 'base', 'element'],
    'BIOLOGY': ['biology', 'bio', 'cell', 'genetics', 'dna', 'organism'],
    'ENGLISH': ['english', 'grammar', 'vocabulary', 'literature', 'writing'],
  };
  static const actionKeywords = {
    BotAction.hint: ['hint', 'clue', 'help me', 'stuck', 'give hint'],
    BotAction.explain: ['explain', 'explanation', 'why', 'clarify'],
    BotAction.skip: ['skip', 'next', 'pass', 'another question'],
    BotAction.progress: ['progress', 'stats', 'score', 'how am i doing'],
    BotAction.newTopic: ['new topic', 'change subject', 'switch', 'subjects'],
    BotAction.help: ['help', 'how to', 'guide', 'what can you do'],
    BotAction.start: ['start', 'begin', 'quiz', 'question', 'study', 'practice', 'test'],
  };
  static BotIntent analyze(String text) {
    final lower = text.toLowerCase();
    final greeting = RegExp(r'^(hi|hello|hey|greetings|good morning|good afternoon|good evening)\b').hasMatch(lower);
    String? subject;
    for (final e in subjectKeywords.entries) {
      if (e.value.any((k) => lower.contains(k))) { subject = e.key; break; }
    }
    var action = BotAction.none;
    for (final e in actionKeywords.entries) {
      if (e.value.any((k) => lower.contains(k))) { action = e.key; break; }
    }
    return BotIntent(subject: subject, action: action, isGreeting: greeting);
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
