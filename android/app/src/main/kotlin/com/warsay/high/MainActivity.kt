package com.warsay.high

import android.Manifest
import android.content.Intent
import android.content.pm.PackageManager
import android.net.Uri
import android.provider.Settings
import android.view.WindowManager
import androidx.core.app.ActivityCompat
import androidx.core.content.ContextCompat
import com.google.mlkit.vision.barcode.common.Barcode
import com.google.mlkit.vision.codescanner.GmsBarcodeScannerOptions
import com.google.mlkit.vision.codescanner.GmsBarcodeScanning
import io.flutter.embedding.android.FlutterActivity
import io.flutter.embedding.engine.FlutterEngine
import io.flutter.plugin.common.MethodChannel

class MainActivity : FlutterActivity() {
    private val cameraWaiters = mutableListOf<MethodChannel.Result>()
    private var scanAfterPermission: MethodChannel.Result? = null
    private var secureWanted = false

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
        MethodChannel(flutterEngine.dartExecutor.binaryMessenger, "com.warsay.high/secure")
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
                    "hasCamera" -> {
                        val ok = ContextCompat.checkSelfPermission(this, Manifest.permission.CAMERA) ==
                            PackageManager.PERMISSION_GRANTED
                        result.success(ok)
                    }
                    "openAppSettings" -> {
                        runOnUiThread {
                            val intent = Intent(Settings.ACTION_APPLICATION_DETAILS_SETTINGS)
                            intent.data = Uri.fromParts("package", packageName, null)
                            startActivity(intent)
                            result.success(null)
                        }
                    }
                    "scanQr" -> scanQr(result)
                    else -> result.notImplemented()
                }
            }
    }

    private fun requestCamera(result: MethodChannel.Result) {
        if (ContextCompat.checkSelfPermission(this, Manifest.permission.CAMERA) ==
            PackageManager.PERMISSION_GRANTED
        ) {
            result.success(true)
            return
        }
        runOnUiThread {
            cameraWaiters.add(result)
            ActivityCompat.requestPermissions(this, arrayOf(Manifest.permission.CAMERA), 71)
        }
    }

    private fun scanQr(result: MethodChannel.Result) {
        runOnUiThread {
            setSecure(false)
            window.clearFlags(WindowManager.LayoutParams.FLAG_SECURE)
            if (ContextCompat.checkSelfPermission(this, Manifest.permission.CAMERA) !=
                PackageManager.PERMISSION_GRANTED
            ) {
                scanAfterPermission = result
                ActivityCompat.requestPermissions(this, arrayOf(Manifest.permission.CAMERA), 72)
                return@runOnUiThread
            }
            startScanner(result)
        }
    }

    private fun startScanner(result: MethodChannel.Result) {
        val options = GmsBarcodeScannerOptions.Builder()
            .setBarcodeFormats(Barcode.FORMAT_QR_CODE)
            .enableAutoZoom()
            .build()
        GmsBarcodeScanning.getClient(this, options)
            .startScan()
            .addOnSuccessListener { barcode ->
                result.success(barcode.rawValue ?: "")
            }
            .addOnCanceledListener {
                result.success("")
            }
            .addOnFailureListener { error ->
                result.error("scan", error.message ?: "Camera did not open", null)
            }
    }

    override fun onRequestPermissionsResult(
        requestCode: Int,
        permissions: Array<out String>,
        grantResults: IntArray,
    ) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults)
        val ok = grantResults.isNotEmpty() && grantResults[0] == PackageManager.PERMISSION_GRANTED
        if (requestCode == 71) {
            val waiters = cameraWaiters.toList()
            cameraWaiters.clear()
            waiters.forEach { it.success(ok) }
        }
        if (requestCode == 72) {
            val pending = scanAfterPermission
            scanAfterPermission = null
            if (pending == null) return
            if (ok) startScanner(pending) else pending.success("")
        }
    }

    private fun setSecure(on: Boolean) {
        secureWanted = false
        window.clearFlags(WindowManager.LayoutParams.FLAG_SECURE)
    }
}
