import 'package:flutter/material.dart';

/// Examprep clay design — used everywhere in 4.
class FourTheme {
  FourTheme._();

  static const Color bg = Color(0xFFF7F0E5);
  static const Color surface = Color(0xFFFFFAF2);
  static const Color surface2 = Color(0xFFF3EADC);
  static const Color ink = Color(0xFF3E3129);
  static const Color ink2 = Color(0xFF6F6055);
  static const Color ink3 = Color(0xFFA3938A);
  static const Color line = Color(0x1A785A3C);
  static const Color coral = Color(0xFFEE7B5F);
  static const Color coralTop = Color(0xFFF59A7F);
  static const Color tint = Color(0xFF785537);

  static const Color sageTile = Color(0xFFDCEBD5);
  static const Color sageMid = Color(0xFFA9CBA4);
  static const Color sageDeep = Color(0xFF5B8C63);
  static const Color peachTile = Color(0xFFFADAD0);
  static const Color peachMid = Color(0xFFF4A58E);
  static const Color peachDeep = Color(0xFFD56A50);
  static const Color butterTile = Color(0xFFFBEBC1);
  static const Color butterMid = Color(0xFFF5D27A);
  static const Color butterDeep = Color(0xFFB08316);
  static const Color blueTile = Color(0xFFDCE7F2);
  static const Color blueMid = Color(0xFFA8C4E0);
  static const Color blueDeep = Color(0xFF4F7BA6);
  static const Color lilacTile = Color(0xFFE8DFF4);
  static const Color lilacMid = Color(0xFFC6B3E3);
  static const Color lilacDeep = Color(0xFF8466B5);
  static const Color roseTile = Color(0xFFF8DCE3);
  static const Color roseMid = Color(0xFFEDAFBF);
  static const Color roseDeep = Color(0xFFBD5577);
  static const Color mintTile = Color(0xFFD5EEE9);
  static const Color mintMid = Color(0xFF9FD6CB);
  static const Color mintDeep = Color(0xFF3C8C7D);

  static const Color primary = sageDeep;
  static const Color primaryDark = sageDeep;
  static const Color primarySoft = sageTile;
  static const Color accent = butterMid;
  static const Color accentDeep = butterDeep;
  static const Color violet = lilacDeep;
  static const Color rose = peachDeep;
  static const Color mint = mintDeep;
  static const Color inkSoft = ink2;
  static const Color muted = ink2;
  static const Color surfaceAlt = surface2;
  static const Color glass = surface;
  static const Color glassDark = Color(0x99211C18);
  static const Color darkBg = Color(0xFF211C18);
  static const Color darkSurface = Color(0xFF2C2621);
  static const Color darkCard = Color(0xFF362F29);
  static const Color darkBorder = Color(0x12FFEBD2);
  static const Color darkText = Color(0xFFF4EADC);
  static const Color darkMuted = Color(0xFFCDBFB0);
  static const Color darkCyan = mintMid;
  static const Color darkViolet = lilacMid;
  static const Color darkAmber = butterMid;

  static const LinearGradient heroGradient = LinearGradient(
    begin: Alignment.topCenter,
    end: Alignment.bottomCenter,
    colors: [coralTop, coral],
  );
  static const LinearGradient heroGradientDark = LinearGradient(
    begin: Alignment.topLeft,
    end: Alignment.bottomRight,
    colors: [Color(0xFF4B3530), Color(0xFF3E3549)],
  );
  static const LinearGradient cardGradient = LinearGradient(
    begin: Alignment.topLeft,
    end: Alignment.bottomRight,
    colors: [sageTile, mintTile],
  );
  static const LinearGradient ctaGradient = LinearGradient(
    begin: Alignment.topCenter,
    end: Alignment.bottomCenter,
    colors: [coralTop, coral],
  );

  static List<BoxShadow> clay({bool small = false}) => small
      ? [
          BoxShadow(
            color: tint.withOpacity(0.30),
            offset: const Offset(0, 6),
            blurRadius: 12,
            spreadRadius: -6,
          ),
        ]
      : [
          BoxShadow(
            color: tint.withOpacity(0.28),
            offset: const Offset(0, 12),
            blurRadius: 24,
            spreadRadius: -10,
          ),
          BoxShadow(
            color: tint.withOpacity(0.10),
            offset: const Offset(0, 3),
            blurRadius: 7,
            spreadRadius: -2,
          ),
        ];

  static Color subjectTile(String subject) {
    switch (subject.toUpperCase()) {
      case 'BIOLOGY':
        return sageTile;
      case 'BUSINESS_ECONOMICS':
      case 'BUSINESS':
      case 'SOCIAL_STUDIES':
        return peachTile;
      case 'HISTORY':
      case 'AGRICULTURE':
      case 'GENERAL_KNOWLEDGE':
        return butterTile;
      case 'GEOGRAPHY':
      case 'MATH':
      case 'MATHEMATICS':
        return blueTile;
      case 'CHEMISTRY':
        return lilacTile;
      case 'ENGLISH':
        return roseTile;
      case 'PHYSICS':
      case 'ICT':
      case 'GENERAL_SCIENCE':
        return mintTile;
      default:
        return surface2;
    }
  }

  static Color subjectDeep(String subject) {
    switch (subject.toUpperCase()) {
      case 'BIOLOGY':
        return sageDeep;
      case 'BUSINESS_ECONOMICS':
      case 'BUSINESS':
      case 'SOCIAL_STUDIES':
        return peachDeep;
      case 'HISTORY':
      case 'AGRICULTURE':
      case 'GENERAL_KNOWLEDGE':
        return butterDeep;
      case 'GEOGRAPHY':
      case 'MATH':
      case 'MATHEMATICS':
        return blueDeep;
      case 'CHEMISTRY':
        return lilacDeep;
      case 'ENGLISH':
        return roseDeep;
      case 'PHYSICS':
      case 'ICT':
      case 'GENERAL_SCIENCE':
        return mintDeep;
      default:
        return ink;
    }
  }

  static ThemeData get highschool {
    const text = TextTheme(
      titleLarge: TextStyle(
          fontSize: 20, fontWeight: FontWeight.w900, color: ink, height: 1.2),
      titleMedium: TextStyle(
          fontSize: 16.5, fontWeight: FontWeight.w900, color: ink),
      bodyLarge: TextStyle(
          fontSize: 15.5, fontWeight: FontWeight.w700, color: ink, height: 1.55),
      bodyMedium: TextStyle(
          fontSize: 14, fontWeight: FontWeight.w600, color: ink2, height: 1.55),
      labelLarge: TextStyle(
          fontSize: 13, fontWeight: FontWeight.w800, color: ink),
    );
    final base = ThemeData(
      useMaterial3: true,
      brightness: Brightness.light,
      fontFamily: 'Nunito',
      fontFamilyFallback: const ['NotoSansEthiopic', 'NotoSans'],
      textTheme: text,
      primaryTextTheme: text,
      colorScheme: const ColorScheme.light(
        primary: sageDeep,
        onPrimary: Colors.white,
        secondary: coral,
        onSecondary: Colors.white,
        tertiary: lilacDeep,
        surface: surface,
        onSurface: ink,
        error: peachDeep,
      ),
      scaffoldBackgroundColor: bg,
    );
    return base.copyWith(
      appBarTheme: const AppBarTheme(
        backgroundColor: bg,
        foregroundColor: ink,
        elevation: 0,
        centerTitle: false,
        titleTextStyle: TextStyle(
          fontFamily: 'Nunito',
          color: ink,
          fontSize: 20,
          fontWeight: FontWeight.w900,
        ),
      ),
      cardTheme: CardThemeData(
        color: surface,
        elevation: 0,
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(24)),
        margin: EdgeInsets.zero,
      ),
      chipTheme: ChipThemeData(
        backgroundColor: surface,
        selectedColor: butterMid,
        labelStyle: const TextStyle(
          fontFamily: 'Nunito',
          fontWeight: FontWeight.w800,
          fontSize: 13,
          color: ink,
        ),
        side: const BorderSide(color: line),
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(999)),
      ),
      navigationBarTheme: NavigationBarThemeData(
        backgroundColor: surface,
        indicatorColor: sageTile,
        elevation: 0,
        height: 70,
        labelTextStyle: WidgetStateProperty.resolveWith((s) {
          final on = s.contains(WidgetState.selected);
          return TextStyle(
            fontFamily: 'Nunito',
            fontSize: 11.5,
            fontWeight: FontWeight.w800,
            color: on ? sageDeep : ink3,
          );
        }),
        iconTheme: WidgetStateProperty.resolveWith((s) {
          final on = s.contains(WidgetState.selected);
          return IconThemeData(color: on ? sageDeep : ink3, size: 24);
        }),
      ),
      filledButtonTheme: FilledButtonThemeData(
        style: FilledButton.styleFrom(
          backgroundColor: coral,
          foregroundColor: Colors.white,
          textStyle: const TextStyle(
              fontFamily: 'Nunito', fontWeight: FontWeight.w800, fontSize: 15),
          padding: const EdgeInsets.symmetric(horizontal: 22, vertical: 16),
          shape:
              RoundedRectangleBorder(borderRadius: BorderRadius.circular(999)),
        ),
      ),
      textButtonTheme: TextButtonThemeData(
        style: TextButton.styleFrom(
          foregroundColor: sageDeep,
          textStyle: const TextStyle(
              fontFamily: 'Nunito', fontWeight: FontWeight.w800),
        ),
      ),
      dialogTheme: DialogThemeData(
        backgroundColor: surface,
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(28)),
        titleTextStyle: const TextStyle(
          fontFamily: 'Nunito',
          fontSize: 18,
          fontWeight: FontWeight.w900,
          color: ink,
        ),
      ),
    );
  }

  static Widget glassPanel({
    required Widget child,
    EdgeInsetsGeometry padding = const EdgeInsets.all(16),
    bool dark = false,
  }) {
    return Container(
      padding: padding,
      decoration: BoxDecoration(
        color: dark ? darkCard : surface,
        borderRadius: BorderRadius.circular(24),
        boxShadow: clay(),
        border: Border.all(color: dark ? darkBorder : line),
      ),
      child: child,
    );
  }
}
