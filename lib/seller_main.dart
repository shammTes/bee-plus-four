import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:qr_flutter/qr_flutter.dart';

import 'core/licensing/seller_store.dart';
import 'core/theme/four_theme.dart';
import 'features/scan/qr_scan_page.dart';

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

  @override
  void dispose() {
    redeemCtrl.dispose();
    studentCtrl.dispose();
    sellerCtrl.dispose();
    quotaCtrl.dispose();
    super.dispose();
  }

  Future<void> _refresh() async => setState(() {});

  Future<void> _openScan({
    required String title,
    required String hint,
    required ValueChanged<String> onResult,
  }) async {
    await Navigator.of(context).push(
      MaterialPageRoute(
        builder: (_) => QrScanPage(
          title: title,
          hint: hint,
          onScan: onResult,
        ),
      ),
    );
  }

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
    final quota = store.quota;
    return Scaffold(
      appBar: AppBar(
        title: const Text('Bee Seller'),
        actions: [
          Padding(
            padding: const EdgeInsets.only(right: 12),
            child: Center(
              child: Text(
                'Quota: $quota',
                style: const TextStyle(fontWeight: FontWeight.w900),
              ),
            ),
          ),
        ],
      ),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          Text('Your seller Device ID',
              style: Theme.of(context).textTheme.titleSmall),
          Card(
            child: ListTile(
              title: SelectableText(
                deviceId,
                style: const TextStyle(fontWeight: FontWeight.w700),
              ),
              trailing: IconButton(
                icon: const Icon(Icons.copy),
                onPressed: () =>
                    Clipboard.setData(ClipboardData(text: deviceId)),
              ),
            ),
          ),
          const SizedBox(height: 16),
          const Text('1) Redeem Master / parent grant',
              style: TextStyle(fontWeight: FontWeight.w900)),
          const SizedBox(height: 6),
          TextField(
            controller: redeemCtrl,
            maxLines: 2,
            decoration: InputDecoration(
              border: const OutlineInputBorder(),
              hintText: 'Paste WHOLESALE/SELLER code or scan QR',
              suffixIcon: IconButton(
                tooltip: 'Scan QR',
                icon: const Icon(Icons.qr_code_scanner),
                onPressed: () => _openScan(
                  title: 'Scan grant QR',
                  hint: 'Scan Master or parent-seller grant QR',
                  onResult: (v) => setState(() => redeemCtrl.text = v),
                ),
              ),
            ),
          ),
          const SizedBox(height: 8),
          Row(
            children: [
              Expanded(
                child: FilledButton(
                  onPressed: _redeem,
                  child: const Text('Redeem grant'),
                ),
              ),
              const SizedBox(width: 8),
              FilledButton.tonalIcon(
                onPressed: () => _openScan(
                  title: 'Scan grant QR',
                  hint: 'Scan Master or parent-seller grant QR',
                  onResult: (v) async {
                    setState(() => redeemCtrl.text = v);
                    await _redeem();
                  },
                ),
                icon: const Icon(Icons.qr_code_scanner),
                label: const Text('Scan'),
              ),
            ],
          ),
          const SizedBox(height: 20),
          const Text('2) Unlock a student',
              style: TextStyle(fontWeight: FontWeight.w900)),
          const SizedBox(height: 4),
          const Text(
            'Scan the student Device ID QR from app 4, or type it.',
            style: TextStyle(color: FourTheme.muted, fontSize: 13),
          ),
          const SizedBox(height: 6),
          TextField(
            controller: studentCtrl,
            decoration: InputDecoration(
              border: const OutlineInputBorder(),
              hintText: 'Student Device ID',
              suffixIcon: IconButton(
                tooltip: 'Scan student QR',
                icon: const Icon(Icons.qr_code_scanner),
                onPressed: () => _openScan(
                  title: 'Scan student Device ID',
                  hint: 'Scan the Device ID QR on the student phone',
                  onResult: (v) => setState(() => studentCtrl.text = v),
                ),
              ),
            ),
          ),
          const SizedBox(height: 8),
          Row(
            children: [
              Expanded(
                child: FilledButton(
                  onPressed: _issueStudent,
                  child: const Text('Generate student unlock QR'),
                ),
              ),
              const SizedBox(width: 8),
              FilledButton.tonalIcon(
                onPressed: () => _openScan(
                  title: 'Scan student Device ID',
                  hint: 'Scan the Device ID QR on the student phone',
                  onResult: (v) async {
                    setState(() => studentCtrl.text = v);
                    await _issueStudent();
                  },
                ),
                icon: const Icon(Icons.qr_code_scanner),
                label: const Text('Scan'),
              ),
            ],
          ),
          const SizedBox(height: 20),
          const Text('3) Wholesale to another seller',
              style: TextStyle(fontWeight: FontWeight.w900)),
          const SizedBox(height: 4),
          const Text(
            'Scan their seller Device ID QR, set quota, generate grant.',
            style: TextStyle(color: FourTheme.muted, fontSize: 13),
          ),
          const SizedBox(height: 6),
          TextField(
            controller: sellerCtrl,
            decoration: InputDecoration(
              border: const OutlineInputBorder(),
              hintText: 'Other seller Device ID',
              suffixIcon: IconButton(
                tooltip: 'Scan seller QR',
                icon: const Icon(Icons.qr_code_scanner),
                onPressed: () => _openScan(
                  title: 'Scan seller Device ID',
                  hint: 'Scan the other seller Device ID QR',
                  onResult: (v) => setState(() => sellerCtrl.text = v),
                ),
              ),
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
            child: const Text('Generate seller code QR'),
          ),
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
            SelectableText(lastCode!, style: const TextStyle(fontSize: 11)),
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
          ...store.history.take(12).map(
                (h) => ListTile(
                  dense: true,
                  title: Text('${h['type']} → ${h['target']}'),
                  subtitle: Text('${h['at']}'),
                ),
              ),
        ],
      ),
    );
  }
}
