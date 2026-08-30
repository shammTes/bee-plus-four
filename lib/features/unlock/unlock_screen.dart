import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import '../../core/licensing/device_id.dart';
import '../../core/licensing/unlock_store.dart';

class UnlockScreen extends StatefulWidget {
  const UnlockScreen({super.key});
  @override
  State<UnlockScreen> createState() => _UnlockScreenState();
}
class _UnlockScreenState extends State<UnlockScreen> {
  final controller = TextEditingController();
  String? deviceId; String? message; Set<String> unlocked = {};
  @override
  void initState() {
    super.initState();
    DeviceIdProvider.getId().then((id) { if (mounted) setState(() => deviceId = id); });
    unlocked = UnlockStore.instance.unlockedPackages;
  }
  @override
  void dispose() { controller.dispose(); super.dispose(); }
  Future<void> _apply() async {
    final r = await UnlockStore.instance.applyPayload(controller.text.trim());
    setState(() { message = r.isOk ? r.value : r.error; unlocked = UnlockStore.instance.unlockedPackages; });
  }
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Unlock')),
      body: ListView(padding: const EdgeInsets.all(16), children: [
        const Text('Device ID (show to seller):'),
        Card(child: ListTile(
          title: Text(deviceId ?? '…', style: const TextStyle(fontWeight: FontWeight.w600)),
          trailing: IconButton(icon: const Icon(Icons.copy), onPressed: deviceId == null ? null : () {
            Clipboard.setData(ClipboardData(text: deviceId!));
          }),
        )),
        Text(unlocked.isEmpty ? 'Unlocked: None (demo content available)' : 'Unlocked: ${unlocked.join(', ')}'),
        const SizedBox(height: 16),
        TextField(controller: controller, maxLines: 3,
          decoration: const InputDecoration(labelText: 'Paste unlock QR payload', border: OutlineInputBorder())),
        const SizedBox(height: 12),
        FilledButton(onPressed: _apply, child: const Text('Apply unlock')),
        if (message != null) Padding(padding: const EdgeInsets.only(top: 12), child: Text(message!)),
        const SizedBox(height: 20),
        Text('App 4: Highschool package (G9–G12). HMAC-signed, device-bound, single-use, permanent.',
          style: Theme.of(context).textTheme.bodySmall),
      ]),
    );
  }
}
