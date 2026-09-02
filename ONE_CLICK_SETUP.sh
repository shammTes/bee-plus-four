#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
echo "4 — one-click setup"
echo "Assets are already in assets/content/ (including illustrated slides)."
if command -v flutter >/dev/null 2>&1; then
  flutter pub get
  echo ""
  echo "Done. Build APK:"
  echo "  flutter build apk --release"
  echo "Or run: flutter run"
else
  echo "Flutter not in PATH. Open this folder in Android Studio and Run."
fi
