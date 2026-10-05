# High / bee-plus-four — progress (`fix/high-qr-embedded-only`)

Updated: 2026-10-05 ~16:45 (Africa/Asmera, UTC+3)

## URGENT: camera error after PR #8

### What still failed
PR #8 preferred native Play Services `scanQr`, then fell back to embedded `MobileScanner`.
`scanQr` **steals the camera**; after cancel/fail, CameraX still often hits **`genericError`**.

### Fix (this branch)
1. **Never call native `scanQr`** after CAMERA grant (Dart unlock path removed; native method returns `use_embedded` without opening camera).
2. **Only** `MobileScannerController` with `CameraFacing.back`, `autoStart: false`, start after widget attach + **500ms**, single instance, full dispose on leave/retry.
3. Clear error UI: Retry Scan + Enter unlock code + Open Settings; **never** show raw `genericError`.
4. `MainActivity` still grants CAMERA via **`ActivityResultContracts.RequestPermission`** (`requestCamera` / `hasCamera` / rationale / settings). Logcat tag **`HighSecure`**.

### Verify
```bash
adb logcat -s HighSecure
# Fresh install → Scan seller QR → Allow → on-screen preview (no GMS UI)
# Fail path → human message, Retry / Enter code / Settings — never "genericError"
```
