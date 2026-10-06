// Background JSON work that really runs in the background.
//
// Isolate.run sends its closure, including every variable the closure's context chain holds. A closure written inside
// a repo method shares a context with the method's other closures, so it drags `this` (the repo, its asset bundle and
// pending Futures) into the isolate message: that either throws ("object is unsendable") or copies the whole repo.
// Before this helper the exam/notes loaders hit exactly that, so the app silently fell back to decoding everything on
// the UI thread. Closures created here capture only [f] and [arg]; pass a top-level or static function as [f].
import 'dart:convert';
import 'dart:isolate';

Future<R> offThread<A, R>(R Function(A) f, A arg) => Isolate.run(() => f(arg));

/// jsonDecode; a top-level function so it can be handed to [offThread]
Object? decodeJson(String s) => jsonDecode(s);

/// decode many files; empty or broken ones become null
List<Object?> decodeJsonListLenient(List<String> raws) => [
  for (final s in raws)
    if (s.isEmpty) null else _tryDecode(s),
];

Object? _tryDecode(String s) {
  try {
    return jsonDecode(s);
  } catch (_) {
    return null;
  }
}

/// decode many files; throws on a broken one (same as decoding them one by one)
List<Object?> decodeJsonList(List<String> raws) => [for (final s in raws) jsonDecode(s)];
