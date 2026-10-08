# Build 4 APK: the workflow fix

`build-four-apk.fixed.yml` is a drop-in replacement for `.github/workflows/build-four-apk.yml`.
Bots and tokens without the `workflow` scope cannot change files under `.github/workflows`, so a person has to paste it.

## Why
The "Add Sawa model exams" step only passed when five exact file names were present with at least 383 questions between them.
If any were missing, it downloaded `https://litter.catbox.moe/ti37hq.tgz`.
catbox "litter" links expire within days, so once dedupe replaced one of those files the download returned 404 and the build failed. The school-paper step has the same weakness with its `qt60om.tgz` link.

## What changed
- **School papers:** the download now runs only when the pack is not already in the repo. If the link is dead, the step warns and continues instead of failing.
  - It still fails when `index.json` points at a missing file.
  - The fixed count of 5908 is gone.
- **Sawa exams:** the step is replaced by "Check exam packs". That step:
  - checks that every paper listed in `assets/high/exams/index.json` exists, parses and has at least one question;
  - checks that every listed media file exists.
  - There are no hard-coded file names and no hard-coded question total, so dedupe or merge work can't break the build. There is also no catbox download, because the papers are committed.
- **Unchanged:** the icon, commit, Flutter and build steps.

## How to apply (GitHub web editor, about 1 minute)
1. Open this file on GitHub at `docs/ci/build-four-apk.fixed.yml`, click **Raw**, then select all and copy.
2. Go to `.github/workflows/build-four-apk.yml` on `main` and click the pencil icon (**Edit this file**).
3. Select all the text in the editor, delete it, and paste.
4. Click **Commit changes…**. Either commit directly to `main` or pick "Create a new branch … and start a pull request" and merge that PR.
5. In **Actions → Build 4 APK**, the new run should go green. You can also start one with **Run workflow**.

After that, `tool/matric_audit/dedupe.py` no longer needs its `PINNED` list. It can stay; it does no harm.
