// Exercise tab extension point.
//
// The Exercise tab browses Grade -> Subject -> Unit (from the notes index) and asks the registered
// [HighExerciseSource] for that unit's exercises. The default [EmptyExerciseSource] returns nothing, so the tab shows
// a friendly "Exercises coming soon". A host app plugs its own bank in once at start-up:
//
//   HighExercises.register(MyExerciseSource());   // before/after High.init()
//
// See README.md, "Plugging in exercises".
import 'package:flutter/widgets.dart';

/// one exercise item. [options] null => written answer (shown with [answer] on reveal); otherwise MCQ letter -> text.
class HighExercise {
  const HighExercise({required this.id, required this.prompt, this.options, required this.answer, this.explanation, this.extra = const {}});
  final String id;

  /// plain text; `$…$` inline LaTeX is rendered
  final String prompt;
  final Map<String, String>? options;

  /// MCQ: the correct option key ("A"); written: the model answer
  final String answer;
  final String? explanation;
  final Map<String, Object?> extra;

  factory HighExercise.fromJson(Map<String, dynamic> j) => HighExercise(
    id: '${j['id']}',
    prompt: '${j['prompt'] ?? j['stem'] ?? ''}',
    options: (j['options'] as Map?)?.map((k, v) => MapEntry('$k', '$v')),
    answer: '${j['answer'] ?? ''}',
    explanation: j['explanation'] as String?,
    extra: Map<String, Object?>.from((j['extra'] as Map?) ?? const {}),
  );
}

/// where the Exercise tab gets its items from. [subject] is the notes subject key (e.g. `biology`), [unitId] the notes
/// unit id from `assets/high/notes/notes/index.json`.
abstract class HighExerciseSource {
  const HighExerciseSource();
  Future<List<HighExercise>> exercisesFor({required int grade, required String subject, required String unitId});

  /// optional: return a fully custom widget for the unit instead of the built-in list
  Widget? buildUnit(BuildContext context, {required int grade, required String subject, required String unitId}) => null;

  /// optional: quick count for the unit list badges (null = unknown, not shown)
  int? countFor({required int grade, required String subject, required String unitId}) => null;
}

class EmptyExerciseSource extends HighExerciseSource {
  const EmptyExerciseSource();
  @override
  Future<List<HighExercise>> exercisesFor({required int grade, required String subject, required String unitId}) async => const [];
}

/// registry used by the Exercise tab
abstract final class HighExercises {
  static HighExerciseSource source = const EmptyExerciseSource();
  static void register(HighExerciseSource s) => source = s;
}
