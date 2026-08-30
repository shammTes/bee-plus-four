import 'package:flutter/material.dart';

class FourTheme {
  static ThemeData highschool() {
    const bg = Color(0xFFF0FDFA);
    const teal = Color(0xFF0D9488);
    return ThemeData(
      useMaterial3: true,
      brightness: Brightness.light,
      colorScheme: ColorScheme.light(
        primary: teal,
        onPrimary: Colors.white,
        primaryContainer: const Color(0xFFCCFBF1),
        onPrimaryContainer: const Color(0xFF134E4A),
        secondary: const Color(0xFF0891B2),
        surface: Colors.white,
        onSurface: const Color(0xFF0F172A),
        surfaceContainerHighest: const Color(0xFFE0F2FE),
        onSurfaceVariant: const Color(0xFF475569),
        error: const Color(0xFFDC2626),
      ),
      scaffoldBackgroundColor: bg,
      appBarTheme: const AppBarTheme(backgroundColor: bg, foregroundColor: Color(0xFF134E4A), elevation: 0),
      cardTheme: CardThemeData(
        color: Colors.white,
        elevation: 2,
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(18)),
      ),
    );
  }
}
