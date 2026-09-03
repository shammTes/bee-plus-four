import 'package:flutter/material.dart';

import '../../core/bot/offline_bot.dart';
import '../../core/models/content_models.dart';
import '../../core/theme/four_theme.dart';

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
    messages.add(const _ChatLine(
      bot: true,
      text:
          'Study Coach — offline only.\nG9–G12 · quizzes · exam practice.\n\nPick a subject or tap Start quiz.',
    ));
    quick = const [
      QuickAction('Start quiz', BotAction.start),
      QuickAction('Subjects', BotAction.newTopic),
      QuickAction('Help', BotAction.help),
    ];
  }

  @override
  void dispose() {
    controller.dispose();
    scroll.dispose();
    super.dispose();
  }

  Future<void> _send(String text) async {
    if (text.trim().isEmpty || busy) return;
    setState(() {
      busy = true;
      messages.add(_ChatLine(bot: false, text: text.trim()));
      controller.clear();
    });
    BotReply reply;
    try {
      reply = await bot.handle(text);
    } catch (e) {
      reply = BotReply(
        'Coach error. Try Help or Start quiz.\n($e)',
        quick: const [
          QuickAction('Start quiz', BotAction.start),
          QuickAction('Help', BotAction.help),
        ],
      );
    }
    if (!mounted) return;
    setState(() {
      messages.add(_ChatLine(bot: true, text: reply.text));
      quick = reply.quick;
      activeQ = reply.question;
      busy = false;
    });
    await Future<void>.delayed(const Duration(milliseconds: 40));
    if (scroll.hasClients) {
      scroll.animateTo(
        scroll.position.maxScrollExtent + 80,
        duration: const Duration(milliseconds: 220),
        curve: Curves.easeOut,
      );
    }
  }

  Future<void> _quick(QuickAction a) async {
    if (a.action == BotAction.subject && a.value != null) {
      bot.activeSubject = a.value;
      await _send(a.value!);
      return;
    }
    const map = {
      BotAction.start: 'start quiz',
      BotAction.hint: 'hint',
      BotAction.explain: 'explain',
      BotAction.skip: 'skip',
      BotAction.progress: 'progress',
      BotAction.newTopic: 'change subject',
      BotAction.help: 'help',
    };
    await _send(map[a.action] ?? a.label);
  }

  Future<void> _pickOption(int i) async {
    if (busy || activeQ == null) return;
    setState(() {
      busy = true;
      messages.add(_ChatLine(bot: false, text: String.fromCharCode(65 + i)));
    });
    BotReply reply;
    try {
      reply = await bot.answerIndex(i);
    } catch (e) {
      reply = BotReply('Could not grade. Try Next.\n($e)');
    }
    if (!mounted) return;
    setState(() {
      messages.add(_ChatLine(bot: true, text: reply.text));
      quick = reply.quick.isEmpty
          ? const [
              QuickAction('Next', BotAction.start),
              QuickAction('Subjects', BotAction.newTopic),
            ]
          : reply.quick;
      activeQ = null;
      busy = false;
    });
  }

  @override
  Widget build(BuildContext context) {
    final top = MediaQuery.paddingOf(context).top;
    return Container(
      decoration: const BoxDecoration(
        gradient: LinearGradient(
          begin: Alignment.topCenter,
          end: Alignment.bottomCenter,
          colors: [Color(0xFFE0F2FE), Color(0xFFF5F3FF), Color(0xFFF0F9FF)],
        ),
      ),
      child: Column(
        children: [
          Container(
            width: double.infinity,
            padding: EdgeInsets.fromLTRB(16, top + 10, 16, 14),
            decoration: const BoxDecoration(
              gradient: FourTheme.heroGradient,
              borderRadius: BorderRadius.only(
                bottomLeft: Radius.circular(24),
                bottomRight: Radius.circular(24),
              ),
            ),
            child: const Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text('Coach',
                    style: TextStyle(
                        color: Colors.white,
                        fontSize: 22,
                        fontWeight: FontWeight.w800)),
                SizedBox(height: 2),
                Text('Offline · quiz · tips',
                    style: TextStyle(color: Color(0xFFCCFBF1), fontSize: 13)),
              ],
            ),
          ),
          Expanded(
            child: ListView.builder(
              controller: scroll,
              padding: const EdgeInsets.fromLTRB(12, 12, 12, 8),
              itemCount: messages.length + (busy ? 1 : 0),
              itemBuilder: (context, i) {
                if (busy && i == messages.length) {
                  return const Padding(
                    padding: EdgeInsets.all(12),
                    child: Text('Thinking…', style: TextStyle(color: FourTheme.muted)),
                  );
                }
                final m = messages[i];
                return Align(
                  alignment: m.bot ? Alignment.centerLeft : Alignment.centerRight,
                  child: Container(
                    margin: const EdgeInsets.symmetric(vertical: 5),
                    padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 11),
                    constraints: BoxConstraints(
                      maxWidth: MediaQuery.of(context).size.width * 0.86,
                    ),
                    decoration: BoxDecoration(
                      gradient: m.bot ? null : FourTheme.cardGradient,
                      color: m.bot ? Colors.white.withOpacity(0.9) : null,
                      borderRadius: BorderRadius.only(
                        topLeft: const Radius.circular(18),
                        topRight: const Radius.circular(18),
                        bottomLeft: Radius.circular(m.bot ? 4 : 18),
                        bottomRight: Radius.circular(m.bot ? 18 : 4),
                      ),
                      border: m.bot ? Border.all(color: Colors.white) : null,
                      boxShadow: [
                        BoxShadow(
                          color: Colors.black.withOpacity(0.06),
                          blurRadius: 12,
                          offset: const Offset(0, 4),
                        ),
                      ],
                    ),
                    child: Text(
                      m.text,
                      style: TextStyle(
                        color: m.bot ? FourTheme.ink : Colors.white,
                        height: 1.35,
                        fontWeight: m.bot ? FontWeight.w500 : FontWeight.w600,
                      ),
                    ),
                  ),
                );
              },
            ),
          ),
          if (activeQ != null)
            Padding(
              padding: const EdgeInsets.fromLTRB(12, 0, 12, 6),
              child: FourTheme.glassPanel(
                padding: const EdgeInsets.all(10),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(activeQ!.prompt,
                        style: const TextStyle(
                            fontWeight: FontWeight.w700, fontSize: 13)),
                    const SizedBox(height: 8),
                    Wrap(
                      spacing: 6,
                      runSpacing: 6,
                      children: List.generate(activeQ!.options.length, (i) {
                        return ActionChip(
                          label: Text(
                            '${String.fromCharCode(65 + i)}. ${activeQ!.options[i]}',
                            style: const TextStyle(fontSize: 12),
                          ),
                          onPressed: busy ? null : () => _pickOption(i),
                          backgroundColor: FourTheme.primarySoft,
                        );
                      }),
                    ),
                  ],
                ),
              ),
            ),
          if (quick.isNotEmpty)
            SingleChildScrollView(
              scrollDirection: Axis.horizontal,
              padding: const EdgeInsets.fromLTRB(10, 0, 10, 6),
              child: Row(
                children: quick
                    .map((q) => Padding(
                          padding: const EdgeInsets.only(right: 6),
                          child: ActionChip(
                            label: Text(q.label,
                                style: const TextStyle(
                                    fontWeight: FontWeight.w700, fontSize: 12)),
                            onPressed: busy ? null : () => _quick(q),
                            backgroundColor: Colors.white,
                          ),
                        ))
                    .toList(),
              ),
            ),
          SafeArea(
            top: false,
            child: Padding(
              padding: const EdgeInsets.fromLTRB(10, 0, 10, 10),
              child: FourTheme.glassPanel(
                padding: const EdgeInsets.fromLTRB(8, 6, 6, 6),
                child: Row(
                  children: [
                    Expanded(
                      child: TextField(
                        controller: controller,
                        decoration: const InputDecoration(
                          hintText: 'Ask coach…',
                          border: InputBorder.none,
                          isDense: true,
                        ),
                        onSubmitted: _send,
                      ),
                    ),
                    FilledButton(
                      onPressed: busy ? null : () => _send(controller.text),
                      style: FilledButton.styleFrom(
                        shape: const CircleBorder(),
                        padding: const EdgeInsets.all(12),
                      ),
                      child: const Icon(Icons.send_rounded, size: 20),
                    ),
                  ],
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }
}

class _ChatLine {
  final bool bot;
  final String text;
  const _ChatLine({required this.bot, required this.text});
}
