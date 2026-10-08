// Dart side of FourVideo.kt: an ExoPlayer on a Flutter texture, fed by a native AES-GCM DataSource.
import 'package:flutter/services.dart';

class VideoState {
  const VideoState(this.m);
  final Map<Object?, Object?> m;
  int get pos => (m['pos'] as num?)?.toInt() ?? 0;
  int get dur => (m['dur'] as num?)?.toInt() ?? 0;
  int get buffered => (m['buf'] as num?)?.toInt() ?? 0;
  bool get playing => m['playing'] == true;
  bool get buffering => m['buffering'] == true;
  bool get ended => m['ended'] == true;
  int get w => (m['w'] as num?)?.toInt() ?? 0;
  int get h => (m['h'] as num?)?.toInt() ?? 0;
  String? get error => m['error'] as String?;
}

class NativeVideo {
  NativeVideo._(this.id);
  final int id;
  static const _ch = MethodChannel('com.warsay.high/video');

  /// [key] is the content key; it is handed to native memory and zeroed here.
  static Future<NativeVideo> open(String path, Uint8List key) async {
    try {
      final r = await _ch.invokeMapMethod<String, Object?>('create', {'path': path, 'key': key});
      return NativeVideo._((r!['id'] as num).toInt());
    } finally {
      key.fillRange(0, key.length, 0);
    }
  }

  Future<void> play() => _ch.invokeMethod('play', {'id': id});
  Future<void> loop(bool on) => _ch.invokeMethod('loop', {'id': id, 'on': on});
  Future<void> pause() => _ch.invokeMethod('pause', {'id': id});
  Future<void> seek(int ms) => _ch.invokeMethod('seek', {'id': id, 'ms': ms});
  Future<void> speed(double rate) => _ch.invokeMethod('speed', {'id': id, 'rate': rate});
  Future<VideoState?> state() async {
    final m = await _ch.invokeMethod<Map<Object?, Object?>>('state', {'id': id});
    return m == null ? null : VideoState(m);
  }

  Future<void> dispose() => _ch.invokeMethod('dispose', {'id': id});
}

String fmtMs(int ms) {
  final s = ms ~/ 1000, h = s ~/ 3600, m = (s ~/ 60) % 60, ss = (s % 60).toString().padLeft(2, '0');
  return h > 0 ? '$h:${m.toString().padLeft(2, '0')}:$ss' : '$m:$ss';
}
