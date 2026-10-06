Generated per-unit notes (one small JSON per unit). Not committed: run

    python3 tool/split_notes.py

before `flutter build` / `flutter run` (CI does it in .github/workflows/build-four-apk.yml). Without these files the
app still works: it falls back to the full book files in ../notes/ (slower to open a unit on low-end phones).
