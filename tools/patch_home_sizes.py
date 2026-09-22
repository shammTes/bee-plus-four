from pathlib import Path
p = Path('lib/features/home/home_screen.dart')
t = p.read_text(encoding='utf-8')
t2 = t
t2 = t2.replace('height: 64,\n              alignment: Alignment.center,', 'height: 80,\n              alignment: Alignment.center,', 1)
t2 = t2.replace('fontSize: label.length > 4 ? 13 : 20,', 'fontSize: label.length > 4 ? 15 : 22,')
t2 = t2.replace(
    'padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 12),',
    'padding: const EdgeInsets.symmetric(horizontal: 18, vertical: 16),',
)
t2 = t2.replace('Icon(icon, size: 18, color: FourTheme.primary),', 'Icon(icon, size: 22, color: FourTheme.primary),')
t2 = t2.replace(
    '''              Text(label,
                  style: TextStyle(
                    fontWeight: FontWeight.w800,
                    fontSize: 13,''',
    '''              Text(label,
                  style: TextStyle(
                    fontWeight: FontWeight.w900,
                    fontSize: 15,''',
)
if t2 == t:
    print('no changes applied (already patched?)')
else:
    p.write_text(t2, encoding='utf-8')
    print('home sizes patched')
