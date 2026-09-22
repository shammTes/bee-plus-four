# Expansion status (2026-09-22)

## Device QA (code-verified; install APK to confirm)

| Check | Code status |
|-------|-------------|
| Tigrinya onboarding | `onboarding_walkthrough.dart` Tigrinya-only steps + NotoSansEthiopic |
| Ethiopic font | Theme fallback + onboarding fontFamily |
| Coach bot choices + Continue | `bot_screen.dart` lists A–D options |
| Back Leave exits | `app_shell.dart` SystemNavigator.pop on leave |
| Illustrated entry | Notes unit hub loads cards JSON |
| Chem matric 2000–2002 | Year packs on main (15+22+17) |

## Illustrated decks

- G9: 18 · G10: 14 · G11: 12 · G12: 10

## Matric interactive

- Physics, Biology, Chemistry catalogued
- Math year packs 2000/2001/2002/2018/2023 (loader wired)

## Seller QR + desktop

- Student: Device ID QR + Scan unlock QR
- Seller: Scan student / grant / seller + Generate unlock QR
- Windows: Flutter desktop + `tools/bee_seller_windows/bee_seller_desktop.py`
