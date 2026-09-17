import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:qr_flutter/qr_flutter.dart';

import 'core/licensing/seller_store.dart';
import 'core/theme/four_theme.dart';

/// Bee Seller app entry — issue student unlock QR + wholesale sub-seller codes.
Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await SellerStore.instance.init();
  runApp(const BeeSellerApp());
}

class BeeSellerApp extends StatelessWidget {
  const BeeSellerApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Bee Seller',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        colorSchemeSeed: const Color(0xFF0D9488),
        useMaterial3: true,
      ),
      home: const SellerHomePage(),
    );
  }
}

class SellerHomePage extends StatefulWidget {
  const SellerHomePage({super.key});

  @override
  State<SellerHomePage> createState() => _SellerHomePageState();
}

class _SellerHomePageState extends State<SellerHomePage> {
  final store = SellerStore.instance;
  String deviceId = '…';
  final redeemCtrl = TextEditingController();
  final studentCtrl = TextEditingController();
  final sellerCtrl = TextEditingController();
  final quotaCtrl = TextEditingController(text: '10');
  String? lastCode;
  String status = '';

  @override
  void initState() {
    super.initState();
    store.deviceId().then((id) {
      if (mounted) setState(() => deviceId = id);
    });
  }

  Future<void> _refresh() async => setState(() {});

  Future<void> _redeem() async {
    final msg = await store.redeemAuthCode(redeemCtrl.text);
    setState(() => status = msg);
    await _refresh();
  }

  Future<void> _issueStudent() async {
    final r = await store.issueStudentUnlock(studentCtrl.text);
    if (r.error != null) {
      setState(() {
        status = r.error!;
        lastCode = null;
      });
    } else {
      setState(() {
        lastCode = r.code;
        status = 'Student unlock QR ready.';
      });
    }
    await _refresh();
  }

  Future<void> _issueSeller() async {
    final q = int.tryParse(quotaCtrl.text.trim()) ?? 0;
    final r = await store.issueSellerCode(
      targetSellerDeviceId: sellerCtrl.text,
      grantQuota: q,
    );
    if (r.error != null) {
      setState(() {
        status = r.error!;
        lastCode = null;
      });
    } else {
      setState(() {
        lastCode = r.code;
        status = 'Seller code QR ready.';
      });
    }
    await _refresh();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Bee Seller',
            style: TextStyle(fontWeight: FontWeight.w900)),
        backgroundColor: const Color(0xFF0D9488),
        foregroundColor: Colors.white,
      ),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          Card(
            child: ListTile(
              title: const Text('Seller Device ID',
                  style: TextStyle(fontWeight: FontWeight.w800)),
              subtitle: SelectableText(deviceId),
              trailing: IconButton(
                icon: const Icon(Icons.copy),
                onPressed: () {
                  Clipboard.setData(ClipboardData(text: deviceId));
                  ScaffoldMessenger.of(context).showSnackBar(
                    const SnackBar(content: Text('Copied seller Device ID')),
                  );
                },
              ),
            ),
          ),
          const SizedBox(height: 8),
          Card(
            color: const Color(0xFFECFDF5),
            child: Padding(
              padding: const EdgeInsets.all(16),
              child: Row(
                children: [
                  Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text('Quota: ${store.quotaRemaining}',
                            style: const TextStyle(
                                fontSize: 22, fontWeight: FontWeight.w900)),
                        Text(
                          store.isWholesale
                              ? 'Wholesale · can grant seller codes'
                              : 'Standard seller',
                          style: const TextStyle(color: FourTheme.muted),
                        ),
                      ],
                    ),
                  ),
                  const Icon(Icons.qr_code_2, size: 40, color: Color(0xFF0D9488)),
                ],
              ),
            ),
          ),
          const SizedBox(height: 16),
          const Text('1) Redeem Master / wholesale code',
              style: TextStyle(fontWeight: FontWeight.w900)),
          const SizedBox(height: 6),
          TextField(
            controller: redeemCtrl,
            decoration: const InputDecoration(
              border: OutlineInputBorder(),
              hintText: 'Paste WHOLESALE or SELLER code',
            ),
            maxLines: 2,
          ),
          const SizedBox(height: 8),
          FilledButton(onPressed: _redeem, child: const Text('Redeem code')),
          const SizedBox(height: 20),
          const Text('2) Unlock a student device',
              style: TextStyle(fontWeight: FontWeight.w900)),
          const SizedBox(height: 6),
          TextField(
            controller: studentCtrl,
            decoration: const InputDecoration(
              border: OutlineInputBorder(),
              hintText: 'Student Device ID from app Home QR',
            ),
          ),
          const SizedBox(height: 8),
          FilledButton(
              onPressed: _issueStudent,
              child: const Text('Generate student unlock QR')),
          if (store.isWholesale) ...[
            const SizedBox(height: 20),
            const Text('3) Wholesale · grant another seller',
                style: TextStyle(fontWeight: FontWeight.w900)),
            const Text(
              'Creates a SELLER code bound to their Device ID. Uses your quota.',
              style: TextStyle(color: FourTheme.muted, fontSize: 13),
            ),
            const SizedBox(height: 6),
            TextField(
              controller: sellerCtrl,
              decoration: const InputDecoration(
                border: OutlineInputBorder(),
                hintText: 'Other seller Device ID',
              ),
            ),
            const SizedBox(height: 8),
            TextField(
              controller: quotaCtrl,
              keyboardType: TextInputType.number,
              decoration: const InputDecoration(
                border: OutlineInputBorder(),
                labelText: 'Quota to grant',
              ),
            ),
            const SizedBox(height: 8),
            FilledButton.tonal(
                onPressed: _issueSeller,
                child: const Text('Generate seller code QR')),
          ],
          if (status.isNotEmpty) ...[
            const SizedBox(height: 16),
            Text(status, style: const TextStyle(fontWeight: FontWeight.w700)),
          ],
          if (lastCode != null) ...[
            const SizedBox(height: 12),
            Center(
              child: Container(
                padding: const EdgeInsets.all(12),
                color: Colors.white,
                child: QrImageView(
                  data: lastCode!,
                  size: 220,
                  backgroundColor: Colors.white,
                ),
              ),
            ),
            const SizedBox(height: 8),
            SelectableText(lastCode!,
                style: const TextStyle(fontSize: 11)),
            OutlinedButton.icon(
              onPressed: () {
                Clipboard.setData(ClipboardData(text: lastCode!));
              },
              icon: const Icon(Icons.copy),
              label: const Text('Copy code'),
            ),
          ],
          const SizedBox(height: 24),
          const Text('Recent issues',
              style: TextStyle(fontWeight: FontWeight.w900)),
          ...store.history.take(12).map((h) => ListTile(
                dense: true,
                title: Text('${h['type']} → ${h['target']}'),
                subtitle: Text('${h['at']}'),
              )),
        ],
      ),
    );
  }
}
