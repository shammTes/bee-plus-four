# 4 — Highschool BEE PLUS

Offline study app for Eritrean high school (G9–G12): unit notes, compact textbooks, practice MCQs, matric/model exams, Tigrinya onboarding, coach bot, tools.

Three apps from one repo (product flavors):

| Flavor | applicationId | Launcher name | Entry |
|--------|---------------|---------------|--------|
| student | `com.four.student` | **4** | `lib/main.dart` |
| seller | `com.bee.seller` | **Bee Seller** | `lib/seller_main.dart` |
| master | `com.shamm.master` | **Shamm Master** | `lib/master_main.dart` |

## Get the APKs (GitHub Actions)

1. Open **Actions** → **Build 4 APKs (student / seller / master)**
2. **Run workflow**
3. Download artifact **`four-three-apks`**

## Local build

```bash
flutter pub get
flutter build apk --release --flavor student --target lib/main.dart
flutter build apk --release --flavor seller  --target lib/seller_main.dart
flutter build apk --release --flavor master  --target lib/master_main.dart
```

## Full source snapshot

Complete tree with latest seller QR, unit notes (194), notes textbook wiring:

- Drive: https://drive.google.com/file/d/1RgyIjy-CMxxkEwyPDxFYZGIEsw-BtVe6/view

Extract over this repo, then `flutter pub get` and build.

## Content strategy

- **Compact official textbooks** (~70 MB catalog)
- **194 unit notes** (WYSS Study Guides for G9 Geo/History/Business)
- Practice + matric banks from JSON
- CI downloads Drive content pack for full offline assets

## Features

- Interactive Tigrinya onboarding
- Multi-unit practice CTA + direct-tap question list
- Notes → **Full textbook** offline PDF
- Bee Seller: wholesale redeem, student unlocks, **scannable QR** + copy
- Shamm Master: WHOLESALE:quota codes for Seller Device ID
- Offline-first, device-bound HMAC unlock (BEE1)

minSdk 23 (Android 6.0+)
