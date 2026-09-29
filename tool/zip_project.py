#!/usr/bin/env python3
# Zips the project to /workspace/High-flutter-project.zip (no build/, .dart_tool/, compare images, APKs).
import os, zipfile
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = '/workspace/High-flutter-project.zip'
SKIP = {'build', '.dart_tool', 'compare', '.idea', '.gradle', '__pycache__'}
with zipfile.ZipFile(OUT, 'w', zipfile.ZIP_DEFLATED) as z:
    for d, ds, fs in os.walk(ROOT):
        ds[:] = [x for x in ds if x not in SKIP]
        for f in fs:
            if f.endswith('.apk'): continue
            p = os.path.join(d, f)
            z.write(p, os.path.join('high_flutter', os.path.relpath(p, ROOT)))
print(OUT, os.path.getsize(OUT) // 1024, 'KB')
