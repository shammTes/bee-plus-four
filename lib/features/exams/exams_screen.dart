import 'package:flutter/material.dart';
import 'package:webview_flutter/webview_flutter.dart';

import '../../core/theme/four_theme.dart';
import 'examprep_engine.dart';

/// Exact Warsay Prep preview — full-screen WebView, pack + Kokob tutor included.
class ExamsScreen extends StatefulWidget {
  const ExamsScreen({super.key});

  @override
  State<ExamsScreen> createState() => _ExamsScreenState();
}

class _ExamsScreenState extends State<ExamsScreen> {
  @override
  void initState() {
    super.initState();
    ExamPrepEngine.instance.preload();
  }

  @override
  Widget build(BuildContext context) {
    final engine = ExamPrepEngine.instance;
    return ColoredBox(
      color: FourTheme.bg,
      child: ValueListenableBuilder<bool>(
        valueListenable: engine.loading,
        builder: (context, loading, _) {
          if (engine.error != null && engine.controller == null) {
            return Center(
              child: Padding(
                padding: const EdgeInsets.all(24),
                child: Text(
                  'Warsay Prep failed to open.\n${engine.error}',
                  textAlign: TextAlign.center,
                  style: const TextStyle(color: FourTheme.ink, fontWeight: FontWeight.w700),
                ),
              ),
            );
          }
          return Stack(
            children: [
              if (engine.controller != null)
                WebViewWidget(controller: engine.controller!),
              if (loading)
                const ColoredBox(
                  color: FourTheme.bg,
                  child: Center(
                    child: Column(
                      mainAxisSize: MainAxisSize.min,
                      children: [
                        CircularProgressIndicator(color: FourTheme.coral),
                        SizedBox(height: 12),
                        Text('Opening Warsay Prep…',
                            style: TextStyle(
                                color: FourTheme.ink2, fontWeight: FontWeight.w800)),
                      ],
                    ),
                  ),
                ),
            ],
          );
        },
      ),
    );
  }
}
