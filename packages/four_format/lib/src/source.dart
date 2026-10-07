import 'dart:io';
import 'dart:typed_data';

/// Random-access bytes (a file, or memory in tests).
abstract class FourSource {
  int get length;
  Future<Uint8List> read(int offset, int len);
  Future<void> close() async {}
}

class BytesSource extends FourSource {
  BytesSource(this.bytes);
  final Uint8List bytes;
  @override
  int get length => bytes.length;
  @override
  Future<Uint8List> read(int offset, int len) async {
    if (offset < 0 || offset + len > bytes.length) throw RangeError('read past end');
    return Uint8List.sublistView(bytes, offset, offset + len);
  }
}

/// File source. Reads are serialised (RandomAccessFile allows one pending op).
class FileSource extends FourSource {
  FileSource._(this._raf, this.length);
  final RandomAccessFile _raf;
  @override
  final int length;
  Future<void> _q = Future.value();

  static Future<FileSource> open(String path) async {
    final raf = await File(path).open();
    return FileSource._(raf, await raf.length());
  }

  @override
  Future<Uint8List> read(int offset, int len) {
    if (offset < 0 || offset + len > length) return Future.error(RangeError('read past end'));
    final done = _q.then((_) async {
      await _raf.setPosition(offset);
      final b = await _raf.read(len);
      if (b.length != len) throw const FileSystemException('short read');
      return b;
    });
    _q = done.then((_) {}, onError: (_) {});
    return done;
  }

  @override
  Future<void> close() => _q.then((_) => _raf.close());
}
