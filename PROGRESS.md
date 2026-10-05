# High / bee-plus-four — progress (`fix/high-qr-decode-reliability`)

Updated: 2026-10-05 ~17:25 (Africa/Asmera, UTC+3)

## CRITICAL: Camera opens but QR does not decode (after PR #11)

### Root cause
PR #11 correctly switched unlock to **system TakePicture → still JPEG → ML Kit**, so the
camera app opens. Decode was still brittle:

1. **Single ML Kit pass** on an EXIF-rotated bitmap only (no `fromFilePath`, no rotation retries)
2. **No secondary decoder** when ML Kit missed contrast / orientation edge cases
3. **Aggressive downscale** (1600px) could shrink dense unlock QR modules too far
4. **Empty / tiny JPEG** (some OEM cameras + FileProvider) was treated like “no QR”
5. Did not prefer `BEE1|` payloads when multiple barcodes appeared

### Fix (this branch)
Keep system camera flow. Harden still-photo decode:

1. Log photo **path + byte size**; fail clearly if camera wrote an empty/tiny file
2. **ML Kit** `InputImage.fromFilePath` (content Uri, auto EXIF) first
3. Then ML Kit on bitmap at **0/90/180/270°** (formats: QR + Aztec + Data Matrix)
4. **ZXing** fallback (`TRY_HARDER`, same rotations, inverted luminance)
5. Optional **hi-res retry** (3200px) if still missing
6. Prefer raw values containing `BEE1|`
7. UI: `No QR found — retake photo closer / better light`; invalid content after scan is explicit
8. **Enter unlock code** remains always visible
9. HighSecure logs: path, size, barcode count, redacted values, unlock success/fail

### Files
- `android/.../MainActivity.kt` — robust multi-pass decode
- `android/app/build.gradle.kts` — `com.google.zxing:core:3.5.3`
- `lib/licensing/lock_screen.dart` — clearer no-QR / invalid-QR messages + logs
- `PROGRESS.md`

### How to test
```bash
flutter pub get
# After merge: uninstall old APK, install Actions APK
adb logcat -s HighSecure
# Scan unlock QR → system camera → hold steady, QR fills much of frame → shutter
# Or paste code → Unlock 4
```
