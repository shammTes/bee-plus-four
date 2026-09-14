import 'package:flutter/material.dart';

import '../../core/models/content_models.dart';
import '../../core/progress/mastery_store.dart';
import '../../core/theme/four_theme.dart';

/// Scrollable list of questions → open one → answer → back to list.
class PracticeListSession extends StatefulWidget {
  const PracticeListSession({
    super.key,
    required this.title,
    required this.grade,
    required this.subject,
    required this.unitNumber,
    required this.pool,
  });

  final String title;
  final String grade;
  final String subject;
  final int unitNumber;
  final List<PracticeQuestion> pool;

  @override
  State<PracticeListSession> createState() => _PracticeListSessionState();
}

class _PracticeListSessionState extends State<PracticeListSession> {
  PracticeQuestion? open;
  int? selected;
  bool revealed = false;
  final Set<String> done = {};
  final Set<String> correctIds = {};

  @override
  Widget build(BuildContext context) {
    final dark = Theme.of(context).brightness == Brightness.dark;

    if (open != null) {
      final q = open!;
      return Scaffold(
        appBar: AppBar(
          leading: IconButton(
            icon: const Icon(Icons.arrow_back),
            onPressed: () => setState(() {
              open = null;
              selected = null;
              revealed = false;
            }),
          ),
          title: Text(widget.title,
              style: const TextStyle(fontWeight: FontWeight.w800)),
        ),
        body: ListView(
          padding: const EdgeInsets.all(16),
          children: [
            Text(q.prompt,
                style: const TextStyle(
                    fontSize: 16, fontWeight: FontWeight.w700, height: 1.4)),
            const SizedBox(height: 14),
            ...List.generate(q.options.length, (i) {
              final isSel = selected == i;
              final isCorrect = revealed && i == q.correctIndex;
              final isWrong = revealed && isSel && i != q.correctIndex;
              Color border =
                  dark ? FourTheme.darkBorder : const Color(0xFFE2E8F0);
              Color bg = dark ? FourTheme.darkCard : Colors.white;
              if (isCorrect) {
                border = const Color(0xFF10B981);
                bg = dark
                    ? const Color(0xFF064E3B)
                    : const Color(0xFFECFDF5);
              } else if (isWrong) {
                border = const Color(0xFFEF4444);
                bg = dark
                    ? const Color(0xFF7F1D1D)
                    : const Color(0xFFFEF2F2);
              } else if (isSel) {
                border = FourTheme.violet;
              }
              return Padding(
                padding: const EdgeInsets.only(bottom: 8),
                child: Material(
                  color: bg,
                  borderRadius: BorderRadius.circular(14),
                  child: InkWell(
                    borderRadius: BorderRadius.circular(14),
                    onTap: revealed ? null : () => setState(() => selected = i),
                    child: Container(
                      padding: const EdgeInsets.all(14),
                      decoration: BoxDecoration(
                        borderRadius: BorderRadius.circular(14),
                        border: Border.all(color: border, width: 1.5),
                      ),
                      child: Text(
                        '${String.fromCharCode(65 + i)}. ${q.options[i]}',
                        style: const TextStyle(fontWeight: FontWeight.w600),
                      ),
                    ),
                  ),
                ),
              );
            }),
            const SizedBox(height: 12),
            if (!revealed)
              FilledButton(
                onPressed: selected == null
                    ? null
                    : () async {
                        setState(() => revealed = true);
                        final ok = selected == q.correctIndex;
                        done.add(q.id);
                        if (ok) correctIds.add(q.id);
                        await MasteryStore.instance.record(
                          widget.grade,
                          widget.subject,
                          widget.unitNumber == 0 ? 1 : widget.unitNumber,
                          correct: ok,
                        );
                      },
                child: const Text('Check answer'),
              )
            else ...[
              if (q.explanation.isNotEmpty)
                Padding(
                  padding: const EdgeInsets.only(bottom: 12),
                  child: Text(q.explanation, style: const TextStyle(height: 1.4)),
                ),
              FilledButton(
                onPressed: () => setState(() {
                  open = null;
                  selected = null;
                  revealed = false;
                }),
                child: const Text('Back to list'),
              ),
            ],
          ],
        ),
      );
    }

    return Scaffold(
      appBar: AppBar(
        title: Text(widget.title,
            style: const TextStyle(fontWeight: FontWeight.w800)),
      ),
      body: widget.pool.isEmpty
          ? const Center(child: Text('No questions in this set.'))
          : Column(
              children: [
                Padding(
                  padding: const EdgeInsets.fromLTRB(16, 12, 16, 4),
                  child: Text(
                    '${widget.pool.length} questions · ${done.length} tried · ${correctIds.length} correct',
                    style: TextStyle(
                      fontWeight: FontWeight.w700,
                      color: dark ? FourTheme.darkMuted : FourTheme.muted,
                    ),
                  ),
                ),
                Expanded(
                  child: ListView.builder(
                    padding: const EdgeInsets.all(12),
                    itemCount: widget.pool.length,
                    itemBuilder: (ctx, i) {
                      final q = widget.pool[i];
                      final tried = done.contains(q.id);
                      final ok = correctIds.contains(q.id);
                      return Card(
                        margin: const EdgeInsets.only(bottom: 8),
                        child: ListTile(
                          leading: CircleAvatar(
                            backgroundColor: tried
                                ? (ok
                                    ? const Color(0xFF10B981)
                                    : const Color(0xFFEF4444))
                                : (dark
                                    ? FourTheme.darkBorder
                                    : const Color(0xFFE2E8F0)),
                            foregroundColor: tried
                                ? Colors.white
                                : (dark
                                    ? FourTheme.darkText
                                    : FourTheme.ink),
                            child: Text('${i + 1}',
                                style: const TextStyle(
                                    fontWeight: FontWeight.w900,
                                    fontSize: 13)),
                          ),
                          title: Text(
                            q.prompt,
                            maxLines: 2,
                            overflow: TextOverflow.ellipsis,
                            style:
                                const TextStyle(fontWeight: FontWeight.w600),
                          ),
                          subtitle: Text(
                            '${q.options.length} options',
                            style: const TextStyle(fontSize: 11),
                          ),
                          trailing: const Icon(Icons.chevron_right),
                          onTap: () => setState(() {
                            open = q;
                            selected = null;
                            revealed = false;
                          }),
                        ),
                      );
                    },
                  ),
                ),
              ],
            ),
    );
  }
}
