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

  static const LinearGradient heroGradient = LinearGradient(
    begin: Alignment.topLeft,
    end: Alignment.bottomRight,
    colors: [Color(0xFF0E7490), Color(0xFF4F46E5), Color(0xFF7C3AED)],
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
        labelStyle: const TextStyle(fontWeight: FontWeight.w700, fontSize: 12),
        padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 2),
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
      ),
      navigationBarTheme: NavigationBarThemeData(
        backgroundColor: Colors.white.withOpacity(0.92),
        indicatorColor: primarySoft,
        labelTextStyle: WidgetStateProperty.resolveWith((s) {
          final selected = s.contains(WidgetState.selected);
          return TextStyle(
            fontSize: 11,
            fontWeight: selected ? FontWeight.w800 : FontWeight.w600,
            color: selected ? primaryDark : muted,
          );
        }),
        iconTheme: WidgetStateProperty.resolveWith((s) {
          final selected = s.contains(WidgetState.selected);
          return IconThemeData(
            color: selected ? primaryDark : muted,
            size: 24,
          );
        }),
        height: 68,
        elevation: 8,
        shadowColor: Colors.black26,
      ),
      filledButtonTheme: FilledButtonThemeData(
        style: FilledButton.styleFrom(
          backgroundColor: primaryDark,
          foregroundColor: Colors.white,
          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(14)),
          padding: const EdgeInsets.symmetric(horizontal: 18, vertical: 12),
          textStyle: const TextStyle(fontWeight: FontWeight.w800),
        ),
      ),
      inputDecorationTheme: InputDecorationTheme(
        filled: true,
        fillColor: Colors.white.withOpacity(0.9),
        border: OutlineInputBorder(
          borderRadius: BorderRadius.circular(16),
          borderSide: BorderSide.none,
        ),
        contentPadding: const EdgeInsets.symmetric(horizontal: 14, vertical: 12),
      ),
    );
  }

  static Widget glassPanel({
    required Widget child,
    EdgeInsetsGeometry padding = const EdgeInsets.all(14),
    BorderRadius? radius,
    Color? tint,
  }) {
    final r = radius ?? BorderRadius.circular(20);
    return ClipRRect(
      borderRadius: r,
      child: BackdropFilter(
        filter: ImageFilter.blur(sigmaX: 14, sigmaY: 14),
        child: Container(
          padding: padding,
          decoration: BoxDecoration(
            color: tint ?? glass,
            borderRadius: r,
            border: Border.all(color: Colors.white.withOpacity(0.55)),
            boxShadow: [
              BoxShadow(
                color: Colors.black.withOpacity(0.06),
                blurRadius: 18,
                offset: const Offset(0, 8),
              ),
            ],
          ),
          child: child,
        ),
      ),
    );
  }
}
