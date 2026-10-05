// Background loading must really run in an isolate (a closure that drags the repo into the isolate message throws, and
// the app then silently decodes everything on the UI thread).
import 'package:flutter_test/flutter_test.dart';
import 'package:high/high/data/repository.dart';
import 'package:high/high/notes/jr/data/repository.dart';

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();

  test('exam packs load with useIsolate: true', () async {
    final r = ExamRepo(useIsolate: true);
    await r.init();
    expect(r.exams, isNotEmpty);
  });

  test('a notes book parses in a background isolate', () async {
    final r = NotesRepo(useIsolate: true);
    await r.init();
    expect(r.books, isNotEmpty);
    final b = await r.book(r.books.first.id);
    expect(b.units, isNotEmpty);
    // same content as the synchronous path
    final s = NotesRepo(useIsolate: false);
    await s.init();
    final b2 = await s.book(r.books.first.id);
    expect(b.units.length, b2.units.length);
    expect(b.units.first.lessons.length, b2.units.first.lessons.length);
  });
}
