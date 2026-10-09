package com.warsay.high

import android.annotation.SuppressLint
import android.app.Activity
import android.graphics.Color
import android.os.Bundle
import android.view.Gravity
import android.view.View
import android.view.ViewGroup
import android.view.WindowManager
import android.webkit.WebChromeClient
import android.webkit.PermissionRequest
import android.webkit.WebResourceRequest
import android.webkit.WebResourceResponse
import android.webkit.WebSettings
import android.webkit.WebView
import android.webkit.WebViewClient
import android.widget.LinearLayout
import android.widget.TextView
import java.io.ByteArrayInputStream
import java.io.File
import java.io.InputStream
import java.util.zip.ZipInputStream

/**
 * Offline interactive page from a `.4web` resource (encrypted zip of HTML/JS/CSS/assets).
 * The zip is decrypted with [FourChunkReader] straight into memory and unpacked into a map; nothing decrypted is
 * written to disk. Pages are served from that map through [WebViewClient.shouldInterceptRequest] on a fake origin
 * (https://4web.invalid/), every other request gets 403, so the page has no network. CSP is sent as well.
 */
class FourWebBundle(val files: Map<String, ByteArray>, val entry: String) {
    data class Res(val status: Int, val mime: String, val body: ByteArray)

    companion object {
        const val HOST = "4web.invalid"
        const val ORIGIN = "https://$HOST/"
        const val MAX_BYTES = 200L shl 20
        const val CSP = "default-src 'self' 'unsafe-inline' 'unsafe-eval' data: blob:; connect-src 'self' data: blob:; " +
            "form-action 'none'; base-uri 'self'; frame-src 'self' data: blob:; worker-src 'self' blob:"

        /** Decrypts and unpacks the zip. [key] is zeroed by the caller after this returns. */
        fun open(file: File, key: ByteArray, entry: String): FourWebBundle = FourChunkReader(file, key).use { r ->
            require(r.length <= MAX_BYTES) { "bundle too large" }
            unzip(ChunkStream(r), entry)
        }

        fun unzip(input: InputStream, entry: String): FourWebBundle {
            val map = HashMap<String, ByteArray>()
            var total = 0L
            ZipInputStream(input.buffered(1 shl 16)).use { z ->
                while (true) {
                    val e = z.nextEntry ?: break
                    if (e.isDirectory) continue
                    val name = e.name.replace('\\', '/').trimStart('/')
                    if (name.contains("../") || name.startsWith("__MACOSX/")) continue
                    val b = z.readBytes()
                    total += b.size
                    require(total <= MAX_BYTES) { "bundle too large when unpacked" }
                    map[name] = b
                }
            }
            val start = entry.ifEmpty { "index.html" }
            require(map.containsKey(start)) { "start page $start missing" }
            return FourWebBundle(map, start)
        }

        fun mimeOf(path: String): String = when (path.substringAfterLast('.', "").lowercase()) {
            "html", "htm" -> "text/html"
            "js", "mjs" -> "text/javascript"
            "css" -> "text/css"
            "json", "map" -> "application/json"
            "svg" -> "image/svg+xml"
            "png" -> "image/png"
            "jpg", "jpeg" -> "image/jpeg"
            "gif" -> "image/gif"
            "webp" -> "image/webp"
            "ico" -> "image/x-icon"
            "woff" -> "font/woff"
            "woff2" -> "font/woff2"
            "ttf" -> "font/ttf"
            "otf" -> "font/otf"
            "mp3" -> "audio/mpeg"
            "ogg" -> "audio/ogg"
            "wav" -> "audio/wav"
            "m4a" -> "audio/mp4"
            "mp4" -> "video/mp4"
            "webm" -> "video/webm"
            "vtt" -> "text/vtt"
            "xml" -> "application/xml"
            "txt", "csv" -> "text/plain"
            "wasm" -> "application/wasm"
            else -> "application/octet-stream"
        }
    }

    val entryUrl: String get() = ORIGIN + entry.split('/').joinToString("/") { android.net.Uri.encode(it) }

    /** Routing used by the WebView (pure, unit-tested). */
    fun resolve(url: String): Res {
        if (!url.startsWith(ORIGIN)) return Res(403, "text/plain", ByteArray(0))
        var path = java.net.URLDecoder.decode(url.removePrefix(ORIGIN).substringBefore('#').substringBefore('?').replace("+", "%2B"), "UTF-8")
        if (path.isEmpty() || path.endsWith("/")) path += "index.html"
        val b = files[path] ?: return Res(404, "text/plain", ByteArray(0))
        return Res(200, mimeOf(path), b)
    }
}

/** Sequential plaintext stream over a [FourChunkReader] (one 256 KiB chunk in memory at a time). */
private class ChunkStream(private val r: FourChunkReader) : InputStream() {
    private var ci = 0
    private var buf = ByteArray(0)
    private var pos = 0
    private fun fill(): Boolean {
        while (pos >= buf.size) {
            if (ci >= r.pre.chunkCount) return false
            buf = r.chunk(ci++); pos = 0
        }
        return true
    }
    override fun read(): Int = if (!fill()) -1 else buf[pos++].toInt() and 0xff
    override fun read(b: ByteArray, off: Int, len: Int): Int {
        if (len == 0) return 0
        if (!fill()) return -1
        val n = minOf(len, buf.size - pos)
        System.arraycopy(buf, pos, b, off, n); pos += n
        return n
    }
}

/** Hand-off from the Flutter channel to the activity without putting the key in an Intent. */
object FourWebHolder {
    @Volatile var bundle: FourWebBundle? = null
    @Volatile var title: String = ""
    @Volatile var credit: String = ""
}

class FourWebActivity : Activity() {
    private var web: WebView? = null

    @SuppressLint("SetJavaScriptEnabled")
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        window.addFlags(WindowManager.LayoutParams.FLAG_SECURE)
        val bundle = FourWebHolder.bundle
        if (bundle == null) { finish(); return } // process was recreated: decrypted data is gone, reopen from 4
        title = FourWebHolder.title
        val w = WebView(this)
        web = w
        with(w.settings) {
            javaScriptEnabled = true // interactives need JS; the page has no network and no bridge to the app
            domStorageEnabled = true
            allowFileAccess = false
            allowContentAccess = false
            @Suppress("DEPRECATION") allowFileAccessFromFileURLs = false
            @Suppress("DEPRECATION") allowUniversalAccessFromFileURLs = false
            cacheMode = WebSettings.LOAD_NO_CACHE
            mixedContentMode = WebSettings.MIXED_CONTENT_NEVER_ALLOW
            setSupportMultipleWindows(false)
            javaScriptCanOpenWindowsAutomatically = false
            setGeolocationEnabled(false)
            mediaPlaybackRequiresUserGesture = false
            useWideViewPort = true
            loadWithOverviewMode = true
            builtInZoomControls = true
            displayZoomControls = false
        }
        w.webViewClient = object : WebViewClient() {
            override fun shouldInterceptRequest(view: WebView, request: WebResourceRequest): WebResourceResponse {
                val r = bundle.resolve(request.url.toString())
                val headers = mapOf("Content-Security-Policy" to FourWebBundle.CSP, "Cache-Control" to "no-store", "Access-Control-Allow-Origin" to FourWebBundle.ORIGIN.trimEnd('/'))
                val reason = when (r.status) { 200 -> "OK"; 404 -> "Not Found"; else -> "Forbidden" }
                return WebResourceResponse(r.mime, if (r.mime.startsWith("text/") || r.mime.endsWith("json") || r.mime.endsWith("javascript")) "utf-8" else null, r.status, reason, headers, ByteArrayInputStream(r.body))
            }

            override fun shouldOverrideUrlLoading(view: WebView, request: WebResourceRequest): Boolean =
                !request.url.toString().startsWith(FourWebBundle.ORIGIN) // external links: blocked
        }
        w.webChromeClient = object : WebChromeClient() {
            override fun onPermissionRequest(request: PermissionRequest) = request.deny()
        }
        val root = LinearLayout(this).apply { orientation = LinearLayout.VERTICAL; setBackgroundColor(Color.WHITE) }
        root.addView(w, LinearLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, 0, 1f))
        val credit = FourWebHolder.credit
        if (credit.isNotEmpty()) root.addView(TextView(this).apply {
            text = credit
            textSize = 11f
            setTextColor(Color.DKGRAY)
            gravity = Gravity.CENTER
            setPadding(16, 6, 16, 8)
        })
        setContentView(root)
        w.loadUrl(bundle.entryUrl)
    }

    @Deprecated("Deprecated in Java")
    override fun onBackPressed() {
        val w = web
        if (w != null && w.canGoBack()) w.goBack() else @Suppress("DEPRECATION") super.onBackPressed()
    }

    override fun onDestroy() {
        web?.apply { stopLoading(); clearCache(true); clearHistory(); (parent as? ViewGroup)?.removeView(this); destroy() }
        web = null
        if (isFinishing) { FourWebHolder.bundle = null; FourWebHolder.credit = "" }
        super.onDestroy()
    }
}
