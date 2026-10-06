Generated per-unit notes (one small JSON per unit), committed so every build ships them. Do not edit by hand:
the books in ../notes/ (and their unit_<id>.json overrides) are the source. After changing notes, or after a rebase /
merge that touched them, run

    python3 tool/split_notes.py

`flutter test` (test/notes_split_test.dart) fails while these files are stale. Output is deterministic, so a merge
conflict here is resolved by re-running the script. If a file is missing the app falls back to the full book file.
