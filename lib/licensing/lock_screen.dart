import 'dart:async';
import 'dart:math' as math;

import 'package:flutter/foundation.dart' show TargetPlatform, defaultTargetPlatform, debugPrint, kIsWeb;
import 'package:flutter/services.dart';
import 'package:flutter/widgets.dart';
import 'package:mobile_scanner/mobile_scanner.dart';
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

/// Human text for scanner failures (never show raw names like "genericError").
String _scannerErrorText(MobileScannerException error) {
  final code = error.errorCode;
  if (code == MobileScannerErrorCode.permissionDenied) {
    return 'Camera permission is off. Open Settings, enable Camera for 4, then tap Retry — or enter the unlock code below.';
  }
  if (code == MobileScannerErrorCode.unsupported) {
    return 'This phone cannot open the camera scanner. Enter the unlock code below, or tap Open Settings.';
  }
  if (code == MobileScannerErrorCode.genericError) {
    // Never surface raw "genericError" — usually HAL busy / start-before-attach / camera in use.
    return 'Camera could not open (busy or not ready). Wait a moment, tap Retry Scan, or enter the unlock code below.';
  }
  // Prefer the package human message over enum .name (avoids "genericError" style strings).
  final msg = code.message.trim();
  if (msg.isNotEmpty && !msg.toLowerCase().contains('generic')) {
    return '$msg Tap Retry Scan, or enter the unlock code below.';
  }
  return 'Camera was not ready. Tap Retry Scan, or enter the unlock code below.';
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
  MobileScannerController? _scanner;
  String? _id;
  String? _message;
  bool _busy = false;
  bool _scanning = false;
  bool _needSettings = false;
  bool _awaitingPermission = false;
  bool _showCodeEntryHint = false;
  bool _detecting = false;
  bool _startingEmbedded = false;
  int _scannerGen = 0;

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
    _scannerGen++;
    _startingEmbedded = false;
    unawaited(_stopScanner());
    _tilt.dispose();
    _code.dispose();
    _focus.dispose();
    super.dispose();
  }

  Future<void> _stopScanner() async {
    final c = _scanner;
    _scanner = null;
    if (c == null) return;
    debugPrint('HighSecure: dispose MobileScannerController');
    try {
      await c.stop();
    } catch (_) {}
    try {
      await c.dispose();
    } catch (_) {}
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

  void _failCamera(String why, {bool needSettings = false}) {
    debugPrint('HighSecure camera fail: $why settings=$needSettings');
    _startingEmbedded = false;
    setState(() {
      _awaitingPermission = false;
      _scanning = false;
      _needSettings = needSettings;
      _showCodeEntryHint = true;
      _message = why;
    });
  }

  /// Embedded MobileScanner only — never call native Play Services scanQr (it steals the camera).
  Future<void> _openScan() async {
    if (_busy || _awaitingPermission || _scanning || _startingEmbedded) return;
    setState(() {
      _message = null;
      _needSettings = false;
      _showCodeEntryHint = false;
    });
    await _nativeLog('openScan begin (embedded-only; no scanQr)');

    if (_isAndroid) {
      var granted = await _hasCameraPermission();
      if (!granted) {
        setState(() {
          _awaitingPermission = true;
          _message = '4 needs the camera to scan the Bee Seller unlock QR. Allow camera on the next prompt.';
        });
        granted = await _requestCameraPermission();
        if (!mounted) return;
        setState(() => _awaitingPermission = false);
        if (!granted) {
          final rationale = await _shouldShowRationale();
          _failCamera(
            rationale
                ? 'Camera permission was denied. Tap Scan again and choose Allow, or enter the unlock code below.'
                : 'Camera permission is off. Open Settings, enable Camera for 4, then tap Scan — or enter the unlock code below.',
            needSettings: !rationale,
          );
          return;
        }
        // First-install: HAL needs a beat after Activity Result grant before CameraX opens.
        await _nativeLog('permission granted via ActivityResult; settling 500ms before MobileScanner');
        await Future<void>.delayed(const Duration(milliseconds: 500));
        if (!mounted) return;
      }
    }

    await _startEmbeddedScanner();
  }

  Future<void> _startEmbeddedScanner() async {
    if (_startingEmbedded || _scanning) {
      await _nativeLog('embedded start skipped (already starting/scanning)');
      return;
    }
    if (_isAndroid) {
      final granted = await _hasCameraPermission();
      if (!granted) {
        _failCamera(
          'Camera permission is off. Open Settings or enter the unlock code below.',
          needSettings: true,
        );
        return;
      }
    }

    _startingEmbedded = true;
    final gen = ++_scannerGen;
    // Single instance: fully dispose any previous controller before creating another.
    await _stopScanner();
    if (!mounted || gen != _scannerGen) {
      _startingEmbedded = false;
      return;
    }

    final controller = MobileScannerController(
      autoStart: false,
      facing: CameraFacing.back,
      detectionSpeed: DetectionSpeed.normal,
      formats: const [BarcodeFormat.qrCode],
    );
    _scanner = controller;
    _detecting = false;
    setState(() {
      _scanning = true;
      _message = null;
      _needSettings = false;
    });

    // Attach MobileScanner widget first; start only after attach + 500ms (avoids start-before-attach genericError).
    WidgetsBinding.instance.addPostFrameCallback((_) async {
      if (!mounted || gen != _scannerGen || _scanner != controller) {
        _startingEmbedded = false;
        return;
      }
      // Second frame ensures PlatformView / texture is in the tree.
      WidgetsBinding.instance.addPostFrameCallback((_) async {
        if (!mounted || gen != _scannerGen || _scanner != controller) {
          _startingEmbedded = false;
          return;
        }
        await _nativeLog('widget attached; waiting 500ms before start');
        await Future<void>.delayed(const Duration(milliseconds: 500));
        if (!mounted || gen != _scannerGen || _scanner != controller) {
          _startingEmbedded = false;
          return;
        }
        try {
          await _nativeLog('MobileScannerController.start() facing=back');
          try {
            await controller.start(cameraDirection: CameraFacing.back);
          } catch (_) {
            await controller.start();
          }
          _startingEmbedded = false;
          await _nativeLog('MobileScannerController.start() ok');
        } on MobileScannerException catch (e) {
          // Log enum name for debug; never show it in UI.
          await _nativeLog('MobileScannerException ${e.errorCode.name}: ${e.errorDetails}');
          if (!mounted) return;
          await _stopScanner();
          final denied = e.errorCode == MobileScannerErrorCode.permissionDenied;
          _failCamera(_scannerErrorText(e), needSettings: denied);
        } catch (e) {
          await _nativeLog('MobileScanner start failed: $e');
          if (!mounted) return;
          await _stopScanner();
          _failCamera('Camera could not open. Tap Retry Scan, or enter the unlock code below.');
        }
      });
    });
  }

  Future<void> _retryScan() async {
    await _nativeLog('retryScan');
    _scannerGen++;
    _startingEmbedded = false;
    await _stopScanner();
    if (mounted) {
      setState(() {
        _scanning = false;
        _message = null;
      });
    }
    await Future<void>.delayed(const Duration(milliseconds: 500));
    if (!mounted) return;
    await _openScan();
  }

  Future<void> _closeEmbeddedScanner() async {
    _scannerGen++;
    _startingEmbedded = false;
    await _stopScanner();
    if (mounted) {
      setState(() {
        _scanning = false;
        _showCodeEntryHint = true;
        _message = 'Camera closed. Paste or type the Bee Seller unlock code below.';
      });
    }
  }

  Future<void> _onEmbeddedError(MobileScannerException error) async {
    await _nativeLog('errorBuilder ${error.errorCode.name}');
    if (!mounted) return;
    _scannerGen++;
    _startingEmbedded = false;
    await _stopScanner();
    final denied = error.errorCode == MobileScannerErrorCode.permissionDenied;
    _failCamera(_scannerErrorText(error), needSettings: denied);
  }

  Future<void> _onScan(String code) async {
    if (_detecting) return;
    _detecting = true;
    if (_scanning) {
      _scannerGen++;
      setState(() => _scanning = false);
      await _stopScanner();
    }
    final text = code.trim();
    if (text.isEmpty) {
      _detecting = false;
      setState(() {
        _showCodeEntryHint = true;
        _message = 'No code scanned. Paste the Bee Seller code, or try again.';
      });
      return;
    }
    _code.text = text;
    await _apply(text);
    _detecting = false;
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

  Future<void> _apply(String raw) async {
    if (_busy) return;
    setState(() {
      _busy = true;
      _message = null;
      _needSettings = false;
    });
    final r = await widget.unlock.applyPayload(raw);
    if (!mounted) return;
    if (r.isOk) {
      _scannerGen++;
      await _stopScanner();
      widget.onUnlocked();
      return;
    }
    setState(() {
      _busy = false;
      _showCodeEntryHint = true;
      _message = r.error;
    });
  }

  @override
  Widget build(BuildContext context) {
    final pad = MediaQuery.paddingOf(context);
    final keyboard = MediaQuery.viewInsetsOf(context).bottom;
    if (_scanning) {
      final controller = _scanner;
      return ColoredBox(
        color: const Color(0xFF1A120E),
        child: Stack(
          fit: StackFit.expand,
          children: [
            if (controller != null)
              MobileScanner(
                controller: controller,
                fit: BoxFit.cover,
                onDetect: (capture) {
                  final raw = capture.barcodes.isEmpty ? null : capture.barcodes.first.rawValue;
                  if (raw != null && raw.isNotEmpty) _onScan(raw);
                },
                errorBuilder: (context, error, child) {
                  // Never surface raw "genericError" — map + offer actions.
                  WidgetsBinding.instance.addPostFrameCallback((_) {
                    if (mounted && _scanning) unawaited(_onEmbeddedError(error));
                  });
                  return Center(
                    child: Padding(
                      padding: const EdgeInsets.all(24),
                      child: Text(
                        _scannerErrorText(error),
                        textAlign: TextAlign.center,
                        style: _ts(15, FontWeight.w800, _peach),
                      ),
                    ),
                  );
                },
              )
            else
              const Center(child: SizedBox(width: 36, height: 36, child: DecoratedBox(decoration: BoxDecoration(color: _peach, shape: BoxShape.circle)))),
            Positioned(
              left: 16,
              right: 16,
              bottom: 28 + pad.bottom,
              child: Column(
                mainAxisSize: MainAxisSize.min,
                children: [
                  _Btn(label: 'Retry Scan', filled: true, onTap: _busy ? null : _retryScan),
                  const SizedBox(height: 8),
                  _Btn(
                    label: 'Enter unlock code instead',
                    filled: false,
                    onTap: _busy
                        ? null
                        : () async {
                            await _closeEmbeddedScanner();
                            if (mounted) _focus.requestFocus();
                          },
                  ),
                  const SizedBox(height: 8),
                  _Btn(
                    label: 'Open Settings',
                    filled: false,
                    onTap: _busy ? null : _openAppSettings,
                  ),
                ],
              ),
            ),
          ],
        ),
      );
    }
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
            Text(_showCodeEntryHint ? 'Paste or type the Bee Seller code' : 'Already have a code?', style: _ts(16, FontWeight.w900, const Color(0xFFFFFFFF))),
            const SizedBox(height: 4),
            Text('Type it, paste it, or scan the Bee Seller QR.', style: _ts(13, FontWeight.w700, const Color(0xFFFFE7D4))),
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
            const SizedBox(height: 8),
            _Btn(
              label: _awaitingPermission ? 'Waiting for camera\u2026' : 'Scan seller QR',
              filled: false,
              onTap: (_busy || _awaitingPermission || _startingEmbedded) ? null : _openScan,
            ),
            if (_showCodeEntryHint || _message != null) ...[
              const SizedBox(height: 8),
              _Btn(label: 'Retry Scan', filled: false, onTap: (_busy || _awaitingPermission || _startingEmbedded) ? null : _retryScan),
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
