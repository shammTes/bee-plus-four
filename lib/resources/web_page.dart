// Offline interactive pages (.4web). The page runs in FourWebActivity.kt (the only WebView in 4, created only
// when such a page is opened). Dart unwraps the content key through the unlock gate and hands it to native
// memory; the zip is decrypted into RAM there and served from memory with no network access.
import 'package:flutter/services.dart';
import 'package:flutter/widgets.dart';
import 'package:four_format/four_format.dart';

import '../high/screens/toast.dart';
import 'library.dart';

const _ch = MethodChannel('com.warsay.high/resources');

Future<void> openWebResource(BuildContext context, ResEntry e) async {
  try {
    final src = await FileSource.open(e.path);
    final r = await FourReader.open(src, ResourceLibrary.instance.gate.masterKey);
    try {
      final key = await r.contentKey();
      try {
        await _ch.invokeMethod('openWeb', {'path': e.path, 'key': key, 'entry': r.meta.entry, 'title': r.meta.title, 'credit': r.meta.creditLine});
      } finally {
        key.fillRange(0, key.length, 0);
      }
    } finally {
      await r.close();
    }
  } catch (err) {
    if (context.mounted) toast(context, err is FourKeyException ? 'This phone cannot open this file. Unlock 4 first.' : 'Could not open this page. Copy the file again and tap Refresh.');
  }
}
