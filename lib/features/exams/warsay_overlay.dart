import 'package:flutter/material.dart';
import 'package:webview_flutter/webview_flutter.dart';

import '../../core/theme/four_theme.dart';
import 'examprep_engine.dart';

enum WarsayStage { hidden, mini, open }

class WarsayOverlay extends StatelessWidget {
  const WarsayOverlay({
    super.key,
    required this.stage,
    required this.onStage,
  });

  final WarsayStage stage;
  final ValueChanged<WarsayStage> onStage;

  @override
  Widget build(BuildContext context) {
    final engine = ExamPrepEngine.instance;
    if (stage == WarsayStage.hidden) {
      return Positioned(
        right: 16,
        bottom: 8,
        child: Material(
          color: FourTheme.coral,
          elevation: 8,
          borderRadius: BorderRadius.circular(22),
          child: InkWell(
            onTap: () {
              engine.preload();
              onStage(WarsayStage.open);
            },
            borderRadius: BorderRadius.circular(22),
            child: const Padding(
              padding: EdgeInsets.symmetric(horizontal: 14, vertical: 12),
              child: Row(
                mainAxisSize: MainAxisSize.min,
                children: [
                  Icon(Icons.auto_awesome, color: Colors.white, size: 18),
                  SizedBox(width: 8),
                  Text('Warsay',
                      style: TextStyle(
                          color: Colors.white, fontWeight: FontWeight.w900)),
                ],
              ),
            ),
          ),
        ),
      );
    }

    final mini = stage == WarsayStage.mini;
    return Positioned(
      left: mini ? null : 12,
      right: 12,
      bottom: 8,
      top: mini ? null : 56,
      width: mini ? 148 : null,
      height: mini ? 196 : null,
      child: Material(
        color: FourTheme.surface,
        elevation: 16,
        shadowColor: FourTheme.tint.withValues(alpha: 0.4),
        borderRadius: BorderRadius.circular(24),
        clipBehavior: Clip.antiAlias,
        child: Column(
          children: [
            Container(
              height: 40,
              color: FourTheme.ink,
              padding: const EdgeInsets.symmetric(horizontal: 8),
              child: Row(
                children: [
                  const Icon(Icons.auto_awesome,
                      color: Color(0xFFFFC9A3), size: 16),
                  const SizedBox(width: 6),
                  const Expanded(
                    child: Text(
                      'Warsay Prep',
                      maxLines: 1,
                      overflow: TextOverflow.ellipsis,
                      style: TextStyle(
                        color: Colors.white,
                        fontWeight: FontWeight.w900,
                        fontSize: 13,
                      ),
                    ),
                  ),
                  IconButton(
                    padding: EdgeInsets.zero,
                    constraints: const BoxConstraints.tightFor(
                        width: 32, height: 32),
                    icon: Icon(
                      mini ? Icons.open_in_full : Icons.photo_size_select_small,
                      color: Colors.white,
                      size: 18,
                    ),
                    onPressed: () => onStage(
                      mini ? WarsayStage.open : WarsayStage.mini,
                    ),
                  ),
                  IconButton(
                    padding: EdgeInsets.zero,
                    constraints: const BoxConstraints.tightFor(
                        width: 32, height: 32),
                    icon: const Icon(Icons.close, color: Colors.white, size: 18),
                    onPressed: () => onStage(WarsayStage.hidden),
                  ),
                ],
              ),
            ),
            Expanded(
              child: engine.controller == null
                  ? const ColoredBox(
                      color: FourTheme.bg,
                      child: Center(
                        child: CircularProgressIndicator(color: FourTheme.coral),
                      ),
                    )
                  : WebViewWidget(controller: engine.controller!),
            ),
          ],
        ),
      ),
    );
  }
}
