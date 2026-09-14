import 'dart:ui';

import 'package:flutter/material.dart';

/// High-contrast glass theme for BEE PLUS 4 (highschool).
class FourTheme {
  FourTheme._();

  static const Color primary = Color(0xFF06B6D4);
  static const Color primaryDark = Color(0xFF0891B2);
  static const Color primarySoft = Color(0xFFCFFAFE);
  static const Color accent = Color(0xFFFBBF24);
  static const Color accentDeep = Color(0xFFF59E0B);
  static const Color violet = Color(0xFF8B5CF6);
  static const Color rose = Color(0xFFF43F5E);
  static const Color mint = Color(0xFF34D399);

  static const Color ink = Color(0xFF0F172A);
  static const Color inkSoft = Color(0xFF1E293B);
  static const Color muted = Color(0xFF64748B);
  static const Color surface = Color(0xFFF0F9FF);
  static const Color surfaceAlt = Color(0xFFE0F2FE);
  static const Color glass = Color(0xCCFFFFFF);
  static const Color glassDark = Color(0x990F172A);

  // Modern dark palette (not muddy gray)
  static const Color darkBg = Color(0xFF0B1220);
  static const Color darkSurface = Color(0xFF111827);
  static const Color darkCard = Color(0xFF1A2332);
  static const Color darkBorder = Color(0xFF2A3648);
  static const Color darkText = Color(0xFFF1F5F9);
  static const Color darkMuted = Color(0xFF94A3B8);
  static const Color darkCyan = Color(0xFF22D3EE);
  static const Color darkViolet = Color(0xFFA78BFA);
  static const Color darkAmber = Color(0xFFFBBF24);

  static const LinearGradient heroGradient = LinearGradient(
    begin: Alignment.topLeft,
    end: Alignment.bottomRight,
    colors: [Color(0xFF0E7490), Color(0xFF4F46E5), Color(0xFF7C3AED)],
  );

  static const LinearGradient heroGradientDark = LinearGradient(
    begin: Alignment.topLeft,
    end: Alignment.bottomRight,
    colors: [Color(0xFF083344), Color(0xFF312E81), Color(0xFF4C1D95)],
  );

  static const LinearGradient cardGradient = LinearGradient(
    begin: Alignment.topLeft,
    end: Alignment.bottomRight,
    colors: [Color(0xFF06B6D4), Color(0xFF6366F1)],
  );

  static ThemeData get highschool {
    final base = ThemeData(
      useMaterial3: true,
      brightness: Brightness.light,
      colorScheme: ColorScheme.fromSeed(
        seedColor: primary,
        primary: primaryDark,
        secondary: accentDeep,
        tertiary: violet,
        surface: surface,
        error: rose,
        brightness: Brightness.light,
      ),
      scaffoldBackgroundColor: surface,
    );
    return base.copyWith(
      appBarTheme: const AppBarTheme(
        backgroundColor: Colors.transparent,
        foregroundColor: ink,
        elevation: 0,
        centerTitle: false,
        titleTextStyle: TextStyle(
          color: ink,
          fontSize: 18,
          fontWeight: FontWeight.w800,
        ),
      ),
      cardTheme: CardThemeData(
        color: glass,
        elevation: 0,
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(20)),
        margin: EdgeInsets.zero,
      ),
      chipTheme: base.chipTheme.copyWith(
        labelStyle: const TextStyle(
          fontWeight: FontWeight.w700,
          fontSize: 12,
          color: Color(0xFF0F172A),
        ),
        padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 2),
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(20)),
        side: const BorderSide(color: Color(0xFFE2E8F0)),
        selectedColor: const Color(0xFFFBBF24),
        backgroundColor: Colors.white,
      ),
      navigationBarTheme: NavigationBarThemeData(
        backgroundColor: Colors.white.withOpacity(0.92),
        indicatorColor: primarySoft,
        labelTextStyle: WidgetStateProperty.resolveWith((s) {
          final selected = s.contains(WidgetState.selected);
          return TextStyle(
            fontSize: 11,
            fontWeight: FontWeight.w800,
            color: selected ? primaryDark : muted,
          );
        }),
        iconTheme: WidgetStateProperty.resolveWith((s) {
          final selected = s.contains(WidgetState.selected);
          return IconThemeData(
            color: selected ? primaryDark : muted,
          );
        }),
      ),
      filledButtonTheme: FilledButtonThemeData(
        style: FilledButton.styleFrom(
          backgroundColor: primaryDark,
          foregroundColor: Colors.white,
          shape:
              RoundedRectangleBorder(borderRadius: BorderRadius.circular(14)),
          padding: const EdgeInsets.symmetric(horizontal: 18, vertical: 14),
          textStyle: const TextStyle(fontWeight: FontWeight.w800),
        ),
      ),
    );
  }

  /// Modern dark — deep navy + cyan/violet accents (not flat gray).
  static ThemeData get highschoolDark {
    final base = ThemeData(
      useMaterial3: true,
      brightness: Brightness.dark,
      colorScheme: const ColorScheme.dark(
        primary: darkCyan,
        onPrimary: Color(0xFF083344),
        secondary: darkAmber,
        onSecondary: Color(0xFF0F172A),
        tertiary: darkViolet,
        surface: darkSurface,
        onSurface: darkText,
        error: Color(0xFFFB7185),
        outline: darkBorder,
      ),
      scaffoldBackgroundColor: darkBg,
    );
    return base.copyWith(
      appBarTheme: const AppBarTheme(
        backgroundColor: Colors.transparent,
        foregroundColor: darkText,
        elevation: 0,
        centerTitle: false,
        titleTextStyle: TextStyle(
          color: darkText,
          fontSize: 18,
          fontWeight: FontWeight.w800,
        ),
      ),
      cardTheme: CardThemeData(
        color: darkCard,
        elevation: 0,
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(20),
          side: const BorderSide(color: darkBorder),
        ),
        margin: EdgeInsets.zero,
      ),
      chipTheme: base.chipTheme.copyWith(
        labelStyle: const TextStyle(
          fontWeight: FontWeight.w800,
          fontSize: 12,
          color: darkText,
        ),
        padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 2),
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(20)),
        side: const BorderSide(color: darkBorder),
        selectedColor: const Color(0xFF155E75),
        backgroundColor: darkCard,
        checkmarkColor: darkCyan,
      ),
      navigationBarTheme: NavigationBarThemeData(
        backgroundColor: const Color(0xEE0B1220),
        indicatorColor: const Color(0xFF164E63),
        labelTextStyle: WidgetStateProperty.resolveWith((s) {
          final selected = s.contains(WidgetState.selected);
          return TextStyle(
            fontSize: 11,
            fontWeight: FontWeight.w800,
            color: selected ? darkCyan : darkMuted,
          );
        }),
        iconTheme: WidgetStateProperty.resolveWith((s) {
          final selected = s.contains(WidgetState.selected);
          return IconThemeData(
            color: selected ? darkCyan : darkMuted,
          );
        }),
      ),
      filledButtonTheme: FilledButtonThemeData(
        style: FilledButton.styleFrom(
          backgroundColor: darkCyan,
          foregroundColor: const Color(0xFF083344),
          shape:
              RoundedRectangleBorder(borderRadius: BorderRadius.circular(14)),
          padding: const EdgeInsets.symmetric(horizontal: 18, vertical: 14),
          textStyle: const TextStyle(fontWeight: FontWeight.w900),
        ),
      ),
      dialogTheme: DialogThemeData(
        backgroundColor: darkCard,
        titleTextStyle: const TextStyle(
          color: darkText,
          fontWeight: FontWeight.w900,
          fontSize: 18,
        ),
      ),
      switchTheme: SwitchThemeData(
        thumbColor: WidgetStateProperty.resolveWith(
            (s) => s.contains(WidgetState.selected) ? darkCyan : darkMuted),
        trackColor: WidgetStateProperty.resolveWith((s) =>
            s.contains(WidgetState.selected)
                ? const Color(0xFF155E75)
                : darkBorder),
      ),
      dividerColor: darkBorder,
      listTileTheme: const ListTileThemeData(
        textColor: darkText,
        iconColor: darkCyan,
      ),
    );
  }

  static Widget glassPanel({
    required Widget child,
    EdgeInsetsGeometry padding = const EdgeInsets.all(14),
    bool dark = false,
  }) {
    return ClipRRect(
      borderRadius: BorderRadius.circular(18),
      child: BackdropFilter(
        filter: ImageFilter.blur(sigmaX: 12, sigmaY: 12),
        child: Container(
          padding: padding,
          decoration: BoxDecoration(
            color: dark ? const Color(0x661A2332) : glass,
            borderRadius: BorderRadius.circular(18),
            border: Border.all(
              color: dark ? darkBorder : const Color(0x66FFFFFF),
            ),
          ),
          child: child,
        ),
      ),
    );
  }
}
