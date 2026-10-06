package com.warsay.high

import org.junit.Assert.assertEquals
import org.junit.Assert.assertNull
import org.junit.Assert.assertTrue
import org.junit.Test

/**
 * Samples are produced exactly like the sellers do (see tool/unlock_samples.py):
 *  - Kotlin Bee Seller: BEE1|dev|pkg|nonce|ts|HMAC-SHA256(SHARED_SECRET)[0..12] hex
 *  - Flutter Bee Seller: BEE1|HIGHSCHOOL|dev|nonce|HMAC-SHA256 hex
 */
class UnlockCodeRecoveryTest {
    private val dev = "ABC234DEF567"
    private val k6 = "BEE1|ABC234DEF567|H|a1b2c3d4|1696000000000|4bab47f28ff8495ea2321e99"
    private val k6jh = "BEE1|ABC234DEF567|JH|9f8e7d6c|1759740000000|63876437cff32f3128cea9a0"
    private val f5 = "BEE1|HIGHSCHOOL|ABC234DEF567|0123456789ab|e55e3d2def0a3eb4d977598de639f0d48c02645f37c4226bcb84d0d24b9793d4"

    @Test fun exactSamplesVerify() {
        assertTrue(UnlockCodeRecovery.verifyExact(k6))
        assertTrue(UnlockCodeRecovery.verifyExact(k6jh))
        assertTrue(UnlockCodeRecovery.verifyExact(f5))
    }

    @Test fun cleanTextWithUiNoise() {
        val ocr = "Give this payload to the student (or encode as QR):\n$k6\nCopy"
        assertEquals(k6, UnlockCodeRecovery.recover(ocr, dev)?.payload)
    }

    @Test fun wrappedOverTwoLines() {
        val ocr = "BEE1|ABC234DEF567|H|a1b2c3d4|16960\n00000000|4bab47f28ff8495ea2321e99"
        assertEquals(k6, UnlockCodeRecovery.recover(ocr, dev)?.payload)
    }

    @Test fun barsReadAsLettersAndLookalikes() {
        // | -> I / l, 0 -> O, 1 -> l, b -> 6? (kept), 8 -> B
        val ocr = "BEE1IABC234DEF567lHIa1b2c3d4l169600OOOOOOOI4bab47f2Bff8495ea232le99"
        assertEquals(k6, UnlockCodeRecovery.recover(ocr, dev)?.payload)
    }

    @Test fun deviceFieldMisreadButPhoneIdKnown() {
        val ocr = "BEE1|A8C234DEF5G7|JH|9f8e7d6c|1759740000000|63876437cff32f3128cea9a0"
        assertEquals(k6jh, UnlockCodeRecovery.recover(ocr, dev)?.payload)
    }

    @Test fun flutterLayout() {
        val ocr = "unlock QR ready.\n" + f5.replace("|", "I").replace("0", "O") + "\nCopy code"
        assertEquals(f5, UnlockCodeRecovery.recover(ocr, dev)?.payload)
    }

    @Test fun tamperedCodeNeverVerifies() {
        val bad = k6.replace("|H|", "|J|")
        assertNull(UnlockCodeRecovery.recover(bad, dev))
        val bad2 = k6.dropLast(1) + "0"
        assertNull(UnlockCodeRecovery.recover(bad2, dev))
        assertNull(UnlockCodeRecovery.recover("hello world BEE1 nothing here", dev))
    }

    @Test fun urlEncodedBars() {
        assertEquals(k6, UnlockCodeRecovery.recover(k6.replace("|", "%7C"), dev)?.payload)
    }
}
