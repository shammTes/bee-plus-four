#!/usr/bin/env python3
"""Make Bee Seller unlock codes exactly like the real sellers, for tests and manual checks.

Kotlin Bee Seller (shammTes/bee-plus-ecosystem core-licensing QrPayload.createUnlockCode):
    data = "BEE1|{deviceId}|{pkg}|{nonce8}|{timestampMs}"
    code = data + "|" + hex(HMAC-SHA256("BEE-PLUS-OFFLINE-SECRET-v1-ET-2026-SHAM", data)[:12])
Flutter Bee Seller / Windows seller (old seller_main.dart, bee_seller_desktop.py):
    body = "BEE1|HIGHSCHOOL|{deviceId}|{nonce}"
    code = body + "|" + hex(HMAC-SHA256("BEE_PLUS_ERITREA_OFFLINE_HMAC_V1_CHANGE_IN_RELEASE", body))

    python3 tool/unlock_samples.py ABC234DEF567            # print codes for this phone id
    python3 tool/unlock_samples.py ABC234DEF567 --png out  # also write QR PNGs (pip install segno)
"""
import hashlib
import hmac
import sys
import time
import uuid

SELLER_KEY = b"BEE-PLUS-OFFLINE-SECRET-v1-ET-2026-SHAM"
FLUTTER_KEY = b"BEE_PLUS_ERITREA_OFFLINE_HMAC_V1_CHANGE_IN_RELEASE"


def kotlin_seller(device_id, pkg="H", nonce=None, ts=None):
    nonce = nonce or str(uuid.uuid4())[:8]
    ts = ts or int(time.time() * 1000)
    data = f"BEE1|{device_id}|{pkg}|{nonce}|{ts}"
    return data + "|" + hmac.new(SELLER_KEY, data.encode(), hashlib.sha256).digest()[:12].hex()


def flutter_seller(device_id, pkg="HIGHSCHOOL", nonce=None):
    nonce = nonce or uuid.uuid4().hex[:12]
    body = f"BEE1|{pkg}|{device_id}|{nonce}"
    return body + "|" + hmac.new(FLUTTER_KEY, body.encode(), hashlib.sha256).hexdigest()


if __name__ == "__main__":
    dev = sys.argv[1] if len(sys.argv) > 1 else "ABC234DEF567"
    codes = {"kotlin_H": kotlin_seller(dev), "flutter_HIGHSCHOOL": flutter_seller(dev)}
    for name, code in codes.items():
        print(f"{name}: {code}")
    if "--png" in sys.argv:
        import segno  # ZXing / qr_flutter default: error correction L, auto version

        out = sys.argv[sys.argv.index("--png") + 1]
        for name, code in codes.items():
            segno.make_qr(code, error="L", boost_error=False).save(f"{out}_{name}.png", scale=8, border=4)
