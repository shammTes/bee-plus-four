# Build 4 APK: hardened workflow

`build-four-apk.fixed.yml` replaces `.github/workflows/build-four-apk.yml`. The current workflow downloads packs from
`litter.catbox.moe`, and those links expire. Its Sawa step also needs five exact files holding at least 383 questions,
so de-duplicating papers or an expired link turns the build red.

Changes in the fixed version:
- **School pack:** only downloaded if it is missing from the repo. A failed download is a warning, not an error. The
  check is now that every file in the index exists and the pack is not empty. The fixed count of 5908 is gone.
- **Sawa models:** the download step is removed, because the files are committed. It is replaced by a check that
  every paper listed in `assets/high/exams/index.json` exists and has questions. If a Sawa file is missing, that is
  only a warning.
- Everything else (icon, commit, Java/Flutter setup, build, upload) is unchanged.

## How to install it (GitHub web editor; the bot token cannot edit workflows)
1. Open https://github.com/shammTes/bee-plus-four/blob/main/docs/ci/build-four-apk.fixed.yml, click **Raw** and copy
   everything (Ctrl+A, Ctrl+C).
2. Open https://github.com/shammTes/bee-plus-four/edit/main/.github/workflows/build-four-apk.yml. This is the same as
   opening the file on GitHub and clicking the pencil (Edit) icon.
3. Select all the text in the editor (Ctrl+A), paste (Ctrl+V), and keep the indentation exactly as it is.
4. Click **Commit changes…**, choose *Commit directly to the main branch*, then click **Commit changes**.
5. Open **Actions → Build 4 APK**. The push starts a run; it can also be started with **Run workflow**. Check that
   the run is green.
