# Bee Seller — Windows

## Build (Flutter Windows, same code as Android seller)

```bat
flutter config --enable-windows-desktop
flutter pub get
flutter build windows --release -t lib/seller_main.dart
```

Output folder: `build\\windows\\x64\\runner\\Release\\`

Features (same as mobile Bee Seller):
- Scan student Device ID QR
- Generate unlock QR / codes
- Wholesale seller codes

Run without packaging:
```bat
flutter run -d windows -t lib/seller_main.dart
```
