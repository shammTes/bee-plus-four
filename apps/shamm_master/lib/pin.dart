import 'package:flutter/material.dart';

import 'store.dart';
import 'widgets.dart';

/// Admin PIN screen: set a PIN the first time, then type it every time the app opens.
class PinScreen extends StatefulWidget {
  const PinScreen({super.key, required this.store, required this.onUnlocked, this.changing = false});
  final Store store;
  final VoidCallback onUnlocked;

  /// Set a new PIN (from the menu) instead of unlocking.
  final bool changing;

  @override
  State<PinScreen> createState() => _PinScreenState();
}

class _PinScreenState extends State<PinScreen> {
  String entry = '';
  String? first;
  String? error;
  int wrong = 0;
  DateTime? waitUntil;

  bool get setting => widget.changing || !widget.store.hasPin;

  String get title {
    if (!setting) return 'Type your PIN';
    return first == null ? 'Make a PIN (4 to 6 numbers)' : 'Type the same PIN again';
  }

  void tap(String d) {
    if (waitUntil != null && DateTime.now().isBefore(waitUntil!)) {
      setState(() => error = 'Too many wrong tries. Wait ${waitUntil!.difference(DateTime.now()).inSeconds + 1} seconds.');
      return;
    }
    if (entry.length >= 6) return;
    setState(() {
      entry += d;
      error = null;
    });
    if (!setting && entry.length >= 4 && widget.store.checkPin(entry)) {
      widget.onUnlocked();
    }
  }

  void back() => setState(() => entry = entry.isEmpty ? entry : entry.substring(0, entry.length - 1));

  Future<void> ok() async {
    if (entry.length < 4) {
      setState(() => error = 'The PIN needs 4 to 6 numbers.');
      return;
    }
    if (setting) {
      if (first == null) {
        setState(() {
          first = entry;
          entry = '';
        });
        return;
      }
      if (first != entry) {
        setState(() {
          first = null;
          entry = '';
          error = 'The two PINs are not the same. Start again.';
        });
        return;
      }
      await widget.store.setPin(entry);
      widget.onUnlocked();
      return;
    }
    if (widget.store.checkPin(entry)) {
      widget.onUnlocked();
      return;
    }
    wrong++;
    setState(() {
      entry = '';
      error = 'Wrong PIN.';
      if (wrong % 5 == 0) {
        waitUntil = DateTime.now().add(Duration(seconds: 30 * (wrong ~/ 5)));
        error = 'Wrong PIN 5 times. Wait ${30 * (wrong ~/ 5)} seconds.';
      }
    });
  }

  Widget key_(String label, {VoidCallback? onTap, IconData? icon, Key? k}) => Expanded(
    child: Padding(
      padding: const EdgeInsets.all(6),
      child: Material(
        color: Colors.white,
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(18),
          side: const BorderSide(color: Color(0xFFE6E8EF)),
        ),
        child: InkWell(
          key: k,
          borderRadius: BorderRadius.circular(18),
          onTap: onTap ?? () => tap(label),
          child: SizedBox(
            height: 62,
            child: Center(
              child: icon != null
                  ? Icon(icon, color: ink)
                  : Text(
                      label,
                      style: const TextStyle(fontSize: 24, fontWeight: FontWeight.w600, color: ink),
                    ),
            ),
          ),
        ),
      ),
    ),
  );

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: widget.changing ? AppBar(title: const Text('Change PIN')) : null,
      body: SafeArea(
        child: Center(
          child: ConstrainedBox(
            constraints: const BoxConstraints(maxWidth: 420),
            child: Padding(
              padding: const EdgeInsets.symmetric(horizontal: 24),
              child: Column(
                children: [
                  const Spacer(),
                  const CircleAvatar(
                    radius: 32,
                    backgroundColor: brand,
                    child: Icon(Icons.lock_outline, color: Colors.white, size: 30),
                  ),
                  const SizedBox(height: 14),
                  const Text(
                    'Shamm Master',
                    style: TextStyle(fontSize: 22, fontWeight: FontWeight.w800, color: ink),
                  ),
                  const SizedBox(height: 6),
                  Text(
                    title,
                    key: const Key('pinTitle'),
                    style: const TextStyle(fontSize: 16, color: soft),
                  ),
                  const SizedBox(height: 20),
                  Row(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      for (var i = 0; i < 6; i++)
                        Container(
                          margin: const EdgeInsets.all(6),
                          width: 14,
                          height: 14,
                          decoration: BoxDecoration(
                            shape: BoxShape.circle,
                            color: i < entry.length ? brand : Colors.transparent,
                            border: Border.all(color: i < 4 ? brand : const Color(0xFFC7CAD6), width: 2),
                          ),
                        ),
                    ],
                  ),
                  SizedBox(
                    height: 28,
                    child: error == null
                        ? null
                        : Text(
                            error!,
                            key: const Key('pinError'),
                            style: const TextStyle(color: Color(0xFFDC2626)),
                          ),
                  ),
                  const Spacer(),
                  for (final row in const [
                    ['1', '2', '3'],
                    ['4', '5', '6'],
                    ['7', '8', '9'],
                  ])
                    Row(children: [for (final d in row) key_(d, k: Key('pin$d'))]),
                  Row(
                    children: [
                      key_('back', icon: Icons.backspace_outlined, onTap: back, k: const Key('pinBack')),
                      key_('0', k: const Key('pin0')),
                      key_('OK', icon: Icons.check, onTap: ok, k: const Key('pinOk')),
                    ],
                  ),
                  const SizedBox(height: 16),
                ],
              ),
            ),
          ),
        ),
      ),
    );
  }
}
