package com.beeplus.seller

import com.beeplus.licensing.QrPayload
import com.beeplus.licensing.SellerApp
import com.beeplus.licensing.SellerCreditManager
import com.beeplus.licensing.SellerCreditManager.Redeem
import org.junit.Assert.assertEquals
import org.junit.Assert.assertTrue
import org.junit.Test
import java.io.File

/**
 * Shamm Master -> Bee Seller 1.2.0 compatibility. Copied into a scratch copy of bee-plus-ecosystem by
 * apps/shamm_master/tool/bee_seller_compat.sh; reads the codes the Dart issuer wrote (test/grant_test.dart)
 * and redeems each one through Bee Seller's own parser (ScanParse.topUpCode + SellerCreditManager.redeemWith).
 */
class BeeSellerCompatTest {
    @Test fun shammMasterCodesRedeemInBeeSeller() {
        val path = System.getenv("SHAMM_VECTORS") ?: error("set SHAMM_VECTORS")
        val rows = File(path).readLines().filter { it.isNotBlank() }.map { it.split('\t') }
        assertTrue(rows.size >= 30)
        for ((id, appCode, n, code) in rows) {
            val used = mutableSetOf<String>()
            val bal = mutableMapOf(SellerApp.FOUR to 0, SellerApp.WINNER to 0)
            fun add(raw: String) = SellerCreditManager.redeemWith(raw, id, { used.contains(QrPayload.fingerprint(it)) },
                { used.add(QrPayload.fingerprint(it)) }, { app, k -> bal[app] = bal.getValue(app) + k })
            assertEquals("scan/paste reader keeps the code: $code", code, ScanParse.topUpCode(code))
            val r = add(code)
            assertTrue("redeem $code -> $r", r is Redeem.Added)
            r as Redeem.Added
            val app = SellerApp.fromCode(appCode)!!
            assertEquals(n.toInt(), r.credits)
            assertEquals(app, r.app)
            assertEquals(n.toInt(), bal.getValue(app))
            assertEquals(0, bal.getValue(if (app == SellerApp.FOUR) SellerApp.WINNER else SellerApp.FOUR))
            assertTrue("one use only", add(code) is Redeem.Refused)
            // Wrong seller, changed amount: refused.
            val other = if (id.startsWith("BEE-A0")) "BEE-A1111111111111111" else "BEE-A0123456789ABCDEF"
            assertTrue(SellerCreditManager.redeemWith(code, other, { false }, {}, { _, _ -> }) is Redeem.Refused)
            assertTrue(add(code.replaceFirst(":$n|", ":${n.toInt() + 1}|")) is Redeem.Refused)
        }
        println("BeeSellerCompat: ${rows.size} Shamm Master codes redeemed OK")
    }
}
