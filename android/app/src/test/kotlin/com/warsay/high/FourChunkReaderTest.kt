package com.warsay.high

import androidx.media3.common.C
import androidx.media3.datasource.DataSpec
import android.net.Uri
import org.junit.Assert.assertArrayEquals
import org.junit.Assert.assertEquals
import org.junit.Assert.assertTrue
import org.junit.Test
import java.io.File
import java.nio.ByteBuffer
import java.security.MessageDigest
import javax.crypto.AEADBadTagException
import javax.crypto.Cipher
import javax.crypto.spec.GCMParameterSpec
import javax.crypto.spec.SecretKeySpec

/**
 * JVM tests for the native video decrypt path. Fixture `pattern.4vid` = 100 000 bytes of (i*31+7)&0xff,
 * 4 KiB chunks, made with `four_encrypt --chunk 4096` and the DEV master key.
 */
class FourChunkReaderTest {
    private val uri: Uri = org.mockito.Mockito.mock(Uri::class.java)
    private val fixture = File(javaClass.classLoader!!.getResource("pattern.4vid")!!.toURI())
    private fun expected(n: Int = 100_000) = ByteArray(n) { ((it * 31 + 7) and 0xff).toByte() }

    private fun gcmOpen(key: ByteArray, wrapped: ByteArray, aad: ByteArray): ByteArray {
        val c = Cipher.getInstance("AES/GCM/NoPadding")
        c.init(Cipher.DECRYPT_MODE, SecretKeySpec(key, "AES"), GCMParameterSpec(128, wrapped.copyOfRange(0, 12)))
        c.updateAAD(aad)
        return c.doFinal(wrapped, 12, wrapped.size - 12)
    }

    private fun contentKey(): ByteArray {
        val mk = MessageDigest.getInstance("SHA-256").digest("4RES-DEV-MASTER-KEY-v1-CHANGE-IN-RELEASE".toByteArray())
        val p = FourPreamble.read(fixture)
        val bk = gcmOpen(mk, p.wrappedBatchKey, "4RES-BK|${p.batchId}".toByteArray())
        return gcmOpen(bk, p.wrappedContentKey, p.fileId)
    }

    @Test fun readsWholeFile() {
        FourChunkReader(fixture, contentKey()).use { r ->
            assertEquals(100_000L, r.length)
            val out = ByteArray(100_000)
            var pos = 0
            while (pos < out.size) pos += r.read(pos.toLong(), out, pos, 7000)
            assertArrayEquals(expected(), out)
        }
    }

    @Test fun seekDecryptsOnlyTouchedChunk() {
        FourChunkReader(fixture, contentKey()).use { r ->
            val b = ByteArray(100)
            val n = r.read(50_000, b, 0, 100)
            assertEquals(100, n)
            assertArrayEquals(expected().copyOfRange(50_000, 50_100), b)
            assertEquals(1L, r.chunksDecrypted)
            r.read(50_200, b, 0, 50) // same chunk → cached
            assertEquals(1L, r.chunksDecrypted)
            assertEquals(-1, r.read(100_000, b, 0, 10))
        }
    }

    @Test fun dataSourceRangeRequests() {
        FourChunkReader(fixture, contentKey()).use { r ->
            val ds = FourDataSource(r)
            val len = ds.open(DataSpec.Builder().setUri(uri).setPosition(40_000).setLength(10_000).build())
            assertEquals(10_000L, len)
            val out = ByteArray(10_000)
            var got = 0
            while (true) {
                val n = ds.read(out, got, out.size - got + 100)
                if (n == C.RESULT_END_OF_INPUT) break
                got += n
            }
            ds.close()
            assertEquals(10_000, got)
            assertArrayEquals(expected().copyOfRange(40_000, 50_000), out)
            // open-ended
            assertEquals(1_000L, ds.open(DataSpec.Builder().setUri(uri).setPosition(99_000).build()))
            ds.close()
        }
    }

    @Test(expected = AEADBadTagException::class) fun wrongKeyFails() {
        FourChunkReader(fixture, ByteArray(32)).use { it.read(0, ByteArray(10), 0, 10) }
    }

    @Test fun tamperedChunkFails() {
        val tmp = File.createTempFile("four", ".4vid")
        fixture.copyTo(tmp, overwrite = true)
        val p = FourPreamble.read(tmp)
        val bytes = tmp.readBytes()
        bytes[(p.offsetOf(3) + 10).toInt()] = (bytes[(p.offsetOf(3) + 10).toInt()].toInt() xor 1).toByte()
        tmp.writeBytes(bytes)
        FourChunkReader(tmp, contentKey()).use { r ->
            r.read(0, ByteArray(10), 0, 10)
            var failed = false
            try { r.read(3L * 4096, ByteArray(10), 0, 10) } catch (_: AEADBadTagException) { failed = true }
            assertTrue(failed)
        }
        tmp.delete()
    }

    @Test fun truncatedFileRejected() {
        val tmp = File.createTempFile("four", ".4vid")
        tmp.writeBytes(fixture.readBytes().copyOfRange(0, fixture.length().toInt() - 50))
        var failed = false
        try { FourChunkReader(tmp, contentKey()) } catch (_: IllegalArgumentException) { failed = true }
        assertTrue(failed)
        tmp.delete()
    }

    /** Throughput of the same AES-GCM chunk work on this JVM (desktop number; phones are slower). */
    @Test fun benchmarkThroughput() {
        val key = SecretKeySpec(ByteArray(32) { it.toByte() }, "AES")
        val chunk = ByteArray(256 * 1024) { it.toByte() }
        val enc = Cipher.getInstance("AES/GCM/NoPadding")
        val nonce = ByteArray(12)
        enc.init(Cipher.ENCRYPT_MODE, key, GCMParameterSpec(128, nonce))
        val ct = enc.doFinal(chunk)
        val dec = Cipher.getInstance("AES/GCM/NoPadding")
        repeat(300) { dec.init(Cipher.DECRYPT_MODE, key, GCMParameterSpec(128, nonce)); dec.doFinal(ct) }
        val n = 1000
        val t0 = System.nanoTime()
        repeat(n) { dec.init(Cipher.DECRYPT_MODE, key, GCMParameterSpec(128, nonce)); dec.doFinal(ct) }
        val s = (System.nanoTime() - t0) / 1e9
        println("FOUR_BENCH javax AES-GCM decrypt: %.0f MB/s (%d x 256 KiB)".format(n * 0.262144 / s, n))
        ByteBuffer.allocate(1)
    }
}
