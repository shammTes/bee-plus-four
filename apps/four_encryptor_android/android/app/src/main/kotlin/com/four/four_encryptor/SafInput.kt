package com.four.four_encryptor

import java.io.EOFException
import java.io.IOException
import java.io.InputStream

/** Random-access reads for the encryptor. Two implementations: pread on a seekable fd, or a sequential stream. */
interface ChunkInput : AutoCloseable {
    val size: Long
    val mode: String
    fun read(off: Long, len: Int): ByteArray
}

/** Reads a fully seekable source with positional reads (no shared file position). */
class PreadInput(override val size: Long, private val pread: (ByteArray, Int, Int, Long) -> Int, private val onClose: () -> Unit) : ChunkInput {
    override val mode = "pread"
    override fun read(off: Long, len: Int): ByteArray {
        checkRange(off, len, size)
        val b = ByteArray(len)
        var done = 0
        while (done < len) {
            val n = pread(b, done, len - done, off + done)
            if (n <= 0) throw EOFException("file ended after ${off + done} of $size bytes (provider reported a larger size)")
            done += n
        }
        return b
    }
    override fun close() = onClose()
}

/**
 * Sequential fallback for providers that hand out pipes or non-seekable streams (cloud/Photos items, some
 * gallery apps). The encryptor reads chunks in increasing order, so this costs nothing; a backwards read reopens.
 */
class StreamInput(override val size: Long, private val open: () -> InputStream) : ChunkInput {
    override val mode = "stream"
    private var ins: InputStream? = null
    private var pos = 0L

    override fun read(off: Long, len: Int): ByteArray {
        checkRange(off, len, size)
        if (ins == null || off < pos) { ins?.close(); ins = open(); pos = 0 }
        val s = ins!!
        while (pos < off) {
            val k = s.skip(off - pos)
            if (k <= 0) { if (s.read() < 0) throw EOFException("file ended at $pos of $size bytes"); pos++ } else pos += k
        }
        val b = ByteArray(len)
        var done = 0
        while (done < len) {
            val n = s.read(b, done, len - done)
            if (n < 0) throw EOFException("file ended after ${pos + done} of $size bytes")
            done += n
        }
        pos += len
        return b
    }
    override fun close() { ins?.close(); ins = null }
}

internal fun checkRange(off: Long, len: Int, size: Long) {
    if (off < 0 || len < 0 || off + len > size) throw IOException("read outside file: offset $off + $len > size $size")
}
