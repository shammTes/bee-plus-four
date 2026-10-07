package com.warsay.high

import java.io.File
import java.io.RandomAccessFile
import java.nio.ByteBuffer
import javax.crypto.Cipher
import javax.crypto.spec.GCMParameterSpec
import javax.crypto.spec.SecretKeySpec

/** Plaintext preamble of a 4 resource (see packages/four_format/lib/src/format.dart). */
class FourPreamble(
    val fileId: ByteArray,
    val noncePrefix: ByteArray,
    val chunkSize: Int,
    val chunkCount: Int,
    val plainSize: Long,
    val dataStart: Long,
    val wrappedBatchKey: ByteArray,
    val wrappedContentKey: ByteArray,
    val batchId: String,
) {
    fun plainLenOf(i: Int): Int = if (i < chunkCount - 1) chunkSize else (plainSize - chunkSize.toLong() * (chunkCount - 1)).toInt()
    fun offsetOf(i: Int): Long = dataStart + i.toLong() * (chunkSize + 16)

    companion object {
        fun read(file: File): FourPreamble = RandomAccessFile(file, "r").use { raf ->
            val head = ByteArray(minOf(raf.length(), 300L).toInt())
            raf.readFully(head)
            parse(head)
        }

        fun parse(b: ByteArray): FourPreamble {
            require(b.size >= 26 && b[0] == 0x34.toByte() && b[1] == 0x52.toByte() && b[2] == 0x45.toByte() && b[3] == 0x53.toByte()) { "not a 4 resource" }
            require(b[4].toInt() == 1) { "unsupported version ${b[4]}" }
            val bb = ByteBuffer.wrap(b) // big-endian
            bb.position(8)
            val id = ByteArray(16).also { bb.get(it) }
            val bl = bb.get().toInt() and 0xff
            val bid = ByteArray(bl).also { bb.get(it) }
            val wbk = ByteArray(60).also { bb.get(it) }
            val wck = ByteArray(60).also { bb.get(it) }
            val np = ByteArray(8).also { bb.get(it) }
            val cs = bb.int
            val cc = bb.int
            val ps = bb.long
            val hl = bb.int.toLong() and 0xffffffffL
            val tl = bb.int.toLong() and 0xffffffffL
            val encoded = bb.position().toLong()
            require(cs in 1..(8 shl 20)) { "bad chunk size" }
            return FourPreamble(id, np, cs, cc, ps, encoded + hl + tl, wbk, wck, String(bid, Charsets.UTF_8))
        }
    }
}

/**
 * Random-access plaintext over an encrypted 4 file. Decrypts only the 256 KiB chunk a read touches
 * (javax.crypto AES-GCM: hardware AES on ARMv8 phones), keeping the last chunk cached for sequential reads.
 * Thread-safe; the content key is passed from Dart after the unlock gate released it and never touches disk.
 */
class FourChunkReader(file: File, key: ByteArray, val pre: FourPreamble = FourPreamble.read(file)) : AutoCloseable {
    private val raf = RandomAccessFile(file, "r")
    private val keySpec = SecretKeySpec(key.copyOf(), "AES")
    private val cipher = Cipher.getInstance("AES/GCM/NoPadding")
    private val cipherBuf = ByteArray(pre.chunkSize + 16)
    private var cachedIndex = -1
    private var cached = ByteArray(0)
    var chunksDecrypted = 0L
        private set

    val length: Long get() = pre.plainSize

    init {
        require(raf.length() == pre.dataStart + pre.plainSize + pre.chunkCount * 16L + 36) { "file length mismatch (truncated?)" }
    }

    @Synchronized
    fun chunk(i: Int): ByteArray {
        if (i == cachedIndex) return cached
        val len = pre.plainLenOf(i)
        raf.seek(pre.offsetOf(i))
        raf.readFully(cipherBuf, 0, len + 16)
        val nonce = ByteArray(12)
        System.arraycopy(pre.noncePrefix, 0, nonce, 0, 8)
        ByteBuffer.wrap(nonce, 8, 4).putInt(i)
        val aad = ByteArray(21)
        System.arraycopy(pre.fileId, 0, aad, 0, 16)
        ByteBuffer.wrap(aad, 16, 4).putInt(i)
        aad[20] = if (i == pre.chunkCount - 1) 1 else 0
        cipher.init(Cipher.DECRYPT_MODE, keySpec, GCMParameterSpec(128, nonce))
        cipher.updateAAD(aad)
        val out = cipher.doFinal(cipherBuf, 0, len + 16) // throws AEADBadTagException if modified
        cachedIndex = i
        cached = out
        chunksDecrypted++
        return out
    }

    /** Copies plaintext at [pos] into [buf]; returns bytes copied (≤ len, stops at a chunk boundary), -1 at end. */
    @Synchronized
    fun read(pos: Long, buf: ByteArray, off: Int, len: Int): Int {
        if (pos >= pre.plainSize) return -1
        val ci = (pos / pre.chunkSize).toInt()
        val inner = (pos - ci.toLong() * pre.chunkSize).toInt()
        val c = chunk(ci)
        val n = minOf(len, c.size - inner)
        System.arraycopy(c, inner, buf, off, n)
        return n
    }

    @Synchronized
    override fun close() {
        raf.close()
        cached.fill(0)
        cachedIndex = -1
    }
}
