import 'package:flutter/material.dart';
import '../../core/bot/offline_bot.dart';
import '../../core/models/content_models.dart';

class BotScreen extends StatefulWidget {
  const BotScreen({super.key});
  @override
  State<BotScreen> createState() => _BotScreenState();
}

class _BotScreenState extends State<BotScreen> {
  final bot = OfflineBot();
  final controller = TextEditingController();
  final scroll = ScrollController();
  final messages = <_ChatLine>[];
  List<QuickAction> quick = const [];
  PracticeQuestion? activeQ;
  bool busy = false;

  @override
  void initState() {
    super.initState();
    messages.add(_ChatLine(bot: true, text: 'Offline study coach (controlled responses only).\nHighschool G9–G12 · no internet.\nSay hi, pick a subject, or start a quiz.'));
    quick = const [QuickAction('Start quiz', BotAction.start), QuickAction('Subjects', BotAction.newTopic), QuickAction('Help', BotAction.help)];
  }

  @override
  void dispose() { controller.dispose(); scroll.dispose(); super.dispose(); }

  Future<void> _send(String text) async {
    if (text.trim().isEmpty || busy) return;
    setState(() { busy = true; messages.add(_ChatLine(bot: false, text: text.trim())); controller.clear(); });
    final reply = await bot.handle(text);
    if (!mounted) return;
    setState(() { messages.add(_ChatLine(bot: true, text: reply.text)); quick = reply.quick; activeQ = reply.question; busy = false; });
    await Future<void>.delayed(const Duration(milliseconds: 50));
    if (scroll.hasClients) scroll.animateTo(scroll.position.maxScrollExtent, duration: const Duration(milliseconds: 200), curve: Curves.easeOut);
  }

  Future<void> _quick(QuickAction a) async {
    if (a.action == BotAction.subject && a.value != null) { bot.activeSubject = a.value; await _send(a.value!); return; }
    const map = {
      BotAction.start: 'start quiz', BotAction.hint: 'hint', BotAction.explain: 'explain',
      BotAction.skip: 'skip', BotAction.progress: 'progress', BotAction.newTopic: 'change subject', BotAction.help: 'help',
    };
    await _send(map[a.action] ?? a.label);
  }

  Future<void> _pickOption(int i) async {
    if (busy) return;
    setState(() { busy = true; messages.add(_ChatLine(bot: false, text: String.fromCharCode(65 + i))); });
    final reply = await bot.answerIndex(i);
    if (!mounted) return;
    setState(() { messages.add(_ChatLine(bot: true, text: reply.text)); quick = reply.quick; activeQ = null; busy = false; });
  }

  @override
  Widget build(BuildContext context) {
    final cs = Theme.of(context).colorScheme;
    return Column(children: [
      Expanded(child: ListView.builder(
        controller: scroll, padding: const EdgeInsets.all(12), itemCount: messages.length,
        itemBuilder: (context, i) {
          final m = messages[i];
          return Align(
            alignment: m.bot ? Alignment.centerLeft : Alignment.centerRight,
            child: Container(
              margin: const EdgeInsets.symmetric(vertical: 4),
              padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 10),
              constraints: BoxConstraints(maxWidth: MediaQuery.of(context).size.width * 0.85),
              decoration: BoxDecoration(
                color: m.bot ? cs.primaryContainer.withValues(alpha: 0.55) : cs.primary,
                borderRadius: BorderRadius.circular(16),
              ),
              child: Text(m.text, style: TextStyle(color: m.bot ? cs.onSurface : cs.onPrimary)),
            ),
          );
        },
      )),
      if (activeQ != null) Padding(
        padding: const EdgeInsets.symmetric(horizontal: 8),
        child: Wrap(spacing: 6, children: List.generate(activeQ!.options.length, (i) =>
          ActionChip(label: Text(String.fromCharCode(65 + i)), onPressed: () => _pickOption(i)))),
      ),
      if (quick.isNotEmpty) SingleChildScrollView(
        scrollDirection: Axis.horizontal,
        padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 6),
        child: Row(children: quick.map((q) => Padding(
          padding: const EdgeInsets.only(right: 6),
          child: ActionChip(label: Text(q.label), onPressed: () => _quick(q)),
        )).toList()),
      ),
      SafeArea(child: Padding(
        padding: const EdgeInsets.fromLTRB(8, 0, 8, 8),
        child: Row(children: [
          Expanded(child: TextField(
            controller: controller,
            decoration: InputDecoration(hintText: 'Message study coach…',
              border: OutlineInputBorder(borderRadius: BorderRadius.circular(14)), isDense: true),
            onSubmitted: _send,
          )),
          const SizedBox(width: 8),
          FilledButton(onPressed: busy ? null : () => _send(controller.text), child: const Icon(Icons.send)),
        ]),
      )),
    ]);
  }
}

class _ChatLine {
  final bool bot; final String text;
  _ChatLine({required this.bot, required this.text});
}
