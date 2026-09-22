#!/usr/bin/env python3
"""Merge practice_g*_p*.json into practice_from_notes.json if Drive pack is thin."""
import json, glob
from pathlib import Path

def count_qs(path: Path) -> int:
    if not path.exists() or path.stat().st_size < 500:
        return 0
    try:
        d = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(d, list):
            return len(d)
        if isinstance(d, dict):
            for k in ("questions", "items", "notes"):
                if isinstance(d.get(k), list):
                    return len(d[k])
    except Exception:
        return 0
    return 0

def main():
    target = Path("assets/content/practice_from_notes.json")
    n = count_qs(target)
    print("practice_from_notes count", n)
    if n >= 80:
        return
    allq = []
    seen = set()
    for f in sorted(glob.glob("assets/content/practice_g*_p*.json")):
        try:
            d = json.loads(Path(f).read_text(encoding="utf-8"))
            qs = d if isinstance(d, list) else d.get("questions", d.get("items", []))
            for q in qs:
                if not isinstance(q, dict):
                    continue
                pid = str(q.get("id") or q.get("prompt", ""))[:120]
                if pid in seen:
                    continue
                seen.add(pid)
                allq.append(q)
        except Exception as e:
            print("skip", f, e)
    if allq:
        target.write_text(json.dumps(allq, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
        print("merged practice parts", len(allq), "->", target)
    else:
        print("no practice parts found")

if __name__ == "__main__":
    main()
