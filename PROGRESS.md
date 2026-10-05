# High / bee-plus-four — progress (`fix/high-qr-generic-error`)

Updated: 2026-10-05 ~16:45 (Africa/Asmera, UTC+3)

## URGENT: "Camera error: genericError" on first-install unlock

### Exact source
`lib/licensing/lock_screen.dart` → `MobileScanner` `errorBuilder` previously rendered:

`Camera error: ${error.errorCode.name}`

When `MobileScannerErrorCode.genericError` fired, the user saw **"Camera error: genericError"**.

### Root cause
1. After permission, flow prefers Play Services `scanQr`. On first install that often **cancels/fails** (barcode UI module) or user backs out.
2. Embedded `MobileScannerController.start()` ran **immediately** (≈50 ms) while GMS / CameraX still held the camera → CameraX init fails → **`genericError`**.
3. `errorBuilder` exposed the raw enum **name** instead of a human message; no settle delay / single-flight guard.

### Fix
- Prefer native `scanQr` after CAMERA grant; **settle 400–500 ms** (Dart + native `postDelayed`) before embedded fallback.
- Embedded: full dispose between attempts; `_startingEmbedded` + `_scannerGen` prevent double-start; create controller after permission; start only after widget attach + **~400 ms**; `CameraFacing.back`.
- Map `genericError` (and others) to human copy; **Retry Scan** + **Enter unlock code** + **Open Settings**.
- Native `log` MethodChannel + Logcat tag **`HighSecure`**.

### Verify
```bash
adb logcat -s HighSecure
# Fresh install → Scan → Allow → system scanner OR on-screen after settle
# Deny / fail → human message, not "genericError"
```
