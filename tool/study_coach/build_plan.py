#!/usr/bin/env python3
"""Study Coach check-in + 30-day plan → assets/high/coach/plan.json.

Adapted from the Focus30 design (/workspace/student-app, 11 Oct 2026): the 14-question check-in, the friendly
profiles with top 2 focus areas, and 6 tracks × 25 short lessons. All text is rewritten in very simple English for
Eritrean Grade 9-12 students. Research sources stay in metadata only (plan_sources.py).
No diagnosis words, no helpline numbers.

  python3 tool/study_coach/build_plan.py          # write
  python3 tool/study_coach/build_plan.py --check  # fail if the JSON is out of date
"""
import json, os, re, sys

sys.path.insert(0, os.path.dirname(__file__))
from plan_sources import SOURCES  # noqa: E402

OUT = os.path.join(os.path.dirname(__file__), '..', '..', 'assets', 'high', 'coach', 'plan.json')

SCALE = ['Never', 'Rarely', 'Sometimes', 'Often', 'Almost always']

# area id, name, short, tone, icon, related Study Coach topic
AREAS = [
    ('focus', 'Focus', 'Staying on one task', 'blue', 'target', 'how_to_study'),
    ('procrastination', 'Getting started', 'Starting tasks on time', 'peach', 'clock', 'procrastination'),
    ('stress', 'Stress', 'Handling pressure', 'rose', 'sparkle', 'exam_anxiety'),
    ('sleep', 'Sleep', 'Rest and a regular bedtime', 'lilac', 'moon', 'sleep_health'),
    ('phone', 'Phone', 'Using your phone on purpose', 'mint', 'monitor', 'focus_phone'),
    ('motivation', 'Drive', 'Wanting to study', 'butter', 'flame', 'motivation'),
]

# 14 questions: (id, area, text, reverse)
ITEMS = [
    ('F1', 'focus', 'When I study, my mind wanders after a few minutes.', False),
    ('F2', 'focus', 'I can stay on one task for 25 minutes.', True),
    ('P1', 'procrastination', 'I start homework at the last moment.', False),
    ('P2', 'procrastination', 'When a task feels big, I avoid it.', False),
    ('P3', 'procrastination', 'After I put something off, I am very hard on myself.', False),
    ('S1', 'stress', 'I feel there is too much to do.', False),
    ('S2', 'stress', 'Before tests, worry makes it hard to think.', False),
    ('Z1', 'sleep', 'I go to bed at very different times.', False),
    ('Z2', 'sleep', 'I wake up feeling rested.', True),
    ('Z3', 'sleep', 'I use a phone or screen just before sleep.', False),
    ('H1', 'phone', 'I check my phone while studying, without planning to.', False),
    ('H2', 'phone', 'I lose track of time on videos or chats.', False),
    ('M1', 'motivation', 'I can see how school links to things I care about.', True),
    ('M2', 'motivation', 'It is hard to get going, even on things I want to do.', False),
]
TIE = ['stress', 'sleep', 'procrastination', 'focus', 'phone', 'motivation']

# one private question, never saved: Often or Almost always → the gentle "talk to someone" card
# profiles: id → (name, tagline, about, strengths, watch, first tip)
PROFILES = {
    'overwhelmed_planner': ('The Busy Planner', 'You care a lot. The to-do list feels too big.',
        'You see everything you must do. So starting feels heavy. Your plan makes tasks small and calms your mind.',
        ['You take your work seriously', 'You see the big picture', 'You want to do well'],
        ['Waiting to feel calm before you start', 'Being hard on yourself after a delay'],
        'Pick one task. Write its first 5-minute step on paper.'),
    'night_scroller': ('The Night Scroller', 'Your phone keeps you up at night.',
        'Late-night phone time is very common. Apps are made to be hard to put down. Your plan protects your sleep with small changes.',
        ['You are curious', 'You know what you enjoy', 'You noticed the pattern'],
        ['"Just one more video" at bedtime', 'Sleeping late only on weekends'],
        'Tonight, charge your phone where you cannot reach it from bed.'),
    'busy_multitasker': ('The Multitasker', 'Chats open, videos playing, homework waiting.',
        'You are quick and like variety. But jumping between things tires your focus. Your plan gives you short times with one task only.',
        ['You think fast', 'You handle many things', 'You stay in touch'],
        ['Checking messages "for a second"', 'Studying with the phone on'],
        'Do one 25-minute study time. Put your phone in another room.'),
    'last_minute_sprinter': ('The Last-Minute Runner', 'You finish at the last moment. It costs you.',
        'Deadlines wake you up. You can finish under pressure. But rushing every time is stressful. Your plan helps you start earlier.',
        ['You work well under pressure', 'You get things done', 'You find a way'],
        ['"I will start when I feel like it"', 'Thinking tasks take less time than they do'],
        'Set your own deadline two days before the real one. Tell someone.'),
    'overloaded_juggler': ('The Juggler', 'So much to carry. Little time to breathe.',
        'You carry a lot. Stress means your body is working hard. It does not mean you are failing. Your plan teaches quick ways to calm down.',
        ['You are committed', 'You keep going when it is hard', 'You care about doing well'],
        ['Skipping rest to do more', 'Keeping worries inside'],
        'Before you study, breathe slowly for two minutes.'),
    'curious_wanderer': ('The Wanderer', 'Your mind loves to explore, even while you study.',
        'You are curious. Your mind jumps to new ideas. Your plan helps you park those ideas and come back to the task.',
        ['You are curious', 'You have lots of ideas', 'You notice things'],
        ['Following every new thought', 'Studying with no clear goal'],
        'Keep a "later" list next to you. Write stray thoughts there.'),
    'night_owl': ('The Night Owl', 'You wake up late at night. Mornings are hard.',
        'Your energy comes late. But school starts early. Your plan helps you move your body clock with small steps.',
        ['You can work late', 'You have energy in the evening', 'You notice your rhythm'],
        ['Very late bedtimes', 'Big sleep-ins on weekends'],
        'Pick one wake-up time. Keep it every day, even Sunday.'),
    'notification_magnet': ('The Phone Magnet', 'Every buzz pulls you in.',
        'Phones are made to grab you. That is not your fault. Your plan helps you use your phone when you choose.',
        ['You stay connected', 'You reply fast', 'You know what is going on'],
        ['Phone next to you while studying', 'Checking after every buzz'],
        'Turn off sounds for every app except real people.'),
    'spark_seeker': ('The Spark Seeker', 'You are looking for a reason that makes it click.',
        'Studying feels hard when you do not see why. Your plan helps you find your reason and get small wins.',
        ['You ask "why"', 'You want it to matter', 'You can work hard for things you care about'],
        ['Waiting to feel like studying', 'Giving up after one bad day'],
        'Write one sentence: how can a subject help you or your family?'),
    'steady_builder': ('The Steady Builder', 'You have good habits. You are ready to grow.',
        'Things are going well for you. Your plan keeps your habits strong in busy weeks, like exam time.',
        ['You have good routines', 'You know what works', 'You keep going'],
        ['Dropping habits in exam weeks', 'Doing too much at once'],
        'Pick one habit to protect in your next busy week.'),
}
RULES = {
    'lowThreshold': 35, 'pairMinSecond': 40,
    'pairs': [(['stress', 'procrastination'], 'overwhelmed_planner'), (['phone', 'sleep'], 'night_scroller'), (['focus', 'phone'], 'busy_multitasker')],
    'primary': {'procrastination': 'last_minute_sprinter', 'stress': 'overloaded_juggler', 'focus': 'curious_wanderer',
                'sleep': 'night_owl', 'phone': 'notification_magnet', 'motivation': 'spark_seeker'},
    'fallback': 'steady_builder',
}

# one plain "Why this works" line per technique (the full sources stay in metadata)
WHY = {
    'implementation_intentions': 'A clear "when… then…" plan makes you far more likely to act.',
    'mcii': 'Thinking about the problem before it comes helps you beat it. It was tested with high school students.',
    'task_breakdown': 'Small, clear steps are easier to start. Each one done gives you hope.',
    'timeboxing': 'Short study times with planned breaks keep your mind fresh.',
    'retrieval_spacing': 'Testing yourself, a few days apart, is a top way to learn.',
    'sleep_hygiene': 'Regular sleep times and a calm bedtime help you sleep better.',
    'caffeine_timing': 'Coffee or strong tea, even 6 hours before bed, can cut your sleep.',
    'bedtime_todo': 'Writing tomorrow\'s list helped people fall asleep faster.',
    'sleep_memory': 'Sleep saves what you learned. Less sleep means you forget more.',
    'social_jetlag': 'Very different sleep times on weekends make Monday feel bad.',
    'activity': 'Moving your body helps sleep and lowers worry.',
    'phone_friction': 'A phone close by steals some attention, even when silent.',
    'self_compassion': 'Students who forgave themselves put things off less next time.',
    'procrastination_mood': 'We put things off to escape a bad feeling. It is not laziness.',
    'precommitment': 'Students who set their own small deadlines did better.',
    'temptation_bundling': 'Pairing a dull task with something you enjoy makes it easier to do.',
    'planning_fallacy': 'Most people think tasks take less time than they do. Timing yourself fixes this.',
    'self_monitoring': 'Keeping track of your progress helps you reach your goal.',
    'habit_formation': 'Same time, same place, every day: that is how habits grow.',
    'thought_check': 'Checking a bad thought and finding a fairer one helps you.',
    'growth_mindset': 'Knowing your brain can grow helped many students do better.',
    'stress_reappraisal': 'Seeing a fast heartbeat as "getting ready" helped students in exams.',
    'expressive_writing': 'Writing worries down before a test helped students get better marks.',
    'breathing': 'Slow breathing with a long breath out calms your body in minutes.',
    'worry_time': 'Giving worries a set time stops them filling your whole day.',
    'social_support': 'People you can talk to make stress lighter.',
    'positive_activities': 'Noticing good things and planning small joys lifts your mood.',
    'mindfulness': 'Calm attention to the present moment lowers stress.',
    'autonomy_purpose': 'You try harder when you see why it matters to you.',
    'values_affirmation': 'Writing about what matters to you can lower stress.',
    'struggle_stories': 'Learning that great scientists struggled helped students try harder.',
    'giving_advice': 'Students who gave study tips to others did better themselves.',
    'boredom': 'Practising quiet time helps you handle slow, dull work.',
}

# lessons: (title, text, tiny action, technique[, tool])
L = {}
L['focus'] = [
    ('Focus is like a muscle', 'Focus gets tired. It also grows with practice. Everyone\'s mind wanders. Noticing it is the first skill.', 'Study for 10 minutes. Make a mark each time your mind wanders.', 'self_monitoring'),
    ('One task at a time', 'Jumping between tasks wastes energy. Clear everything else away before you start.', 'Before you study, clear your desk. Write your one task on paper.', 'phone_friction'),
    ('The 25-5 timer', 'Study 25 minutes. Rest 5 minutes. Short blocks keep you sharp.', 'Do one 25-minute study block. Then rest 5 minutes.', 'timeboxing', 'pomodoro'),
    ('Make breaks real breaks', 'A phone break often grows to 40 minutes. Real breaks are short and calm.', 'Write three breaks with no phone. Use one today.', 'timeboxing'),
    ('The "later" list', 'Random thoughts pull you off task. Write them down. Then let them go.', 'Keep a "later" list next to you while you study.', 'implementation_intentions'),
    ('Pick a study spot', 'Places can switch your brain to study mode. A bed says "rest".', 'Choose one study spot. Use it all week.', 'habit_formation'),
    ('Start with a finish line', '"Study maths" is too vague. "Do 10 questions" is clear.', 'Before you study, finish this: "By the end, I will…"', 'task_breakdown'),
    ('Plan for distractions', 'Decide before: "If I want my phone, I write it down instead."', 'Write two "if… then…" plans. Put them where you study.', 'implementation_intentions'),
    ('Test yourself', 'Reading again feels good but teaches little. Close the book and remember.', 'After reading, close the book. Write three things you remember.', 'retrieval_spacing'),
    ('Little and often', 'Short study times over days beat one long night.', 'Plan two short reviews of today\'s topic in the next 3 days.', 'retrieval_spacing', 'spaced'),
    ('Your best hours', 'Focus is easier at some times of day. Do hard work then.', 'Rate your focus from 1 to 5: morning, afternoon, evening.', 'self_monitoring'),
    ('Two blocks in a row', 'One block is easy now. Try two with a longer break.', 'Do two 25-minute blocks. Rest 10 minutes between them.', 'timeboxing', 'pomodoro'),
    ('Quiet or music?', 'Songs with words can fight with reading. Test what works for you.', 'Study once in quiet, once with soft music. Rate each 1 to 5.', 'self_monitoring'),
    ('Move to reset', 'When focus fades, a short walk brings it back.', 'Between study blocks, walk or stretch for 3 minutes.', 'activity'),
    ('Start with the easy part', 'Starting is the hardest part. An easy start gets you moving.', 'Start with 5 minutes on the easiest part.', 'task_breakdown'),
    ('Messages at set times', 'Replying all day breaks your focus. Pick two times for messages.', 'Choose two times today for messages. Ignore them otherwise.', 'phone_friction'),
    ('Focus in class', 'Write notes in your own words. Write your questions too.', 'In one class, write three notes in your words and one question.', 'retrieval_spacing'),
    ('When focus falls apart', 'Bad sessions happen. Stand up. Breathe three times. Start a 10-minute timer.', 'Next time you lose focus: stand, breathe, set 10 minutes.', 'self_compassion'),
    ('Plan your week', 'Put study times in your week like class times.', 'Write three study times for this week in your planner.', 'timeboxing'),
    ('Teach it back', 'Explain a topic out loud, like a teacher. You see what you really know.', 'Explain one thing you learned for 2 minutes, out loud.', 'retrieval_spacing'),
    ('Study groups that work', 'Groups can help or waste time. A goal and a timer keep it useful.', 'With friends, agree on a goal and 25 minutes before chatting.', 'timeboxing'),
    ('Protect study time', 'Tell your family when you study. Put your phone on silent.', 'Put your phone on silent for one study block. Tell someone.', 'phone_friction'),
    ('Look at your progress', 'Compare with Day 1. Small progress counts.', 'Study 10 minutes and mark each wander again. Compare with Day 1.', 'self_monitoring'),
    ('Your focus tools', 'You tried many tools. Keep the three that helped most.', 'Write your top three focus tools in your notebook.', 'habit_formation'),
    ('After Day 30', 'Habits keep growing for weeks. Plans help them last.', 'Write three "if… then…" plans for next month.', 'implementation_intentions'),
]
L['procrastination'] = [
    ('It is not laziness', 'We put things off to escape a bad feeling. Bored? Confused? Scared? Name it.', 'Pick one task you avoid. Name the feeling behind it.', 'procrastination_mood'),
    ('Make the first step tiny', '"Do the project" is too big. "Write the title" is easy.', 'Write a first step under 5 minutes. Do it now.', 'task_breakdown'),
    ('Just 10 minutes', 'Promise only 10 minutes. Once you start, going on is easier.', 'Set 10 minutes on a task you avoid. You may stop after.', 'timeboxing', 'twomin'),
    ('Start at a set time', '"At 4 pm, after tea, I open my notes." No deciding needed.', 'Write when and where you will start tomorrow\'s task.', 'implementation_intentions'),
    ('Forgive yesterday', 'Being hard on yourself adds another bad feeling. Be kind instead.', 'Write one kind sentence about a task you delayed.', 'self_compassion'),
    ('Break a big task up', 'One big task is scary. Five small steps with dates are not.', 'Split one big task into five steps. Give each a day.', 'task_breakdown'),
    ('Write it down', 'Tasks in your head are easy to dodge. Paper makes them real.', 'Write your next three tasks with a time for each.', 'implementation_intentions'),
    ('"I will start when I feel ready"', 'The ready feeling comes after you start, not before.', 'Write one delaying thought. Write a fairer one next to it.', 'thought_check', 'reframe'),
    ('Get ready the night before', 'Looking for a pen or notes becomes a reason to wait.', 'Tonight, put out everything for tomorrow\'s first task.', 'implementation_intentions'),
    ('Reward after, not instead', 'A small treat after studying teaches your brain that starting pays.', 'Pick a small treat. Have it only after one study block.', 'temptation_bundling'),
    ('Start messy', 'Wanting it perfect stops you starting. A first try can be messy.', 'Spend 10 minutes on a rough first try. Messy is fine.', 'self_compassion'),
    ('Set your own deadlines', 'Small deadlines before the real one stop the last-minute rush.', 'Set two small deadlines before your next test or homework.', 'precommitment'),
    ('Wish, picture, problem, plan', 'Picture your goal. Picture what may stop you. Plan for it.', 'For one goal, write: wish, best result, problem, plan.', 'mcii'),
    ('Busy but not studying', 'Tidying your desk can be a way to avoid the real task.', 'Notice today if you do "useful" things to avoid studying.', 'self_monitoring'),
    ('Ask early', 'Being confused makes us wait. Ask a teacher or friend early.', 'Write one question about a task. Ask it today.', 'social_support'),
    ('Tell someone your plan', 'Saying "I start at 5" to someone helps you do it.', 'Tell one person what you will start, and when.', 'precommitment'),
    ('Tick it off', 'Ticks and crossed-out steps keep you going.', 'Tick each small step you finish today.', 'self_monitoring'),
    ('Slipped? Restart today', 'Missing a day does not wipe out your work. Start small today.', 'Do a 5-minute restart step now.', 'self_compassion'),
    ('See yourself finished', 'Picture the evening after the task is done. How does it feel?', 'Picture finishing for 3 minutes. Write one problem and one plan.', 'mcii'),
    ('Pair the boring with the nice', 'Do the dull task in your favourite spot, or with tea.', 'Choose one treat you only have while studying. Use it today.', 'temptation_bundling'),
    ('How long will it really take?', 'Tasks take longer than we think. Time yourself.', 'Guess how long one task takes. Time it. Compare.', 'planning_fallacy'),
    ('Say no to one thing', 'Sometimes there is just too much. Drop one small thing.', 'Pick one thing to say no to, or move, this week.', 'task_breakdown'),
    ('Spot your pattern', 'When and where do you put things off? Patterns show fixes.', 'Write your top two delay times and one fix for each.', 'self_monitoring'),
    ('Your start routine', 'Join your best tools: phone away, 10-minute timer, tiny step.', 'Write your 3-step start routine. Use it once today.', 'habit_formation'),
    ('After Day 30', 'Plans keep your new skills going.', 'Write three "if… then…" plans for next month.', 'implementation_intentions'),
]
L['stress'] = [
    ('Stress means "getting ready"', 'A fast heart before a test is your body getting ready. It does not mean you will fail.', 'When stressed, say: "My body is getting ready to help me."', 'stress_reappraisal'),
    ('Breathe out long', 'Breathe in slowly. Breathe out even longer. Your body calms down.', 'Do 2 minutes of slow breathing today.', 'breathing', 'breath478'),
    ('Empty your head', 'Write every worry on paper. Your mind gets more space.', 'Write all your worries for 5 minutes. Nobody will see it.', 'expressive_writing'),
    ('What can I change?', 'Some worries you can change. Some you cannot. Work on the first kind.', 'Draw two circles: "I can change" and "I cannot". Sort your worries.', 'thought_check'),
    ('"What if everything goes wrong?"', 'Stress loves the worst case. Check the facts. Find a fairer thought.', 'Write one worried thought, the facts, and a fairer thought.', 'thought_check', 'reframe'),
    ('Top three for tomorrow', 'When everything feels urgent, pick just three.', 'Tonight, write the three most important things for tomorrow.', 'task_breakdown'),
    ('Stress and sleep', 'Stress makes sleep hard. Bad sleep makes stress bigger.', 'Tonight, start calming down 30 minutes before bed.', 'sleep_hygiene'),
    ('Move it out', 'A short walk can take the edge off stress.', 'Walk or play for 10 minutes today.', 'activity'),
    ('Talk it out', 'Talking to someone you trust makes stress lighter.', 'Talk to one person you trust about how things are.', 'social_support'),
    ('Talk to yourself like a friend', 'Would you call a friend "useless"? Be kind to yourself too.', 'Write what you would tell a friend. Read it to yourself.', 'self_compassion'),
    ('Your test-nerves plan', 'Before a test: write worries, breathe slowly, say "I am ready".', 'Write your 3-step plan for your next test.', 'expressive_writing'),
    ('Plan a small joy', 'Small happy moments are not wasted time. They give you energy.', 'Plan one small thing you enjoy. Do it today or tomorrow.', 'positive_activities'),
    ('A finish time for study', 'Studying until you drop raises stress. Pick a time to stop.', 'Choose a "study ends at" time tonight. Keep it.', 'timeboxing'),
    ('The comparison trap', 'Others show only their good side. You see all of yours.', 'Notice one comparison thought. Write a fairer one.', 'thought_check'),
    ('High goals, kind voice', 'You can aim high and still be kind to yourself.', 'Rewrite one harsh thing you told yourself. Make it kind and true.', 'self_compassion'),
    ('Ask for what you need', 'Asking for help is a skill, not a weakness.', 'Write a short message asking a teacher or friend for help.', 'social_support'),
    ('One calm minute', 'Notice your breath, the sounds, your feet on the floor.', 'For 3 minutes, notice your breath and the sounds around you.', 'mindfulness'),
    ('Your warning signs', 'A tight jaw? Snapping at people? Bad sleep? Spot stress early.', 'List three stress signs. Write one helpful action for each.', 'self_monitoring'),
    ('Worry time', 'Give worries 15 minutes a day. At other times, write them down for later.', 'Pick a 15-minute worry time today. Use it.', 'worry_time'),
    ('Balance check', 'Study, rest, family and fun. Is one pushing out the others?', 'Rate your week 1 to 5 for study, rest, people and fun.', 'self_monitoring'),
    ('A bad day is information', 'A bad mark does not say who you are. It shows what to fix.', 'Write about one setback: what happened, what you learned, next step.', 'growth_mindset'),
    ('Three good things', 'Writing three good things each day lifts your mood.', 'Tonight, write three good things from today.', 'positive_activities'),
    ('Your calm kit', 'List what calms you. Breathing, a walk, a person, a song.', 'Write your calm kit list. Keep it in your notebook.', 'habit_formation'),
    ('Who is on your team?', 'Family, friends, teachers and the school counsellor can help.', 'Write three people you can talk to, and how to reach them.', 'social_support'),
    ('After Day 30', 'Plans keep your calm skills going.', 'Write three plans. Example: "If it feels too much, I list my top three."', 'implementation_intentions'),
]
L['sleep'] = [
    ('How much sleep you need', 'Teenagers need 8 to 10 hours. Most students get less.', 'Tonight, write when you go to bed and when you wake.', 'sleep_hygiene'),
    ('Wake up at the same time', 'A steady wake-up time sets your body clock.', 'Choose a wake-up time. Keep it every day, even Sunday.', 'sleep_hygiene'),
    ('30 minutes to slow down', 'Your brain needs time to land. Wash, read, or talk quietly.', 'Plan three calm steps for before bed. Try them tonight.', 'sleep_hygiene'),
    ('Phones and bedtime', 'A phone in bed keeps your brain awake. Charge it far away.', 'Tonight, charge your phone where you cannot reach it from bed.', 'phone_friction'),
    ('No coffee late', 'Coffee or strong tea late in the day steals sleep. Have it in the morning.', 'Pick a time today after which you have no coffee.', 'caffeine_timing'),
    ('List before bed', 'Write tomorrow\'s list before bed. Your mind can rest.', 'Tonight, write a short list for tomorrow.', 'bedtime_todo'),
    ('Morning sun', 'Daylight after waking sets your body clock.', 'Get 10 minutes of daylight within an hour of waking.', 'sleep_hygiene'),
    ('Bed is for sleep', 'If you study in bed, your brain learns bed means awake.', 'Today, study at a table, not on your bed.', 'sleep_hygiene'),
    ('Short naps only', 'A short nap before 3 pm can help. Long naps spoil the night.', 'If you nap today, keep it under 30 minutes.', 'sleep_hygiene'),
    ('Cannot sleep? Get up', 'After 20 minutes awake, get up. Do something calm. Then try again.', 'Decide what calm thing you will do if you cannot sleep.', 'sleep_hygiene'),
    ('No all-night study', 'Sleep saves what you learned. Studying all night means you forget more.', 'Plan your sleep for your next busy week. No all-nighters.', 'sleep_memory'),
    ('The weekend trap', 'Sleeping very late on weekends makes Monday feel awful.', 'Plan this weekend\'s sleep within an hour of school days.', 'social_jetlag'),
    ('Cool, dark, quiet', 'A cool, dark, quiet room helps you sleep.', 'Make one change to your sleeping place tonight.', 'sleep_hygiene'),
    ('Worries at bedtime', 'Give worries an earlier time. Write them down before bed.', 'Write your worries for 5 minutes, an hour before bed.', 'worry_time'),
    ('Move by day, sleep by night', 'Moving in the day helps you sleep at night.', 'Walk, run or play for 20 minutes today.', 'activity'),
    ('Late food', 'A big meal right before bed can spoil your sleep.', 'Eat your big meal 2 to 3 hours before bed tonight.', 'sleep_hygiene'),
    ('Look at your sleep notes', 'Your notes show patterns since Day 1.', 'Write your usual bedtime, wake time, and one pattern.', 'self_monitoring'),
    ('Move bedtime slowly', 'Big changes do not last. Move bedtime 15 minutes earlier.', 'Go to bed 15 minutes earlier tonight.', 'sleep_hygiene'),
    ('Sleep and mood', 'Many people feel cross or stressed after short nights.', 'Rate your mood 1 to 5. Write how many hours you slept.', 'self_monitoring'),
    ('Exam-time sleep plan', 'In exam time, sleep matters most. Plan it now.', 'Write your exam-time plan: bedtime, calm time, no late coffee.', 'sleep_memory'),
    ('After a late night', 'Weddings and holidays mean late nights. Wake at your usual time anyway.', 'Write your plan for the day after a late night.', 'social_jetlag'),
    ('"Just one more video"', 'Videos are made to keep you watching. Plan a stop.', 'Write: "If a video ends after 10 pm, I stop."', 'implementation_intentions'),
    ('When to tell someone', 'If sleep stays hard for weeks, tell a parent, teacher or nurse.', 'Write who you would talk to if sleep stays hard.', 'social_support'),
    ('Your sleep card', 'Put your best sleep habits on one card.', 'Write your card: wake time, calm time, phone spot, coffee time.', 'habit_formation'),
    ('After Day 30', 'Plans keep your sleep rhythm going.', 'Write three "if… then…" plans for your sleep next month.', 'implementation_intentions'),
]
L['phone'] = [
    ('Your phone is not the enemy', 'Phones are useful. Many apps are made to grab you. Use it on purpose.', 'Write how long you used your phone today, and on what.', 'self_monitoring'),
    ('Out of sight', 'A phone on the desk takes attention, even when quiet.', 'For one study time, put your phone in another room.', 'phone_friction'),
    ('Fewer buzzes', 'Every buzz pulls at your attention. Fewer sounds, fewer breaks.', 'Turn off sounds for apps that are not real people.', 'phone_friction'),
    ('Make it a bit harder', 'Move tempting apps off the first screen. You open them less.', 'Move your two most distracting apps into a folder.', 'phone_friction'),
    ('Plan for the urge', '"If I reach for my phone, I take one breath and keep going."', 'Write one "if… then…" plan for phone urges. Use it today.', 'implementation_intentions'),
    ('Phone-free mornings', 'Messages first thing make you rush. Start the day calm.', 'Tomorrow, wait 20 minutes after waking before you check your phone.', 'habit_formation'),
    ('Swap, do not just stop', 'If you stop scrolling with nothing to do, the urge comes back.', 'Write three things to do instead of scrolling when bored.', 'implementation_intentions'),
    ('Set a time limit', 'A limit makes you stop and choose.', 'Set a daily limit for your most-used app.', 'phone_friction'),
    ('Grey screen test', 'A grey screen makes colourful apps less tempting.', 'Turn your screen grey for one day. Notice the change.', 'phone_friction'),
    ('Clean your feed', 'Some accounts make you feel worse. You can mute them.', 'Mute five accounts or groups that make you feel bad.', 'thought_check'),
    ('Phone-free people time', 'A phone on the table takes away from talking.', 'Have one meal or coffee time today with no phone.', 'phone_friction'),
    ('Park your phone at night', 'A phone in bed pushes sleep later.', 'Tonight, charge your phone away from your bed.', 'sleep_hygiene'),
    ('Check at set times', 'Checking all day breaks your day into pieces.', 'Pick three times today to check messages.', 'timeboxing'),
    ('"I will miss something!"', 'It feels true. It is rarely true. Messages wait.', 'Write: "Important messages will still be there in 25 minutes."', 'thought_check', 'reframe'),
    ('Study mode', 'Turn on silent or flight mode while you study. 4 works offline.', 'Turn on flight mode for one study block.', 'phone_friction', 'pomodoro'),
    ('Tell your friends', 'Tell friends when you are studying. They will not wait for fast replies.', 'Tell your group chat when you will be offline today.', 'precommitment'),
    ('Count the urges', 'When do you want your phone? Bored? Stuck? Worried?', 'Count your phone urges in one study time. Note why.', 'self_monitoring'),
    ('Slip without a spiral', 'Lost an evening to your phone? It happens. Be kind. Try again.', 'If you slip, write one kind sentence and one plan for tomorrow.', 'self_compassion'),
    ('Screens off time', 'Pick a time each evening when screens go off.', 'Choose a screens-off time tonight. Keep it.', 'sleep_hygiene'),
    ('Make your phone your helper', 'Use it for good: study timer, reminders, alarm.', 'Set two reminders: "start studying" and "get ready for bed".', 'implementation_intentions'),
    ('Busy group chats', 'Mute busy groups. Check them at set times.', 'Mute one busy group chat today.', 'phone_friction'),
    ('Five minutes of nothing', 'Sitting with your thoughts is hard. Practice makes slow work easier.', 'Sit 5 minutes with no phone and no music. Notice what happens.', 'boredom'),
    ('Compare with Day 1', 'Look at your phone time now. What changed?', 'Write your phone time now and one thing that helped.', 'self_monitoring'),
    ('Your phone rules', 'Turn what worked into a few simple rules.', 'Write three phone rules, like "phone stays away while I study".', 'habit_formation'),
    ('After Day 30', 'Plans keep your balance.', 'Write three "if… then…" plans for your phone next month.', 'implementation_intentions'),
]
L['motivation'] = [
    ('Doing comes first', 'We wait to feel like it. But the feeling comes after we start.', 'Pick one goal. Do a 2-minute version today.', 'habit_formation', 'twomin'),
    ('Find your reason', 'Link school to what you care about: a job, your family, your village.', 'Write two sentences: how can one subject help you or others?', 'autonomy_purpose', 'goal'),
    ('Your choice', 'Feeling in charge helps. Even choosing the first task helps.', 'Today, choose the order of your tasks yourself.', 'autonomy_purpose'),
    ('Your brain can grow', 'Skills grow with effort, good methods and help.', 'Write about one skill you got better at by practice.', 'growth_mindset'),
    ('Count small wins', 'Small progress keeps you going. Write it down.', 'Write three small wins from today.', 'self_monitoring'),
    ('Wish, picture, problem, plan', 'Picture your goal. Picture what may stop you. Plan for it.', 'For one goal, write: wish, best result, problem, plan.', 'mcii'),
    ('Join it to a habit', '"After dinner, I read my notes for 10 minutes."', 'Write one "after… I will…" sentence. Try it today.', 'implementation_intentions'),
    ('Better together', 'Studying with a friend makes it less lonely.', 'Ask one friend to study with you this week.', 'social_support'),
    ('"Not yet"', '"I am bad at maths" shuts the door. "Not yet" keeps it open.', 'Change one "I can\'t" into "I can\'t yet. I can try…"', 'growth_mindset', 'reframe'),
    ('Why it matters to you', 'How could today\'s topic help in real life? On the farm? At home?', 'Write a few lines: how is today\'s topic useful in your life?', 'autonomy_purpose'),
    ('Rewards that help', 'A small treat after studying makes starting easier.', 'Pick a small treat for after one study task today.', 'temptation_bundling'),
    ('No-energy days', 'Some days you will not feel it. Do 10 minutes anyway.', 'Today, do just 10 minutes of something on your list.', 'timeboxing'),
    ('Big goal, small steps', 'Link your matric goal to this week\'s small steps.', 'Write one big goal. Write three steps for this week.', 'task_breakdown', 'goal'),
    ('See how you grew', 'Seeing your skills grow gives you energy.', 'Compare something you can do now with a month ago.', 'autonomy_purpose'),
    ('Mistakes teach', 'Every mistake shows what to practise next.', 'Look at one mistake. Write what it teaches you.', 'growth_mindset'),
    ('Fuel your body', 'Low energy can feel like no motivation. Sleep, food and water matter.', 'Fix one basic today: sleep, water, food or a walk.', 'activity'),
    ('Even great people struggled', 'Famous scientists failed many times before they succeeded.', 'Think of someone you admire who struggled first.', 'struggle_stories'),
    ('Bigger than you', 'Learning can help others: your family, your village, your country.', 'Write one way your learning could help others one day.', 'autonomy_purpose'),
    ('What matters most to you', 'Writing about what you value lowers stress.', 'Write for 5 minutes about something that really matters to you.', 'values_affirmation'),
    ('Plan for low days', 'Low days will come. Plan a small version now.', 'Write: "If I feel low, I will do 10 minutes of…"', 'implementation_intentions'),
    ('Celebrate', 'You are three weeks in. Be proud of your effort.', 'Celebrate in a small way. Write what you are proud of.', 'positive_activities'),
    ('Help someone else', 'Students who gave study tips to younger students did better too.', 'Share one study tip with a brother, sister or classmate.', 'giving_advice'),
    ('Look back', 'What gave you energy these weeks? What took it away?', 'Write two things that helped and one that drained you.', 'self_monitoring'),
    ('Your drive kit', 'Keep your best tools in one place: your reason, small steps, rewards.', 'Write your list of drive tools in your notebook.', 'habit_formation'),
    ('After Day 30', 'Plans keep you going.', 'Write three "if… then…" plans for next month.', 'implementation_intentions'),
]

REFLECT = {
    'title': 'Week {w}: look back',
    'text': 'Take 5 minutes. What worked this week? Keep doing it.',
    'prompts': [('well', 'What went well this week?'), ('hard', 'What got in the way?'), ('next', 'One thing to try next week:')],
    'mood': {'text': 'How was your week?', 'labels': ['Very hard', 'Hard', 'Okay', 'Good', 'Great']},
}
RECHECK = {'title': 'Day 30: see how far you came', 'text': 'You made it! Take the same check-in again. Compare it with Day 1. Any change counts.'}

LONG = 13
PROBLEMS = []


def check_plain(s, where):
    for sen in re.split(r'(?:(?<=[.!?…])|(?<=[.!?…]["”]))\s+', s):
        n = len(re.findall(r"[A-Za-z0-9'’%-]+", sen))
        if n > LONG:
            PROBLEMS.append(f'too long ({n} words) in {where}: {sen}')
    for w in ('diagnos', 'disorder', 'depress', 'adhd', 'anxiety disorder', 'symptom', 'addict', 'trauma', 'insomnia'):
        if w in s.lower():
            PROBLEMS.append(f'clinical word "{w}" in {where}: {s}')


def build():
    assert len(ITEMS) == 14 and {a for _, a, _, _ in ITEMS} == {a[0] for a in AREAS}
    for k, ls in L.items():
        assert len(ls) == 25, (k, len(ls))
    lessons = {}
    for k, ls in L.items():
        out = []
        for i, l in enumerate(ls, 1):
            title, text, action, tech = l[:4]
            assert tech in WHY and tech in SOURCES, (k, i, tech)
            d = {'id': f'{k}-{i:02d}', 'n': i, 'title': title, 'text': text, 'action': action, 'why': WHY[tech], 'technique': tech}
            if len(l) > 4:
                d['tool'] = l[4]
            out.append(d)
        lessons[k] = out
    profiles = []
    for pid, (name, tag, about, strengths, watch, tip) in PROFILES.items():
        profiles.append({'id': pid, 'name': name, 'tagline': tag, 'about': about, 'strengths': strengths, 'watch': watch, 'tip': tip})
    d = {
        'source': 'Adapted from the Focus30 design (student self-help app, Oct 2026), rewritten for Four.',
        'checkin': {
            'title': 'Study check-in',
            'intro': '14 quick questions. Think about the last two weeks. There are no right or wrong answers. This is not a test.',
            'scale': SCALE,
            'areas': [{'id': i, 'name': n, 'short': s, 'tone': t, 'icon': ic, 'topic': tp} for i, n, s, t, ic, tp in AREAS],
            'items': [{'id': i, 'area': a, 'text': t, 'reverse': r} for i, a, t, r in ITEMS],
            'tieBreak': TIE,
            'bands': [{'max': 34, 'label': 'Going well'}, {'max': 59, 'label': 'Room to grow'}, {'max': 100, 'label': 'Focus here'}],
            'betterBy': 15,
        },
        'profiles': profiles,
        'rules': {**RULES, 'pairs': [{'pair': p, 'profile': q} for p, q in RULES['pairs']]},
        'plan': {
            'days': 30, 'reflectDays': [7, 14, 21, 28], 'recheckDay': 30,
            'intro': 'One short lesson and one tiny action a day. About 5 minutes. Missed a day? Just carry on.',
            'reflect': {**REFLECT, 'prompts': [{'id': i, 'text': t} for i, t in REFLECT['prompts']]},
            'recheck': RECHECK,
        },
        'lessons': lessons,
        'techniques': {k: {'name': v['name'], 'why': WHY[k], 'sources': v['sources']} for k, v in SOURCES.items() if k in WHY},
    }
    # plain-English lint over everything a student reads
    def walk(o, where):
        if isinstance(o, str):
            check_plain(o, where)
        elif isinstance(o, list):
            for i, x in enumerate(o):
                walk(x, f'{where}[{i}]')
        elif isinstance(o, dict):
            for k, v in o.items():
                if k not in ('techniques', 'source', 'id', 'technique', 'tool', 'tone', 'icon', 'topic', 'area', 'profile', 'primary', 'fallback', 'pair', 'tieBreak'):
                    walk(v, f'{where}.{k}')
    walk({k: v for k, v in d.items() if k != 'techniques'}, 'plan')
    if PROBLEMS:
        raise SystemExit('\n'.join(PROBLEMS))
    return json.dumps(d, ensure_ascii=False, indent=1) + '\n'


if __name__ == '__main__':
    s = build()
    if '--check' in sys.argv:
        if not os.path.exists(OUT) or open(OUT, encoding='utf-8').read() != s:
            raise SystemExit('plan.json is out of date: run python3 tool/study_coach/build_plan.py')
        print('plan.json up to date')
    else:
        open(OUT, 'w', encoding='utf-8').write(s)
        print(f'wrote {os.path.relpath(OUT)} ({sum(len(v) for v in L.values())} lessons, {len(PROFILES)} profiles)')
