package com.warsay.high

import android.content.ClipData
import android.content.Context
import android.content.Intent
import android.content.pm.PackageInfo
import android.content.pm.PackageManager
import android.net.Uri
import android.os.Build
import android.provider.DocumentsContract
import android.provider.Settings
import androidx.activity.result.ActivityResultLauncher
import androidx.activity.result.contract.ActivityResultContracts
import androidx.core.content.FileProvider
import io.flutter.embedding.android.FlutterFragmentActivity
import io.flutter.plugin.common.BinaryMessenger
import io.flutter.plugin.common.MethodChannel
import java.io.File
import java.security.MessageDigest
import java.util.concurrent.Executors

/**
 * App updates from a FILE only (`com.warsay.high/update`). There is no network code: a newer 4 APK arrives by
 * SHAREit / Bluetooth / Nearby Share / cable and is checked here before the system installer opens.
 *  - info                    → {package, versionCode, versionName, cert, canInstall}
 *  - inspectApk{path}        → {package, versionCode, versionName, cert} of an APK file (null if unreadable)
 *  - findApks{trees, package, above, skip}
 *                            → APKs in the SAF folders (3 levels deep) whose manifest is [package] with
 *                              versionCode > [above]: [{uri, name, size, modified, key, versionCode, versionName}].
 *                              Other APKs come back as {key, other: true} so Dart can skip them next time.
 *                              Manifest-only parse (cheap); the full signature check runs on the copy (inspectApk).
 *  - pickApk                 → SAF "open document" for one .apk (starts in Download); returns uri or null
 *  - install{path}           → opens the system installer (one tap "Update"); asks for "install unknown apps" first
 *  - shareSelf               → copies the installed APK (+ splits) to cacheDir/share and opens the share sheet;
 *                              returns {files, splits, bytes}
 * cert = SHA-256 of the signing certificate, lowercase hex. Android refuses an update signed with another key
 * anyway; checking first gives a clear message instead of "App not installed".
 * No storage permission is used: SAF grants access to the folders / files the user chose.
 */
class UpdateChannel(private val activity: FlutterFragmentActivity) {
    private val io = Executors.newSingleThreadExecutor()
    private var pickResult: MethodChannel.Result? = null

    private object OpenApk : ActivityResultContracts.OpenDocument() {
        override fun createIntent(context: Context, input: Array<String>): Intent {
            val i = super.createIntent(context, input)
            if (Build.VERSION.SDK_INT >= 26) {
                // start where SHAREit / Bluetooth / browsers save files; the user can browse elsewhere
                i.putExtra(DocumentsContract.EXTRA_INITIAL_URI, DocumentsContract.buildDocumentUri("com.android.externalstorage.documents", "primary:Download"))
            }
            return i
        }
    }

    private val apkLauncher: ActivityResultLauncher<Array<String>> =
        activity.registerForActivityResult(OpenApk) { uri ->
            val r = pickResult
            pickResult = null
            r?.success(uri?.toString())
        }

    fun attach(messenger: BinaryMessenger) {
        MethodChannel(messenger, "com.warsay.high/update").setMethodCallHandler { call, result ->
            try {
                when (call.method) {
                    "info" -> result.success(info())
                    "inspectApk" -> {
                        val path = call.argument<String>("path")!!
                        bg(result, "inspectApk") { inspect(path) }
                    }
                    "findApks" -> {
                        val trees = call.argument<List<String>>("trees") ?: emptyList()
                        val pkg = call.argument<String>("package") ?: activity.packageName
                        val above = (call.argument<Number>("above") ?: 0).toLong()
                        val skip = (call.argument<List<String>>("skip") ?: emptyList()).toHashSet()
                        bg(result, "findApks") { findApks(trees, pkg, above, skip) }
                    }
                    "pickApk" -> {
                        pickResult?.success(null)
                        pickResult = result
                        try {
                            apkLauncher.launch(arrayOf("application/vnd.android.package-archive", "application/octet-stream", "application/zip"))
                        } catch (e: Throwable) {
                            pickResult = null
                            result.error("no_picker", "No file picker on this phone: ${e.message}", null)
                        }
                    }
                    "install" -> result.success(install(call.argument<String>("path")!!))
                    "shareSelf" -> bg(result, "shareSelf") { shareSelf() }
                    else -> result.notImplemented()
                }
            } catch (e: Throwable) {
                HighLog.e("update ${call.method} failed", e)
                result.error("update", "${e.javaClass.simpleName}: ${e.message}", null)
            }
        }
    }

    /** Runs [work] off the UI thread; replies on it. */
    private fun bg(result: MethodChannel.Result, what: String, work: () -> Any?) {
        io.execute {
            try {
                val r = work()
                activity.runOnUiThread { result.success(r) }
            } catch (e: Throwable) {
                HighLog.e(what, e)
                activity.runOnUiThread { result.error("update", "${e.javaClass.simpleName}: ${e.message}", null) }
            }
        }
    }

    @Suppress("DEPRECATION")
    private fun pkgInfo(pm: PackageManager, archive: String?, certs: Boolean = true): PackageInfo? {
        val flags = if (!certs) 0 else if (Build.VERSION.SDK_INT >= 28) PackageManager.GET_SIGNING_CERTIFICATES else PackageManager.GET_SIGNATURES
        return if (archive != null) pm.getPackageArchiveInfo(archive, flags) else pm.getPackageInfo(activity.packageName, flags)
    }

    @Suppress("DEPRECATION")
    private fun certOf(p: PackageInfo): String? {
        val sig = if (Build.VERSION.SDK_INT >= 28) {
            val si = p.signingInfo ?: return null
            (if (si.hasMultipleSigners()) si.apkContentsSigners else si.signingCertificateHistory)?.lastOrNull()
        } else p.signatures?.firstOrNull()
        return sig?.let { MessageDigest.getInstance("SHA-256").digest(it.toByteArray()).joinToString("") { b -> "%02x".format(b) } }
    }

    @Suppress("DEPRECATION")
    private fun code(p: PackageInfo): Long = if (Build.VERSION.SDK_INT >= 28) p.longVersionCode else p.versionCode.toLong()

    private fun info(): Map<String, Any?> {
        val pm = activity.packageManager
        val p = pkgInfo(pm, null)!!
        return mapOf(
            "package" to activity.packageName,
            "versionCode" to code(p),
            "versionName" to p.versionName,
            "cert" to certOf(p),
            "canInstall" to (Build.VERSION.SDK_INT < 26 || pm.canRequestPackageInstalls()),
        )
    }

    private fun inspect(path: String): Map<String, Any?>? {
        val p = pkgInfo(activity.packageManager, path) ?: return null
        return mapOf("package" to p.packageName, "versionCode" to code(p), "versionName" to p.versionName, "cert" to certOf(p))
    }

    // ---- automatic folder scan ------------------------------------------------------------------------------

    private class Doc(val uri: Uri, val name: String, val size: Long, val modified: Long)

    private fun findApks(trees: List<String>, pkg: String, above: Long, skip: Set<String>): List<Map<String, Any?>> {
        val docs = ArrayList<Doc>()
        for (t in trees) {
            try {
                val tree = Uri.parse(t)
                val root = DocumentsContract.buildDocumentUriUsingTree(tree, DocumentsContract.getTreeDocumentId(tree))
                walk(tree, DocumentsContract.getDocumentId(root), 0, docs)
            } catch (e: Throwable) {
                HighLog.w("findApks: cannot list $t: ${e.message}") // permission revoked / folder gone
            }
        }
        val out = ArrayList<Map<String, Any?>>()
        for (d in docs) {
            val key = "${d.uri}|${d.size}|${d.modified}"
            if (key in skip) continue
            val p = try { peek(d.uri) } catch (e: Throwable) { null }
            if (p == null || p.packageName != pkg || code(p) <= above) {
                out.add(mapOf("key" to key, "other" to true, "name" to d.name))
                continue
            }
            out.add(mapOf("key" to key, "uri" to d.uri.toString(), "name" to d.name, "size" to d.size, "modified" to d.modified, "versionCode" to code(p), "versionName" to p.versionName))
        }
        return out
    }

    /** Manifest of an APK behind a content uri without copying it when the provider gives a real file descriptor. */
    private fun peek(uri: Uri): PackageInfo? {
        val pm = activity.packageManager
        try {
            activity.contentResolver.openFileDescriptor(uri, "r")?.use { pfd ->
                pm.getPackageArchiveInfo("/proc/self/fd/${pfd.fd}", 0)?.let { return it }
            }
        } catch (_: Throwable) {}
        // fallback: some providers hand out pipes; copy to a scratch file once
        val tmp = File(activity.cacheDir, "updates/peek.apk")
        tmp.parentFile?.mkdirs()
        try {
            activity.contentResolver.openInputStream(uri)!!.use { ins -> tmp.outputStream().use { ins.copyTo(it, 256 * 1024) } }
            return pm.getPackageArchiveInfo(tmp.path, 0)
        } finally {
            tmp.delete()
        }
    }

    private fun walk(tree: Uri, docId: String, depth: Int, out: ArrayList<Doc>) {
        val children = DocumentsContract.buildChildDocumentsUriUsingTree(tree, docId)
        val cols = arrayOf(
            DocumentsContract.Document.COLUMN_DOCUMENT_ID,
            DocumentsContract.Document.COLUMN_DISPLAY_NAME,
            DocumentsContract.Document.COLUMN_MIME_TYPE,
            DocumentsContract.Document.COLUMN_SIZE,
            DocumentsContract.Document.COLUMN_LAST_MODIFIED,
        )
        activity.contentResolver.query(children, cols, null, null, null)?.use { c ->
            while (c.moveToNext()) {
                val id = c.getString(0) ?: continue
                val name = c.getString(1) ?: ""
                val mime = c.getString(2) ?: ""
                if (mime == DocumentsContract.Document.MIME_TYPE_DIR) {
                    if (depth < 3) walk(tree, id, depth + 1, out)
                    continue
                }
                if (!name.endsWith(".apk", true) && mime != "application/vnd.android.package-archive") continue
                val size = if (c.isNull(3)) 0L else c.getLong(3)
                val modified = if (c.isNull(4)) 0L else c.getLong(4)
                out.add(Doc(DocumentsContract.buildDocumentUriUsingTree(tree, id), name, size, modified))
            }
        }
    }

    // ---- install / share ------------------------------------------------------------------------------------

    private fun install(path: String): String {
        val pm = activity.packageManager
        if (Build.VERSION.SDK_INT >= 26 && !pm.canRequestPackageInstalls()) {
            activity.startActivity(Intent(Settings.ACTION_MANAGE_UNKNOWN_APP_SOURCES, Uri.parse("package:${activity.packageName}")))
            return "permission"
        }
        val f = File(path)
        val uri = FileProvider.getUriForFile(activity, "${activity.packageName}.fileprovider", f)
        val i = Intent(Intent.ACTION_VIEW).apply {
            setDataAndType(uri, "application/vnd.android.package-archive")
            addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION or Intent.FLAG_ACTIVITY_NEW_TASK)
        }
        activity.startActivity(i)
        return "started"
    }

    /** "Send 4 to a friend": the installed APK itself (CI builds are universal, so normally one file). */
    private fun shareSelf(): Map<String, Any?> {
        val ai = activity.applicationInfo
        val p = pkgInfo(activity.packageManager, null, certs = false)!!
        val dir = File(activity.cacheDir, "share")
        dir.mkdirs()
        val tag = "${p.versionName ?: "x"}-${code(p)}".replace(Regex("[^A-Za-z0-9._-]"), "_")
        val sources = listOf(File(ai.sourceDir)) + (ai.splitSourceDirs ?: emptyArray()).map { File(it) }
        val keep = HashSet<String>()
        val files = sources.mapIndexed { n, src ->
            val name = if (n == 0) "4-$tag.apk" else "4-$tag-${src.nameWithoutExtension}.apk"
            val dst = File(dir, name)
            keep.add(name)
            if (!dst.exists() || dst.length() != src.length()) {
                val part = File(dir, "$name.part")
                src.inputStream().use { ins -> part.outputStream().use { ins.copyTo(it, 256 * 1024) } }
                if (!part.renameTo(dst)) throw IllegalStateException("rename failed")
            }
            dst
        }
        dir.listFiles()?.forEach { if (it.name !in keep) it.delete() } // older versions' copies
        val auth = "${activity.packageName}.fileprovider"
        val uris = files.map { FileProvider.getUriForFile(activity, auth, it) }
        val type = "application/vnd.android.package-archive"
        val send = if (uris.size == 1) {
            Intent(Intent.ACTION_SEND).apply { putExtra(Intent.EXTRA_STREAM, uris[0]) }
        } else {
            Intent(Intent.ACTION_SEND_MULTIPLE).apply { putParcelableArrayListExtra(Intent.EXTRA_STREAM, ArrayList(uris)) }
        }
        send.type = type
        send.putExtra(Intent.EXTRA_TITLE, files[0].name)
        send.clipData = ClipData.newUri(activity.contentResolver, files[0].name, uris[0]).also { c -> uris.drop(1).forEach { c.addItem(ClipData.Item(it)) } }
        send.addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION)
        activity.runOnUiThread {
            activity.startActivity(Intent.createChooser(send, "Send 4 ${p.versionName ?: ""}").addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION))
        }
        return mapOf("files" to files.size, "splits" to (files.size - 1), "bytes" to files.sumOf { it.length() }, "name" to files[0].name)
    }
}
