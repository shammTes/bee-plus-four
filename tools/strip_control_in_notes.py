#!/usr/bin/env python3
"""Strip ASCII control chars that render as □ in Flutter notes."""
import json, re, sys
from pathlib import Path

CTRL = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f]")

def clean(o):
    if isinstance(o, str):
        return CTRL.sub("", o)
    if isinstance(o, list):
        return [clean(x) for x in o]
    if isinstance(o, dict):
        return {k: clean(v) for k, v in o.items()}
    return o

def main():
    path = Path(sys.argv[1] if len(sys.argv) > 1 else "assets/content/unit_notes_rich.json")
    if not path.exists():
        print("skip missing", path)
        return
    data = json.loads(path.read_text(encoding="utf-8", errors="replace"))
    data = clean(data)
    path.write_text(json.dumps(data, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    print("cleaned", path)

if __name__ == "__main__":
    main()
