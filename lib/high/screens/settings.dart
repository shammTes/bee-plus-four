// Settings tab: profile + name, appearance, progress summary, content summary, reset.
import 'package:flutter/widgets.dart';

import '../data/models.dart';
import '../state/app_state.dart';
import '../theme/tokens.dart';
import '../media/media.dart' show CreditsPage, MediaLib;
import '../widgets/kit.dart';
import '../widgets/page.dart';
import '../teacher/teacher.dart' show TeacherPage;
import 'home.dart' show Stagger;
import 'toast.dart';

class SettingsPage extends StatefulWidget {
  const SettingsPage({super.key, this.controller});
  final ScrollController? controller;
  @override
  State<SettingsPage> createState() => _SettingsPageState();
}

class _SettingsPageState extends State<SettingsPage> {
  late final TextEditingController _nm = TextEditingController(text: HighScope.read(context).name ?? '');
  bool _sure = false;
  @override
  void dispose() {
    _nm.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final k = Kit.of(context), p = k.p, s = k.s, r = s.repo;
    final st = s.stats(), cur = s.theme ?? 'auto', nm = s.name ?? 'Student';
    final nQ = r.exams.fold(0, (a, e) => a + e.questions.length);
    Widget kv(String a, String b, bool first) => DecoratedBox(
      decoration: BoxDecoration(border: first ? null : Border(top: BorderSide(color: p.line, width: 1))),
      child: Padding(
        padding: EdgeInsets.fromLTRB(2, first ? 10 : 11, 2, 10),
        child: Row(
          children: [
            Text(a, style: ts(13.5, w800, p.ink2)),
            const SizedBox(width: 12),
            Expanded(child: Text(b, textAlign: TextAlign.right, style: ts(13.5, w800, p.ink))),
          ],
        ),
      ),
    );
    Widget kvCard(List<(String, String)> l) => Panel(
      padding: const EdgeInsets.fromLTRB(16, 4, 16, 4),
      child: Column(children: [for (var i = 0; i < l.length; i++) kv(l[i].$1, l[i].$2, i == 0)]),
    );
    return PageShell(
      top: const TopBar(title: 'Settings', sub: 'Profile, theme & progress'),
      body: ScreenList(
        controller: widget.controller,
        children: Stagger.wrap([
          Panel(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: [
                Row(
                  spacing: 14,
                  children: [
                    const Avatar(size: 64, fontSize: 27),
                    Expanded(
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text(nm, style: ts(19, w900, p.ink), maxLines: 1, overflow: TextOverflow.ellipsis),
                          const SizedBox(height: 2),
                          Text('Grade 9–12 · Warsay Yikealo Secondary School, Sawa', style: ts(12.5, w700, p.ink3)),
                        ],
                      ),
                    ),
                  ],
                ),
                Padding(
                  padding: const EdgeInsets.fromLTRB(4, 16, 0, 0),
                  child: Text('Your name', style: ts(12.5, w700, p.ink3)),
                ),
                Padding(
                  padding: const EdgeInsets.fromLTRB(0, 4, 0, 12),
                  child: Field(controller: _nm, placeholder: 'Student', maxLength: 24, fieldKey: const ValueKey('nameField')),
                ),
                Btn(
                  'Save name',
                  icon: 'check',
                  block: true,
                  onTap: () {
                    s.setName(_nm.text.trim().isEmpty ? 'Student' : _nm.text.trim());
                    toast(context, 'Saved ✓');
                  },
                ),
              ],
            ),
          ),
          const SectionLabel('Appearance'),
          Panel(
            padding: const EdgeInsets.all(12),
            child: Seg(
              current: cur,
              items: [
                for (final t in const ['light', 'dark', 'auto'])
                  (id: t, label: t[0].toUpperCase() + t.substring(1), icon: t == 'light' ? 'sun' : t == 'dark' ? 'moon' : 'sparkle', count: null, tone: 'sage', enabled: true),
              ],
              onPick: (t) => s.setTheme(t == 'auto' ? null : t),
            ),
          ),
          const SectionLabel('Teacher'),
          Panel(
            padding: const EdgeInsets.all(12),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.stretch,
              spacing: 10,
              children: [
                Seg(
                  current: s.teacher ? 'on' : 'off',
                  items: const [
                    (id: 'off', label: 'Student', icon: 'user', count: null, tone: 'sage', enabled: true),
                    (id: 'on', label: 'Teacher mode', icon: 'grid', count: null, tone: 'sage', enabled: true),
                  ],
                  onPick: (v) => s.setTeacher(v == 'on'),
                ),
                if (s.teacher) Btn('Open teacher tools', icon: 'grid', kind: BtnKind.soft, block: true, onTap: () => HighNav.of(context).open('teacher', () => const TeacherPage())),
              ],
            ),
          ),
          const SectionLabel('Your progress'),
          kvCard([
            ('Questions answered', '${st.answered}'),
            ('Accuracy', st.acc == null ? '—' : '${st.acc}%'),
            ('Best streak', '${st.best} day${st.best == 1 ? '' : 's'}'),
            ('Total study time', fmtDur(st.studyAll)),
            ('Mistakes to retry', '${s.mistakes.where(r.byId.containsKey).length}'),
            ('Bookmarks', '${s.bookmarks.where(r.byId.containsKey).length}'),
          ]),
          const SectionLabel('Content'),
          kvCard([
            ('Matric exams', '${r.exams.length} exams · ${r.subjects.length} subjects'),
            ('Categories', kCats.map((c) => '${r.catExams(c.id).length} ${c.label.toLowerCase()}').join(' · ')),
            ('Questions', thousands(nQ)),
            ('Notes', 'Grade 9–12 · 8 subjects'),
            ('Pictures & 3D', '${MediaLib.credits.length} openly licensed items'),
          ]),
          Btn('Credits (pictures and 3D models)', icon: 'book', kind: BtnKind.soft, block: true, onTap: () => HighNav.of(context).open('credits', () => const CreditsPage())),
          Panel(
            child: Row(
              spacing: 12,
              children: [
                const Badge('peach', 'repeat', s: 40),
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text('Reset progress', style: ts(15, w900, p.ink)),
                      Text('Clears answers, mistakes and bookmarks', style: ts(12.5, w700, p.ink3)),
                    ],
                  ),
                ),
                _ResetBtn(
                  sure: _sure,
                  onTap: () {
                    if (_sure) {
                      s.resetProgress();
                      setState(() => _sure = false);
                      toast(context, 'Progress reset');
                    } else {
                      setState(() => _sure = true);
                    }
                  },
                ),
              ],
            ),
          ),
          const SectionLabel('About'),
          Panel(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text('4', style: ts(18, w900, p.ink)),
                const SizedBox(height: 4),
                Text('Developed by Shamm Tesfalem, 07162947', style: ts(14, w800, p.ink2)),
                const SizedBox(height: 4),
                Text('Grade 9–12 · works fully offline', style: ts(12.5, w700, p.ink3)),
              ],
            ),
          ),
          Blk(
            margin: const EdgeInsets.only(top: 18),
            child: Text('4 · works fully offline', textAlign: TextAlign.center, style: ts(12.5, w700, p.ink3)),
          ),
        ]),
      ),
    );
  }
}

class _ResetBtn extends StatelessWidget {
  const _ResetBtn({required this.sure, required this.onTap});
  final bool sure;
  final VoidCallback onTap;
  @override
  Widget build(BuildContext context) {
    final k = Kit.of(context);
    return Press(
      onTap: onTap,
      deco: k.d.btnSoft(),
      pressedDeco: k.d.btnSoftPressed(),
      dy: 4,
      label: 'Reset progress',
      padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 10),
      child: Text(sure ? 'Tap again' : 'Reset', style: ts(13, w900, sure ? k.p.peach.deep : k.p.ink)),
    );
  }
}
