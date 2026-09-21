#!/usr/bin/env python3
"""Download illustrated PDFs from illustrated_drive_catalog.json into assets/content/illustrated_pdf/."""
from __future__ import annotations
import json, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "assets" / "content"
OUT = CONTENT / "illustrated_pdf"
CATALOG = CONTENT / "illustrated_drive_catalog.json"

def gdown(file_id: str, dest: Path) -> bool:
    dest.parent.mkdir(parents=True, exist_ok=True)
    url = f"https://drive.google.com/uc?id={file_id}&export=download"
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-q", "gdown"], check=False)
        subprocess.check_call(
            [sys.executable, "-m", "gdown", url, "-O", str(dest)],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.STDOUT,
        )
        return dest.exists() and dest.stat().st_size > 1000
    except Exception as e:
        print("fail", file_id, e)
        return False

def main():
    if not CATALOG.exists():
        print("no drive catalog"); return
    data = json.loads(CATALOG.read_text(encoding="utf-8"))
    decks = data.get("decks") or []
    updated, ok = [], 0
    for d in decks:
        fid = d.get("drive_file_id")
        if not fid:
            updated.append(d); continue
        grade = d.get("grade") or "G9"
        subject = (d.get("subject") or "GEN").replace(" ", "_")
        unit = d.get("unit_number") or 0
        rel = f"assets/content/illustrated_pdf/{grade}_{subject}_u{unit}.pdf"
        dest = ROOT / rel
        print("download", d.get("title"), "->", rel)
        if gdown(fid, dest):
            ok += 1
            d = dict(d)
            d["pdf_asset"] = rel
            d["type"] = "illustrated_pdf"
        updated.append(d)
    data["decks"] = updated
    data["downloaded"] = ok
    CATALOG.write_text(json.dumps(data, indent=2), encoding="utf-8")
    by_key = {(x.get("grade"), x.get("subject"), x.get("unit_number")): x for x in updated}
    for g in ("g9", "g10", "g11", "g12"):
        path = CONTENT / f"illustrated_catalog_{g}.json"
        if not path.exists(): continue
        cat = json.loads(path.read_text(encoding="utf-8"))
        for d in cat.get("decks") or []:
            k = (d.get("grade"), d.get("subject"), d.get("unit_number"))
            if k in by_key and by_key[k].get("pdf_asset"):
                d["pdf_asset"] = by_key[k]["pdf_asset"]
                d["type"] = "illustrated_pdf"
        path.write_text(json.dumps(cat, indent=2), encoding="utf-8")
    print(f"downloaded {ok}/{len(updated)} illustrated PDFs")

if __name__ == "__main__":
    main()
