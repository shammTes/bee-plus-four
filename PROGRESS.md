# High / bee-plus-four — progress (`fix/high-qr-system-camera`)

Updated: 2026-10-05 ~17:10 (Africa/Asmera, UTC+3)

## CRITICAL: QR unlock camera never opens (after PRs #5 / #8 / #9)

### Root cause (product)
In-app CameraX / `mobile_scanner` and Play Services barcode UI failed to open a usable camera
preview on the user’s low-end / first-install Android builds (`genericError`, busy HAL, etc.).

### Fix (this branch) — system camera app
**Do not use `mobile_scanner` for unlock.** Flow:

1. User taps **Scan unlock QR**
2. `ActivityResultContracts.RequestPermission` for `CAMERA` (unchanged)
3. Native **`ActivityResultContracts.TakePicture`** → system camera app (`ACTION_IMAGE_CAPTURE`)
4. Photo saved via **FileProvider** into app cache
5. On-device **ML Kit `barcode-scanning`** reads QR from the still image (downscaled for low RAM)
6. Payload returned on MethodChannel `captureAndScanQr` → existing `UnlockStore.applyPayload`

Secondary UX: **Enter unlock code** field always visible (paste / type / Unlock 4).

### Files
- `lib/licensing/lock_screen.dart` — rewritten; no MobileScanner
- `android/.../MainActivity.kt` — `captureAndScanQr` + ML Kit decode; tag **`HighSecure`**
- `AndroidManifest.xml` — CAMERA, FileProvider, `IMAGE_CAPTURE` query, `barcode` ML Kit meta
- `android/app/build.gradle.kts` — `barcode-scanning` + `exifinterface` (drop code-scanner UI)
- `pubspec.yaml` — removed `mobile_scanner`
- `res/xml/file_paths.xml` — cache FileProvider paths

### How to test
```bash
flutter pub get
flutter build apk   # or run on device
adb logcat -s HighSecure

# Fresh install:
# 1. Open 4 → lock screen
# 2. Tap "Scan unlock QR" → Allow camera
# 3. System camera app opens (not in-app preview)
# 4. Photograph Bee Seller unlock QR → shutter / OK
# 5. App unlocks OR human error ("No QR…") + Enter unlock code / Retry / Settings
#
# Also: paste unlock code → Unlock 4 (always works without camera)
```
