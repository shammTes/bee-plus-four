#!/usr/bin/env python3
"""Builds assets/high/motivation/quotes.json: original quote cards for the Motivation gallery.

Every quote is public domain, a short attributed line from a famous person, a traditional proverb, or an
original line written for 4 (author "4 · original"). No song lyrics, no copyrighted artwork: the cards are
drawn natively in Flutter (lib/high/motivation/quote_art.dart) from the [art] motif and [tone] gradient below.
    python3 tool/motivation/build_quotes.py          # write
    python3 tool/motivation/build_quotes.py --check  # fail if the asset is stale
"""
import json, sys, pathlib

ORIG = '4 · original'
# (text, author, source, category, art, tone)
Q = [
  # ---- start
  ('A journey of a thousand miles begins with a single step.', 'Lao Tzu', 'Tao Te Ching, 64', 'start', 'road', 'sunrise'),
  ('The beginning is the most important part of the work.', 'Plato', 'The Republic', 'start', 'sprout', 'meadow'),
  ('He who has begun is half done. Dare to be wise; begin!', 'Horace', 'Epistles, I.2', 'start', 'sun', 'sunrise'),
  ('First say to yourself what you would be; and then do what you have to do.', 'Epictetus', 'Discourses, III.23', 'start', 'flag', 'sky'),
  ('Lost time is never found again.', 'Benjamin Franklin', "Poor Richard's Almanack, 1748", 'start', 'clock', 'dusk'),
  ('While we are postponing, life speeds by.', 'Seneca', 'Letters to Lucilius, 1', 'start', 'clock', 'sand'),
  ('Do what you can, with what you have, where you are.', 'Theodore Roosevelt', 'quoting Bill Widener, Autobiography, 1913', 'start', 'desk', 'meadow'),
  ('Open the book for two minutes. Starting is the hardest part, and you just did it.', ORIG, None, 'start', 'book', 'butter'),
  ('Today one page. Tomorrow one more. That is how a whole textbook gets read.', ORIG, None, 'start', 'book', 'sky'),
  ('Well done is better than well said.', 'Benjamin Franklin', "Poor Richard's Almanack, 1737", 'start', 'pencil', 'coral'),
  # ---- keep going
  ('Little by little does the trick.', 'Aesop', 'The Crow and the Pitcher', 'keep', 'stones', 'sea'),
  ('Slow and steady wins the race.', 'Aesop', 'The Tortoise and the Hare', 'keep', 'road', 'meadow'),
  ('Dripping water hollows out stone.', 'Ovid', 'Letters from Pontus, IV.10', 'keep', 'stones', 'sea'),
  ('No great thing is created suddenly.', 'Epictetus', 'Discourses, I.15', 'keep', 'tree', 'meadow'),
  ('Fall seven times, stand up eight.', 'Japanese proverb', None, 'keep', 'mountain', 'sunrise'),
  ('Slowly, slowly, the egg will walk on its own legs.', 'Proverb from the Horn of Africa', None, 'keep', 'sprout', 'butter'),
  ('Little by little, the bird builds its nest.', 'French proverb', None, 'keep', 'tree', 'sand'),
  ('Never give in, never give in, never, never, never.', 'Winston Churchill', 'Harrow School, 1941', 'keep', 'flag', 'dusk'),
  ('Genius is one per cent inspiration, ninety-nine per cent perspiration.', 'Thomas Edison', None, 'keep', 'lamp', 'night'),
  ('Life is like riding a bicycle. To keep your balance you must keep moving.', 'Albert Einstein', 'letter to his son Eduard, 1930', 'keep', 'bicycle', 'sky'),
  ('The road from Massawa climbs to Asmara one bend at a time. So does your revision.', ORIG, None, 'keep', 'road', 'sunrise'),
  ('A bad mark is a map. It shows you where to study next.', ORIG, None, 'keep', 'map', 'coral'),
  ('Diligence is the mother of good luck.', 'Benjamin Franklin', 'The Way to Wealth, 1758', 'keep', 'sun', 'butter'),
  # ---- learning
  ('To know what you know and to know what you do not know, that is true knowledge.', 'Confucius', 'Analects, 2.17', 'learn', 'book', 'lilac'),
  ('Learning without thought is labour lost; thought without learning is perilous.', 'Confucius', 'Analects, 2.15', 'learn', 'bulb', 'lilac'),
  ('The roots of education are bitter, but the fruit is sweet.', 'Aristotle', 'as told by Diogenes Laertius', 'learn', 'tree', 'meadow'),
  ('For the things we have to learn before we can do them, we learn by doing them.', 'Aristotle', 'Nicomachean Ethics, II', 'learn', 'pencil', 'sand'),
  ('The mind is not a vessel to be filled, but a fire to be kindled.', 'Plutarch', 'On Listening to Lectures (paraphrase)', 'learn', 'lamp', 'night'),
  ('As long as you live, keep learning how to live.', 'Seneca', 'Letters to Lucilius, 76', 'learn', 'book', 'sky'),
  ('If I have seen further it is by standing on the shoulders of giants.', 'Isaac Newton', 'letter to Robert Hooke, 1675', 'learn', 'mountain', 'dusk'),
  ('The important thing is not to stop questioning.', 'Albert Einstein', 'LIFE magazine, 1955', 'learn', 'bulb', 'butter'),
  ('Chance favours only the prepared mind.', 'Louis Pasteur', 'lecture at Lille, 1854', 'learn', 'flask', 'mint'),
  ('Iron rusts from disuse; even so does inaction sap the vigour of the mind.', 'Leonardo da Vinci', 'Notebooks', 'learn', 'gear', 'sand'),
  ('Close the book and say it in your own words. If you can, you have learned it.', ORIG, None, 'learn', 'chat', 'mint'),
  ('Education is the most powerful weapon which you can use to change the world.', 'Nelson Mandela', '2003', 'learn', 'cap', 'coral'),
  ('One child, one teacher, one book, one pen can change the world.', 'Malala Yousafzai', 'United Nations, 2013', 'learn', 'pencil', 'sky'),
  ('Knowledge is power. Information is liberating. Education is the premise of progress, in every society, in every family.', 'Kofi Annan', '1997', 'learn', 'globe', 'lilac'),
  # ---- mind
  ('Men are disturbed not by things, but by the views which they take of things.', 'Epictetus', 'Enchiridion, 5', 'mind', 'cloud', 'sky'),
  ('There is nothing either good or bad, but thinking makes it so.', 'William Shakespeare', 'Hamlet', 'mind', 'moon', 'night'),
  ('Our doubts are traitors, and make us lose the good we oft might win by fearing to attempt.', 'William Shakespeare', 'Measure for Measure', 'mind', 'mountain', 'dusk'),
  ('The impediment to action advances action. What stands in the way becomes the way.', 'Marcus Aurelius', 'Meditations, 5.20 (tr. Gregory Hays)', 'mind', 'stones', 'sand'),
  ('Very little is needed to make a happy life; it is all within yourself, in your way of thinking.', 'Marcus Aurelius', 'Meditations, 7.67', 'mind', 'sun', 'meadow'),
  ('Nothing in life is to be feared, it is only to be understood.', 'Marie Curie', None, 'mind', 'flask', 'mint'),
  ('Optimism is the faith that leads to achievement.', 'Helen Keller', 'Optimism, 1903', 'mind', 'sun', 'sunrise'),
  ('Trust thyself: every heart vibrates to that iron string.', 'Ralph Waldo Emerson', 'Self-Reliance, 1841', 'mind', 'star', 'night'),
  ('Breathe in for four. You are here, you are ready, you know more than you think.', ORIG, None, 'mind', 'cloud', 'lilac'),
  ('The five fingers are not the same, and each one is needed. Run your own race.', ORIG, None, 'mind', 'stones', 'butter'),
  ('Compare yourself with who you were last month, not with the student next to you.', ORIG, None, 'mind', 'chart', 'mint'),
  # ---- together
  ('If you want to go fast, go alone. If you want to go far, go together.', 'African proverb', None, 'together', 'palms', 'sand'),
  ("Do your little bit of good where you are; it's those little bits of good put together that overwhelm the world.", 'Desmond Tutu', None, 'together', 'globe', 'meadow'),
  ('A question asked is a lesson learned. Your teacher is waiting for it.', ORIG, None, 'together', 'chat', 'sky'),
  ('Coffee is better shared, and so is a hard maths problem.', ORIG, None, 'together', 'jebena', 'coral'),
  ('Teach a friend what you learned today and you will remember it twice as well.', ORIG, None, 'together', 'board', 'mint'),
  # ---- courage
  ('Success is to be measured not so much by the position that one has reached in life as by the obstacles which he has overcome while trying to succeed.', 'Booker T. Washington', 'Up from Slavery, 1901', 'courage', 'mountain', 'sunrise'),
  ('It is not because things are difficult that we do not dare; it is because we do not dare that they are difficult.', 'Seneca', 'Letters to Lucilius, 104', 'courage', 'flag', 'coral'),
  ('The fault, dear Brutus, is not in our stars, but in ourselves.', 'William Shakespeare', 'Julius Caesar', 'courage', 'star', 'night'),
  ('Nothing great was ever achieved without enthusiasm.', 'Ralph Waldo Emerson', 'Circles, 1841', 'courage', 'sun', 'butter'),
  ('What we hope ever to do with ease, we must learn first to do with diligence.', 'Samuel Johnson', 'in Boswell, Life of Johnson', 'courage', 'pencil', 'lilac'),
  ('I attribute my success to this: I never gave or took any excuse.', 'Florence Nightingale', None, 'courage', 'lamp', 'dusk'),
  ('The Red Sea is wide, but every boat crosses it one wave at a time.', ORIG, None, 'courage', 'boat', 'sea'),
  ('You do not need to be the best in class. You need to be better than yesterday.', ORIG, None, 'courage', 'cap', 'sky'),
]

# plain meaning shown under each famous quote (keyed by the first words of the quote)
MEAN = {
  'A journey of a thousand': 'Every big thing starts with one small step.',
  'The beginning is': 'Starting well matters most.',
  'He who has begun': 'Once you start, you are halfway there.',
  'First say to yourself': 'Decide who you want to be. Then do the work.',
  'Lost time is': 'You cannot get wasted time back.',
  'While we are postponing': 'If you wait and wait, life goes by.',
  'Do what you can': 'Start now, with what you have.',
  'Well done is better': 'Doing is better than talking.',
  'Little by little does': 'Small steps get the job done.',
  'Slow and steady': 'Keep going. Slow is fine.',
  'Dripping water': 'Small efforts, again and again, make big changes.',
  'No great thing': 'Great things take time.',
  'Fall seven times': 'Each time you fall, get up again.',
  'Slowly, slowly, the egg': 'With time, small things grow big.',
  'Little by little, the bird': 'Small steps build big things.',
  'Never give in': 'Do not give up.',
  'Genius is one': 'Success is mostly hard work.',
  'Life is like riding': 'Keep moving forward, or you fall.',
  'Diligence is the mother': 'Hard work brings good luck.',
  'To know what you know': 'Be honest about what you know and do not know.',
  'Learning without thought': 'Read and think. You need both.',
  'The roots of education': 'Learning is hard at first. The results are sweet.',
  'For the things we have': 'We learn by doing.',
  'The mind is not a vessel': 'Learning should make you curious, not just full of facts.',
  'As long as you live': 'Never stop learning.',
  'If I have seen further': 'We learn from people who came before us.',
  'The important thing is not': 'Keep asking questions.',
  'Chance favours only': 'Luck helps people who are ready.',
  'Iron rusts from disuse': 'Use your mind, or it gets weak.',
  'Education is the most': 'Learning can change the world.',
  'One child, one teacher': 'Small things, like one book, can change the world.',
  'Knowledge is power': 'Learning helps people and countries grow.',
  'Men are disturbed': 'How we think about a problem matters most.',
  'There is nothing either good': 'Your thoughts change how things feel.',
  'Our doubts are traitors': 'Fear of trying makes us miss good things.',
  'The impediment to action': 'A problem can show you the way forward.',
  'Very little is needed': 'Happiness comes from how you think.',
  'Nothing in life is to be feared': 'Learn about what scares you. Then you fear it less.',
  'Optimism is the faith': 'Hope helps you succeed.',
  'Trust thyself': 'Believe in yourself.',
  'If you want to go fast': 'Alone is fast. Together goes further.',
  'Do your little bit': 'Small good acts add up.',
  'Success is to be measured': 'What you overcome shows your success.',
  'It is not because things are difficult': 'Things feel hard because we are scared to try.',
  'The fault, dear Brutus': 'Your choices matter more than luck.',
  'Nothing great was ever': 'Big things need energy and love.',
  'What we hope ever to do': 'Hard work first. Then it becomes easy.',
  'I attribute my success': 'No excuses. Just do it.',
}

CATS = [
  {'id': 'start', 'label': 'Get started', 'tone': 'peach'},
  {'id': 'keep', 'label': 'Keep going', 'tone': 'sage'},
  {'id': 'learn', 'label': 'Learning', 'tone': 'blue'},
  {'id': 'mind', 'label': 'Calm mind', 'tone': 'lilac'},
  {'id': 'together', 'label': 'Together', 'tone': 'mint'},
  {'id': 'courage', 'label': 'Courage', 'tone': 'butter'},
]


def build():
  out = []
  for i, (t, a, src, c, art, tone) in enumerate(Q):
    d = {'id': f'q{i + 1:02d}', 'text': t, 'author': a, 'cat': c, 'art': art, 'tone': tone}
    if src: d['source'] = src
    m = [v for k, v in MEAN.items() if t.startswith(k)]
    if m: d['meaning'] = m[0]
    elif a != ORIG: raise SystemExit(f'no plain meaning for: {t}')
    out.append(d)
  return {'version': 1, 'note': 'Public-domain, attributed or original lines; artwork drawn in-app.', 'categories': CATS, 'quotes': out}


if __name__ == '__main__':
  root = pathlib.Path(__file__).resolve().parents[2]
  p = root / 'assets/high/motivation/quotes.json'
  s = json.dumps(build(), ensure_ascii=False, indent=1) + '\n'
  if '--check' in sys.argv:
    ok = p.exists() and p.read_text(encoding='utf-8') == s
    print('quotes.json up to date' if ok else 'quotes.json is stale: run tool/motivation/build_quotes.py')
    sys.exit(0 if ok else 1)
  p.parent.mkdir(parents=True, exist_ok=True)
  p.write_text(s, encoding='utf-8')
  print(f'wrote {p} ({len(Q)} quotes)')
