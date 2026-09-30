package com.warsay.high

import android.Manifest
import android.content.pm.PackageManager
import android.os.Bundle
import android.view.WindowManager
import androidx.core.app.ActivityCompat
import androidx.core.content.ContextCompat
import io.flutter.embedding.android.FlutterActivity
import io.flutter.embedding.engine.FlutterEngine
import io.flutter.plugin.common.MethodChannel

class MainActivity : FlutterActivity() {
    private val cameraWaiters = mutableListOf<MethodChannel.Result>()

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setSecure(true)
    }

    override fun configureFlutterEngine(flutterEngine: FlutterEngine) {
        super.configureFlutterEngine(flutterEngine)
        MethodChannel(flutterEngine.dartExecutor.binaryMessenger, "com.warsay.high/secure")
            .setMethodCallHandler { call, result ->
                when (call.method) {
                    "set" -> {
                        runOnUiThread { setSecure(call.arguments == true) }
                        result.success(null)
                    }
                    "requestCamera" -> requestCamera(result)
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
        cameraWaiters.add(result)
        ActivityCompat.requestPermissions(this, arrayOf(Manifest.permission.CAMERA), 71)
    }

    override fun onRequestPermissionsResult(
        requestCode: Int,
        permissions: Array<out String>,
        grantResults: IntArray,
    ) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults)
        if (requestCode != 71) return
        val ok = grantResults.isNotEmpty() && grantResults[0] == PackageManager.PERMISSION_GRANTED
        cameraWaiters.forEach { it.success(ok) }
        cameraWaiters.clear()
    }

    private fun setSecure(on: Boolean) {
        if (on) {
            window.setFlags(
                WindowManager.LayoutParams.FLAG_SECURE,
                WindowManager.LayoutParams.FLAG_SECURE,
            )
        } else {
            window.clearFlags(WindowManager.LayoutParams.FLAG_SECURE)
        }
    }
}
