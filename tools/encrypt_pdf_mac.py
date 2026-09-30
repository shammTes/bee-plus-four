#!/usr/bin/env python3
"""Encrypt a paper PDF on a Mac so it can be unlocked later.

4 does not ship a PDF renderer (that would stall low-end phones).
Two outputs:

  lock   — standard password-PDF via qpdf if installed
           (`brew install qpdf`), else an AES-256 .fourpdf wrapper
           using the Mac `openssl` binary.
  unlock — reverse either format.
  pack   — wrap a 4 exam JSON as .fourpack (this is what 4 can import).

Examples
  python3 tools/encrypt_pdf_mac.py lock  Physics_2024.pdf --password sawa
  python3 tools/encrypt_pdf_mac.py pack  physics_2024_matric.json --password sawa
  python3 tools/encrypt_pdf_mac.py unlock Physics_2024.pdf.fourpdf --password sawa
"""
from __future__ import annotations
import argparse, shutil, subprocess, sys
from pathlib import Path

MAGIC = b"FOURPDF1"


def _run(cmd: list[str]) -> None:
    subprocess.check_call(cmd)


def _openssl_enc(src: Path, dest: Path, password: str, decrypt: bool) -> None:
    cmd = [
        "openssl", "enc",
        "-aes-256-cbc", "-pbkdf2", "-iter", "200000", "-salt",
        "-in", str(src), "-out", str(dest),
        "-pass", f"pass:{password}",
    ]
    if decrypt:
        cmd.insert(2, "-d")
    _run(cmd)


def lock_pdf(src: Path, password: str, dest: Path | None) -> Path:
    src = src.expanduser().resolve()
    if not src.exists():
        raise SystemExit(f"missing file: {src}")
    qpdf = shutil.which("qpdf")
    if qpdf:
        out = dest or src.with_name(src.stem + ".locked.pdf")
        _run([qpdf, f"--encrypt={password}", password, "256", "--", str(src), str(out)])
        print(f"qpdf AES-256 → {out}")
        return out
    out = dest or src.with_suffix(src.suffix + ".fourpdf")
    wrapped = out.with_suffix(".tmp")
    _openssl_enc(src, wrapped, password, decrypt=False)
    out.write_bytes(MAGIC + wrapped.read_bytes())
    wrapped.unlink(missing_ok=True)
    print(f"openssl AES-256 wrapper → {out}")
    print("Install qpdf (`brew install qpdf`) next time for a normal locked PDF.")
    return out


def unlock_file(src: Path, password: str, dest: Path | None) -> Path:
    src = src.expanduser().resolve()
    data = src.read_bytes()
    if data.startswith(MAGIC):
        out = dest or src.with_suffix("").with_name(src.stem.replace(".pdf", "") + ".unlocked.pdf")
        enc = src.with_suffix(".enc.tmp")
        enc.write_bytes(data[len(MAGIC):])
        try:
            _openssl_enc(enc, out, password, decrypt=True)
        finally:
            enc.unlink(missing_ok=True)
        print(f"unlocked wrapper → {out}")
        return out
    qpdf = shutil.which("qpdf")
    if not qpdf:
        raise SystemExit("need qpdf to unlock a standard PDF (`brew install qpdf`)")
    out = dest or src.with_name(src.stem + ".unlocked.pdf")
    _run([qpdf, f"--password={password}", "--decrypt", str(src), str(out)])
    print(f"qpdf decrypt → {out}")
    return out


def pack_json(src: Path, password: str, dest: Path | None) -> Path:
    src = src.expanduser().resolve()
    if src.suffix.lower() != ".json":
        raise SystemExit("pack expects a 4 exam JSON file")
    out = dest or src.with_suffix(".fourpack")
    wrapped = out.with_suffix(".tmp")
    _openssl_enc(src, wrapped, password, decrypt=False)
    out.write_bytes(b"FOURPACK" + wrapped.read_bytes())
    wrapped.unlink(missing_ok=True)
    print(f"exam pack → {out}")
    print("Unlock on the Mac, then copy the JSON into assets/high/exams and the Model tab.")
    return out


def main() -> None:
    p = argparse.ArgumentParser(description="Lock papers on a Mac for 4")
    sub = p.add_subparsers(dest="cmd", required=True)
    for name, help_ in (("lock", "encrypt a PDF"), ("unlock", "decrypt a PDF / .fourpdf"), ("pack", "wrap exam JSON as .fourpack")):
        s = sub.add_parser(name, help=help_)
        s.add_argument("src")
        s.add_argument("--password", required=True)
        s.add_argument("--out")
    args = p.parse_args()
    src, dest = Path(args.src), Path(args.out) if args.out else None
    if args.cmd == "lock":
        lock_pdf(src, args.password, dest)
    elif args.cmd == "unlock":
        unlock_file(src, args.password, dest)
    else:
        pack_json(src, args.password, dest)


if __name__ == "__main__":
    main()
