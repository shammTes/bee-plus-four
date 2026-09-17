import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:qr_flutter/qr_flutter.dart';
import 'package:uuid/uuid.dart';

import 'core/licensing/qr_payload.dart';
import 'core/theme/four_theme.dart';

/// Master (Shamm) app — generate wholesale codes for Bee Sellers.
Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();
  runApp(const MasterApp());
}

class MasterApp extends StatelessWidget {
  const MasterApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Shamm Master',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        colorSchemeSeed: const Color(0xFF7C3AED),
        useMaterial3: true,
      ),
      home: const MasterHomePage(),
    );
  }
}

class MasterHomePage extends StatefulWidget {
  const MasterHomePage({super.key});

  @override
  State<MasterHomePage> createState() => _MasterHomePageState();
}

class _MasterHomePageState extends State<MasterHomePage> {
  final sellerIdCtrl = TextEditingController();
  final quotaCtrl = TextEditingController(text: '50');
  String? lastCode;
  String status = '';
  final history = <Map<String, String>>[];

  void _generate() {
    final sid = sellerIdCtrl.text.trim();
    final q = int.tryParse(quotaCtrl.text.trim()) ?? 0;
    if (sid.isEmpty) {
      setState(() => status = 'Enter Bee Seller Device ID.');
      return;
    }
    if (q < 1) {
      setState(() => status = 'Quota must be at least 1.');
      return;
    }
    final nonce = const Uuid().v4().replaceAll('-', '').substring(0, 12);
    final payload = QrPayload.issueWholesale(
      sellerDeviceId: sid,
      quota: q,
      nonce: nonce,
    );
    final code = payload.encode();
    setState(() {
      lastCode = code;
      status = 'Wholesale code ready for seller $sid (+$q).';
      history.insert(0, {
        'seller': sid,
        'quota': '$q',
        'at': DateTime.now().toIso8601String(),
        'code': code,
      });
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Shamm · Master',
            style: TextStyle(fontWeight: FontWeight.w900)),
        backgroundColor: const Color(0xFF7C3AED),
        foregroundColor: Colors.white,
      ),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          const Text(
            'Generate wholesale codes for Bee Sellers.\n'
            'Seller redeems the code on their Bee Seller app, then can unlock students and grant sub-seller codes.',
            style: TextStyle(height: 1.4),
          ),
          const SizedBox(height: 16),
          TextField(
            controller: sellerIdCtrl,
            decoration: const InputDecoration(
              border: OutlineInputBorder(),
              labelText: 'Bee Seller Device ID',
              hintText: 'From Bee Seller home screen',
            ),
          ),
          const SizedBox(height: 12),
          TextField(
            controller: quotaCtrl,
            keyboardType: TextInputType.number,
            decoration: const InputDecoration(
              border: OutlineInputBorder(),
              labelText: 'Unlock quota to grant',
            ),
          ),
          const SizedBox(height: 12),
          FilledButton(
            onPressed: _generate,
            child: const Text('Generate wholesale QR'),
          ),
          if (status.isNotEmpty) ...[
            const SizedBox(height: 12),
            Text(status, style: const TextStyle(fontWeight: FontWeight.w700)),
          ],
          if (lastCode != null) ...[
            const SizedBox(height: 16),
            Center(
              child: Container(
                padding: const EdgeInsets.all(12),
                color: Colors.white,
                child: QrImageView(
                  data: lastCode!,
                  size: 240,
                  backgroundColor: Colors.white,
                ),
              ),
            ),
            const SizedBox(height: 8),
            SelectableText(lastCode!, style: const TextStyle(fontSize: 11)),
            OutlinedButton.icon(
              onPressed: () =>
                  Clipboard.setData(ClipboardData(text: lastCode!)),
              icon: const Icon(Icons.copy),
              label: const Text('Copy wholesale code'),
            ),
          ],
          const SizedBox(height: 24),
          const Text('Session history',
              style: TextStyle(fontWeight: FontWeight.w900)),
          ...history.take(20).map((h) => ListTile(
                dense: true,
                title: Text('${h['seller']} · +${h['quota']}'),
                subtitle: Text(h['at'] ?? ''),
              )),
          const SizedBox(height: 24),
          const Text(
            'Developed by SHAMM TESFALEM · Phone: 07162947',
            style: TextStyle(color: FourTheme.muted, fontSize: 12),
          ),
        ],
      ),
    );
  }
}
