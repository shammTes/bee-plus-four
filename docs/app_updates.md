# In-app updates for 4

## How it works
- **Online** (`lib/update/updater.dart`):
  - Timing: about 6 s after start, unlocked phones check at most once a day. The default is Wi-Fi only; Settings → App updates can switch it to Wi-Fi or mobile data.
  - Manifest: they read `https://github.com/shammTes/bee-plus-four/releases/latest/download/four-update.json`. A build can point elsewhere with `--dart-define=FOUR_UPDATE_URL=…`.
  - Prompt: if `versionCode` is higher than the installed one, Home shows "New 4 version …".
  - Download: resumable (HTTP Range on a `.part` file in cacheDir/updates), with a progress bar. The phone picks its own per-ABI APK when the manifest lists one.
- **Checks before installing**: SHA-256 against the manifest, then the APK's package name, a higher `versionCode`, and its signing certificate. The certificate must equal the installed app's, and the manifest's `cert` if one is given.
- **Install**: the system package installer opens through FileProvider, and the user taps **Update** once. Android does not allow silent installs for sideloaded apps. The first time, Android sends the user to "Install unknown apps → allow for 4".
- **Offline**: when Resources → Refresh scans the chosen folder, it also looks at `*.apk` files (e.g. received via SHAREit). A file is offered only if it passes the same package, version and certificate checks.
- **Locked phones**: they never reach the app UI and do not check. A fresh install of a newer APK still works, because unlocking happens after install.
- **Data**: same `applicationId` (`com.four.student`) + same signing key = Android keeps all app data: unlock state, secure-storage proof, progress and imported resources.

## IMPORTANT: the current workflow cannot produce updatable builds
`.github/workflows/build-four-apk.yml` runs `flutter build apk --release`, and `android/app/build.gradle.kts` used to sign
release builds with the **debug key**. On a fresh GitHub runner that key is generated anew every run, so each CI
APK has a different signature:
1. Android refuses to install one over another ("App not installed"), and in-app updates can never succeed.
2. The `versionCode` is always 1 (`pubspec.yaml` `1.0.0+1`), so no build counts as newer.

This PR makes `build.gradle.kts` sign with a stable release key when one is provided (env vars or `android/key.properties`).
It falls back to debug when none is given. The workflow itself must be changed by someone with workflow permission:

### One-time setup (on your computer)
```
keytool -genkeypair -v -keystore four-release.jks -alias four -keyalg RSA -keysize 4096 -validity 36500
base64 -w0 four-release.jks > four-release.jks.b64        # macOS: base64 -i four-release.jks
```
- Keep `four-release.jks` and its passwords **safe and backed up**. If they are lost, phones can never be updated again: users would have to uninstall, which loses their unlock.
- Add these repository secrets: `FOUR_KEYSTORE_B64` (contents of the .b64 file), `FOUR_KEYSTORE_PASSWORD`, `FOUR_KEY_ALIAS` (= `four`), `FOUR_KEY_PASSWORD`.
- Optional, to make encrypted resources stronger: add `FOUR_MK` (from `four_encrypt newkey`) and use it in the Mac encryptor too.

### Workflow change
Copy `docs/ci/build-four-apk-signed.yml` over `.github/workflows/build-four-apk.yml`. It has the same content steps as today, plus:
- Release signing from the secrets.
- `--build-number=${{ github.run_number }}`, so every build has a higher `versionCode`.
- Universal + per-ABI APKs.
- A GitHub Release with `four-update.json` on manual runs (`workflow_dispatch` with "publish" checked).

### Switching existing phones (once)
Phones that have a CI build signed with an old random debug key cannot update to the first release-key build. Install it once by uninstalling first (this loses unlock and resources on that phone), or keep those phones as they are. From then on, every update keeps data.

## Releasing a new version (each time)
- **CI** (after the workflow change): Actions → "Build 4 APK" → Run workflow → tick *publish* and enter notes. Phones see the update at their next daily check, or immediately with Settings → Check for updates.
- **By hand**:
  ```
  flutter build apk --release --build-number=<higher number> [--split-per-abi]   # with FOUR_KEYSTORE… env set
  python3 tool/publish_update.py build/app/outputs/flutter-apk/app-release.apk \
      [build/app/outputs/flutter-apk/app-arm64-v8a-release.apk build/app/outputs/flutter-apk/app-armeabi-v7a-release.apk] \
      --notes "What changed" --publish
  ```
  `publish_update.py` writes `four-update.json` (versionCode, versionName, URLs, SHA-256, size, signing cert), creates the GitHub Release `v<name>-<code>` marked latest, and uploads everything. It warns if the APK is debug-signed.
- **Offline**: send the new APK by SHAREit into the phone's resources folder, then Extra resources → Refresh → Home card "New 4 version" → Install.

## Tests
`flutter test test/updater_test.dart` uses a local HTTP server with Range support. It covers: newer-version detection + ABI pick, resume after a partial download (`Range: bytes=300000-`), SHA check, a wrong-key APK being refused, and "up to date".
