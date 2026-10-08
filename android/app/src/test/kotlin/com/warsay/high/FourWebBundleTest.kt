package com.warsay.high

import org.junit.Assert.assertArrayEquals
import org.junit.Assert.assertEquals
import org.junit.Assert.assertThrows
import org.junit.Test
import java.io.ByteArrayInputStream
import java.io.ByteArrayOutputStream
import java.util.zip.ZipEntry
import java.util.zip.ZipOutputStream

class FourWebBundleTest {
    private fun zip(vararg files: Pair<String, String>): ByteArray {
        val bos = ByteArrayOutputStream()
        ZipOutputStream(bos).use { z -> files.forEach { (n, c) -> z.putNextEntry(ZipEntry(n)); z.write(c.toByteArray()); z.closeEntry() } }
        return bos.toByteArray()
    }

    @Test fun servesOnlyBundleFilesOnTheFakeOrigin() {
        val b = FourWebBundle.unzip(ByteArrayInputStream(zip("sim/index.html" to "<h1>hi</h1>", "sim/js/app.js" to "x=1", "sim/img/a b.png" to "P", "../evil" to "no")), "sim/index.html")
        assertEquals(200, b.resolve("https://4web.invalid/sim/index.html").status)
        assertEquals("text/html", b.resolve("https://4web.invalid/sim/index.html?x=1#top").mime)
        assertEquals("text/javascript", b.resolve("https://4web.invalid/sim/js/app.js").mime)
        assertArrayEquals("P".toByteArray(), b.resolve("https://4web.invalid/sim/img/a%20b.png").body)
        assertEquals(200, b.resolve("https://4web.invalid/sim/").status) // directory → index.html
        assertEquals(404, b.resolve("https://4web.invalid/sim/missing.js").status)
        assertEquals(403, b.resolve("https://cdn.example.com/lib.js").status) // network blocked
        assertEquals(403, b.resolve("http://4web.invalid/sim/index.html").status)
        assertEquals(404, b.resolve("https://4web.invalid/evil").status) // zip-slip entries dropped
    }

    @Test fun missingStartPageIsRejected() {
        assertThrows(IllegalArgumentException::class.java) { FourWebBundle.unzip(ByteArrayInputStream(zip("a.html" to "x")), "index.html") }
    }
}
