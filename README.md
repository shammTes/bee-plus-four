# 4 — Highschool BEE PLUS

Offline study app: notes, illustrated decks, practice MCQs, matric/model exams, coach bot, tools.

## Build APK on GitHub (one click)

1. Open **Actions** → **Build 4 APK**
2. Click **Run workflow** → **Run workflow**
3. When green, open the run → **Artifacts** → download **four-release-apk**

Every push to `main` also builds an APK.

## Local (Mac)

```bash
chmod +x ONE_CLICK_SETUP.sh
./ONE_CLICK_SETUP.sh
flutter build apk --release
```

## Contents

- `lib/` — Home, Notes, Practice, Coach, Exams, Tools, Unlock
- `assets/content/` — unit notes, practice, matric bank, illustrated index

App ID: `com.four.student` · minSdk 23 (Android 6)
