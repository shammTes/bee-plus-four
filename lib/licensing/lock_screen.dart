import 'dart:math' as math;

import 'package:flutter/services.dart';
import 'package:flutter/widgets.dart';
import 'package:mobile_scanner/mobile_scanner.dart';
import 'package:qr_flutter/qr_flutter.dart';

import 'unlock_store.dart';

const _ink = Color(0xFF3E3129);
const _cream = Color(0xFFFFFCF7);
const _peach = Color(0xFFFFC9A3);
const _coral = Color(0xFFC24E32);

TextStyle _ts(double size, FontWeight w, Color color) => TextStyle(
      fontFamily: 'HighNunito',
      fontSize: size,
      fontWeight: w,
      color: color,
      height: 1.25,
    );

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

  bool _scanning = false;

  Future<void> _openScan() async {
    setState(() {
      _message = null;
      _scanning = true;
    });
  }

  Future<void> _onScan(String code) async {
    if (!_scanning) return;
    setState(() => _scanning = false);
    final text = code.trim();
    if (text.isEmpty) {
      setState(() => _message = 'No code scanned. Paste the Bee Seller code, or try again.');
      return;
    }
    _code.text = text;
    await _apply(text);
  }

  Future<void> _paste() async {
    final data = await Clipboard.getData(Clipboard.kTextPlain);
    final text = data?.text?.trim() ?? '';
    if (!mounted) return;
    if (text.isEmpty) {
      setState(() => _message = 'Clipboard is empty. Copy the code, then paste.');
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
    });
    final r = await widget.unlock.applyPayload(raw);
    if (!mounted) return;
    if (r.isOk) {
      widget.onUnlocked();
      return;
    }
    setState(() {
      _busy = false;
      _message = r.error;
    });
  }

  @override
  Widget build(BuildContext context) {
    final pad = MediaQuery.paddingOf(context);
    final keyboard = MediaQuery.viewInsetsOf(context).bottom;
    if (_scanning) {
      return ColoredBox(
        color: const Color(0xFF1A120E),
        child: Stack(
          fit: StackFit.expand,
          children: [
            MobileScanner(
              onDetect: (capture) {
                final raw = capture.barcodes.isEmpty ? null : capture.barcodes.first.rawValue;
                if (raw != null && raw.isNotEmpty) _onScan(raw);
              },
            ),
            Positioned(
              left: 16,
              right: 16,
              bottom: 28,
              child: _Btn(label: 'Close camera', filled: true, onTap: () => setState(() => _scanning = false)),
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
            Text('Already have a code?', style: _ts(16, FontWeight.w900, const Color(0xFFFFFFFF))),
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
            _Btn(label: 'Scan seller QR', filled: false, onTap: _busy ? null : _openScan),
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

