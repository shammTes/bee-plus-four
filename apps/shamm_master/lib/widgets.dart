import 'package:flutter/material.dart';

const brand = Color(0xFF4F46E5);
const ink = Color(0xFF1F2937);
const soft = Color(0xFF6B7280);
const paper = Color(0xFFF6F7FB);

ThemeData buildTheme() {
  final scheme = ColorScheme.fromSeed(seedColor: brand, surface: Colors.white);
  final border = OutlineInputBorder(
    borderRadius: BorderRadius.circular(14),
    borderSide: const BorderSide(color: Color(0xFFD9DCE5)),
  );
  return ThemeData(
    useMaterial3: true,
    colorScheme: scheme,
    scaffoldBackgroundColor: paper,
    // No ink sparkle shader: cheaper on low-end GPUs.
    splashFactory: InkRipple.splashFactory,
    appBarTheme: const AppBarTheme(
      backgroundColor: paper,
      foregroundColor: ink,
      elevation: 0,
      scrolledUnderElevation: 0,
      centerTitle: false,
    ),
    inputDecorationTheme: InputDecorationTheme(
      filled: true,
      fillColor: Colors.white,
      border: border,
      enabledBorder: border,
      focusedBorder: border.copyWith(borderSide: const BorderSide(color: brand, width: 2)),
      contentPadding: const EdgeInsets.symmetric(horizontal: 14, vertical: 14),
    ),
    filledButtonTheme: FilledButtonThemeData(
      style: FilledButton.styleFrom(
        minimumSize: const Size.fromHeight(52),
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(14)),
        textStyle: const TextStyle(fontSize: 16, fontWeight: FontWeight.w600),
      ),
    ),
    outlinedButtonTheme: OutlinedButtonThemeData(
      style: OutlinedButton.styleFrom(
        minimumSize: const Size(48, 48),
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(14)),
      ),
    ),
    cardTheme: CardThemeData(
      color: Colors.white,
      elevation: 0,
      margin: EdgeInsets.zero,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(18),
        side: const BorderSide(color: Color(0xFFE6E8EF)),
      ),
    ),
    chipTheme: const ChipThemeData(showCheckmark: false),
  );
}

/// White card with a small step title.
class Section extends StatelessWidget {
  const Section({super.key, required this.title, required this.child, this.step});
  final String title;
  final Widget child;
  final int? step;

  @override
  Widget build(BuildContext context) => Card(
    child: Padding(
      padding: const EdgeInsets.all(16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              if (step != null) ...[
                CircleAvatar(
                  radius: 12,
                  backgroundColor: brand,
                  child: Text(
                    '$step',
                    style: const TextStyle(color: Colors.white, fontSize: 13, fontWeight: FontWeight.bold),
                  ),
                ),
                const SizedBox(width: 8),
              ],
              Expanded(
                child: Text(
                  title,
                  style: const TextStyle(fontSize: 16, fontWeight: FontWeight.w700, color: ink),
                ),
              ),
            ],
          ),
          const SizedBox(height: 12),
          child,
        ],
      ),
    ),
  );
}

/// Text field with a Clear (X) button. scrollPadding keeps it above the keyboard.
class ClearField extends StatefulWidget {
  const ClearField({
    super.key,
    required this.controller,
    required this.label,
    this.hint,
    this.keyboardType,
    this.onChanged,
    this.onSubmitted,
    this.prefixIcon,
    this.extra,
    this.maxLines = 1,
    this.textInputAction,
    this.fieldKey,
  });

  final TextEditingController controller;
  final String label;
  final String? hint;
  final TextInputType? keyboardType;
  final ValueChanged<String>? onChanged;
  final ValueChanged<String>? onSubmitted;
  final IconData? prefixIcon;

  /// Extra button before the X (for example Scan).
  final Widget? extra;
  final int maxLines;
  final TextInputAction? textInputAction;
  final Key? fieldKey;

  @override
  State<ClearField> createState() => _ClearFieldState();
}

class _ClearFieldState extends State<ClearField> {
  @override
  void initState() {
    super.initState();
    widget.controller.addListener(_changed);
  }

  @override
  void didUpdateWidget(ClearField old) {
    super.didUpdateWidget(old);
    if (old.controller != widget.controller) {
      old.controller.removeListener(_changed);
      widget.controller.addListener(_changed);
    }
  }

  @override
  void dispose() {
    widget.controller.removeListener(_changed);
    super.dispose();
  }

  bool _hadText = false;
  void _changed() {
    final has = widget.controller.text.isNotEmpty;
    if (has != _hadText) setState(() => _hadText = has);
  }

  @override
  Widget build(BuildContext context) {
    _hadText = widget.controller.text.isNotEmpty;
    return TextField(
      key: widget.fieldKey,
      controller: widget.controller,
      keyboardType: widget.keyboardType,
      maxLines: widget.maxLines,
      minLines: 1,
      textInputAction: widget.textInputAction,
      onChanged: widget.onChanged,
      onSubmitted: widget.onSubmitted,
      scrollPadding: const EdgeInsets.only(bottom: 160),
      decoration: InputDecoration(
        labelText: widget.label,
        hintText: widget.hint,
        prefixIcon: widget.prefixIcon == null ? null : Icon(widget.prefixIcon),
        suffixIcon: Row(
          mainAxisSize: MainAxisSize.min,
          children: [
            if (widget.extra != null) widget.extra!,
            if (_hadText)
              IconButton(
                tooltip: 'Clear',
                icon: const Icon(Icons.close),
                onPressed: () {
                  widget.controller.clear();
                  widget.onChanged?.call('');
                },
              ),
          ],
        ),
      ),
    );
  }
}

void toast(BuildContext context, String msg) {
  ScaffoldMessenger.of(context)
    ..hideCurrentSnackBar()
    ..showSnackBar(SnackBar(content: Text(msg), behavior: SnackBarBehavior.floating, duration: const Duration(seconds: 2)));
}
