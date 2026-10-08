package com.four.four_encryptor

import android.app.Activity
import android.content.ClipData
import android.content.Intent
import android.graphics.Bitmap
import android.graphics.pdf.PdfRenderer
import android.media.MediaMetadataRetriever
import android.net.Uri
import android.os.Handler
import android.os.Looper
import android.os.ParcelFileDescriptor
import android.provider.DocumentsContract
import android.provider.OpenableColumns
import io.flutter.embedding.android.FlutterActivity
import io.flutter.embedding.engine.FlutterEngine
import io.flutter.plugin.common.MethodCall
import io.flutter.plugin.common.MethodChannel
import java.io.ByteArrayOutputStream
import java.io.File
import java.io.FileInputStream
import java.io.OutputStream
import java.nio.ByteBuffer
import java.util.concurrent.Executors
import java.util.zip.ZipEntry
import java.util.zip.ZipInputStream
import java.util.zip.ZipOutputStream

/**
 * Storage Access Framework I/O for the encryptor. Inputs are read in place through their content URI
 * (positional reads on a file descriptor, one chunk per call), so a 2 GB video is never copied or held in RAM.
 * Outputs are created in the folder the user picked. There is no decrypt path in this app.
 */
class MainActivity : FlutterActivity() {
    private val io = Executors.newSingleThreadExecutor()
    private val main = Handler(Looper.getMainLooper())
    private var pending: MethodChannel.Result? = null
    private var pendingKind = ""
    private val inputs = HashMap<Int, ParcelFileDescriptor>()
    private val outputs = HashMap<Int, Pair<OutputStream, Uri>>()
    private var nextHandle = 1

    override fun configureFlutterEngine(flutterEngine: FlutterEngine) {
        super.configureFlutterEngine(flutterEngine)
        MethodChannel(flutterEngine.dartExecutor.binaryMessenger, "four.encryptor/io").setMethodCallHandler { call, result ->
            when (call.method) {
                "pickFiles" -> pick(result, "files") {
                    Intent(Intent.ACTION_OPEN_DOCUMENT).apply {
                        addCategory(Intent.CATEGORY_OPENABLE)
                        type = "*/*"
                        putExtra(Intent.EXTRA_MIME_TYPES, arrayOf("application/pdf", "video/*", "application/zip", "application/x-zip-compressed"))
                        putExtra(Intent.EXTRA_ALLOW_MULTIPLE, true)
                    }
                }
                "pickFolder" -> pick(result, "folder") {
                    Intent(Intent.ACTION_OPEN_DOCUMENT_TREE).addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION or Intent.FLAG_GRANT_WRITE_URI_PERMISSION or Intent.FLAG_GRANT_PERSISTABLE_URI_PERMISSION)
                }
                "pickBundleFolder" -> pick(result, "bundle") { Intent(Intent.ACTION_OPEN_DOCUMENT_TREE).addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION) }
                "hasFolder" -> result.success(contentResolver.persistedUriPermissions.any { it.uri.toString() == call.argument<String>("uri") && it.isWritePermission })
                "folderName" -> result.success(treeName(Uri.parse(call.argument<String>("uri")!!)))
                "share" -> { share(call.argument<List<String>>("uris")!!); result.success(null) }
                else -> bg(call, result)
            }
        }
    }

    private fun bg(call: MethodCall, result: MethodChannel.Result) = io.execute {
        try {
            val r: Any? = when (call.method) {
                "probe" -> probe(Uri.parse(call.argument<String>("uri")!!), call.argument<String>("mime") ?: "")
                "openIn" -> openIn(call.argument<String>("uri")!!)
                "read" -> read(call.argument<Int>("h")!!, (call.argument<Any>("off") as Number).toLong(), call.argument<Int>("len")!!)
                "closeIn" -> { inputs.remove(call.argument<Int>("h"))?.close(); null }
                "createOut" -> createOut(call.argument<String>("tree")!!, call.argument<String>("name")!!)
                "write" -> { outputs[call.argument<Int>("h")!!]!!.first.write(call.argument<ByteArray>("b")!!); null }
                "closeOut" -> closeOut(call.argument<Int>("h")!!, call.argument<Boolean>("ok") ?: true)
                "zipEntries" -> zipEntries(Uri.parse(call.argument<String>("uri")!!))
                "zipFolder" -> zipFolder(Uri.parse(call.argument<String>("uri")!!))
                "zipFiles" -> zipFiles(call.argument<String>("dir")!!)
                "deleteTemp" -> { File(call.argument<String>("path")!!).takeIf { it.canonicalPath.startsWith(cacheDir.canonicalPath) }?.delete(); null }
                "tempDir" -> File(cacheDir, "web").apply { mkdirs() }.path
                else -> { main.post { result.notImplemented() }; return@execute }
            }
            main.post { result.success(r) }
        } catch (e: Throwable) {
            main.post { result.error("io", e.message ?: e.toString(), null) }
        }
    }

    // ---- pickers
    private fun pick(result: MethodChannel.Result, kind: String, intent: () -> Intent) {
        if (pending != null) { result.error("busy", "picker already open", null); return }
        pending = result; pendingKind = kind
        @Suppress("DEPRECATION")
        startActivityForResult(intent(), 4711)
    }

    @Deprecated("Deprecated in Java")
    override fun onActivityResult(requestCode: Int, resultCode: Int, data: Intent?) {
        @Suppress("DEPRECATION")
        super.onActivityResult(requestCode, resultCode, data)
        if (requestCode != 4711) return
        val r = pending ?: return
        pending = null
        if (resultCode != Activity.RESULT_OK || data == null) { r.success(null); return }
        when (pendingKind) {
            "files" -> {
                val uris = mutableListOf<Uri>()
                data.clipData?.let { c -> for (i in 0 until c.itemCount) uris += c.getItemAt(i).uri }
                if (uris.isEmpty()) data.data?.let { uris += it }
                io.execute {
                    val list = uris.map { describe(it) }
                    main.post { r.success(list) }
                }
            }
            "folder" -> {
                val u = data.data!!
                contentResolver.takePersistableUriPermission(u, Intent.FLAG_GRANT_READ_URI_PERMISSION or Intent.FLAG_GRANT_WRITE_URI_PERMISSION)
                r.success(u.toString())
            }
            else -> r.success(data.data?.toString())
        }
    }

    private fun share(uris: List<String>) {
        if (uris.isEmpty()) return
        val list = ArrayList(uris.map { Uri.parse(it) })
        val send = if (list.size == 1) Intent(Intent.ACTION_SEND).putExtra(Intent.EXTRA_STREAM, list[0])
        else Intent(Intent.ACTION_SEND_MULTIPLE).putParcelableArrayListExtra(Intent.EXTRA_STREAM, list)
        send.type = "application/octet-stream"
        send.clipData = ClipData.newRawUri("", list[0]).apply { list.drop(1).forEach { addItem(ClipData.Item(it)) } }
        send.addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION)
        startActivity(Intent.createChooser(send, "Share encrypted files").addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION))
    }

    private fun describe(u: Uri): Map<String, Any?> {
        var name = u.lastPathSegment ?: "file"
        var size = -1L
        contentResolver.query(u, arrayOf(OpenableColumns.DISPLAY_NAME, OpenableColumns.SIZE), null, null, null)?.use { c ->
            if (c.moveToFirst()) {
                c.getString(0)?.let { name = it }
                if (!c.isNull(1)) size = c.getLong(1)
            }
        }
        return mapOf("uri" to u.toString(), "name" to name, "size" to size, "mime" to (contentResolver.getType(u) ?: ""))
    }

    private fun treeName(tree: Uri): String = try {
        val doc = DocumentsContract.buildDocumentUriUsingTree(tree, DocumentsContract.getTreeDocumentId(tree))
        contentResolver.query(doc, arrayOf(DocumentsContract.Document.COLUMN_DISPLAY_NAME), null, null, null)?.use { c -> if (c.moveToFirst()) c.getString(0) else null } ?: tree.lastPathSegment ?: "folder"
    } catch (_: Exception) { tree.lastPathSegment ?: "folder" }

    // ---- probe: duration / size / thumbnail / pdf pages (all platform APIs, nothing bundled)
    private fun probe(u: Uri, mime: String): Map<String, Any?> {
        val out = HashMap<String, Any?>()
        if (mime.startsWith("video/")) {
            val m = MediaMetadataRetriever()
            try {
                m.setDataSource(this, u)
                val w = m.extractMetadata(MediaMetadataRetriever.METADATA_KEY_VIDEO_WIDTH)?.toIntOrNull() ?: 0
                val h = m.extractMetadata(MediaMetadataRetriever.METADATA_KEY_VIDEO_HEIGHT)?.toIntOrNull() ?: 0
                val rot = m.extractMetadata(MediaMetadataRetriever.METADATA_KEY_VIDEO_ROTATION)?.toIntOrNull() ?: 0
                val dur = m.extractMetadata(MediaMetadataRetriever.METADATA_KEY_DURATION)?.toLongOrNull()
                val portrait = if (rot == 90 || rot == 270) w > h else h > w
                out["width"] = if (rot == 90 || rot == 270) h else w
                out["height"] = if (rot == 90 || rot == 270) w else h
                out["portrait"] = portrait
                out["durationMs"] = dur
                val at = ((dur ?: 10000L) / 10).coerceAtMost(2000L) * 1000L
                m.getFrameAtTime(at, MediaMetadataRetriever.OPTION_CLOSEST_SYNC)?.let { out["thumb"] = jpeg(it) }
            } finally {
                m.release()
            }
        } else if (mime == "application/pdf") {
            contentResolver.openFileDescriptor(u, "r")?.use { fd ->
                PdfRenderer(fd).use { pdf ->
                    out["pages"] = pdf.pageCount
                    if (pdf.pageCount > 0) pdf.openPage(0).use { p ->
                        val w = 240
                        val h = (240f * p.height / p.width).toInt().coerceIn(1, 480)
                        val bmp = Bitmap.createBitmap(w, h, Bitmap.Config.ARGB_8888)
                        bmp.eraseColor(android.graphics.Color.WHITE)
                        p.render(bmp, null, null, PdfRenderer.Page.RENDER_MODE_FOR_DISPLAY)
                        out["thumb"] = jpeg(bmp, false)
                        bmp.recycle()
                    }
                }
            }
        }
        return out
    }

    private fun jpeg(src: Bitmap, scale: Boolean = true): ByteArray {
        val b = if (scale && src.width > 320) Bitmap.createScaledBitmap(src, 320, (320f * src.height / src.width).toInt().coerceAtLeast(1), true) else src
        val bos = ByteArrayOutputStream()
        b.compress(Bitmap.CompressFormat.JPEG, 70, bos)
        if (b !== src) b.recycle()
        return bos.toByteArray()
    }

    // ---- streaming input
    private fun openIn(uri: String): Map<String, Any> {
        val u = Uri.parse(uri)
        val fd = if (uri.startsWith("/")) ParcelFileDescriptor.open(File(uri), ParcelFileDescriptor.MODE_READ_ONLY)
        else contentResolver.openFileDescriptor(u, "r") ?: throw IllegalStateException("cannot open $uri")
        val h = nextHandle++
        inputs[h] = fd
        return mapOf("h" to h, "size" to fd.statSize)
    }

    private fun read(h: Int, off: Long, len: Int): ByteArray {
        val fd = inputs[h] ?: throw IllegalStateException("closed")
        val ch = FileInputStream(fd.fileDescriptor).channel // positional read, no shared position
        val buf = ByteBuffer.allocate(len)
        var pos = off
        while (buf.hasRemaining()) {
            val n = ch.read(buf, pos)
            if (n < 0) throw IllegalStateException("short read")
            pos += n
        }
        return buf.array()
    }

    // ---- output into the picked folder
    private fun createOut(tree: String, name: String): Map<String, Any> {
        val t = Uri.parse(tree)
        val parent = DocumentsContract.buildDocumentUriUsingTree(t, DocumentsContract.getTreeDocumentId(t))
        // "application/octet-stream" keeps providers from appending their own extension
        val doc = DocumentsContract.createDocument(contentResolver, parent, "application/octet-stream", name) ?: throw IllegalStateException("cannot create $name")
        val os = contentResolver.openOutputStream(doc, "w") ?: throw IllegalStateException("cannot write $name")
        val h = nextHandle++
        outputs[h] = Pair(os.buffered(1 shl 18), doc)
        return mapOf("h" to h, "uri" to doc.toString(), "name" to (describe(doc)["name"] ?: name))
    }

    private fun closeOut(h: Int, ok: Boolean): Any? {
        val (os, doc) = outputs.remove(h) ?: return null
        try { os.close() } finally { if (!ok) runCatching { DocumentsContract.deleteDocument(contentResolver, doc) } }
        return null
    }

    // ---- web bundles (.4web): a saved page folder or a .zip with an index.html
    private fun zipEntries(u: Uri): List<String> {
        val names = mutableListOf<String>()
        contentResolver.openInputStream(u)?.use { s -> ZipInputStream(s.buffered()).use { z ->
            while (true) { val e = z.nextEntry ?: break; if (!e.isDirectory) names += e.name; if (names.size > 20000) break }
        } }
        return names
    }

    /** Zips a SAF folder tree into the app cache (stored as a temp file; deleted after encryption). */
    private fun zipFolder(tree: Uri): Map<String, Any> {
        val out = File(File(cacheDir, "web").apply { mkdirs() }, "bundle_${System.currentTimeMillis()}.zip")
        val names = mutableListOf<String>()
        ZipOutputStream(out.outputStream().buffered()).use { z ->
            fun walk(docId: String, prefix: String) {
                val children = DocumentsContract.buildChildDocumentsUriUsingTree(tree, docId)
                contentResolver.query(children, arrayOf(DocumentsContract.Document.COLUMN_DOCUMENT_ID, DocumentsContract.Document.COLUMN_DISPLAY_NAME, DocumentsContract.Document.COLUMN_MIME_TYPE), null, null, null)?.use { c ->
                    while (c.moveToNext()) {
                        val id = c.getString(0); val name = c.getString(1); val mime = c.getString(2)
                        if (mime == DocumentsContract.Document.MIME_TYPE_DIR) walk(id, "$prefix$name/")
                        else {
                            z.putNextEntry(ZipEntry("$prefix$name"))
                            contentResolver.openInputStream(DocumentsContract.buildDocumentUriUsingTree(tree, id))?.use { it.copyTo(z, 1 shl 16) }
                            z.closeEntry()
                            names += "$prefix$name"
                        }
                    }
                }
            }
            walk(DocumentsContract.getTreeDocumentId(tree), "")
        }
        return mapOf("path" to out.path, "entries" to names, "name" to treeName(tree))
    }

    /** Zips a plain directory written by the LabXchange importer (cache/web/<id>/) and removes the directory. */
    private fun zipFiles(dir: String): Map<String, Any> {
        val root = File(dir)
        require(root.canonicalPath.startsWith(cacheDir.canonicalPath)) { "outside cache" }
        val out = File(root.parentFile, "${root.name}.zip")
        val names = mutableListOf<String>()
        ZipOutputStream(out.outputStream().buffered()).use { z ->
            root.walkTopDown().filter { it.isFile }.forEach { f ->
                val n = f.relativeTo(root).invariantSeparatorsPath
                z.putNextEntry(ZipEntry(n)); f.inputStream().use { it.copyTo(z, 1 shl 16) }; z.closeEntry(); names += n
            }
        }
        root.deleteRecursively()
        return mapOf("path" to out.path, "entries" to names)
    }

    override fun onDestroy() {
        inputs.values.forEach { runCatching { it.close() } }
        outputs.values.forEach { runCatching { it.first.close() } }
        super.onDestroy()
    }
}
