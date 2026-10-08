package com.warsay.high

import android.content.Intent
import android.content.pm.PackageInfo
import android.content.pm.PackageManager
import android.net.ConnectivityManager
import android.net.NetworkCapabilities
import android.net.Uri
import android.os.Build
import android.provider.Settings
import androidx.core.content.FileProvider
import io.flutter.embedding.android.FlutterFragmentActivity
import io.flutter.plugin.common.BinaryMessenger
import io.flutter.plugin.common.MethodChannel
import java.io.File
import java.security.MessageDigest
import java.util.concurrent.Executors

/**
 * App updates (`com.warsay.high/update`). Download + SHA-256 happen in Dart; this side answers what only Android knows:
 *  - info                → {versionCode, versionName, cert, canInstall, network: wifi|cellular|none, metered}
 *  - inspectApk{path}    → {package, versionCode, versionName, cert} of an APK file (null if unreadable)
 *  - install{path}       → opens the system installer (one tap "Update"); asks for "install unknown apps" first if needed
 * cert = SHA-256 of the first signing certificate, lowercase hex. Android refuses an update signed with another key
 * anyway; checking first gives a clear message instead of "App not installed".
 */
class UpdateChannel(private val activity: FlutterFragmentActivity) {
    private val io = Executors.newSingleThreadExecutor()

    fun attach(messenger: BinaryMessenger) {
        MethodChannel(messenger, "com.warsay.high/update").setMethodCallHandler { call, result ->
            try {
                when (call.method) {
                    "info" -> result.success(info())
                    "inspectApk" -> {
                        val path = call.argument<String>("path")!!
                        io.execute {
                            val r = try { inspect(path) } catch (e: Throwable) { HighLog.e("inspectApk", e); null }
                            activity.runOnUiThread { result.success(r) }
                        }
                    }
                    "install" -> result.success(install(call.argument<String>("path")!!))
                    else -> result.notImplemented()
                }
            } catch (e: Throwable) {
                HighLog.e("update ${call.method} failed", e)
                result.error("update", "${e.javaClass.simpleName}: ${e.message}", null)
            }
        }
    }

    @Suppress("DEPRECATION")
    private fun pkgInfo(pm: PackageManager, archive: String?): PackageInfo? {
        val flags = if (Build.VERSION.SDK_INT >= 28) PackageManager.GET_SIGNING_CERTIFICATES else PackageManager.GET_SIGNATURES
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
        val cm = activity.getSystemService(ConnectivityManager::class.java)
        val caps = cm?.getNetworkCapabilities(cm.activeNetwork)
        val net = when {
            caps == null || !caps.hasCapability(NetworkCapabilities.NET_CAPABILITY_INTERNET) -> "none"
            caps.hasTransport(NetworkCapabilities.TRANSPORT_WIFI) || caps.hasTransport(NetworkCapabilities.TRANSPORT_ETHERNET) -> "wifi"
            else -> "cellular"
        }
        return mapOf(
            "package" to activity.packageName,
            "versionCode" to code(p),
            "versionName" to p.versionName,
            "cert" to certOf(p),
            "canInstall" to (Build.VERSION.SDK_INT < 26 || pm.canRequestPackageInstalls()),
            "network" to net,
            "metered" to (cm?.isActiveNetworkMetered ?: true),
            "abis" to Build.SUPPORTED_ABIS.toList(),
        )
    }

    private fun inspect(path: String): Map<String, Any?>? {
        val p = pkgInfo(activity.packageManager, path) ?: return null
        return mapOf("package" to p.packageName, "versionCode" to code(p), "versionName" to p.versionName, "cert" to certOf(p))
    }

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
}
