import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:hive_flutter/hive_flutter.dart';
import 'package:uuid/uuid.dart';

import 'core/licensing/qr_payload.dart';
import 'core/theme/four_theme.dart';

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await SystemChrome.setEnabledSystemUIMode(SystemUiMode.edgeToEdge);
  await Hive.initFlutter();
  runApp(const ShammMasterApp());
}

class ShammMasterApp extends StatelessWidget {
  const ShammMasterApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Shamm Master',
      debugShowCheckedModeBanner: false,
      theme: FourTheme.highschool,
      home: const MasterHome(),
    );
  }
}

class MasterHome extends StatefulWidget {
  const MasterHome({super.key});

  @override
  State<MasterHome> createState() => _MasterHomeState();
}

class _MasterHomeState extends State<MasterHome> {
  final _sellerIdCtrl = TextEditingController();
  final _quotaCtrl = TextEditingController(text: '50');
  String? _lastIssued;
  String? _status;
  final List<Map<String, dynamic>> _history = [];

  @override
  void dispose() {
    _sellerIdCtrl.dispose();
    _quotaCtrl.dispose();
    super.dispose();
  }

  void _generate() {
    final sellerId = _sellerIdCtrl.text.trim();
    final quota = int.tryParse(_quotaCtrl.text.trim()) ?? 0;
    if (sellerId.isEmpty || quota <= 0) {
      setState(() => _status = 'Seller Device ID እና quota ያስገቡ');
      return;
    }
    final nonce = const Uuid().v4().replaceAll('-', '').substring(0, 12);
    final payload = QrPayload.issueWholesale(
      sellerDeviceId: sellerId,
      quota: quota,
      nonce: nonce,
    );
    final encoded = payload.encode();
    setState(() {
      _lastIssued = encoded;
      _status = 'Wholesale ኮድ ተፈጥሯል · $quota unlocks';
      _history.insert(0, {
        'sellerId': sellerId,
        'quota': quota,
        'nonce': nonce,
        'code': encoded,
        'ts': DateTime.now().toIso8601String(),
      });
    });
  }

  void _copy(String text) {
    Clipboard.setData(ClipboardData(text: text));
    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(content: Text('ተቀድቷል / Copied')),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Container(
        decoration: const BoxDecoration(
          gradient: LinearGradient(
            begin: Alignment.topLeft,
            end: Alignment.bottomRight,
            colors: [Color(0xFF1A0A2E), Color(0xFF0D1B2A)],
          ),
        ),
        child: SafeArea(
          child: ListView(
            padding: const EdgeInsets.all(20),
            children: [
              Row(
                children: [
                  Container(
                    width: 52,
                    height: 52,
                    decoration: BoxDecoration(
                      color: const Color(0xFF7C3AED),
                      borderRadius: BorderRadius.circular(14),
                    ),
                    child: const Center(
                      child: Text(
                        'SM',
                        style: TextStyle(
                          color: Colors.white,
                          fontWeight: FontWeight.bold,
                          fontSize: 18,
                        ),
                      ),
                    ),
                  ),
                  const SizedBox(width: 14),
                  const Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          'Shamm Master',
                          style: TextStyle(
                            color: Colors.white,
                            fontSize: 22,
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                        Text(
                          'Wholesale codes for Bee Sellers',
                          style: TextStyle(color: Colors.white70, fontSize: 13),
                        ),
                      ],
                    ),
                  ),
                ],
              ),
              const SizedBox(height: 24),
              _glassCard(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.stretch,
                  children: [
                    const Text(
                      'Generate Wholesale Code',
                      style: TextStyle(
                        color: Colors.white,
                        fontWeight: FontWeight.w600,
                        fontSize: 16,
                      ),
                    ),
                    const SizedBox(height: 6),
                    const Text(
                      'Seller Device ID ን ያስገቡ · ኮታ ይምረጡ',
                      style: TextStyle(color: Colors.white54, fontSize: 12),
                    ),
                    const SizedBox(height: 14),
                    TextField(
                      controller: _sellerIdCtrl,
                      style: const TextStyle(color: Colors.white),
                      decoration: _inputDeco('Seller Device ID'),
                    ),
                    const SizedBox(height: 10),
                    TextField(
                      controller: _quotaCtrl,
                      style: const TextStyle(color: Colors.white),
                      keyboardType: TextInputType.number,
                      decoration: _inputDeco('Quota (number of student unlocks)'),
                    ),
                    const SizedBox(height: 14),
                    FilledButton(
                      onPressed: _generate,
                      style: FilledButton.styleFrom(
                        backgroundColor: const Color(0xFF7C3AED),
                        foregroundColor: Colors.white,
                        padding: const EdgeInsets.symmetric(vertical: 14),
                      ),
                      child: const Text('Generate WHOLESALE Code'),
                    ),
                  ],
                ),
              ),
              const SizedBox(height: 16),
              if (_lastIssued != null)
                _glassCard(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.stretch,
                    children: [
                      const Text(
                        'Issued Code (copy + give to Seller)',
                        style: TextStyle(
                          color: Colors.white,
                          fontWeight: FontWeight.w600,
                        ),
                      ),
                      const SizedBox(height: 8),
                      SelectableText(
                        _lastIssued!,
                        style: const TextStyle(
                          color: Color(0xFFC4B5FD),
                          fontSize: 12,
                          fontFamily: 'monospace',
                        ),
                      ),
                      const SizedBox(height: 12),
                      OutlinedButton.icon(
                        onPressed: () => _copy(_lastIssued!),
                        icon: const Icon(Icons.copy, size: 18),
                        label: const Text('Copy Code'),
                        style: OutlinedButton.styleFrom(
                          foregroundColor: Colors.white,
                          side: const BorderSide(color: Colors.white38),
                        ),
                      ),
                    ],
                  ),
                ),
              if (_status != null) ...[
                const SizedBox(height: 12),
                Text(
                  _status!,
                  style: const TextStyle(
                    color: Color(0xFFC4B5FD),
                    fontWeight: FontWeight.w500,
                  ),
                ),
              ],
              if (_history.isNotEmpty) ...[
                const SizedBox(height: 24),
                const Text(
                  'History',
                  style: TextStyle(color: Colors.white70, fontWeight: FontWeight.w600),
                ),
                const SizedBox(height: 8),
                ..._history.take(15).map((h) {
                  final ts = (h['ts'] as String?)?.substring(0, 16) ?? '';
                  return Padding(
                    padding: const EdgeInsets.only(bottom: 6),
                    child: Text(
                      '$ts · ${h['quota']} → ${h['sellerId']}',
                      style: const TextStyle(color: Colors.white38, fontSize: 12),
                      maxLines: 1,
                      overflow: TextOverflow.ellipsis,
                    ),
                  );
                }),
              ],
            ],
          ),
        ),
      ),
    );
  }

  Widget _glassCard({required Widget child}) {
    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: Colors.white.withOpacity(0.08),
        borderRadius: BorderRadius.circular(16),
        border: Border.all(color: Colors.white.withOpacity(0.12)),
      ),
      child: child,
    );
  }

  InputDecoration _inputDeco(String hint) {
    return InputDecoration(
      hintText: hint,
      hintStyle: const TextStyle(color: Colors.white38),
      filled: true,
      fillColor: Colors.white.withOpacity(0.06),
      border: OutlineInputBorder(
        borderRadius: BorderRadius.circular(12),
        borderSide: BorderSide.none,
      ),
      contentPadding: const EdgeInsets.symmetric(horizontal: 14, vertical: 12),
    );
  }
}
