#!/usr/bin/env python3
"""Builds the High design reference: the built Warsay Prep preview (/workspace/examprep/preview/index.html, read-only)
+ the 3D clay layer (design/clay3d.css) + High's navigation (Home · Exams · Notes · Mistakes · Settings), branding,
Settings page and the Notes entry card.  Output: /workspace/high/design/reference.html
    python3 tool/build_reference.py [src] [out]"""
import os, sys
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = sys.argv[1] if len(sys.argv) > 1 else '/workspace/examprep/preview/index.html'
OUT = sys.argv[2] if len(sys.argv) > 2 else '/workspace/high/design/reference.html'
html = open(SRC, encoding='utf-8').read()
css = open(os.path.join(HERE, 'design', 'clay3d.css'), encoding='utf-8').read()
css += "\n.card .kv:first-child{border-top:0}\n"

# the head (CSS) and the app script are patched separately so nothing inside the inlined content can match
i = html.index('<script id="pack-data"'); j = html.index('</script>', i) + len('</script>')
head, data, tail = html[:i], html[i:j], html[j:]

def rep(s, a, b, n=1):
    c = s.count(a)
    assert c == n, f'expected {n} x {a[:70]!r}, found {c}'
    return s.replace(a, b)

k = head.index('</style>\n</head>')
head = head[:k] + css + head[k:]
head = rep(head, '<title>Warsay Prep – Grade 12 matric practice (offline preview)</title>', '<title>High – design reference (Warsay Prep + 3D clay)</title>')

t = tail
t = rep(t, "const KEY = 'warsayprep:v2';", "const KEY = 'high:v1';")
t = rep(t, "  zoom: '", "  sliders: '<path d=\"M4 7h9M18 7h2M4 17h4M13 17h7\"/><circle cx=\"15.5\" cy=\"7\" r=\"2.5\"/><circle cx=\"10.5\" cy=\"17\" r=\"2.5\"/>',\n  zoom: '")
t = rep(t, "if (m) m.onclick = profileSheet;", "if (m) m.onclick = () => { hist = []; go('settings', {}, {push: false}); };")
t = rep(t, "Warsay Prep<span class=\"sub\">Grade 12 · Sawa matric practice</span>", "High<span class=\"sub\">Grade 9–12 · matric prep &amp; notes</span>")
t = rep(t, "const TAB_OF = {home: 'home', weak: 'home', subjects: 'subjects', subject: 'subjects', exam: 'subjects', timed: 'subjects', quiz: '', review: 'review', tutor: 'tutor'};",
        "const TAB_OF = {home: 'home', weak: 'home', subjects: 'subjects', subject: 'subjects', exam: 'subjects', timed: 'subjects', quiz: '', review: 'review', tutor: 'home', notes: 'notes', settings: 'settings'};")
t = rep(t, "const NAV = [['home', 'home', 'Home'], ['subjects', 'grid', 'Subjects'], ['review', 'bookmark', 'Review'], ['tutor', 'chat', 'Tutor']];",
        "const NAV = [['home', 'home', 'Home'], ['subjects', 'grid', 'Exams'], ['notes', 'book', 'Notes'], ['review', 'repeat', 'Mistakes'], ['settings', 'sliders', 'Settings']];")
t = rep(t, "review: renderReview, weak: renderWeak, tutor: renderTutor})[name]();", "review: renderReview, weak: renderWeak, tutor: renderTutor, notes: renderNotes, settings: renderSettings})[name]();")
t = rep(t, "tabTop('Subjects', ", "tabTop('Exams', ")
t = rep(t, "tabTop('Review', 'Bookmarks & mistakes · all subjects');", "tabTop('Mistakes', 'Mistakes & bookmarks · all subjects');")
t = rep(t, "let rtab = 'bm', rcat = 'all';", "let rtab = 'mi', rcat = 'all';")
t = rep(t, """<div class="seg"><button class="press ${rtab === 'bm' ? 'on' : ''}" data-t="bm">${ic('bookmark')}Bookmarks <span class="c">${bms.length}</span></button><button class="press ${rtab === 'mi' ? 'on' : ''}" data-t="mi">${ic('x')}Mistakes <span class="c">${mis.length}</span></button></div>""",
        """<div class="seg"><button class="press ${rtab === 'mi' ? 'on' : ''}" data-t="mi">${ic('x')}Mistakes <span class="c">${mis.length}</span></button><button class="press ${rtab === 'bm' ? 'on' : ''}" data-t="bm">${ic('bookmark')}Bookmarks <span class="c">${bms.length}</span></button></div>""")
t = rep(t, '<div class="cats-h"><h3>Exam categories</h3><span>Choose where to practise</span></div>', '<div class="cats-h"><h3>Exams &amp; notes</h3><span>Choose where to study</span></div>')
t = rep(t, """<span class="go">Open${ic('right')}</span></div></button>`; }).join('')}</div></section>""",
        """<span class="go">Open${ic('right')}</span></div></button>`; }).join('')}${notesCard()}</div></section>""")
t = rep(t, """<span class="btn tone t-sage">Explore now</span></section>""",
        """<span class="btn tone t-sage">Explore now</span></section>
  <section class="tile banner t-lilac press" id="askTutor" role="button" style="background:linear-gradient(135deg,var(--lilac),color-mix(in srgb,var(--lilac) 70%,var(--blue)))"><div class="mascot kokob-float">${ART.kokob()}</div><div class="t">Ask Kokob, your tutor<span>Offline answers from your exam packs</span></div><span class="btn tone t-lilac">Ask now</span></section>""")
t = rep(t, "  $('#weak').onclick = () => go('weak');\n",
        "  $('#weak').onclick = () => go('weak');\n  $('#askTutor').onclick = () => go('tutor');\n  $$('[data-home-notes]').forEach(b => b.onclick = () => { hist = []; go('notes', {}, {push: false}); });\n")
t = rep(t, "else go(['subjects', 'review', 'weak'].includes(k) ? k : 'home', {}, {push: false});", "else go(['subjects', 'review', 'weak', 'notes', 'settings'].includes(k) ? k : 'home', {}, {push: false});")

EXTRA = r"""
// ================================================================ High additions (design reference only)
const NOTES_INFO = {grades: 4, subjects: 8, books: 29};
function notesCard(){
  return `<button class="tile cat press t-blue" data-home-notes aria-label="Open Grade 9–12 notes">${badge('blue', 'book', 56)}<div class="ct"><b>Grade 9–12 Notes</b><span class="sub">Textbook notes · concept maps · games</span></div>
      <div class="cnts"><span>${NOTES_INFO.grades} grades</span><span>${NOTES_INFO.subjects} subjects</span><span>${NOTES_INFO.books} books</span></div>
      <div class="prog"><div class="bar"><i style="width:0%"></i></div><em>Not started</em><span class="go">Open${ic('right')}</span></div></button>`;
}
function renderNotes(){
  tabTop('Notes', 'Grade 9–12 · textbook notes');
  screen.innerHTML = `<div class="card empty">${ART.sprout()}<b>Notes</b>The native app renders the Grade 9–12 notes here.</div>`;
}
function renderSettings(){
  tabTop('Settings', 'Profile, theme & progress');
  const st = stats(), cur = S.theme || 'auto', nm = S.name || 'Student';
  const kv = (k, v) => `<div class="kv"><span>${k}</span><b>${v}</b></div>`;
  const nQ = EXAMS.reduce((a, e) => a + e.questions.length, 0);
  screen.innerHTML = `<div class="stagger">
  <section class="card"><div class="prof"><div class="avatar">${esc(nm.trim()[0].toUpperCase())}</div><div style="flex:1;min-width:0"><b>${esc(nm)}</b><span>Grade 9–12 · Warsay Yikealo Secondary School, Sawa</span></div></div>
    <label class="muted" for="nm" style="display:block;margin:16px 0 0 4px">Your name</label><input class="field" id="nm" maxlength="24" value="${esc(S.name || '')}" placeholder="Student" style="margin-bottom:12px">
    <button class="btn coral block press" id="saveMe">${ic('check')}Save name</button></section>
  <div class="section-label">Appearance</div>
  <section class="card" style="padding:12px"><div class="seg">${['light', 'dark', 'auto'].map(t => `<button class="press ${cur === t ? 'on' : ''}" data-th="${t}">${ic(t === 'light' ? 'sun' : t === 'dark' ? 'moon' : 'sparkle')}${t[0].toUpperCase() + t.slice(1)}</button>`).join('')}</div></section>
  <div class="section-label">Your progress</div>
  <section class="card" style="padding:4px 16px 4px">${kv('Questions answered', st.answered)}${kv('Accuracy', st.acc == null ? '—' : st.acc + '%')}${kv('Best streak', st.best + ' day' + (st.best === 1 ? '' : 's'))}${kv('Total study time', fmtDur(st.studyAll))}${kv('Mistakes to retry', S.mistakes.filter(id => byId[id]).length)}${kv('Bookmarks', S.bookmarks.filter(id => byId[id]).length)}</section>
  <div class="section-label">Content</div>
  <section class="card" style="padding:4px 16px 4px">${kv('Exams', `${EXAMS.length} exams · ${SUBJECTS.length} subjects`)}${kv('Categories', CATS.map(c => `${catExams(c.id).length} ${c.label.toLowerCase()}`).join(' · '))}${kv('Questions', nQ.toLocaleString('en'))}${kv('Notes', `Grade 9–12 · ${NOTES_INFO.subjects} subjects`)}</section>
  <section class="card"><div class="setrow">${badge('peach', 'repeat', 40)}<div class="t"><b>Reset progress</b><span>Clears answers, mistakes and bookmarks</span></div><button class="btn soft press" id="reset" style="padding:10px 14px;font-size:13px">Reset</button></div></section>
  <div class="muted" style="text-align:center;margin:18px 0 0">High · works fully offline</div></div>`;
  $$('[data-th]').forEach(b => b.onclick = () => { S.theme = b.dataset.th === 'auto' ? null : b.dataset.th; save(); applyTheme(); rerender(); });
  $('#saveMe').onclick = () => { S.name = $('#nm').value.trim().slice(0, 24) || 'Student'; save(); rerender(); toast('Saved ✓'); };
  const r = $('#reset'); r.onclick = () => { if (r.dataset.sure) { Object.assign(S, {answers: {}, bookmarks: [], mistakes: [], ev: [], study: {}, recent: [], attempts: [], daily: {}}); save(); rerender(); toast('Progress reset'); } else { r.dataset.sure = 1; r.textContent = 'Tap again'; r.style.color = 'var(--peach-3)'; } };
}
"""
t = rep(t, "// ================================================================ profile & onboarding sheets", EXTRA + "// ================================================================ profile & onboarding sheets")
os.makedirs(os.path.dirname(OUT), exist_ok=True)
open(OUT, 'w', encoding='utf-8').write(head + data + t)
print('wrote', OUT, len(head + data + t) // 1024, 'KB')
