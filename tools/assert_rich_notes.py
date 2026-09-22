#!/usr/bin/env python3
import argparse, json, sys
from pathlib import Path

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--final', action='store_true')
    args = ap.parse_args()
    path = Path('assets/content/unit_notes.json' if args.final else 'assets/content/unit_notes_rich.json')
    if not path.exists():
        print('MISSING', path)
        sys.exit(1)
    d = json.loads(path.read_text(encoding='utf-8'))
    if not isinstance(d, list) or len(d) < 50:
        print('TOO THIN', path, type(d), len(d) if isinstance(d, list) else None)
        sys.exit(1)
    print('OK', path, len(d), 'units')

if __name__ == '__main__':
    main()
