package com.warsay.high

import android.Manifest
import android.content.Intent
import android.content.pm.PackageManager
import android.net.Uri
import android.provider.Settings
import android.util.Log
import android.view.WindowManager
import androidx.activity.result.contract.ActivityResultContracts
import androidx.core.app.ActivityCompat
import androidx.core.content.ContextCompat
import io.flutter.embedding.android.FlutterFragmentActivity
import io.flutter.embedding.engine.FlutterEngine
import io.flutter.plugin.common.MethodChannel

/**
 * Secure channel for High lock-screen unlock.
 * Uses FlutterFragmentActivity + Activity Result API so CAMERA permission
 * callbacks always complete (classic onRequestPermissionsResult is unreliable
 * with modern Flutter embeddings on first install).
 */
class MainActivity : FlutterFragmentActivity() {
    companion object {
        private const val TAG = "HighSecure"
        private const val CHANNEL = "com.warsay.high/secure"
    }


    /** MethodChannel.Result may be answered only once; guard against double permission callbacks. */
    private class OnceResult(private val inner: MethodChannel.Result) : MethodChannel.Result {
        @Volatile private var done = false
        override fun success(result: Any?) {
            if (done) return
            done = true
            inner.success(result)
        }
        override fun error(errorCode: String, errorMessage: String?, errorDetails: Any?) {
            if (done) return
            done = true
            inner.error(errorCode, errorMessage, errorDetails)
        }
        override fun notImplemented() {
            if (done) return
            done = true
            inner.notImplemented()
        }
    }

    private val cameraWaiters = mutableListOf<MethodChannel.Result>()
    private var scanAfterPermission: MethodChannel.Result? = null
    private var secureWanted = false

    private val cameraPermissionLauncher =
        registerForActivityResult(ActivityResultContracts.RequestPermission()) { granted ->
            Log.i(TAG, "camera permission result granted=$granted")
            val waiters = cameraWaiters.toList()
            cameraWaiters.clear()
            waiters.forEach { it.success(granted) }

            // Never start GmsBarcodeScanning after permission — unlock is MobileScanner-only.
            val pending = scanAfterPermission
            if (pending != null) {
                scanAfterPermission = null
                pending.error("use_embedded", "Use Flutter MobileScanner; native scanQr disabled", null)
            }
        }

    override fun onCreate(savedInstanceState: android.os.Bundle?) {
        super.onCreate(savedInstanceState)
        window.clearFlags(WindowManager.LayoutParams.FLAG_SECURE)
    }

    override fun onResume() {
        super.onResume()
        if (!secureWanted) window.clearFlags(WindowManager.LayoutParams.FLAG_SECURE)
    }

    override fun configureFlutterEngine(flutterEngine: FlutterEngine) {
        super.configureFlutterEngine(flutterEngine)
        MethodChannel(flutterEngine.dartExecutor.binaryMessenger, CHANNEL)
            .setMethodCallHandler { call, result ->
                when (call.method) {
                    "set" -> {
                        val on = call.arguments == true
                        runOnUiThread {
                            setSecure(on)
                            window.decorView.post { result.success(null) }
                        }
                    }
                    "requestCamera" -> requestCamera(result)
                    "hasCamera" -> result.success(hasCameraPermission())
                    "shouldShowCameraRationale" -> {
                        result.success(
                            ActivityCompat.shouldShowRequestPermissionRationale(
                                this,
                                Manifest.permission.CAMERA,
                            ),
                        )
                    }
                    "openAppSettings" -> {
                        runOnUiThread {
                            try {
                                val intent = Intent(Settings.ACTION_APPLICATION_DETAILS_SETTINGS)
                                intent.data = Uri.fromParts("package", packageName, null)
                                startActivity(intent)
                                result.success(true)
                            } catch (e: Exception) {
                                Log.e(TAG, "openAppSettings failed", e)
                                result.error("settings", e.message, null)
                            }
                        }
                    }
                    "scanQr" -> scanQr(result)
                    "log" -> {
                        Log.i(TAG, call.arguments?.toString() ?: "")
                        result.success(null)
                    }
                    else -> result.notImplemented()
                }
            }
        Log.i(TAG, "MethodChannel $CHANNEL ready")
    }

    private fun hasCameraPermission(): Boolean =
        ContextCompat.checkSelfPermission(this, Manifest.permission.CAMERA) ==
            PackageManager.PERMISSION_GRANTED

    private fun requestCamera(result: MethodChannel.Result) {
        runOnUiThread {
            if (hasCameraPermission()) {
                Log.i(TAG, "requestCamera: already granted")
                result.success(true)
                return@runOnUiThread
            }
            Log.i(TAG, "requestCamera: launching system dialog")
            val once = OnceResult(result)
            cameraWaiters.add(once)
            try {
                cameraPermissionLauncher.launch(Manifest.permission.CAMERA)
            } catch (e: Exception) {
                Log.e(TAG, "requestCamera launch failed", e)
                cameraWaiters.remove(once)
                // Fallback to legacy API
                try {
                    cameraWaiters.add(once)
                    ActivityCompat.requestPermissions(this, arrayOf(Manifest.permission.CAMERA), 71)
                } catch (e2: Exception) {
                    Log.e(TAG, "legacy requestPermissions failed", e2)
                    cameraWaiters.remove(once)
                    once.error("request_failed", e2.message, null)
                }
            }
        }
    }

    /**
     * Unlock QR uses Flutter MobileScanner only. Native GmsBarcodeScanning steals the
     * camera and caused genericError on first install when Dart fell back to embedded.
     * Keep the MethodChannel method for API compat; do not open the camera here.
     */
    private fun scanQr(result: MethodChannel.Result) {
        Log.i(TAG, "scanQr: disabled (embedded MobileScanner only)")
        result.error("use_embedded", "Use Flutter MobileScanner; native scanQr disabled", null)
    }


    @Deprecated("Legacy fallback if Activity Result launcher is unavailable")
    override fun onRequestPermissionsResult(
        requestCode: Int,
        permissions: Array<out String>,
        grantResults: IntArray,
    ) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults)
        if (requestCode != 71 && requestCode != 72) return
        val ok = grantResults.isNotEmpty() && grantResults[0] == PackageManager.PERMISSION_GRANTED
        Log.i(TAG, "legacy onRequestPermissionsResult code=$requestCode granted=$ok")
        if (cameraWaiters.isNotEmpty()) {
            val waiters = cameraWaiters.toList()
            cameraWaiters.clear()
            waiters.forEach { it.success(ok) }
        }
        val pending = scanAfterPermission
        if (pending != null && requestCode == 72) {
            scanAfterPermission = null
            pending.error("use_embedded", "Use Flutter MobileScanner; native scanQr disabled", null)
        }
    }

    private fun setSecure(on: Boolean) {
        // Screenshot blocking disabled for study content; keep channel for API compat.
        secureWanted = false
        window.clearFlags(WindowManager.LayoutParams.FLAG_SECURE)
    }
}
