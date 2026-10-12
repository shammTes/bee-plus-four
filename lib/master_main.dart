// Shamm Master: makes top-up codes for Bee Sellers. Each code is for ONE app: Four or Winner.
// Run: flutter run -t lib/master_main.dart   (see lib/master/master_grant.dart for the code format)
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:qr_flutter/qr_flutter.dart';

import 'master/master_grant.dart';

void main() => runApp(const ShammMasterApp());

class ShammMasterApp extends StatelessWidget {
  const ShammMasterApp({super.key});

  @override
  Widget build(BuildContext context) => MaterialApp(
        title: 'Shamm Master',
        debugShowCheckedModeBanner: false,
        theme: ThemeData(colorSchemeSeed: const Color(0xFF7C3AED), useMaterial3: true),
        home: const MasterHome(),
      );
}

class MasterHome extends StatefulWidget {
  const MasterHome({super.key});

  @override
  State<MasterHome> createState() => MasterHomeState();
}

class MasterHomeState extends State<MasterHome> {
  final sellerIdCtrl = TextEditingController();
  final creditCtrl = TextEditingController(text: '50');
  SellerApp app = SellerApp.four;
  String? code;
  String? status;
  final history = <String>[];

  @override
  void dispose() {
    sellerIdCtrl.dispose();
    creditCtrl.dispose();
    super.dispose();
  }

  void make() {
    final id = MasterGrant.findSellerId(sellerIdCtrl.text) ?? sellerIdCtrl.text.trim();
    final n = int.tryParse(creditCtrl.text.trim()) ?? 0;
    if (id.isEmpty) {
      setState(() => status = 'Type the Seller ID.');
      return;
    }
    if (n < 1 || n > MasterGrant.maxCredit) {
      setState(() => status = 'Type the credit: 1 to ${MasterGrant.maxCredit}.');
      return;
    }
    final c = MasterGrant.issue(sellerId: id, credit: n, app: app);
    setState(() {
      code = c;
      status = 'Code made: $n ${app.label} credit for $id.';
      history.insert(0, '${DateTime.now().toIso8601String().substring(0, 16)} · $n ${app.code} → $id');
    });
  }

  @override
  Widget build(BuildContext context) {
    final c = code;
    return Scaffold(
      appBar: AppBar(title: const Text('Shamm Master')),
      body: ListView(
        padding: const EdgeInsets.all(20),
        children: [
          const Text('Top-up code for a seller', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
          const SizedBox(height: 4),
          const Text('1. Choose the app. The code adds credit to this app only.'),
          const SizedBox(height: 8),
          SegmentedButton<SellerApp>(
            key: const Key('appChoice'),
            segments: [for (final a in SellerApp.values) ButtonSegment(value: a, label: Text(a.label))],
            selected: {app},
            onSelectionChanged: (s) => setState(() => app = s.first),
          ),
          const SizedBox(height: 16),
          const Text('2. Type the Seller ID (BEE-A… or BEE-W…).'),
          TextField(key: const Key('sellerId'), controller: sellerIdCtrl, decoration: const InputDecoration(labelText: 'Seller ID')),
          const SizedBox(height: 12),
          const Text('3. Type the credit (number of students).'),
          TextField(
            key: const Key('credit'),
            controller: creditCtrl,
            keyboardType: TextInputType.number,
            decoration: InputDecoration(labelText: 'Credit for ${app.label}'),
          ),
          const SizedBox(height: 16),
          FilledButton(key: const Key('make'), onPressed: make, child: Text('Make ${app.label} code')),
          if (status != null) Padding(padding: const EdgeInsets.only(top: 12), child: Text(status!, key: const Key('status'))),
          if (c != null) ...[
            const SizedBox(height: 16),
            Center(child: QrImageView(data: c, size: 240, backgroundColor: Colors.white)),
            const SizedBox(height: 8),
            SelectableText(c, key: const Key('code'), style: const TextStyle(fontFamily: 'monospace', fontSize: 12)),
            OutlinedButton.icon(
              onPressed: () {
                Clipboard.setData(ClipboardData(text: c));
                ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('Code copied.')));
              },
              icon: const Icon(Icons.copy),
              label: const Text('Copy code'),
            ),
            const Text('The seller opens Bee Seller, Add credit, and pastes or scans this code. It works one time.'),
          ],
          if (history.isNotEmpty) ...[
            const SizedBox(height: 20),
            const Text('Made today', style: TextStyle(fontWeight: FontWeight.w600)),
            for (final h in history.take(20)) Text(h, style: const TextStyle(fontSize: 12)),
          ],
        ],
      ),
    );
  }
}
