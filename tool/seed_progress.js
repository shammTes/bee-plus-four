() => {
  // deterministic progress spread over the last 10 days (same idea as examprep/tools/screenshots.py), recorded by the app's own API
  const A = window.APP, S = A.S, now = Date.now(), DAY = 864e5;
  const mcq = A.EXAMS.flatMap(e => e.questions.filter(q => q.type === 'mcq' && q.options && Object.keys(q.options).length > 1));
  const per = [6, 9, 0, 12, 8, 14, 11];
  let k = 0;
  for (let d = 9; d >= 7; d--) for (let j = 0; j < 3 - (d % 2); j++) { const q = mcq[(40 + d * 3 + j) % mcq.length]; const L = Object.keys(q.options);
    A.record(q, j === 1 ? L.find(l => l !== q.answer) : q.answer, 'practice', now - d * DAY - j * 60e3); }
  per.forEach((n, i) => { const day = 6 - i;
    for (let j = 0; j < n; j++, k++) { const q = mcq[(k * 7) % mcq.length]; const wrong = (k % 4 === 1) || (k % 9 === 4);
      const letters = Object.keys(q.options); const c = wrong ? letters.find(l => !(q.accepted_answers || [q.answer]).includes(l)) : q.answer;
      const t = now - day * DAY - (n - j) * 90e3 - 3600e3 * (day ? 3 : 0.2); A.record(q, c, j % 3 ? 'practice' : 'quiz', t); }
    if (n) { const d = new Date(now - day * DAY); const key = d.getFullYear() + '-' + String(d.getMonth() + 1).padStart(2, '0') + '-' + String(d.getDate()).padStart(2, '0'); S.study[key] = n * 75; } });
  S.bookmarks.push(mcq[5].id, mcq[18].id, mcq[33].id);
  A.save();
}
