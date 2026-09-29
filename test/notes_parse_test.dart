// every High notes book parses with the ported Junior models
import 'package:flutter_test/flutter_test.dart';
import 'package:high/high/notes/jr/data/repository.dart';

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();
  test('all notes books parse', () async {
    final r = NotesRepo(useIsolate: false);
    await r.init();
    expect(r.books.length, 29);
    final bad = <String>[];
    for (final b in r.books) {
      try {
        await r.book(b.id);
      } catch (e) {
        bad.add('$e');
      }
    }
    expect(bad, isEmpty);
  });
}
