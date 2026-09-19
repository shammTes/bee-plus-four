# 4 — Highschool BEE PLUS

Offline study app for Eritrean high school (G9–G12): unit notes, full textbooks, practice MCQs, matric/model exams, coach bot, tools.

## Three apps (product flavors)

| Flavor | applicationId | Label | Entry |
|--------|---------------|-------|-------|
| student | com.four.student | **4** | `lib/main.dart` |
| seller | com.bee.seller | **Bee Seller** | `lib/seller_main.dart` |
| master | com.shamm.master | **Shamm Master** | `lib/master_main.dart` |

## Build APKs on GitHub

1. **Actions** → **Build 4 APKs (student / seller / master)**
2. **Run workflow**
3. Download artifact **four-three-apks**

## Local build

```bash
flutter pub get
flutter build apk --release --flavor student --target lib/main.dart
flutter build apk --release --flavor seller --target lib/seller_main.dart
flutter build apk --release --flavor master --target lib/master_main.dart
```

## Content

- Compact official textbook PDFs (~70 MB catalog)
- 194 unit notes (including WYSS Study Guide fills for G9 Geo/History/Business)
- Practice + matric banks via CI Drive pack
- Offline-first, device-bound HMAC unlock

minSdk 23 (Android 6.0+)
