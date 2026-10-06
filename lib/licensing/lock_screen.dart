import 'dart:async';
import 'dart:math' as math;

import 'package:flutter/foundation.dart' show TargetPlatform, defaultTargetPlatform, debugPrint, kIsWeb;
import 'package:flutter/services.dart';
import 'package:flutter/widgets.dart';
import 'package:qr_flutter/qr_flutter.dart';

import 'qr_payload.dart';
import 'unlock_store.dart';

const _ink = Color(0xFF3E3129);
const _cream = Color(0xFFFFFCF7);
const _peach = Color(0xFFFFC9A3);
const _coral = Color(0xFFC24E32);

/// Must match MainActivity MethodChannel name exactly.
const _secureChannel = MethodChannel('com.warsay.high/secure');

TextStyle _ts(double size, FontWeight w, Color color) =>
    TextStyle(fontFamily: 'HighNunito', fontSize: size, fontWeight: w, color: color, height: 1.25);

/// Human copy for a native scan error code (never show raw codes).
String _humanScanError(String? code, String? message) {
  switch (code) {
    case 'permission_denied':
      return 'Camera permission is off. Open Settings, enable Camera for 4, then tap Scan unlock code — or type the code below.';
    case 'no_camera_app':
      return 'No camera app found on this phone. Use Scan unlock code, or type the code below.';
    case 'no_camera':
      return 'This phone reports no camera. Type the Bee Seller code below.';
    case 'busy':
      return 'The camera is already opening. Wait a moment and try again.';
    case 'decode':
    case 'camera':
    default:
      final m = message?.trim();
      final lead = m != null && m.isNotEmpty ? '$m ' : 'The camera could not start. ';
      return '${lead}Try again, or type the code below.';
  }
}

class LockScreen extends StatefulWidget {
  const LockScreen({super.key, required this.unlock, required this.onUnlocked});
  final UnlockStore unlock;
  final VoidCallback onUnlocked;

  @override
  State<LockScreen> createState() => _LockScreenState();
}

class _LockScreenState extends State<LockScreen> with SingleTickerProviderStateMixin, WidgetsBindingObserver {
  final _code = TextEditingController();
  final _focus = FocusNode();
  final _fieldKey = GlobalKey();
  late final AnimationController _tilt;
  String? _id;
  String? _message;
  bool _messageIsError = true;
  bool _busy = false;
  bool _awaitingPermission = false;
  bool _scanning = false;
  bool _needSettings = false;
  bool _showCodeEntryHint = false;

  bool get _isAndroid => !kIsWeb && defaultTargetPlatform == TargetPlatform.android;

  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addObserver(this);
    _tilt = AnimationController(vsync: this, duration: const Duration(seconds: 7))..repeat();
    _focus.addListener(_onFocus);
    widget.unlock.deviceId().then((id) {
      if (mounted) setState(() => _id = id);
    });
    if (_isAndroid) {
      // A scan that finished while Android recreated the app (low memory) is delivered here.
      _secureChannel.setMethodCallHandler((call) async {
        if (call.method == 'orphanScanResult' && call.arguments is Map) {
          await _handleScanResult(call.arguments as Map, photo: false);
        }
        return null;
      });
      _invoke<Object?>('takePendingScan')
          .then((r) {
            if (r is Map && mounted) _handleScanResult(r, photo: false);
          })
          .catchError((Object _) {});
    }
  }

  @override
  void dispose() {
    WidgetsBinding.instance.removeObserver(this);
    if (_isAndroid) _secureChannel.setMethodCallHandler(null);
    _tilt.dispose();
    _code.dispose();
    _focus.removeListener(_onFocus);
    _focus.dispose();
    super.dispose();
  }

  // ── keyboard: keep the code field visible above the keyboard ───────────

  void _onFocus() {
    if (_focus.hasFocus) {
      Future<void>.delayed(const Duration(milliseconds: 320), _revealField);
    }
  }

  @override
  void didChangeMetrics() {
    // Keyboard opening/closing changes the view insets; re-reveal after layout.
    if (_focus.hasFocus) WidgetsBinding.instance.addPostFrameCallback((_) => _revealField());
  }

  void _revealField() {
    final ctx = _fieldKey.currentContext;
    if (!mounted || ctx == null || !_focus.hasFocus) return;
    Scrollable.ensureVisible(ctx, alignment: 0.35, duration: const Duration(milliseconds: 200), curve: Curves.easeOut);
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
      final ok = await _invoke<bool>('requestCamera').timeout(const Duration(seconds: 45), onTimeout: () => false);
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
      _messageIsError = true;
      _message = why;
    });
  }

  Future<bool> _ensureCamera() async {
    var granted = await _hasCameraPermission();
    if (granted) return true;
    setState(() {
      _awaitingPermission = true;
      _messageIsError = false;
      _message = '4 needs the camera to read the Bee Seller unlock code. Allow camera on the next prompt.';
    });
    granted = await _requestCameraPermission();
    if (!mounted) return false;
    setState(() => _awaitingPermission = false);
    if (!granted) {
      final rationale = await _shouldShowRationale();
      _fail(
        rationale
            ? 'Camera permission was denied. Tap Scan unlock code again and choose Allow, or type the code below.'
            : 'Camera permission is off. Open Settings, enable Camera for 4, then tap Scan unlock code — or type the code below.',
        needSettings: !rationale,
      );
      return false;
    }
    await Future<void>.delayed(const Duration(milliseconds: 250));
    return mounted;
  }

  /// Primary path: in-app live scanner (QR **or** the printed BEE1|… code text).
  Future<void> _openScan() async {
    if (_busy || _awaitingPermission || _scanning) return;
    if (!_isAndroid) {
      _fail('Scanning needs Android. Paste or type the Bee Seller unlock code below.');
      return;
    }
    FocusScope.of(context).unfocus();
    setState(() {
      _message = null;
      _needSettings = false;
      _showCodeEntryHint = false;
    });
    await _nativeLog('openScan begin (in-app CameraX scanner)');
    if (!await _ensureCamera()) return;
    setState(() {
      _scanning = true;
      _messageIsError = false;
      _message = 'Scanner open… point at the Bee Seller QR or BEE1|… code.';
    });
    try {
      final r = await _invoke<Object?>('scanUnlock', {'deviceId': _id});
      if (!mounted) return;
      await _handleScanResult(r, photo: false);
    } on PlatformException catch (e) {
      await _nativeLog('scanUnlock PlatformException ${e.code}: ${e.message}');
      if (!mounted) return;
      _fail(_humanScanError(e.code, e.message), needSettings: e.code == 'permission_denied');
    } catch (e) {
      await _nativeLog('scanUnlock error: $e');
      if (!mounted) return;
      _fail('Camera scan failed ($e). Try Photo scan, or type the code below.');
    }
  }

  /// Fallback: system camera still photo → native QR + text decode.
  Future<void> _openPhotoScan() async {
    if (_busy || _awaitingPermission || _scanning) return;
    if (!_isAndroid) {
      _fail('Scanning needs Android. Paste or type the Bee Seller unlock code below.');
      return;
    }
    FocusScope.of(context).unfocus();
    setState(() {
      _message = null;
      _needSettings = false;
      _showCodeEntryHint = false;
    });
    await _nativeLog('openPhotoScan begin');
    if (!await _ensureCamera()) return;
    setState(() {
      _scanning = true;
      _messageIsError = false;
      _message = 'Camera app open… photograph the Bee Seller QR or code so it fills the picture, then confirm.';
    });
    try {
      final r = await _invoke<Object?>('capturePhotoAndScanQr', {'deviceId': _id});
      if (!mounted) return;
      if (_scanning) setState(() => _message = 'Reading the photo…');
      await _handleScanResult(r, photo: true);
    } on PlatformException catch (e) {
      if (!mounted) return;
      _fail(_humanScanError(e.code, e.message), needSettings: e.code == 'permission_denied');
    } catch (e) {
      if (!mounted) return;
      _fail('Photo scan failed ($e). Try Scan unlock code, or type the code below.');
    }
  }

  /// Turns a native scan result into either an unlock attempt or a clear message that says
  /// whether the camera read nothing, read the wrong QR, or saw the code text but not all of it.
  Future<void> _handleScanResult(Object? r, {required bool photo}) async {
    if (r is String) {
      // Older native side: plain payload string ('' = cancelled).
      if (r.trim().isEmpty) {
        _fail('Scan cancelled. Try again, or type the code below.');
      } else {
        setState(() => _scanning = false);
        await _apply(r, source: 'scan');
      }
      return;
    }
    final m = r is Map ? r : const {};
    final status = m['status'] as String? ?? 'cancelled';
    final frames = (m['frames'] as num?)?.toInt() ?? 0;
    final sawText = m['sawCodeText'] == true;
    final nonBee = m['nonBee'] as String?;
    await _nativeLog(
      'scan result status=$status via=${m['via']} frames=$frames sawText=$sawText nonBee=${nonBee != null} code=${m['code']}',
    );
    if (!mounted) return;
    switch (status) {
      case 'ok':
        setState(() => _scanning = false);
        final via = m['via'] as String? ?? 'qr';
        await _apply(m['payload'] as String? ?? '', source: via.contains('text') ? 'text' : 'qr');
        return;
      case 'error':
        final code = m['code'] as String?;
        _fail(_humanScanError(code, m['message'] as String?), needSettings: code == 'permission_denied');
        return;
      default:
        final what = photo ? 'in the photo' : 'by the scanner';
        if (sawText) {
          _fail(
            'Camera worked and saw the BEE1|… code text $what, but could not read every character. '
            'Hold the phone closer so the code fills the box, keep it still (tap to focus), or type the code below.',
          );
        } else if (nonBee != null) {
          _fail(
            'Camera read a QR, but it is not a Bee Seller unlock code (it says “$nonBee”). '
            'Scan the unlock code that Bee Seller shows after you tap Generate.',
          );
        } else if (status == 'no_code') {
          _fail('No QR or BEE1|… unlock code was found in the photo. Fill the picture with the code, in good light, or type it below.');
        } else if (frames > 0) {
          _fail(
            'Scanner closed — no Bee Seller QR or BEE1|… code was seen (camera worked). '
            'Try again closer, or type the code below.',
          );
        } else {
          _fail('Scan cancelled. Try again, or type the code below.');
        }
    }
  }

  Future<void> _paste() async {
    final data = await Clipboard.getData(Clipboard.kTextPlain);
    final text = data?.text?.trim() ?? '';
    if (!mounted) return;
    if (text.isEmpty) {
      setState(() {
        _messageIsError = true;
        _message = 'Clipboard is empty. Copy the code from Bee Seller, then paste.';
      });
      return;
    }
    _code.text = text;
    _code.selection = TextSelection.collapsed(offset: _code.text.length);
    _focus.requestFocus();
    setState(() => _message = null);
  }

  /// Native clean-up of look-alike characters (O/0, l/1, …). Only returns HMAC-valid codes.
  Future<String?> _recover(String raw) async {
    if (!_isAndroid) return null;
    try {
      return await _invoke<String>('recoverCode', {'text': raw, 'deviceId': _id});
    } catch (_) {
      return null;
    }
  }

  /// [source]: 'qr' | 'text' (camera) | 'scan' (legacy) | null (typed / pasted).
  Future<void> _apply(String raw, {String? source}) async {
    if (_busy) return;
    setState(() {
      _busy = true;
      _message = null;
      _needSettings = false;
    });
    final fromCamera = source != null;
    await _nativeLog('applyPayload source=${source ?? 'typed'} len=${raw.trim().length}');
    var r = await widget.unlock.applyPayload(raw);
    if (!r.isOk && (r.reason == UnlockFail.notBeeCode || r.reason == UnlockFail.badSignature)) {
      final fixed = await _recover(raw);
      if (fixed != null && fixed != raw.trim()) {
        await _nativeLog('recoverCode fixed the code');
        r = await widget.unlock.applyPayload(fixed);
      }
    }
    if (!mounted) return;
    if (r.isOk) {
      await _nativeLog('unlock success');
      setState(() {
        _messageIsError = false;
        _message = r.value;
      });
      widget.onUnlocked();
      return;
    }
    await _nativeLog('unlock fail reason=${r.reason} : ${r.error}');
    final err = r.error ?? 'Invalid unlock code.';
    final head = switch (source) {
      'qr' => 'QR read ✓ but the code was refused: ',
      'text' => 'Code text read ✓ but the code was refused: ',
      'scan' => 'Code read ✓ but refused: ',
      _ => '',
    };
    setState(() {
      _busy = false;
      _scanning = false;
      _showCodeEntryHint = true;
      _messageIsError = true;
      _message = '$head$err';
      if (fromCamera && r.reason != UnlockFail.otherPhone && r.reason != UnlockFail.alreadyUsed) {
        // Let the user see / fix what the camera read.
        final clean = QrPayload.extract(raw);
        if (clean != null) _code.text = clean;
      }
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
        // Like Scaffold.resizeToAvoidBottomInset: the scroll view ends at the top of the keyboard,
        // so the focused field can always be scrolled into view (WidgetsApp has no Scaffold).
        child: Padding(
          padding: EdgeInsets.only(bottom: keyboard),
          child: ListView(
            keyboardDismissBehavior: ScrollViewKeyboardDismissBehavior.manual,
            padding: EdgeInsets.fromLTRB(20, pad.top + 18, 20, (keyboard > 0 ? 0 : pad.bottom) + 28),
            children: [
              Text('4', textAlign: TextAlign.center, style: _ts(42, FontWeight.w900, const Color(0xFFFFFFFF))),
              const SizedBox(height: 6),
              Text(
                'Grade 9\u201312  \u00b7  Offline  \u00b7  Notes and exams',
                textAlign: TextAlign.center,
                style: _ts(15, FontWeight.w700, const Color(0xFFFFE7D4)),
              ),
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
                                  child: Text(
                                    _id ?? '\u2026',
                                    textAlign: TextAlign.center,
                                    style: _ts(20, FontWeight.w900, _ink).copyWith(letterSpacing: 1.5),
                                  ),
                                ),
                              ],
                            ),
                          ),
                        ),
                        const SizedBox(height: 10),
                        Text(
                          'Bee Seller types this phone ID exactly (tap it to copy), then shows you the unlock code.',
                          textAlign: TextAlign.center,
                          style: _ts(14, FontWeight.w700, _ink),
                        ),
                      ],
                    ),
                  ),
                ),
              ),
              const SizedBox(height: 22),
              // Primary: in-app live scanner (QR or the printed code text)
              _Btn(
                label: _awaitingPermission
                    ? 'Waiting for camera\u2026'
                    : _scanning
                    ? 'Scanner open\u2026'
                    : 'Scan unlock code',
                filled: true,
                onTap: (_busy || _awaitingPermission || _scanning) ? null : _openScan,
              ),
              const SizedBox(height: 8),
              Text(
                'Reads the Bee Seller QR or the BEE1|\u2026 code text on the seller\u2019s screen.',
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
                    child: Text('Enter unlock code', textAlign: TextAlign.center, style: _ts(16, FontWeight.w900, const Color(0xFFFFFFFF))),
                  ),
                ),
                const SizedBox(height: 10),
              ],
              Text('Enter unlock code', style: _ts(16, FontWeight.w900, const Color(0xFFFFFFFF))),
              const SizedBox(height: 4),
              Text(
                'Always available \u2014 paste or type the BEE1|\u2026 code from Bee Seller.',
                style: _ts(13, FontWeight.w700, const Color(0xFFFFE7D4)),
              ),
              const SizedBox(height: 8),
              DecoratedBox(
                decoration: BoxDecoration(color: const Color(0x33FFFFFF), borderRadius: BorderRadius.circular(18)),
                child: Padding(
                  padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 10),
                  child: GestureDetector(
                    key: _fieldKey,
                    onTap: () => _focus.requestFocus(),
                    child: EditableText(
                      controller: _code,
                      focusNode: _focus,
                      // Keep the Paste / Unlock buttons under the field visible too.
                      scrollPadding: const EdgeInsets.fromLTRB(20, 20, 20, 180),
                      autocorrect: false,
                      enableSuggestions: false,
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
                  Expanded(
                    child: _Btn(label: 'Paste', filled: false, onTap: _busy ? null : _paste),
                  ),
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
                _Btn(label: 'Retry Scan unlock code', filled: false, onTap: (_busy || _awaitingPermission || _scanning) ? null : _openScan),
              ],
              if (_needSettings) ...[const SizedBox(height: 8), _Btn(label: 'Open Settings', filled: true, onTap: _openAppSettings)],
              if (_message != null) ...[
                const SizedBox(height: 12),
                Text(
                  _message!,
                  textAlign: TextAlign.center,
                  style: _ts(14, FontWeight.w800, _messageIsError ? _peach : const Color(0xFFFFE7D4)),
                ),
              ],
            ],
          ),
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
