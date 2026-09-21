import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:qr_flutter/qr_flutter.dart';

import '../../core/licensing/device_id.dart';
import '../../core/licensing/unlock_store.dart';
import '../scan/qr_scan_page.dart';

class UnlockScreen extends StatefulWidget {
  const UnlockScreen({super.key});

  @override
  State<UnlockScreen> createState() => _UnlockScreenState();
}

class _UnlockScreenState extends State<UnlockScreen> {
  final controller = TextEditingController();
  String? deviceId;
  String? message;
  Set<String> unlocked = {};

  @override
  void initState() {
    super.initState();
    DeviceIdProvider.getId().then((id) {
      if (mounted) setState(() => deviceId = id);
    });
    unlocked = UnlockStore.instance.unlockedPackages;
  }

  @override
  void dispose() {
    controller.dispose();
    super.dispose();
  }

  Future<void> _apply() async {
    final r = await UnlockStore.instance.applyPayload(controller.text.trim());
    setState(() {
      message = r.isOk ? r.value : r.error;
      unlocked = UnlockStore.instance.unlockedPackages;
    });
  }

  Future<void> _scanUnlock() async {
    await Navigator.of(context).push(
      MaterialPageRoute(
        builder: (_) => QrScanPage(
          title: 'Scan unlock QR',
          hint: 'Scan the QR shown by Bee Seller',
          onScan: (code) async {
            controller.text = code;
            await _apply();
          },
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Unlock')),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          const Text(
            'Your Device ID — show this QR to Bee Seller',
            style: TextStyle(fontWeight: FontWeight.w800),
          ),
          const SizedBox(height: 8),
          Card(
            child: Padding(
              padding: const EdgeInsets.all(12),
              child: Column(
                children: [
                  if (deviceId != null && deviceId!.isNotEmpty)
                    QrImageView(
                      data: deviceId!,
                      size: 180,
                      backgroundColor: Colors.white,
                    )
                  else
                    const Padding(
                      padding: EdgeInsets.all(24),
                      child: CircularProgressIndicator(),
                    ),
                  const SizedBox(height: 8),
                  SelectableText(
                    deviceId ?? '…',
                    style: const TextStyle(fontWeight: FontWeight.w700),
                  ),
                  IconButton(
                    icon: const Icon(Icons.copy),
                    onPressed: deviceId == null
                        ? null
                        : () => Clipboard.setData(
                              ClipboardData(text: deviceId!),
                            ),
                  ),
                ],
              ),
            ),
          ),
          const SizedBox(height: 8),
          Text(
            unlocked.isEmpty
                ? 'Unlocked: None'
                : 'Unlocked: ${unlocked.join(', ')}',
          ),
          const SizedBox(height: 20),
          const Text(
            'Paste or scan unlock code from Bee Seller',
            style: TextStyle(fontWeight: FontWeight.w800),
          ),
          const SizedBox(height: 8),
          TextField(
            controller: controller,
            maxLines: 3,
            decoration: const InputDecoration(
              labelText: 'Unlock code',
              border: OutlineInputBorder(),
            ),
          ),
          const SizedBox(height: 12),
          Row(
            children: [
              Expanded(
                child: FilledButton(
                  onPressed: _apply,
                  child: const Text('Apply unlock'),
                ),
              ),
              const SizedBox(width: 10),
              FilledButton.tonalIcon(
                onPressed: _scanUnlock,
                icon: const Icon(Icons.qr_code_scanner),
                label: const Text('Scan QR'),
              ),
            ],
          ),
          if (message != null)
            Padding(
              padding: const EdgeInsets.only(top: 12),
              child: Text(
                message!,
                style: const TextStyle(fontWeight: FontWeight.w700),
              ),
            ),
          const SizedBox(height: 20),
          Text(
            'App 4: Highschool (G9–G12). Codes are HMAC-signed, device-bound, single-use, permanent.',
            style: Theme.of(context).textTheme.bodySmall,
          ),
        ],
      ),
    );
  }
}
