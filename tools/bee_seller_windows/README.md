# Bee Seller for Windows

Desktop helper that issues the **same offline unlock codes** as the Android Bee Seller app.

## Payload format (matches Flutter)

```
BEE1|<packageCode>|<deviceId>|<nonce>|<hmacSha256Hex>
```

| Package | Meaning |
|---------|---------|
| `HIGHSCHOOL` | Permanent student unlock |
| `WHOLESALE:N` | Master → seller quota grant |
| `SELLER:N` | Seller → sub-seller quota grant |

HMAC-SHA256 is computed over `BEE1|package|deviceId|nonce` using the same key as Flutter:

- Default: `BEE_PLUS_ERITREA_OFFLINE_HMAC_V1_CHANGE_IN_RELEASE`
- Override: set env `BEE_HMAC_KEY` (preferred) or `BEE_HMAC_SECRET`

## Install (Windows)

1. Install [Python 3.10+](https://www.python.org/downloads/) (check **Add to PATH**).
2. Open PowerShell in this folder:

```powershell
cd tools\bee_seller_windows
pip install -r requirements.txt
python bee_seller_desktop.py
```

Optional production key:

```powershell
$env:BEE_HMAC_KEY = "BEE_PLUS_ERITREA_OFFLINE_HMAC_V1_CHANGE_IN_RELEASE"
python bee_seller_desktop.py
```

## Workflow

1. **Get quota** — paste a Master/parent `WHOLESALE:N` or `SELLER:N` code → **Redeem grant**.
2. **Unlock a student** — paste the student’s Device ID from app **4** (Unlock screen) → **Issue student code + QR**.
3. Student scans the QR (or pastes the code) in the **4** app.
4. **Wholesale to another seller** — enter their seller Device ID + quota → **Issue seller grant + QR**.

Quota and history are stored in `%USERPROFILE%\.bee_seller_desktop.json`.

## Testing without Master

Edit the store file and set `"quota": 20`, then issue student codes.

## Note

This tool does **not** replace the Android Bee Seller APK; it is for laptop use when the phone app is inconvenient. Keep the HMAC key secret and identical across Master, Seller, student app, and this desktop tool.
