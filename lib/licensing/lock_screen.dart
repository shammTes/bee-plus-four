import 'dart:async';
import 'dart:math' as math;

import 'package:flutter/foundation.dart' show TargetPlatform, defaultTargetPlatform, debugPrint, kIsWeb;
import 'package:flutter/services.dart';
import 'package:flutter/widgets.dart';
import 'package:qr_flutter/qr_flutter.dart';

import 'unlock_store.dart';

const _ink = Color(0xFF3E3129);
const _cream = Color(0xFFFFFCF7);
const _peach = Color(0xFFFFC9A3);
const _coral = Color(0xFFC24E32);

/// Must match MainActivity MethodChannel name exactly.
const _secureChannel = MethodChannel('com.warsay.high/secure');

TextStyle _ts(double size, FontWeight w, Color color) => TextStyle(
      fontFamily: 'HighNunito',
      fontSize: size,
      fontWeight: w,
      color: color,
      height: 1.25,
    );

/// Map native MethodChannel errors to human copy (never show raw codes).
String _humanChannelError(PlatformException e) {
  switch (e.code) {
    case 'permission_denied':
      return 'Camera permission is off. Open Settings, enable Camera for 4, then tap Scan unlock QR — or enter the unlock code below.';
    case 'no_camera_app':
      return 'No camera app found on this phone. Enter the unlock code from Bee Seller below.';
    case 'no_qr':
      return e.message?.trim().isNotEmpty == true
          ? e.message!.trim()
          : 'No QR found — retake photo closer / better light';
    case 'decode':
      return e.message?.trim().isNotEmpty == true
          ? e.message!.trim()
          : 'Could not read a QR from the photo. Try again in better light, or enter the unlock code below.';
    case 'camera':
    case 'busy':
      return e.message?.trim().isNotEmpty == true
          ? e.message!.trim()
          : 'Camera could not open. Wait a moment and try again, or enter the unlock code below.';
    default:
      final msg = e.message?.trim();
      if (msg != null && msg.isNotEmpty && !msg.toLowerCase().contains('generic')) {
        return '$msg Or enter the unlock code below.';
      }
      return 'Camera scan failed. Try again, or enter the unlock code below.';
  }
}

class LockScreen extends StatefulWidget {
  const LockScreen({super.key, required this.unlock, required this.onUnlocked});
  final UnlockStore unlock;
  final VoidCallback onUnlocked;

  @override
  State<LockScreen> createState() => _LockScreenState();
}

class _LockScreenState extends State<LockScreen> with SingleTickerProviderStateMixin {
  final _code = TextEditingController();
  final _focus = FocusNode();
  late final AnimationController _tilt;
  String? _id;
  String? _message;
  bool _busy = false;
  bool _awaitingPermission = false;
  bool _scanning = false;
  bool _needSettings = false;
  bool _showCodeEntryHint = false;

  bool get _isAndroid => !kIsWeb && defaultTargetPlatform == TargetPlatform.android;

  @override
  void initState() {
    super.initState();
    _tilt = AnimationController(vsync: this, duration: const Duration(seconds: 7))..repeat();
    widget.unlock.deviceId().then((id) {
      if (mounted) setState(() => _id = id);
    });
  }

  @override
  void dispose() {
    _tilt.dispose();
    _code.dispose();
    _focus.dispose();
    super.dispose();
  }

  Future<T?> _invoke<T>(String method, [dynamic args]) async {
    try {
      return await _secureChannel.invokeMethod<T>(method, args);
    } catch (e, st) {
      debugPrint('HighSecure.$method failed: $e\n$st');
      rethrow;
    }
  }

  Future<void> _nativeLog(String msg) async {
    debugPrint('HighSecure: $msg');
    if (!_isAndroid) return;
    try {
      await _secureChannel.invokeMethod<void>('log', msg);
    } catch (_) {}
  }

  Future<bool> _hasCameraPermission() async {
    if (!_isAndroid) return false;
    try {
      return await _invoke<bool>('hasCamera') == true;
    } catch (_) {
      return false;
    }
  }

  Future<bool> _shouldShowRationale() async {
    if (!_isAndroid) return false;
    try {
      return await _invoke<bool>('shouldShowCameraRationale') == true;
    } catch (_) {
      return false;
    }
  }

  Future<bool> _requestCameraPermission() async {
    if (!_isAndroid) return true;
    try {
      final ok = await _invoke<bool>('requestCamera').timeout(
        const Duration(seconds: 45),
        onTimeout: () {
          debugPrint('HighSecure.requestCamera timed out');
          return false;
        },
      );
      return ok == true;
    } catch (e) {
      debugPrint('HighSecure.requestCamera error: $e');
      return false;
    }
  }

  Future<void> _openAppSettings() async {
    if (!_isAndroid) return;
    try {
      await _invoke<void>('openAppSettings');
    } catch (e) {
      debugPrint('HighSecure.openAppSettings error: $e');
      setState(() => _message = 'Open Android Settings → Apps → 4 → Permissions → Camera.');
    }
  }

  void _fail(String why, {bool needSettings = false}) {
    debugPrint('HighSecure fail: $why settings=$needSettings');
    setState(() {
      _awaitingPermission = false;
      _scanning = false;
      _busy = false;
      _needSettings = needSettings;
      _showCodeEntryHint = true;
      _message = why;
    });
  }

  /// Primary path: live native ZXing scanner → UnlockStore.
  /// Photo fallback available via [_openPhotoScan].
  Future<void> _openScan() async {
    if (_busy || _awaitingPermission || _scanning) return;
    if (!_isAndroid) {
      _fail('QR scan needs Android. Paste or type the Bee Seller unlock code below.');
      return;
    }

    setState(() {
      _message = null;
      _needSettings = false;
      _showCodeEntryHint = false;
    });
    await _nativeLog('openScan begin (live ZXing)');

    var granted = await _hasCameraPermission();
    if (!granted) {
      setState(() {
        _awaitingPermission = true;
        _message = '4 needs the camera to photograph the Bee Seller unlock QR. Allow camera on the next prompt.';
      });
      granted = await _requestCameraPermission();
      if (!mounted) return;
      setState(() => _awaitingPermission = false);
      if (!granted) {
        final rationale = await _shouldShowRationale();
        _fail(
          rationale
              ? 'Camera permission was denied. Tap Scan unlock QR again and choose Allow, or enter the unlock code below.'
              : 'Camera permission is off. Open Settings, enable Camera for 4, then tap Scan unlock QR — or enter the unlock code below.',
          needSettings: !rationale,
        );
        return;
      }
      // Brief settle after first-install grant before starting the camera app.
      await _nativeLog('permission granted; settling 300ms');
      await Future<void>.delayed(const Duration(milliseconds: 300));
      if (!mounted) return;
    }

    setState(() {
      _scanning = true;
      _message = 'Opening scanner… Point at the Bee Seller unlock QR until it beeps/reads.';
    });

    try {
      await _nativeLog('invoking captureAndScanQr (live)');
      final code = await _invoke<String>('captureAndScanQr').timeout(
        const Duration(seconds: 180),
        onTimeout: () => '',
      );
      if (!mounted) return;
      final text = (code ?? '').trim();
      if (text.isEmpty) {
        _fail('Scan cancelled. Point the camera at the Bee Seller QR again, try Photo scan, or enter the unlock code below.');
        return;
      }
      await _nativeLog('captureAndScanQr got payload len=${text.length}');
      setState(() => _scanning = false);
      await _apply(text, fromScan: true);
    } on PlatformException catch (e) {
      await _nativeLog('captureAndScanQr PlatformException ${e.code}: ${e.message}');
      if (!mounted) return;
      final denied = e.code == 'permission_denied';
      _fail(_humanChannelError(e), needSettings: denied);
    } catch (e) {
      await _nativeLog('captureAndScanQr error: $e');
      if (!mounted) return;
      _fail('Camera scan failed. Try again, or enter the unlock code below.');
    }
  }


  /// Fallback: system camera still photo → native ML Kit / ZXing decode.
  Future<void> _openPhotoScan() async {
    if (_busy || _awaitingPermission || _scanning) return;
    if (!_isAndroid) {
      _fail('QR scan needs Android. Paste or type the Bee Seller unlock code below.');
      return;
    }
    setState(() {
      _message = null;
      _needSettings = false;
      _showCodeEntryHint = false;
    });
    await _nativeLog('openPhotoScan begin');
    var granted = await _hasCameraPermission();
    if (!granted) {
      granted = await _requestCameraPermission();
      if (!mounted) return;
      if (!granted) {
        _fail('Camera permission is off. Enable Camera for 4, or enter the unlock code below.', needSettings: true);
        return;
      }
    }
    setState(() {
      _scanning = true;
      _message = 'Opening camera… Fill the frame with the Bee Seller QR, then tap the shutter.';
    });
    try {
      final code = await _invoke<String>('capturePhotoAndScanQr').timeout(
        const Duration(seconds: 180),
        onTimeout: () => '',
      );
      if (!mounted) return;
      final text = (code ?? '').trim();
      if (text.isEmpty) {
        _fail('Photo cancelled. Try live Scan unlock QR, or enter the unlock code below.');
        return;
      }
      setState(() => _scanning = false);
      await _apply(text, fromScan: true);
    } on PlatformException catch (e) {
      if (!mounted) return;
      _fail(_humanChannelError(e), needSettings: e.code == 'permission_denied');
    } catch (e) {
      if (!mounted) return;
      _fail('Photo scan failed. Try live Scan unlock QR, or enter the unlock code below.');
    }
  }

  Future<void> _paste() async {
    final data = await Clipboard.getData(Clipboard.kTextPlain);
    final text = data?.text?.trim() ?? '';
    if (!mounted) return;
    if (text.isEmpty) {
      setState(() => _message = 'Clipboard is empty. Copy the code from Bee Seller, then paste.');
      return;
    }
    _code.text = text;
    _code.selection = TextSelection.collapsed(offset: _code.text.length);
    _focus.requestFocus();
    setState(() => _message = null);
  }

  Future<void> _apply(String raw, {bool fromScan = false}) async {
    if (_busy) return;
    setState(() {
      _busy = true;
      _message = null;
      _needSettings = false;
    });
    await _nativeLog(
      'applyPayload fromScan=$fromScan len=${raw.trim().length} preview=${raw.trim().length > 12 ? raw.trim().substring(0, 12) : "***"}',
    );
    final r = await widget.unlock.applyPayload(raw);
    if (!mounted) return;
    if (r.isOk) {
      await _nativeLog('unlock success');
      widget.onUnlocked();
      return;
    }
    await _nativeLog('unlock fail: ${r.error}');
    final err = r.error ?? 'Invalid unlock code.';
    final msg = fromScan
        ? (err.contains('Bee Seller') || err.contains('signature') || err.contains('another phone') || err.contains('already used') || err.contains('Bee Plus')
            ? 'Invalid QR content: $err Retake the Bee Seller unlock QR, or enter the unlock code.'
            : 'Invalid QR content: $err')
        : err;
    setState(() {
      _busy = false;
      _scanning = false;
      _showCodeEntryHint = true;
      _message = msg;
    });
  }

  @override
  Widget build(BuildContext context) {
    final pad = MediaQuery.paddingOf(context);
    final keyboard = MediaQuery.viewInsetsOf(context).bottom;
    return ColoredBox(
      color: const Color(0xFF1A120C),
      child: DecoratedBox(
        decoration: const BoxDecoration(
          gradient: LinearGradient(
            begin: Alignment.topLeft,
            end: Alignment.bottomRight,
            colors: [Color(0xFF2A1A12), Color(0xFF1A120C), Color(0xFF3A2218)],
          ),
        ),
        child: ListView(
          padding: EdgeInsets.fromLTRB(20, pad.top + 18, 20, pad.bottom + 28 + keyboard),
          children: [
            Text('4', textAlign: TextAlign.center, style: _ts(42, FontWeight.w900, const Color(0xFFFFFFFF))),
            const SizedBox(height: 6),
            Text('Grade 9\u201312  \u00b7  Offline  \u00b7  Notes and exams', textAlign: TextAlign.center, style: _ts(15, FontWeight.w700, const Color(0xFFFFE7D4))),
            const SizedBox(height: 22),
            AnimatedBuilder(
              animation: _tilt,
              builder: (context, child) => Transform(
                alignment: Alignment.center,
                transform: Matrix4.identity()
                  ..setEntry(3, 2, 0.0012)
                  ..rotateX(-0.16)
                  ..rotateY(0.08 * math.sin(_tilt.value * math.pi * 2)),
                child: child,
              ),
              child: DecoratedBox(
                decoration: BoxDecoration(color: const Color(0xFFF3C7A6), borderRadius: BorderRadius.circular(32)),
                child: Padding(
                  padding: const EdgeInsets.fromLTRB(18, 18, 18, 16),
                  child: Column(
                    children: [
                      Text('Your classroom, locked in', textAlign: TextAlign.center, style: _ts(18, FontWeight.w900, _ink)),
                      const SizedBox(height: 12),
                      DecoratedBox(
                        decoration: BoxDecoration(color: _cream, borderRadius: BorderRadius.circular(22)),
                        child: Padding(
                          padding: const EdgeInsets.all(12),
                          child: Column(
                            children: [
                              if (_id == null)
                                const SizedBox(width: 168, height: 168)
                              else
                                QrImageView(
                                  data: _id!,
                                  size: 168,
                                  backgroundColor: _cream,
                                  eyeStyle: const QrEyeStyle(eyeShape: QrEyeShape.square, color: _ink),
                                  dataModuleStyle: const QrDataModuleStyle(dataModuleShape: QrDataModuleShape.square, color: _ink),
                                ),
                              const SizedBox(height: 6),
                              GestureDetector(
                                onTap: _id == null ? null : () => Clipboard.setData(ClipboardData(text: _id!)),
                                child: Text(_id ?? '\u2026', textAlign: TextAlign.center, style: _ts(13, FontWeight.w800, _ink)),
                              ),
                            ],
                          ),
                        ),
                      ),
                      const SizedBox(height: 10),
                      Text('Show this QR to Bee Seller. One scan unlocks this phone.', textAlign: TextAlign.center, style: _ts(14, FontWeight.w700, _ink)),
                    ],
                  ),
                ),
              ),
            ),
            const SizedBox(height: 22),
            // Primary: live ZXing scanner
            _Btn(
              label: _awaitingPermission
                  ? 'Waiting for camera\u2026'
                  : _scanning
                      ? 'Scanner open\u2026'
                      : 'Scan unlock QR',
              filled: true,
              onTap: (_busy || _awaitingPermission || _scanning) ? null : _openScan,
            ),
            const SizedBox(height: 8),
            Text(
              'Opens a live scanner. Point at the Bee Seller unlock QR until it reads.',
              textAlign: TextAlign.center,
              style: _ts(12, FontWeight.w700, const Color(0xFFFFE7D4)),
            ),
            const SizedBox(height: 10),
            _Btn(
              label: 'Photo scan (fallback)',
              filled: false,
              onTap: (_busy || _awaitingPermission || _scanning) ? null : _openPhotoScan,
            ),
            const SizedBox(height: 18),
            if (_showCodeEntryHint) ...[
              DecoratedBox(
                decoration: BoxDecoration(color: const Color(0x55C24E32), borderRadius: BorderRadius.circular(16)),
                child: Padding(
                  padding: const EdgeInsets.fromLTRB(14, 12, 14, 12),
                  child: Text(
                    'Enter unlock code',
                    textAlign: TextAlign.center,
                    style: _ts(16, FontWeight.w900, const Color(0xFFFFFFFF)),
                  ),
                ),
              ),
              const SizedBox(height: 10),
            ],
            Text('Enter unlock code', style: _ts(16, FontWeight.w900, const Color(0xFFFFFFFF))),
            const SizedBox(height: 4),
            Text('Always available — paste or type the Bee Seller code.', style: _ts(13, FontWeight.w700, const Color(0xFFFFE7D4))),
            const SizedBox(height: 8),
            DecoratedBox(
              decoration: BoxDecoration(color: const Color(0x33FFFFFF), borderRadius: BorderRadius.circular(18)),
              child: Padding(
                padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 10),
                child: GestureDetector(
                  onTap: () => _focus.requestFocus(),
                  child: EditableText(
                    controller: _code,
                    focusNode: _focus,
                    style: _ts(15, FontWeight.w700, const Color(0xFFFFFFFF)),
                    cursorColor: _peach,
                    backgroundCursorColor: _peach,
                    maxLines: 4,
                    minLines: 2,
                    keyboardType: TextInputType.multiline,
                    textInputAction: TextInputAction.newline,
                  ),
                ),
              ),
            ),
            const SizedBox(height: 10),
            Row(
              children: [
                Expanded(child: _Btn(label: 'Paste', filled: false, onTap: _busy ? null : _paste)),
                const SizedBox(width: 10),
                Expanded(
                  child: _Btn(
                    label: 'Clear',
                    filled: false,
                    onTap: _busy
                        ? null
                        : () {
                            _code.clear();
                            _focus.requestFocus();
                          },
                  ),
                ),
              ],
            ),
            const SizedBox(height: 12),
            _Btn(label: _busy ? 'Checking\u2026' : 'Unlock 4', onTap: _busy ? null : () => _apply(_code.text)),
            if (_showCodeEntryHint || _message != null) ...[
              const SizedBox(height: 8),
              _Btn(
                label: 'Retry Scan unlock QR',
                filled: false,
                onTap: (_busy || _awaitingPermission || _scanning) ? null : _openScan,
              ),
            ],
            if (_needSettings) ...[
              const SizedBox(height: 8),
              _Btn(label: 'Open Settings', filled: true, onTap: _openAppSettings),
            ],
            if (_message != null) ...[
              const SizedBox(height: 12),
              Text(_message!, textAlign: TextAlign.center, style: _ts(14, FontWeight.w800, _peach)),
            ],
          ],
        ),
      ),
    );
  }
}

class _Btn extends StatelessWidget {
  const _Btn({required this.label, required this.onTap, this.filled = true});
  final String label;
  final VoidCallback? onTap;
  final bool filled;
  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      behavior: HitTestBehavior.opaque,
      onTap: onTap,
      child: DecoratedBox(
        decoration: BoxDecoration(color: filled ? _coral : _cream, borderRadius: BorderRadius.circular(999)),
        child: SizedBox(
          height: 54,
          width: double.infinity,
          child: Center(child: Text(label, style: _ts(16, FontWeight.w900, filled ? const Color(0xFFFFFFFF) : _ink))),
        ),
      ),
    );
  }
}
