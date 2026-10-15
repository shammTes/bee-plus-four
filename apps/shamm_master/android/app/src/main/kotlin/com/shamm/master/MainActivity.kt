package com.shamm.master

import android.app.Activity
import android.content.Intent
import androidx.activity.result.contract.ActivityResultContracts
import androidx.core.content.FileProvider
import io.flutter.embedding.android.FlutterFragmentActivity
import io.flutter.embedding.engine.FlutterEngine
import io.flutter.plugin.common.MethodChannel
import java.io.File

/** Native bits for Shamm Master: live QR scanner (ScanActivity) and Android share sheet. Channel com.shamm.master/native. */
class MainActivity : FlutterFragmentActivity() {
    private var scanPending: MethodChannel.Result? = null

    private val scanLauncher = registerForActivityResult(ActivityResultContracts.StartActivityForResult()) { res ->
        val data = res.data
        val payload = data?.getStringExtra(ScanActivity.EXTRA_PAYLOAD)
        val error = data?.getStringExtra(ScanActivity.EXTRA_ERROR)
        val out = HashMap<String, Any?>()
        when {
            res.resultCode == Activity.RESULT_OK && !payload.isNullOrBlank() -> { out["status"] = "ok"; out["payload"] = payload }
            error != null -> { out["status"] = "error"; out["code"] = error; out["message"] = data.getStringExtra(ScanActivity.EXTRA_MESSAGE) }
            else -> out["status"] = "cancelled"
        }
        val p = scanPending
        scanPending = null
        p?.success(out)
    }

    override fun configureFlutterEngine(flutterEngine: FlutterEngine) {
        super.configureFlutterEngine(flutterEngine)
        MethodChannel(flutterEngine.dartExecutor.binaryMessenger, "com.shamm.master/native").setMethodCallHandler { call, result ->
            try {
                when (call.method) {
                    "scan" -> {
                        scanPending?.success(mapOf("status" to "cancelled"))
                        scanPending = result
                        scanLauncher.launch(Intent(this, ScanActivity::class.java)
                            .putExtra(ScanActivity.EXTRA_TITLE, call.argument<String>("title"))
                            .putExtra(ScanActivity.EXTRA_HINT, call.argument<String>("hint")))
                    }
                    "shareText" -> {
                        val send = Intent(Intent.ACTION_SEND).setType("text/plain").putExtra(Intent.EXTRA_TEXT, call.argument<String>("text"))
                        startActivity(Intent.createChooser(send, call.argument<String>("title") ?: "Share"))
                        result.success(true)
                    }
                    "shareFile" -> {
                        val dir = File(cacheDir, "share").apply { mkdirs() }
                        val f = File(dir, call.argument<String>("name") ?: "file.txt")
                        f.writeText(call.argument<String>("content") ?: "")
                        val uri = FileProvider.getUriForFile(this, "$packageName.files", f)
                        val send = Intent(Intent.ACTION_SEND).setType(call.argument<String>("mime") ?: "text/plain")
                            .putExtra(Intent.EXTRA_STREAM, uri).addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION)
                        startActivity(Intent.createChooser(send, call.argument<String>("title") ?: "Share"))
                        result.success(f.absolutePath)
                    }
                    else -> result.notImplemented()
                }
            } catch (e: Throwable) {
                result.error("native", e.message ?: e.javaClass.simpleName, null)
            }
        }
    }
}
