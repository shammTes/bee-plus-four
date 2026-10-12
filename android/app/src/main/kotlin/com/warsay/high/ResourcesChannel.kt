package com.warsay.high

import android.content.Intent
import android.net.Uri
import android.provider.DocumentsContract
import android.view.WindowManager
import androidx.activity.result.ActivityResultLauncher
import androidx.activity.result.contract.ActivityResultContracts
import io.flutter.embedding.android.FlutterFragmentActivity
import io.flutter.plugin.common.BinaryMessenger
import io.flutter.plugin.common.MethodChannel
import java.io.File
import java.util.concurrent.Executors

/**
 * Add-on resources (`com.warsay.high/resources`):
 *  - pickFolder          → SAF folder picker, persisted read permission; returns tree uri or null
 *  - hasFolder(uri)      → permission still held?
 *  - listFolder(uri)     → [{uri, name, size, head(bytes ≤ 64)}] for files (3 levels deep) whose first bytes are "4RES"
 *  - importFile(uri, dest) → streaming copy into app-private storage (still encrypted)
 *  - setSecure(bool)     → FLAG_SECURE on/off (no screenshots / screen recording / recents preview). Dart reference-
 *                          counts the holders (resource viewers + Notes/Matric sections, lib/licensing/screenshot.dart)
 *                          and only sends the 0→1 / 1→0 transitions; onResume re-applies [secure].
 *  - openWeb(path, key, entry, title, credit) → decrypts a .4web zip into memory, opens [FourWebActivity]
 * No storage permission is needed: SAF grants access to the chosen folder only.
 */
class ResourcesChannel(private val activity: FlutterFragmentActivity) {
    companion object {
        const val CHANNEL = "com.warsay.high/resources"
        @Volatile var secure = false
        private val MAGIC = byteArrayOf(0x34, 0x52, 0x45, 0x53)
    }

    private val io = Executors.newSingleThreadExecutor()
    private var pickResult: MethodChannel.Result? = null

    val treeLauncher: ActivityResultLauncher<Uri?> =
        activity.registerForActivityResult(ActivityResultContracts.OpenDocumentTree()) { uri ->
            val r = pickResult
            pickResult = null
            if (uri == null) { r?.success(null); return@registerForActivityResult }
            try {
                activity.contentResolver.takePersistableUriPermission(uri, Intent.FLAG_GRANT_READ_URI_PERMISSION)
            } catch (e: Throwable) {
                HighLog.e("takePersistableUriPermission failed", e)
            }
            r?.success(uri.toString())
        }

    fun attach(messenger: BinaryMessenger) {
        MethodChannel(messenger, CHANNEL).setMethodCallHandler { call, result ->
            when (call.method) {
                "pickFolder" -> {
                    pickResult?.success(null)
                    pickResult = result
                    try { treeLauncher.launch(null) } catch (e: Throwable) {
                        pickResult = null
                        result.error("no_picker", "No folder picker on this phone: ${e.message}", null)
                    }
                }
                "hasFolder" -> {
                    val u = call.argument<String>("uri")
                    result.success(u != null && activity.contentResolver.persistedUriPermissions.any { it.uri.toString() == u && it.isReadPermission })
                }
                "listFolder" -> {
                    val u = Uri.parse(call.argument<String>("uri"))
                    io.execute {
                        try {
                            val out = ArrayList<Map<String, Any?>>()
                            val root = DocumentsContract.buildDocumentUriUsingTree(u, DocumentsContract.getTreeDocumentId(u))
                            walk(u, DocumentsContract.getDocumentId(root), 0, out)
                            activity.runOnUiThread { result.success(out) }
                        } catch (e: Throwable) {
                            HighLog.e("listFolder failed", e)
                            activity.runOnUiThread { result.error("list", "${e.javaClass.simpleName}: ${e.message}", null) }
                        }
                    }
                }
                "listApks" -> {
                    // offline update: APKs shared via SHAREit / cable into the chosen folder
                    val u = Uri.parse(call.argument<String>("uri"))
                    io.execute {
                        try {
                            val apks = ArrayList<Map<String, Any?>>()
                            val root = DocumentsContract.buildDocumentUriUsingTree(u, DocumentsContract.getTreeDocumentId(u))
                            walk(u, DocumentsContract.getDocumentId(root), 0, ArrayList(), apks)
                            activity.runOnUiThread { result.success(apks) }
                        } catch (e: Throwable) {
                            activity.runOnUiThread { result.error("list", "${e.javaClass.simpleName}: ${e.message}", null) }
                        }
                    }
                }
                "importFile" -> {
                    val u = Uri.parse(call.argument<String>("uri"))
                    val dest = File(call.argument<String>("dest")!!)
                    io.execute {
                        try {
                            dest.parentFile?.mkdirs()
                            var n = 0L
                            activity.contentResolver.openInputStream(u)!!.use { ins ->
                                dest.outputStream().use { os -> n = ins.copyTo(os, 256 * 1024) }
                            }
                            activity.runOnUiThread { result.success(n) }
                        } catch (e: Throwable) {
                            dest.delete()
                            HighLog.e("importFile failed", e)
                            activity.runOnUiThread { result.error("import", "${e.javaClass.simpleName}: ${e.message}", null) }
                        }
                    }
                }
                "openWeb" -> {
                    val path = call.argument<String>("path")!!
                    val key = call.argument<ByteArray>("key")!!
                    val entry = call.argument<String>("entry") ?: ""
                    io.execute {
                        try {
                            val b = FourWebBundle.open(File(path), key, entry)
                            key.fill(0)
                            FourWebHolder.bundle = b
                            FourWebHolder.title = call.argument<String>("title") ?: ""
                            FourWebHolder.credit = call.argument<String>("credit") ?: ""
                            activity.runOnUiThread {
                                activity.startActivity(Intent(activity, FourWebActivity::class.java))
                                result.success(null)
                            }
                        } catch (e: Throwable) {
                            key.fill(0)
                            HighLog.e("openWeb failed", e)
                            activity.runOnUiThread { result.error("web", "${e.javaClass.simpleName}: ${e.message}", null) }
                        }
                    }
                }
                "setSecure" -> {
                    val on = call.argument<Boolean>("on") == true
                    secure = on
                    activity.runOnUiThread {
                        if (on) activity.window.addFlags(WindowManager.LayoutParams.FLAG_SECURE)
                        else activity.window.clearFlags(WindowManager.LayoutParams.FLAG_SECURE)
                        result.success(null)
                    }
                }
                else -> result.notImplemented()
            }
        }
    }

    private fun walk(tree: Uri, docId: String, depth: Int, out: ArrayList<Map<String, Any?>>, apks: ArrayList<Map<String, Any?>>? = null) {
        val children = DocumentsContract.buildChildDocumentsUriUsingTree(tree, docId)
        val cols = arrayOf(
            DocumentsContract.Document.COLUMN_DOCUMENT_ID,
            DocumentsContract.Document.COLUMN_DISPLAY_NAME,
            DocumentsContract.Document.COLUMN_MIME_TYPE,
            DocumentsContract.Document.COLUMN_SIZE,
        )
        activity.contentResolver.query(children, cols, null, null, null)?.use { c ->
            while (c.moveToNext()) {
                val id = c.getString(0) ?: continue
                val name = c.getString(1) ?: ""
                val mime = c.getString(2) ?: ""
                val size = if (c.isNull(3)) 0L else c.getLong(3)
                if (mime == DocumentsContract.Document.MIME_TYPE_DIR) {
                    if (depth < 3) walk(tree, id, depth + 1, out, apks)
                    continue
                }
                if (apks != null && (name.endsWith(".apk", true) || mime == "application/vnd.android.package-archive")) {
                    apks.add(mapOf("uri" to DocumentsContract.buildDocumentUriUsingTree(tree, id).toString(), "name" to name, "size" to size))
                    continue
                }
                if (apks != null) continue
                if (size in 1..63) continue
                val docUri = DocumentsContract.buildDocumentUriUsingTree(tree, id)
                // detect by magic bytes, not extension (SHAREit/Bluetooth may rename files)
                val head = try {
                    activity.contentResolver.openInputStream(docUri)?.use { ins ->
                        val b = ByteArray(64)
                        var got = 0
                        while (got < 64) { val r = ins.read(b, got, 64 - got); if (r <= 0) break; got += r }
                        b.copyOf(got)
                    }
                } catch (e: Throwable) { null } ?: continue
                if (head.size < 25 || !(0 until 4).all { head[it] == MAGIC[it] }) continue
                out.add(mapOf("uri" to docUri.toString(), "name" to name, "size" to size, "head" to head))
            }
        }
    }
}
