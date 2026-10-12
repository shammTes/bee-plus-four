#!/usr/bin/env python3
"""Builds assets/high/coach/topics.json: the offline Study Coach ("Help me") lessons.

Plain, short English for Grade 9-12 students in Eritrea. Advice follows well-tested study and psychology research
(retrieval practice, spacing, interleaving, sleep and memory, implementation intentions, cognitive reframing,
paced breathing). It is study support, not therapy: every topic links to the safety note.
Block types the app renders (lib/high/study_coach/):
  note   {title, text, tone?}                       short explainer / Eritrean context
  steps  {title, items: [{t, x}]}                   numbered step cards
  quiz   {id, title, intro, options, scores, questions, bands: [{max, title, advice, tone}]}   self-check with score
  mcq    {id, title, items: [{q, options, answer, why}]}                                     knowledge check
  check  {id, title, items: [..]}                    tick-off checklist (saved)
  tool   {tool, title, text}                         breath478 | pomodoro | twomin | reframe | spaced | goal
  try    {items: [..]}                               "Try this today" actions (saved per day)
  safety {}                                          the gentle safety note
    python3 tool/study_coach/build_topics.py          # write
    python3 tool/study_coach/build_topics.py --check  # fail if the asset is stale
"""
import json, sys, pathlib

FREQ = ['Never', 'Sometimes', 'Often', 'Almost always']
SC = [0, 1, 2, 3]


def note(title, text, tone=None):
  d = {'type': 'note', 'title': title, 'text': text}
  if tone: d['tone'] = tone
  return d


def steps(title, *items):
  return {'type': 'steps', 'title': title, 'items': [{'t': t, 'x': x} for t, x in items]}


def quiz(id, title, intro, questions, bands, options=FREQ, scores=SC):
  return {'type': 'quiz', 'id': id, 'title': title, 'intro': intro, 'options': options, 'scores': scores, 'questions': questions,
          'bands': [{'max': m, 'title': t, 'advice': a, 'tone': tn} for m, t, a, tn in bands]}


def mcq(id, title, *items):
  return {'type': 'mcq', 'id': id, 'title': title, 'items': [{'q': q, 'options': o, 'answer': a, 'why': w} for q, o, a, w in items]}


def check(id, title, *items):
  return {'type': 'check', 'id': id, 'title': title, 'items': list(items)}


def tool(kind, title, text):
  return {'type': 'tool', 'tool': kind, 'title': title, 'text': text}


def tryit(*items):
  return {'type': 'try', 'items': list(items)}


SAFE = {'type': 'safety'}

T = []


def topic(id, title, group, tone, icon, summary, *blocks):
  T.append({'id': id, 'title': title, 'group': group, 'tone': tone, 'icon': icon, 'summary': summary, 'blocks': list(blocks)})


# =====================================================================================================================
# Plain English: short sentences (about 12 words or fewer), everyday words, any special word explained at once.
STUDY, MIND, LIFE = 'Study smarter', 'Feelings and mind', 'Daily life'

topic('how_to_study', 'How to study', STUDY, 'blue', 'book',
  'Reading again and again teaches little. Testing yourself teaches a lot.',
  note('The big idea', 'Your brain learns when it pulls out an answer. '
       'Reading the answer again does not do this. Good study feels a bit hard.'),
  steps('A study session that works',
    ('Pick one small goal', 'Not "study biology". Say "learn the parts of the cell".'),
    ('Read once, carefully', 'Read the notes one time. Underline only key words.'),
    ('Close the book', 'Write or say all you remember. This step matters most.'),
    ('Check and fix', 'Open the book. Mark what you missed.'),
    ('Do questions', 'Do 5 to 10 questions on the same unit.'),
    ('Plan the next look', 'Look again tomorrow, then in 3 days, then in a week.')),
  mcq('study_mcq', 'Quick check: which works best?',
    ('You have one hour before a test. What helps most?',
     ['Read the notes three times', 'Read once, then test yourself with the book closed', 'Copy the notes neatly'], 1,
     'Testing yourself works better than reading again. It feels harder, but you remember more.'),
    ('You study maths. Which plan is better?',
     ['Do 20 questions of one kind', 'Mix questions from different units', 'Only read the examples'], 1,
     'Mixing teaches you to pick the right method. The exam asks you to do that.'),
    ('When is the best time to go over a topic again?',
     ['Only the night before the exam', 'A little, many times, over some weeks', 'Once, for six hours'], 1,
     'Short looks, a few days apart, make memories last longer.')),
  tool('pomodoro', 'Study timer', 'Study for 25 minutes. Rest for 5. Do it again.'),
  tryit('Study one topic for 25 minutes. Close the book for the last 10.', 'Write 3 questions about today\'s lesson. Answer them tomorrow.', 'Tell someone at home one thing you learned.'))

topic('remember_reading', 'Remember what you read', STUDY, 'lilac', 'bulb',
  'Four ways to keep what you read in your head.',
  steps('Test yourself (active recall)',
    ('Read a short part', 'One page or one heading.'),
    ('Cover it', 'Close the book or cover the page.'),
    ('Say it or write it', 'What were the main points? Use your own words.'),
    ('Check', 'Look again. What you forgot is what to study.')),
  steps('Look again, days apart (spaced review)',
    ('Day 1', 'Learn it. Test yourself.'),
    ('Day 2', 'Test again for 5 minutes.'),
    ('Day 4 to 7', 'Test again. It gets easier.'),
    ('After 2 weeks and 1 month', 'Short looks keep it until the matric.')),
  tool('spaced', 'Review planner', 'Type what you studied today. 4 tells you when to look again.'),
  steps('Teach it simply (the Feynman way)',
    ('Pick one idea', 'For example, how plants make food.'),
    ('Explain it to a young child', 'Use easy words and an example from home.'),
    ('Find where you get stuck', 'Go back to the book for that part.'),
    ('Make it simpler', 'Explain again until it is short and clear.')),
  steps('Draw a mind map',
    ('Main idea in the middle', 'Write the unit name in a circle.'),
    ('Add branches', 'One branch for each part. Use one or two words.'),
    ('Add small drawings', 'Pictures help you remember.'),
    ('Draw it again tomorrow', 'Try it without looking.')),
  check('recall_check', 'After a chapter, can you…',
    'Say the main idea in one sentence?', 'Give one example?', 'Answer one past exam question on it?', 'Draw a small picture of it from memory?', 'Explain it to a friend?'),
  tryit('After each page today, close the book. Say the main point.', 'Draw one mind map of a unit.', 'Add today\'s topic to the review planner.'))

topic('problem_solving', 'Tricks for solving problems', STUDY, 'peach', 'math',
  'For maths, physics and chemistry. A simple plan for any problem.',
  steps('Four steps',
    ('Understand', 'Read it twice. Write what you know and what you need.'),
    ('Plan', 'Which rule links them? Have you seen one like it?'),
    ('Do it', 'Go step by step. Write the units.'),
    ('Check', 'Does the answer make sense? A bike cannot go 3000 m/s.')),
  steps('When you are stuck',
    ('Use easy numbers', 'Try simple numbers first. Then use the real ones.'),
    ('Work backwards', 'Start from the answer you need. What do you need to find it?'),
    ('Look for a pattern', 'Try 1, 2, 3. What repeats?'),
    ('Leave it and come back', 'Do another question. Come back in 10 minutes.')),
  mcq('ps_mcq', 'Quick check',
    ('You are not sure in a multiple-choice maths question. What first?',
     ['Pick the longest answer', 'Put each answer back into the question', 'Leave it empty'], 1,
     'Testing each answer often shows the right one fast.'),
    ('Your physics answer has no units. What does it mean?',
     ['Units do not matter', 'You may have a mistake. Check each step.', 'It is surely right'], 1,
     'Units are a free check. Wrong units mean a wrong step.')),
  check('ps_check', 'Before you finish a problem',
    'I wrote what I know and what I need.', 'I drew a picture if it helps.', 'I wrote the formula first.', 'I wrote the units.', 'I checked that the answer makes sense.'),
  tryit('Solve 3 problems with the four steps.', 'Find one old mistake. Write why it happened.', 'Explain one problem to a classmate.'))

topic('exam_prep', 'How to get ready for exams', STUDY, 'sage', 'trophy',
  'A clear plan for tests and the matric. Past papers are the key.',
  note('About the matric', 'The matric is mostly multiple choice. It covers Grade 9 to 12. '
       'Old exam papers show you the style. 4 has many, with answers.'),
  steps('Your plan',
    ('8 weeks before', 'List every unit. Mark each one: strong, okay or weak.'),
    ('6 weeks before', 'Study weak units first. Do one old paper per subject.'),
    ('4 weeks before', 'Do more old papers. Study every question you got wrong.'),
    ('2 weeks before', 'Do full papers with a timer. No phone.'),
    ('Last week', 'Light review and sleep. No big new topics.'),
    ('Night before', 'Pack pens, pencil, eraser and ID. Sleep at your usual time.')),
  steps('On exam day',
    ('Read the rules', 'How many questions? How much time? How to fill the answer sheet?'),
    ('Share your time', 'Do not spend 10 minutes on one question.'),
    ('Easy ones first', 'Answer what you know. Mark hard ones. Come back later.'),
    ('Cross out wrong answers', 'Picking from two is easier than from four.'),
    ('Check the numbers', 'Question 23 on the paper is 23 on the sheet.')),
  check('exam_week', 'Exam week list',
    'I know the date, time and place of each exam.', 'I did at least one full old paper per subject.', 'I studied my past mistakes.',
    'I have pens, pencils, eraser and ruler.', 'I will sleep 8 hours each night.', 'I will eat breakfast and bring water.'),
  tool('pomodoro', 'Timed practice', 'Do old exam questions for 25 minutes. Then rest.'),
  tryit('List your units. Mark each strong, okay or weak.', 'Do 20 questions from one old matric paper in 4.', 'Write down each mistake and the right answer.'))

topic('exam_anxiety', 'Fear before exams', MIND, 'lilac', 'sparkle',
  'Feeling nervous is normal. A little helps you focus. Here is how to stay calm.',
  quiz('anx_quiz', 'How worried am I before exams?', 'Be honest. Only you see this.',
    ['I can\'t sleep the night before an exam.', 'My heart beats fast or my stomach hurts.', 'My mind goes blank, even when I studied.',
     'I keep thinking I will fail.', 'I don\'t study because the exam scares me.', 'I worry what my family will say.',
     'After an exam, I keep thinking about my mistakes.', 'I shake or sweat in the exam room.'],
    [(6, 'Mostly calm', 'You handle exam nerves well. Use calm breathing on hard days.', 'sage'),
     (13, 'Some nerves', 'This is very common. Do old papers with a timer. Breathe slowly before you start.', 'butter'),
     (19, 'Quite worried', 'Worry is getting in your way. Use the steps below each day. Talk to someone you trust.', 'peach'),
     (24, 'Very worried', 'This is a lot to carry alone. Please talk to a parent, teacher or school counsellor soon.', 'rose')]),
  note('Why your body reacts', 'Before an exam, your heart beats fast. This is your body getting ready. '
       'It does not mean you will fail. Slow breathing calms your body.'),
  tool('breath478', 'Calm breathing (4-7-8)', 'Breathe in for 4. Hold for 7. Breathe out for 8. Do it 4 times.'),
  steps('Before and during the exam',
    ('Practise a lot', 'Old papers with a timer make the real exam feel normal.'),
    ('Write your worries down', 'Before the exam, write them on paper. Your mind feels lighter.'),
    ('Say "I am ready"', 'Call the feeling energy, not fear.'),
    ('Start with an easy question', 'One quick win calms you.'),
    ('If your mind goes blank', 'Put the pen down. Take 3 slow breaths. Go to the next question.')),
  tryit('Do calm breathing now, and again before bed.', 'Do one old paper with a timer.', 'Tell one person how you feel about exams.'),
  SAFE)

topic('memory', 'Better memory', STUDY, 'mint', 'sparkle',
  'Memory can grow. Sleep and simple tricks make it stronger.',
  steps('Look after your brain',
    ('Sleep 8 to 10 hours', 'Teenagers need this. Sleep saves what you learned today.'),
    ('Move your body', 'Walk, run or play football. It helps your brain and mood.'),
    ('Drink water. Eat breakfast.', 'A hungry brain can\'t focus.'),
    ('Take short breaks', 'Breaks help new things stick.')),
  steps('Memory tricks',
    ('First letters', 'Make a word from first letters. Colours of light: ROY G BIV.'),
    ('Rhymes and songs', 'Put a list into a simple tune.'),
    ('Small groups', 'Remember 0917 2346 as two groups, not eight numbers.'),
    ('Funny pictures', 'Strange pictures stick. See the cell\'s mitochondria as a power station.')),
  steps('The memory walk (memory palace)',
    ('Pick a place you know', 'Your home, or your walk to school.'),
    ('Pick stops in order', 'Gate, door, kitchen, window, bed.'),
    ('Put one thing at each stop', 'Planets: Mercury at the gate, Venus at the door…'),
    ('Walk it in your mind', 'See each thing at its stop. Do it twice.')),
  mcq('mem_mcq', 'Quick check',
    ('You studied until 2 am. You slept 4 hours. What happens?',
     ['You keep it all', 'You lose a lot. Sleep helps save memories.', 'Sleep does not matter'], 1,
     'Sleep moves new learning into long memory. Short sleep means you forget more.'),
    ('Which list is easiest to remember?',
     ['Random words', 'Words placed on a path you know', 'Words written once'], 1,
     'A memory walk links new things to places you know well.')),
  tryit('Make a memory walk with 5 stops for one list.', 'Go to bed 30 minutes earlier tonight.', 'Make one first-letter trick for your notes.'))

topic('procrastination', 'Putting things off', MIND, 'peach', 'clock',
  'Putting things off (procrastination) is not laziness. We avoid a bad feeling. Make the start tiny.',
  quiz('proc_quiz', 'Do I put things off?', 'Think about the last two weeks.',
    ['I start homework on the last day.', 'I pick up my phone when I sit down to study.', 'I do other jobs so I don\'t have to study.',
     'I tell myself "later" or "tomorrow".', 'I feel bad about wasted time.', 'Big tasks feel too big to start.'],
    [(5, 'Not much', 'You start most tasks on time. Keep it up.', 'sage'),
     (11, 'Sometimes', 'Like most students. Try the 2-minute start and a timer.', 'butter'),
     (18, 'A lot', 'It is a habit now. Habits can change. Use the steps below for a week.', 'peach')]),
  note('Why we wait', 'We wait when a task feels boring, hard or scary. Waiting feels good now. '
       'Later it brings stress. So make the start very small.'),
  tool('twomin', '2-minute start', 'Do the task for only 2 minutes. Then you may stop. Most times, you will go on.'),
  steps('Beat it',
    ('Cut it small', '"Study chemistry" becomes "write the first 10 elements".'),
    ('Set a time and place', '"At 4 pm, I open my maths book at the table."'),
    ('Put the phone away', 'Put it in another room before you start.'),
    ('Give yourself a treat', 'After studying, have tea, see friends or play.')),
  tryit('Pick the task you avoid most. Do it for 2 minutes.', 'Write a time and place for tomorrow\'s study.', 'Put your phone in another room while you study.'))

topic('motivation', 'Feeling lazy or not wanting to study', MIND, 'butter', 'flame',
  'Wanting to study often comes after you start. Small wins help. So does a reason you care about.',
  quiz('mot_quiz', 'How is my drive to study?', 'Think about the last two weeks.',
    ['I feel tired, even after enough sleep.', 'I don\'t see why school matters for me.', 'I start tasks but stop quickly.', 'I think I will fail, so why try.', 'I don\'t enjoy things I used to enjoy.'],
    [(4, 'Doing okay', 'Your drive is steady. Set a goal to aim higher.', 'sage'),
     (9, 'A bit low', 'This is common. Find your reason. Get small wins each day.', 'butter'),
     (15, 'Very low', 'This may be more than laziness. Feeling low for two weeks? Talk to a parent, teacher or counsellor.', 'rose')]),
  steps('Get going again',
    ('Find your reason', 'Why study? A job you want? Helping your family? Write it down.'),
    ('Start very small', 'One question. One page. Doing it brings the wish to do more.'),
    ('Count your days', 'Mark each day you study. Try not to break the chain.'),
    ('Study with a friend', 'A friend who studies too keeps you going.'),
    ('Check your body', 'Low energy can come from short sleep or no breakfast.')),
  tool('goal', 'My reason and my goal', 'Write why you study. Write one small goal for this week.'),
  tryit('Write your reason on paper. Put it where you study.', 'Do one 10-minute task right now.', 'Ask a friend to study with you tomorrow.'),
  SAFE)

topic('self_talk', 'Unkind thoughts about yourself', MIND, 'rose', 'chat',
  '"I am stupid." "I will never pass." Thoughts are not facts. You can change them.',
  quiz('talk_quiz', 'How kind is my inner voice?', 'How often do you think this?',
    ['"I am stupid."', '"Everyone is better than me."', '"I always fail."', '"One mistake means I am a failure."', '"There is no point trying."', '"I will let everyone down."'],
    [(5, 'Mostly kind', 'You are fair to yourself. Keep it up.', 'sage'),
     (11, 'Sometimes harsh', 'Many students are hard on themselves. Try the worksheet below.', 'butter'),
     (18, 'Very harsh', 'These thoughts hurt. Use the worksheet each day. Tell someone you trust how you feel.', 'rose')]),
  steps('Catch it, check it, change it',
    ('Catch it', 'Notice the thought. Say: "I am having the thought that I am stupid."'),
    ('Check it', 'Is it 100% true? What shows it is not true?'),
    ('Change it', 'Make it fair: "This is hard. I can learn it with practice."'),
    ('Talk like a friend', 'What would you tell your best friend? Tell yourself the same.')),
  tool('reframe', 'Change the thought', 'Write the bad thought. Check it. Write a fairer one.'),
  note('Add the word "yet"', 'Change "I can\'t do this" to "I can\'t do this yet." Skills grow with practice.'),
  tryit('Write one unkind thought. Change it into a fair one.', 'Add "yet" to one "I can\'t" sentence.', 'Write 3 things you did well this week.'),
  SAFE)

topic('comparing', 'Comparing yourself with others', MIND, 'mint', 'chart',
  'Comparing yourself with others steals your joy. Good competition pushes you. Bad competition hurts you.',
  quiz('cmp_quiz', 'Do I compare too much?', 'Be honest.',
    ['I feel bad when a friend gets a higher mark.', 'I hide my marks from others.', 'I watch other people\'s marks more than mine.', 'I don\'t share notes, so others don\'t do better.', 'I feel good only if I am the best.'],
    [(4, 'Healthy', 'You keep your eyes on your own road. Good.', 'sage'),
     (9, 'Sometimes', 'Normal, but watch it. Compare with your old self.', 'butter'),
     (15, 'Too much', 'Comparing is hurting you. Try the steps below.', 'peach')]),
  steps('Run your own race',
    ('Compare with yourself', 'Look at your marks last month and now. That is fair.'),
    ('Everyone starts in a different place', 'Some have a quiet room or a helper. You can\'t see their whole story.'),
    ('Learn from others', 'Ask a top student how they study. Most will share.'),
    ('Share and help', 'Teaching others helps you learn. Your class is a team.'),
    ('Social media shows only good days', 'People post their best moments. They have bad days too.')),
  tryit('Write your last two test marks. See your own progress.', 'Ask a classmate how they study one subject.', 'Help someone with a question you understand.'))

topic('self_esteem', 'Believing in yourself', MIND, 'butter', 'star',
  'Confidence is not something you wait for. It grows from small brave steps.',
  quiz('se_quiz', 'How do I see myself?', 'How much do you agree?',
    ['I have good things about me.', 'I can do things as well as most people.', 'I am a person who matters.', 'I can speak in class when I want.', 'A bad mark does not make me worthless.'],
    [(5, 'Low right now', 'You are very hard on yourself. Try the steps below. Talk to someone you trust.', 'rose'),
     (10, 'In the middle', 'Like many teenagers. Get small wins. Notice what you are good at.', 'butter'),
     (15, 'Strong', 'You see your value. Use it to help others too.', 'sage')],
    options=['Not at all', 'A little', 'Mostly', 'Very much']),
  steps('Grow your confidence',
    ('List what you are good at', 'Not only marks. Kind? Hard-working? Good at football?'),
    ('Take small brave steps', 'Ask one question in class this week.'),
    ('Write your wins', 'Each day, write one thing that went well.'),
    ('Care for your body', 'Sleep, food and exercise help you feel ready.'),
    ('Stay near kind people', 'Pick friends who lift you up.')),
  check('se_check', 'This week I will…',
    'Ask or answer one question in class.', 'Write 3 things I am good at.', 'Thank myself for one thing I did well.', 'Try something new for 10 minutes.'),
  tryit('Write 3 things you are good at. Keep the paper in your notebook.', 'Write one win in a notebook tonight.', 'Speak once in class tomorrow.'),
  SAFE)

topic('time_management', 'Using your time well', LIFE, 'sage', 'cal',
  'School, home jobs and the walk take a lot of time. A simple week plan helps.',
  steps('Make a week plan',
    ('Write your fixed times', 'School, the walk, chores, prayer, meals, helping at home.'),
    ('Find free times', 'Look for 30 to 60 free minutes. Early morning is often quiet.'),
    ('Give each subject a time', 'Weak subjects get more time.'),
    ('Plan for power cuts', 'Read and write in daylight. Test yourself in the evening.'),
    ('Keep one free evening', 'Rest is part of the plan.')),
  steps('Use small bits of time',
    ('On the walk to school', 'Go over the last lesson in your head.'),
    ('While you wait', 'Look at five flash cards.'),
    ('Hardest task first', 'Do it while your mind is fresh.')),
  check('tm_check', 'My week',
    'I wrote my fixed times.', 'I found at least 5 study times.', 'Each subject has a time.', 'I planned rest.', 'I will check my plan on Sunday.'),
  tool('pomodoro', 'Study timer', '25 minutes of study makes time feel short and clear.'),
  tryit('Draw your week plan on one page.', 'On the walk to school, go over one lesson.', 'Do your hardest task first tomorrow.'))

topic('focus_phone', 'Focus and your phone', LIFE, 'blue', 'monitor',
  'Each message pulls you away. Coming back takes minutes. Protect your focus.',
  quiz('ph_quiz', 'Does my phone pull me away?', 'Think about your study time.',
    ['I check my phone while studying.', 'My phone is next to me when I study.', 'I lose time on videos or chats.', 'I use my phone in bed late.', 'I feel nervous if I can\'t check it.'],
    [(4, 'In control', 'You handle your phone well.', 'sage'),
     (9, 'Some', 'Try one study time with no phone.', 'butter'),
     (15, 'A lot', 'Your phone takes study and sleep time. Use the steps below each day.', 'peach')]),
  steps('Protect your focus',
    ('Out of sight', 'Even a phone face-down pulls you. Put it in another room.'),
    ('One thing at a time', 'Study and chat together make both slow.'),
    ('Use 4 with no internet', '4 works offline. Turn data off while you study.'),
    ('Check only at break time', 'Messages can wait 25 minutes.'),
    ('No phone in bed', 'Late chats steal your sleep.')),
  tool('pomodoro', 'No-phone study time', 'Start 25 minutes. The phone stays away until the break.'),
  tryit('Study once with your phone in another room.', 'Turn data off during homework.', 'No phone for 30 minutes before sleep.'))

topic('sleep_health', 'Sleep and health', LIFE, 'lilac', 'moon',
  'Sleep, food, water and exercise help you study. A rested brain learns faster.',
  quiz('sl_quiz', 'How are my sleep and health?', 'In the last week, how often…',
    ['I slept less than 7 hours.', 'I skipped breakfast.', 'I drank strong coffee or tea late in the day.', 'I used a screen in bed.', 'I felt sleepy in class.', 'I did no walking, running or sport.'],
    [(5, 'Healthy', 'Good habits. Your brain thanks you.', 'sage'),
     (11, 'Could be better', 'Pick one habit below to fix this week.', 'butter'),
     (18, 'Needs care', 'Your body is tired. Sleep comes first, even in exam time.', 'peach')]),
  steps('Good sleep',
    ('Same time each night', 'Sleep and wake at about the same time each day.'),
    ('8 to 10 hours', 'Teenagers need this much.'),
    ('No strong coffee late', 'Coffee keeps you awake for hours. Have it in the morning.'),
    ('Slow down before bed', 'Last 30 minutes: no screens. Read, pray or talk calmly.'),
    ('Don\'t study all night', 'No sleep makes you forget more.')),
  steps('Body basics',
    ('Breakfast', 'Even bread and tea is better than nothing.'),
    ('Water', 'Keep a bottle with you. Thirst feels like tiredness.'),
    ('Move', 'Walk, run or play for 20 minutes most days.')),
  tool('breath478', 'Calm breathing before sleep', 'A few rounds in bed can help you fall asleep.'),
  tryit('Go to bed at a set time tonight.', 'Drink a glass of water now.', 'Take a 20-minute walk today.'))

topic('family_pressure', 'Stress and pressure from family', MIND, 'peach', 'user',
  'Your family wants the best for you. That can feel heavy. Talking helps.',
  note('You are not alone', 'Many students feel pressure to pass the matric. Some feel pushed to a path. '
       'Your family\'s worry often comes from love and hope.'),
  quiz('fam_quiz', 'How much pressure do I feel?', 'In the last month…',
    ['I feel my family cares only about my marks.', 'I am scared to show my report card.', 'I have too many home jobs to study.', 'I must study a subject I don\'t like.', 'I feel stressed most days.'],
    [(4, 'Okay', 'You handle the pressure well. Keep talking with your family.', 'sage'),
     (9, 'Quite a lot', 'Try a calm talk with your family. See the steps below.', 'butter'),
     (15, 'Very heavy', 'This is a lot. Please talk to a teacher, a relative or a school counsellor.', 'rose')]),
  steps('What helps',
    ('Pick a calm time', 'Not right after a bad mark. Maybe after dinner or coffee.'),
    ('Show your plan', 'Families worry less when they see a study plan.'),
    ('Say how you feel', '"I want to do well too. Your support helps me."'),
    ('Ask for study time', 'Agree on hours for chores and hours for study.'),
    ('Ask an adult to help', 'A teacher or uncle can help you talk to your parents.')),
  tool('breath478', 'Calm breathing', 'When stress grows, breathe slowly 4 times.'),
  tryit('Write 3 sentences you want to tell your family.', 'Show your study plan to a parent.', 'Do one thing just for you today.'),
  SAFE)

topic('failure', 'Bad marks and failing', MIND, 'rose', 'repeat',
  'A bad mark does not say who you are. It shows what to learn next.',
  steps('After a bad mark',
    ('Let yourself feel it', 'It is okay to feel sad or angry for a while.'),
    ('Look at the paper', 'Where did you lose marks?'),
    ('Find the kind of mistake', 'Didn\'t know it? Read it wrong? Ran out of time?'),
    ('Make one fix for each', 'Didn\'t know: study it. Read wrong: underline key words.'),
    ('Try again', 'Do similar questions in 4. Watch yourself get better.')),
  mcq('fail_mcq', 'Quick check',
    ('What helps most with a failed test?',
     ['Throw it away', 'Study each wrong answer and why', 'Decide you are bad at it'], 1,
     'Mistakes show you what to learn next. 4 keeps them on the Mistakes page.'),
    ('Which thought helps more after a bad mark?',
     ['"I am a failure."', '"I failed this test. I can find out why."', '"The teacher hates me."'], 1,
     'One test is not who you are. Fair thoughts help you act.')),
  check('fail_check', 'My mistake check',
    'I listed every wrong question.', 'I wrote the kind of each mistake.', 'I studied the right answers.', 'I tried 5 similar questions.', 'I asked my teacher how to improve.'),
  note('Many great people failed first', 'Thomas Edison tried thousands of things before his light bulb worked.'),
  tryit('List the 3 mistakes you make most.', 'Try your old mistakes again on the Mistakes page in 4.', 'Say to yourself what you would tell a friend who failed.'),
  SAFE)

topic('peer_pressure', 'Pressure from friends', LIFE, 'mint', 'user',
  'Friends matter a lot. Good friends support your goals. You can say no and stay friends.',
  quiz('peer_quiz', 'How much do friends push me?', 'How often…',
    ['I skip study because friends want to go out.', 'I do things I don\'t want, to fit in.', 'I hide that I like studying.', 'Friends laugh at my goals.', 'I find it hard to say no.'],
    [(4, 'Low', 'You make your own choices. Good.', 'sage'),
     (9, 'Some', 'Practise the ways to say no below.', 'butter'),
     (15, 'Strong', 'Friends pull you a lot. Who supports your goals? Feel unsafe? Talk to an adult you trust.', 'peach')]),
  steps('Ways to say no',
    ('Keep it short', '"No, thanks. I have to study tonight."'),
    ('Offer another time', '"Not now. Let\'s play football on Saturday."'),
    ('Give a reason', '"My family needs me at home."'),
    ('Walk away', 'You don\'t need a long reason.'),
    ('Find study friends', 'Spend time with friends who also want to pass.')),
  mcq('peer_mcq', 'What would you do?',
    ('Friends want to skip class and go to town. You have a test tomorrow.',
     ['Go, so they don\'t laugh', '"I can\'t today. Let\'s meet after school."', 'Go, and lie to your family'], 1,
     'Saying no and offering another time keeps your plan and your friends.')),
  tryit('Say one "No, thanks" sentence out loud.', 'Plan one study time with a friend who has goals.', 'Notice one time today you chose what you wanted.'),
  SAFE)

topic('setting_goals', 'Setting goals', STUDY, 'butter', 'target',
  'A clear goal shows you where to go. Make it small and clear, with a date.',
  steps('A good goal (SMART)',
    ('Clear', 'Not "do better in maths". Say "get 70% in the next maths test".'),
    ('Easy to check', 'A mark, a number of papers, or pages.'),
    ('Possible', 'From 40% to 60% is better than 40% to 100%.'),
    ('Important to you', 'It helps you reach the matric or the job you want.'),
    ('With a date', '"By the end of this term."')),
  steps('Big goal to small steps',
    ('Big goal', 'Pass the matric with good marks.'),
    ('This term', 'Finish the Grade 11 units. Do 3 old papers per subject.'),
    ('This week', 'Biology unit 3 and one old paper.'),
    ('Today', '30 minutes on cell division. Then 10 questions.')),
  tool('goal', 'My goal', 'Write one goal and your first small step.'),
  tryit('Write one goal for this term.', 'Cut it into steps for this week.', 'Do today\'s step.'))

topic('group_study', 'Studying in a group', STUDY, 'sage', 'chat',
  'Studying together can help a lot. Or it can waste the day. Here is how to make it work.',
  steps('A group that works',
    ('Keep it small', '3 or 4 people who want to learn.'),
    ('Set a goal', '"Today: chemistry unit 4 questions."'),
    ('Study alone first', 'Come ready. The group is for testing each other.'),
    ('Take turns teaching', 'Each person explains one part. Teaching helps you learn.'),
    ('Ask each other questions', 'Use old exam questions. Explain every answer.'),
    ('Agree on breaks', 'Chat and tea at break time only.')),
  check('grp_check', 'Before the next group meeting',
    'We picked a topic.', 'Everyone studied it alone first.', 'Each person has 3 questions ready.', 'We have a time and place.', 'Phones stay away while we study.'),
  tryit('Invite 2 classmates to study one topic for an hour.', 'Get 3 questions ready for the group.', 'Explain one idea to the group.'))

topic('asking_help', 'Asking for help', LIFE, 'blue', 'chat',
  'Asking for help is a skill, not a weakness. People like to help when you ask clearly.',
  steps('Ask well',
    ('Try first', 'Try for 10 minutes. Then show what you did.'),
    ('Be exact', 'Not "I don\'t get physics". Say "I don\'t get step 3 here".'),
    ('Pick a good time', 'After class or at break.'),
    ('Say thank you', 'Then try a similar question alone.')),
  steps('Who can help',
    ('Your teacher', 'They know the lessons and the exam.'),
    ('A classmate', 'A friend can explain in simple words.'),
    ('An older brother, sister or cousin', 'Many have done the matric before you.'),
    ('The Tutor in 4', 'Ask about any topic. It works with no internet.'),
    ('A school counsellor', 'For stress, worry or problems at home.')),
  check('help_check', 'Before I ask',
    'I tried for at least 10 minutes.', 'I know which part I don\'t understand.', 'I wrote my question down.', 'I picked a good time to ask.'),
  tryit('Write one question. Ask a teacher tomorrow.', 'Ask the Tutor in 4 about a hard topic.', 'Help a classmate who asks you.'),
  SAFE)

topic('sawa_life', 'Grade 12 away from home', LIFE, 'peach', 'home',
  'Living away from home for Grade 12 is a big change. A daily routine helps.',
  note('A new start', 'Many students do Grade 12 and the matric at Sawa. '
       'Missing home is normal, most of all in the first weeks.'),
  steps('Settle in',
    ('Make a daily routine', 'Set times for study, rest and sleep.'),
    ('Find study friends', 'Study with students from your class or town.'),
    ('Keep your notes tidy', 'One bag or box for each subject.'),
    ('Stay in touch with home', 'A short call or message when you can.'),
    ('Look after your health', 'Drink water. Sleep enough. Say if you feel unwell.')),
  check('sawa_check', 'My first week',
    'I know my class timetable.', 'I made a study routine.', 'I found at least one study friend.', 'My notes are sorted by subject.', 'I know who to talk to if I feel sick or sad.'),
  tool('breath478', 'When you miss home', 'Slow breathing calms you when you feel homesick.'),
  tryit('Write tomorrow\'s routine with study times.', 'Ask one classmate to study with you this week.', 'Write a short message to your family.'),
  SAFE)


def build():
  return {'version': 1,
          'safety': {'title': 'If you feel very sad or unsafe',
                     'text': 'These lessons help with study and everyday stress. They are not a doctor. '
                             'Do you feel very sad or unsafe? Do you think about hurting yourself? '
                             'Please talk to a parent, teacher or school counsellor today. You matter. Help is there.'},
          'groups': [STUDY, MIND, LIFE],
          'topics': T}


if __name__ == '__main__':
  root = pathlib.Path(__file__).resolve().parents[2]
  p = root / 'assets/high/coach/topics.json'
  s = json.dumps(build(), ensure_ascii=False, indent=1) + '\n'
  if '--check' in sys.argv:
    ok = p.exists() and p.read_text(encoding='utf-8') == s
    print('topics.json up to date' if ok else 'topics.json is stale: run tool/study_coach/build_topics.py')
    sys.exit(0 if ok else 1)
  p.parent.mkdir(parents=True, exist_ok=True)
  p.write_text(s, encoding='utf-8')
  print(f'wrote {p} ({len(T)} topics)')
