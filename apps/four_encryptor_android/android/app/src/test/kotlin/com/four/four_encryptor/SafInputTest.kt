package com.four.four_encryptor

import java.io.ByteArrayInputStream
import java.io.EOFException
import java.io.FilterInputStream
import java.io.IOException
import java.io.InputStream
import java.io.RandomAccessFile
import org.junit.Assert.assertArrayEquals
import org.junit.Assert.assertEquals
import org.junit.Assert.assertTrue
import org.junit.Test

class SafInputTest {
    private val data = ByteArray(1_000_003) { (it * 31 + 7).toByte() }

    /** Pipe-like stream: short reads, skip() refuses (returns 0) like many provider pipes. */
    private fun pipe(bytes: ByteArray): InputStream = object : FilterInputStream(ByteArrayInputStream(bytes)) {
        override fun read(b: ByteArray, off: Int, len: Int) = super.read(b, off, minOf(len, 4093))
        override fun skip(n: Long) = 0L
    }

    @Test fun streamReadsChunksInOrder() {
        var opens = 0
        val s = StreamInput(data.size.toLong()) { opens++; pipe(data) }
        var off = 0L
        while (off < data.size) {
            val n = minOf(262144L, data.size - off).toInt()
            assertArrayEquals(data.copyOfRange(off.toInt(), off.toInt() + n), s.read(off, n))
            off += n
        }
        assertEquals(1, opens)
        s.close()
    }

    @Test fun streamSkipsForwardAndReopensBackwards() {
        var opens = 0
        val s = StreamInput(data.size.toLong()) { opens++; pipe(data) }
        assertArrayEquals(data.copyOfRange(500_000, 500_100), s.read(500_000, 100))
        assertArrayEquals(data.copyOfRange(10, 20), s.read(10, 10))
        assertEquals(2, opens)
    }

    @Test fun streamShorterThanReportedGivesClearEof() {
        val s = StreamInput(data.size.toLong() + 10) { pipe(data) }
        val e = runCatching { s.read(data.size.toLong() - 5, 15) }.exceptionOrNull()
        assertTrue(e is EOFException && e.message!!.contains("file ended"))
    }

    @Test fun preadOverFile() {
        val f = java.io.File.createTempFile("pin", ".bin").apply { writeBytes(data); deleteOnExit() }
        val raf = RandomAccessFile(f, "r")
        val p = PreadInput(f.length(), { b, o, l, pos -> raf.channel.read(java.nio.ByteBuffer.wrap(b, o, minOf(l, 7000)), pos) }, { raf.close() })
        assertArrayEquals(data.copyOfRange(999_000, 1_000_003), p.read(999_000, 1003))
        assertArrayEquals(data.copyOfRange(0, 300_000), p.read(0, 300_000))
        p.close()
    }

    @Test fun preadEofAndRangeChecks() {
        val p = PreadInput(100, { _, _, _, pos -> if (pos < 50) 10 else -1 }, {})
        assertTrue(runCatching { p.read(0, 100) }.exceptionOrNull() is EOFException)
        assertTrue(runCatching { p.read(95, 10) }.exceptionOrNull() is IOException)
        assertTrue(runCatching { p.read(-1, 1) }.exceptionOrNull() is IOException)
    }

    @Test fun offsetsBeyond2GbUseLongs() {
        val big = 3L * 1024 * 1024 * 1024
        var seen = -1L
        val p = PreadInput(big, { b, o, l, pos -> seen = pos; l }, {})
        p.read(big - 262144, 262144)
        assertEquals(big - 262144, seen)
    }
}
