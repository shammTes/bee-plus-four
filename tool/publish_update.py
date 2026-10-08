#!/usr/bin/env python3
"""Publish a 4 release so unlocked phones can update themselves.

Writes four-update.json (the manifest the app reads) next to the APK and, with --publish, creates the GitHub release
v<versionName>-<versionCode> on shammTes/bee-plus-four and uploads both files. The app reads
https://github.com/<repo>/releases/latest/download/four-update.json, so the newest release must carry the manifest.

  python3 tool/publish_update.py build/app/outputs/flutter-apk/app-release.apk --notes "New videos player" [--publish]
  # smaller downloads: also pass the split APKs (flutter build apk --split-per-abi); phones pick their ABI
  python3 tool/publish_update.py app-release.apk app-arm64-v8a-release.apk app-armeabi-v7a-release.apk --publish

Needs Android build-tools (aapt2 + apksigner, found via $ANDROID_HOME) and, for --publish, an authenticated `gh`.
"""
from __future__ import annotations

import argparse, glob, hashlib, json, os, re, shutil, subprocess, sys
from pathlib import Path


def tool(name: str) -> str:
    p = shutil.which(name)
    if p:
        return p
    home = os.environ.get("ANDROID_HOME") or os.environ.get("ANDROID_SDK_ROOT") or str(Path.home() / "Android/Sdk")
    found = sorted(glob.glob(f"{home}/build-tools/*/{name}"))
    if not found:
        sys.exit(f"{name} not found (install Android build-tools or put it on PATH)")
    return found[-1]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("apks", nargs="+", help="universal APK first, then optional per-ABI split APKs")
    ap.add_argument("--notes", default="")
    ap.add_argument("--repo", default="shammTes/bee-plus-four")
    ap.add_argument("--publish", action="store_true", help="create the GitHub release and upload APK + manifest")
    a = ap.parse_args()
    apk = Path(a.apks[0])
    badging = subprocess.run([tool("aapt2"), "dump", "badging", str(apk)], capture_output=True, text=True, check=True).stdout
    m = re.search(r"package: name='([^']+)' versionCode='(\d+)' versionName='([^']*)'", badging)
    if not m:
        sys.exit("could not read package info")
    pkg, code, name = m.group(1), int(m.group(2)), m.group(3)
    certs = subprocess.run([tool("apksigner"), "verify", "--print-certs", str(apk)], capture_output=True, text=True, check=True).stdout
    c = re.search(r"Signer #1 certificate SHA-256 digest: ([0-9a-f]+)", certs)
    if not c:
        sys.exit("APK is not signed")
    cert = c.group(1)
    if "Android Debug" in certs:
        print("WARNING: signed with a DEBUG key. Phones will refuse to update unless every build uses this same key.", file=sys.stderr)
    sha = hashlib.sha256(apk.read_bytes()).hexdigest()
    tag = f"v{name}-{code}"
    out_apk = apk.with_name(f"four-{name}-{code}.apk")
    if out_apk != apk:
        shutil.copyfile(apk, out_apk)
    manifest = {
        "package": pkg,
        "versionCode": code,
        "versionName": name,
        "apk": f"https://github.com/{a.repo}/releases/download/{tag}/{out_apk.name}",
        "sha256": sha,
        "size": apk.stat().st_size,
        "cert": cert,
        "notes": a.notes,
    }
    uploads = [out_apk]
    abis = {}
    for extra in a.apks[1:]:
        ep = Path(extra)
        am = re.search(r"(arm64-v8a|armeabi-v7a|x86_64)", ep.name)
        if not am:
            sys.exit(f"cannot tell the ABI of {ep.name}")
        b2 = subprocess.run([tool("aapt2"), "dump", "badging", str(ep)], capture_output=True, text=True, check=True).stdout
        if f"versionCode='{code}'" not in b2:
            sys.exit(f"{ep.name}: versionCode differs from the universal APK")
        named = ep.with_name(f"four-{name}-{code}-{am.group(1)}.apk")
        if named != ep:
            shutil.copyfile(ep, named)
        uploads.append(named)
        abis[am.group(1)] = {
            "apk": f"https://github.com/{a.repo}/releases/download/{tag}/{named.name}",
            "sha256": hashlib.sha256(named.read_bytes()).hexdigest(),
            "size": named.stat().st_size,
        }
    if abis:
        manifest["abis"] = abis
    mpath = apk.with_name("four-update.json")
    mpath.write_text(json.dumps(manifest, indent=2) + "\n")
    print(json.dumps(manifest, indent=2))
    if a.publish:
        subprocess.run(["gh", "release", "create", tag, *map(str, uploads), str(mpath), "-R", a.repo, "--title", f"4 {name} ({code})", "--notes", a.notes or f"4 {name}", "--latest"], check=True)
        print(f"published {tag}; phones will see it at their next check")


if __name__ == "__main__":
    main()
