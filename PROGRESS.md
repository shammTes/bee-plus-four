# High / bee-plus-four — progress (`fix/high-qr-camera-retry`)

Updated: 2026-10-05 ~16:20 (Africa/Asmera, UTC+3)

## QR unlock camera — root cause + fix (PRIORITY)

### Root causes (first-install)
1. **Permission callback gap:** `MainActivity` extended `FlutterActivity` and relied on classic `onRequestPermissionsResult`. On modern Flutter/AndroidX embeddings this often **never completes** the MethodChannel `requestCamera` future → UI stuck on “Waiting for camera…” and the scanner never starts.
2. **Play Services Code Scanner cold start:** On first install, `GmsBarcodeScanning.startScan()` frequently fails until the `barcode_ui` module finishes downloading. Without a solid fallback + permission already granted, users see a dead end.
3. **No hard fallback UX:** When camera failed, code entry existed but was not highlighted, so users felt stuck.

### Fix
- **Native (`MainActivity.kt`):** Switch to `FlutterFragmentActivity` + `ActivityResultContracts.RequestPermission` for CAMERA; keep legacy `onRequestPermissionsResult` as backup; `OnceResult` prevents double-reply crashes; Logcat tag `HighSecure`; channel remains `com.warsay.high/secure` (`requestCamera`, `hasCamera`, `shouldShowCameraRationale`, `openAppSettings`, `scanQr`).
- **Dart (`lock_screen.dart`):** On Scan → request CAMERA (45s timeout) → try native `scanQr` → on cancel/failure start **embedded `MobileScannerController` only after permission** (post-frame attach); permanentlyDenied → Open Settings; always surface **“Enter unlock code”** banner + Paste/Unlock; opaque hit-testing on buttons; `errorBuilder` on scanner preview.
- **Manifest:** `CAMERA` permission + optional camera feature + ML Kit `barcode_ui` meta-data (unchanged, verified).

### Verify on device
1. Fresh install → Lock → **Scan seller QR** → system permission dialog appears.
2. Allow → Play scanner **or** on-screen camera preview.
3. Deny → message + **Enter unlock code** + Settings if permanent.
4. Paste Bee Seller payload → Unlock 4.

## Enrichment this branch
- Focused on QR fix. English 12 thematic units already have worked/check/games from prior PRs; no History rewrites; no new Commons images.

## Left
- Device QA of permission/scanner paths (debug + release APK)
- Optional Commons diagrams + credits.json
- Pre-2020 Drive matric gaps (if any)

## Build
```bash
git fetch origin && git checkout fix/high-qr-camera-retry
flutter pub get && flutter analyze
flutter build apk --release
# Logcat: adb logcat -s HighSecure
```
