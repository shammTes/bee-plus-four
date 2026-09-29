// High: notes subjects of the Grade 9-12 books (index.json subject keys). [key] is the display name (labels fall back to it).
class NotesSubject {
  final String key, art, tone;
  const NotesSubject(this.key, this.art, this.tone);
}

const kNotesSubjects = {
  'biology': NotesSubject('Biology', 'leaf', 'sage'),
  'chemistry': NotesSubject('Chemistry', 'flask', 'lilac'),
  'physics': NotesSubject('Physics', 'atom', 'mint'),
  'mathematics': NotesSubject('Mathematics', 'math', 'blue'),
  'agriculture': NotesSubject('Agriculture', 'sprout', 'butter'),
  'geography': NotesSubject('Geography', 'globe', 'blue'),
  'history': NotesSubject('History', 'landmark', 'butter'),
  'business_economics': NotesSubject('Business & Economics', 'chart', 'peach'),
  'english': NotesSubject('English', 'book', 'rose'),
};

const kNotesOrder = ['biology', 'chemistry', 'physics', 'mathematics', 'agriculture', 'geography', 'history', 'business_economics', 'english'];

/// Grade 11–12 streams. Mathematics and Agriculture are taken in both.
const kScienceSubjects = {'biology', 'chemistry', 'physics', 'mathematics', 'agriculture', 'english'};
const kArtSubjects = {'history', 'geography', 'business_economics', 'mathematics', 'agriculture', 'english'};

NotesSubject notesSubject(String s) =>
    kNotesSubjects[s] ?? NotesSubject(s.replaceAll('_', ' ').replaceFirstMapped(RegExp('^.'), (m) => m[0]!.toUpperCase()), 'book', 'sage');

/// grade tile tones on Home (Grade 9-12)
String gradeTone(int g) => const {9: 'sage', 10: 'blue', 11: 'lilac', 12: 'peach'}[g] ?? 'butter';
