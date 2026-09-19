# Bee Seller wholesale (seller-to-seller)

## Flow
1. Seller A has quota (from Master WHOLESALE:N or earlier SELLER:N redeem).
2. Seller B opens Bee Seller and copies **My Device ID**.
3. Seller A opens section **3. Wholesale to another Bee Seller**:
   - Pastes B's Device ID
   - Enters quota to transfer (must be ≤ remaining)
   - Taps **Generate wholesale code + QR**
4. App creates signed payload `SELLER:<quota>` bound to B's device + shows **copyable code + QR**.
5. Seller B **redeems** that code in section 1 → B's quota increases; A's decreases.

## Security
- HMAC-SHA256 signed (`QrPayload`)
- Bound to target `deviceId`
- Single-use nonce stored in Hive
- Cannot transfer more than remaining quota
- Cannot transfer to own device

## Code
- `lib/seller_main.dart` — UI
- `lib/core/licensing/seller_store.dart` — `issueSellerCode` / `redeemAuthCode`
- `lib/core/licensing/qr_payload.dart` — `SELLER:N` package type
