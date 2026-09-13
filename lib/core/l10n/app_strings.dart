/// UI strings: English + Tigrinya (ትግርኛ).
/// Keep Ge'ez orthography accurate for common school-app terms.
class AppStrings {
  AppStrings._();

  static bool tigrinya = false;

  static String get _t => tigrinya ? 'ti' : 'en';

  static String _s(String en, String ti) => tigrinya ? ti : en;

  // Brand / nav
  static String get appName => '4';
  static String get tagline =>
      _s('Study · Practice · Master', 'ተማሃር · ምልምማድ · ብቕዓት');
  static String get home => _s('Home', 'መእተዊ');
  static String get notes => _s('Notes', 'መዘኻኸሪ');
  static String get practice => _s('Practice', 'ምልምማድ');
  static String get coach => _s('Coach', 'ኣሰልጣኒ');
  static String get exams => _s('Exams', 'ፈተናታት');
  static String get labs => _s('Virtual labs', 'ላብ');
  static String get tools => _s('Tools', 'መሳርሒታት');
  static String get about => _s('About', 'ብዛዕባ');
  static String get settings => _s('Settings', 'ስንድኦታት');

  // Common
  static String get grade => _s('Grade', 'ክፍሊ');
  static String get subject => _s('Subject', 'ትምህርቲ');
  static String get unit => _s('Unit', 'ክፍለ-ትምህርቲ');
  static String get start => _s('Start', 'ጀምር');
  static String get next => _s('Next', 'ዝቕጽል');
  static String get checkAnswer => _s('Check answer', 'መልሲ ኣረጋግጽ');
  static String get nextQuestion => _s('Next question', 'ዝቕጽል ሕቶ');
  static String get loading => _s('Loading study content…', 'ትሕዝቶ ይጽዕን ኣሎ…');
  static String get gotIt => _s('Got it', 'ተረዲኡኒ');
  static String get deviceId => _s('Device ID', 'መለለዪ መሳርሒ');
  static String get copyId => _s('Device ID copied', 'መለለዪ ተቐዲሑ');

  // Home cards
  static String get notesSub =>
      _s('Units · illustrated · practice link', 'ክፍለ-ትምህርቲ · ስእላዊ · ምልምማድ');
  static String get practiceSub =>
      _s('Pick unit · adaptive mastery', 'ክፍለ-ትምህርቲ ምረጽ · ብቕዓት');
  static String get coachSub =>
      _s('Notes · quiz · matric mode', 'መዘኻኸሪ · ሕቶ · ማትሪክ');
  static String get examsSub =>
      _s('Matriculation · model papers', 'ማትሪክ · ሞዴል ፈተና');
  static String get labsSub =>
      _s('Physics · Chemistry · Biology', 'ፊዚክስ · ኬሚስትሪ · ባዮሎጂ');
  static String get toolsSub =>
      _s('Calculator · timer · flashcards', 'ኣሃዚ · ሰዓት · ካርድ');

  // Features
  static String get daily10 => _s('Daily 10', 'መዓልታዊ 10');
  static String get daily10Sub =>
      _s('Ten adaptive questions today', 'ሎሚ 10 ሕቶታት');
  static String get weakness => _s('Weakness report', 'ጸብጻብ ድኽመት');
  static String get weaknessSub =>
      _s('Units that need more work', 'ዝያዳ ስራሕ ዘድልዮም ክፍለ-ትምህርትታት');
  static String get flashcards => _s('Flashcards', 'ካርድታት');
  static String get flashcardsSub =>
      _s('Terms & formulas by unit', 'ቃላትን ቀመራትን');
  static String get timedMock => _s('Timed mock exam', 'ብሰዓት ሞዴል ፈተና');
  static String get timedMockSub =>
      _s('Exam clock · real pressure', 'ሰዓት ፈተና');
  static String get studyTimer => _s('Study timer', 'ሰዓት ምምሃር');
  static String get studyTimerSub =>
      _s('Focus 25 min · break 5 min', '25 ደቒቕ ትኹረት');
  static String get progress => _s('Progress', 'ዕቤት');
  static String get progressSub =>
      _s('Study calendar & streaks', 'መዓልታት ምምሃር');
  static String get darkMode => _s('Dark mode', 'ጸሊም ሞድ');
  static String get language => _s('Language', 'ቋንቋ');
  static String get english => _s('English', 'እንግሊዝኛ');
  static String get tigrinyaLabel => _s('Tigrinya', 'ትግርኛ');
  static String get mastery => _s('Mastery', 'ብቕዓት');
  static String get similar => _s('Similar questions', 'ተመሳሳሊ ሕቶታት');
  static String get teachUnit =>
      _s('Teach this unit (3 min)', 'እዚ ክፍለ-ትምህርቲ ኣስተምህር (3 ደቒቕ)');
  static String get explainMistake =>
      _s('Explain my mistake', 'ጌጋይ ኣብርህ');
  static String get matricYear => _s('Matric year', 'ዓመተ ማትሪክ');
  static String get welcomeTitle => _s('Welcome to 4', 'እንቋዕ ናብ 4 መጻእኩም');
  static String get welcomeBody => _s(
        '1) Pick your grade\n'
        '2) Notes → unit cards\n'
        '3) Practice → unit mastery\n'
        '4) Coach → quiz / notes / matric\n'
        '5) Labs · Daily 10 · Timer\n\n'
        'Your Device ID is on Home for Bee Seller unlock.',
        '1) ክፍልኻ ምረጽ\n'
        '2) መዘኻኸሪ → ክፍለ-ትምህርቲ\n'
        '3) ምልምማድ → ብቕዓት\n'
        '4) ኣሰልጣኒ → ሕቶ / መዘኻኸሪ / ማትሪክ\n'
        '5) ላብ · መዓልታዊ 10 · ሰዓት\n\n'
        'መለለዪ መሳርሒ ኣብ መእተዊ ይርከብ።',
      );

  static String get developedBy =>
      _s('Developed by SHAMM TESFALEM\nPhone: 07162947',
          'ዝተዳለወ ብ SHAMM TESFALEM\nተ.ቁ: 07162947');

  static String get newLevel => _s('New', 'ሓድሽ');
  static String get weak => _s('Weak', 'ድኹም');
  static String get building => _s('Building', 'ይሕየል');
  static String get strong => _s('Strong', 'ብርቱዕ');
  static String get mastered => _s('Mastered', 'ተቖጻጺሩ');
}
