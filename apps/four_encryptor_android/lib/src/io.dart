// Bridge to MainActivity.kt: SAF pickers, positional reads, writes into the chosen folder, probe, share.
import 'dart:typed_data';

import 'package:flutter/services.dart';
import 'package:four_format/four_format.dart';

const _ch = MethodChannel('four.encryptor/io');

class Picked {
  Picked(this.uri, this.name, this.size, this.mime);
  final String uri, name, mime;
  final int size;
}

class Io {
  static Future<List<Picked>> pickFiles() async {
    final r = await _ch.invokeListMethod<Map<Object?, Object?>>('pickFiles') ?? const [];
    return [for (final m in r) Picked(m['uri'] as String, m['name'] as String, (m['size'] as num).toInt(), m['mime'] as String? ?? '')];
  }

  static Future<String?> pickFolder() => _ch.invokeMethod<String>('pickFolder');
  static Future<String?> pickBundleFolder() => _ch.invokeMethod<String>('pickBundleFolder');
  static Future<bool> hasFolder(String uri) async => await _ch.invokeMethod<bool>('hasFolder', {'uri': uri}) ?? false;
  static Future<String> folderName(String uri) async => await _ch.invokeMethod<String>('folderName', {'uri': uri}) ?? 'folder';
  static Future<Map<Object?, Object?>> probe(String uri, String mime) async => await _ch.invokeMapMethod<Object?, Object?>('probe', {'uri': uri, 'mime': mime}) ?? const {};
  static Future<List<String>> zipEntries(String uri) async => (await _ch.invokeListMethod<String>('zipEntries', {'uri': uri})) ?? const [];
  static Future<Map<Object?, Object?>> zipFolder(String uri) async => (await _ch.invokeMapMethod<Object?, Object?>('zipFolder', {'uri': uri}))!;
  static Future<Map<Object?, Object?>> zipFiles(String dir) async => (await _ch.invokeMapMethod<Object?, Object?>('zipFiles', {'dir': dir}))!;
  static Future<String> tempDir() async => (await _ch.invokeMethod<String>('tempDir'))!;
  static Future<void> deleteTemp(String path) => _ch.invokeMethod('deleteTemp', {'path': path});
  static Future<void> share(List<String> uris) => _ch.invokeMethod('share', {'uris': uris});
}

/// Random-access input over a content URI (or a temp file path). Reads one chunk per call.
class SafSource extends FourSource {
  SafSource._(this._h, this.length);
  final int _h;
  @override
  final int length;

  static Future<SafSource> open(String uri) async {
    final m = (await _ch.invokeMapMethod<String, Object?>('openIn', {'uri': uri}))!;
    return SafSource._(m['h'] as int, (m['size'] as num).toInt());
  }

  @override
  Future<Uint8List> read(int offset, int len) async {
    if (len == 0) return Uint8List(0);
    return (await _ch.invokeMethod<Uint8List>('read', {'h': _h, 'off': offset, 'len': len}))!;
  }

  @override
  Future<void> close() => _ch.invokeMethod('closeIn', {'h': _h});
}

/// Output document in the picked folder. Small pieces (tags, magic) are batched into ~512 KB writes.
class SafSink {
  SafSink._(this._h, this.uri, this.name);
  final int _h;
  final String uri, name;
  final _buf = BytesBuilder(copy: true);

  static Future<SafSink> create(String tree, String name) async {
    final m = (await _ch.invokeMapMethod<String, Object?>('createOut', {'tree': tree, 'name': name}))!;
    return SafSink._(m['h'] as int, m['uri'] as String, m['name'] as String? ?? name);
  }

  Future<void> add(List<int> b) async {
    _buf.add(b);
    if (_buf.length >= 512 * 1024) await _flush();
  }

  Future<void> _flush() async {
    if (_buf.isEmpty) return;
    await _ch.invokeMethod('write', {'h': _h, 'b': _buf.takeBytes()});
  }

  /// [ok] false deletes the partial file.
  Future<void> close({required bool ok}) async {
    try {
      if (ok) await _flush();
    } finally {
      await _ch.invokeMethod('closeOut', {'h': _h, 'ok': ok});
    }
  }
}
