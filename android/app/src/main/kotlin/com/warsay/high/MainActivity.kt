package com.warsay.high

import android.Manifest
import android.content.Intent
import android.content.pm.PackageManager
import android.graphics.Bitmap
import android.graphics.BitmapFactory
import android.graphics.Matrix
import android.net.Uri
import android.provider.MediaStore
import android.provider.Settings
import android.util.Log
import android.view.WindowManager
import androidx.activity.result.contract.ActivityResultContracts
import androidx.core.app.ActivityCompat
import androidx.core.content.ContextCompat
import androidx.core.content.FileProvider
import androidx.exifinterface.media.ExifInterface
import com.google.mlkit.vision.barcode.BarcodeScannerOptions
import com.google.mlkit.vision.barcode.BarcodeScanning
import com.google.mlkit.vision.barcode.common.Barcode
import com.google.mlkit.vision.common.InputImage
import io.flutter.embedding.android.FlutterFragmentActivity
import io.flutter.embedding.engine.FlutterEngine
import io.flutter.plugin.common.MethodChannel
import java.io.File

/**
 * Unlock QR via the **system camera app** (ACTION_IMAGE_CAPTURE / TakePicture),
 * then on-device ML Kit barcode decode of the still photo.
 *
 * Avoids CameraX / mobile_scanner / Play Services barcode_ui — those failed to open
 * the camera on first-install / low-end devices (genericError).
 *
 * Logcat tag: HighSecure
 */
class MainActivity : FlutterFragmentActivity() {
    companion object {
        private const val TAG = "HighSecure"
        private const val CHANNEL = "com.warsay.high/secure"
        private const val MAX_DECODE_EDGE = 1600
    }

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
    /** After CAMERA grant, launch system camera for unlock scan. */
    private var captureAfterPermission: MethodChannel.Result? = null
    private var capturePending: MethodChannel.Result? = null
    private var photoUri: Uri? = null
    private var photoFile: File? = null
    private var secureWanted = false

    private val cameraPermissionLauncher =
        registerForActivityResult(ActivityResultContracts.RequestPermission()) { granted ->
            Log.i(TAG, "camera permission result granted=$granted")
            val waiters = cameraWaiters.toList()
            cameraWaiters.clear()
            waiters.forEach { it.success(granted) }

            val pendingCapture = captureAfterPermission
            if (pendingCapture != null) {
                captureAfterPermission = null
                if (granted) {
                    launchSystemCamera(pendingCapture)
                } else {
                    pendingCapture.error(
                        "permission_denied",
                        "Camera permission denied",
                        null,
                    )
                }
            }
        }

    /** Opens the device camera app; on success we decode QR from the JPEG. */
    private val takePictureLauncher =
        registerForActivityResult(ActivityResultContracts.TakePicture()) { success ->
            val pending = capturePending
            capturePending = null
            val uri = photoUri
            val file = photoFile
            photoUri = null
            Log.i(TAG, "TakePicture success=$success uri=$uri fileExists=${file?.exists()}")
            if (pending == null) return@registerForActivityResult
            if (!success || uri == null) {
                cleanupPhoto(file)
                // Empty string = user cancelled — Dart shows a clear message.
                pending.success("")
                return@registerForActivityResult
            }
            decodeQrFromPhoto(uri, file, pending)
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
                    // Primary unlock path: system camera → still photo → ML Kit QR.
                    "captureAndScanQr" -> captureAndScanQr(result)
                    // Alias kept for older Dart / docs.
                    "scanQr" -> captureAndScanQr(result)
                    "log" -> {
                        Log.i(TAG, call.arguments?.toString() ?: "")
                        result.success(null)
                    }
                    else -> result.notImplemented()
                }
            }
        Log.i(TAG, "MethodChannel $CHANNEL ready (system-camera unlock)")
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
     * Request CAMERA if needed, then open the **system camera app**.
     * Returns QR payload string, "" if cancelled, or MethodChannel error.
     */
    private fun captureAndScanQr(result: MethodChannel.Result) {
        runOnUiThread {
            setSecure(false)
            window.clearFlags(WindowManager.LayoutParams.FLAG_SECURE)
            if (capturePending != null || captureAfterPermission != null) {
                Log.w(TAG, "captureAndScanQr: busy")
                result.error("busy", "Camera is already opening. Wait a moment and try again.", null)
                return@runOnUiThread
            }
            val once = OnceResult(result)
            if (!hasCameraPermission()) {
                Log.i(TAG, "captureAndScanQr: need CAMERA first")
                captureAfterPermission = once
                try {
                    cameraPermissionLauncher.launch(Manifest.permission.CAMERA)
                } catch (e: Exception) {
                    Log.e(TAG, "capture permission launch failed", e)
                    captureAfterPermission = null
                    once.error("permission_denied", e.message ?: "Camera permission required", null)
                }
                return@runOnUiThread
            }
            launchSystemCamera(once)
        }
    }

    private fun launchSystemCamera(result: MethodChannel.Result) {
        try {
            // Prefer app cache — no storage permission needed.
            val file = File(cacheDir, "unlock_qr_${System.currentTimeMillis()}.jpg")
            if (file.exists()) file.delete()
            file.createNewFile()
            photoFile = file
            // Must match AndroidManifest FileProvider authorities="${applicationId}.fileprovider"
            val uri = FileProvider.getUriForFile(
                this,
                "${applicationContext.packageName}.fileprovider",
                file,
            )
            photoUri = uri
            capturePending = result

            // Probe that a camera app exists (Android 11+ package visibility).
            val probe = Intent(MediaStore.ACTION_IMAGE_CAPTURE)
            if (probe.resolveActivity(packageManager) == null) {
                Log.e(TAG, "no camera app for ACTION_IMAGE_CAPTURE")
                capturePending = null
                photoUri = null
                cleanupPhoto(file)
                result.error(
                    "no_camera_app",
                    "No camera app found on this phone. Enter the unlock code instead.",
                    null,
                )
                return
            }

            Log.i(TAG, "launching system camera TakePicture uri=$uri")
            takePictureLauncher.launch(uri)
        } catch (e: Exception) {
            Log.e(TAG, "launchSystemCamera failed", e)
            capturePending = null
            photoUri = null
            cleanupPhoto(photoFile)
            photoFile = null
            result.error("camera", e.message ?: "Could not open the camera app", null)
        }
    }

    private fun decodeQrFromPhoto(uri: Uri, file: File?, result: MethodChannel.Result) {
        try {
            Log.i(TAG, "decodeQrFromPhoto begin")
            val bitmap = loadBitmapForDecode(uri, file)
                ?: run {
                    cleanupPhoto(file)
                    result.error("decode", "Could not read the photo from the camera.", null)
                    return
                }
            val image = InputImage.fromBitmap(bitmap, 0)
            val options = BarcodeScannerOptions.Builder()
                .setBarcodeFormats(Barcode.FORMAT_QR_CODE)
                .build()
            val scanner = BarcodeScanning.getClient(options)
            scanner.process(image)
                .addOnSuccessListener { barcodes ->
                    val value = barcodes.firstOrNull { !it.rawValue.isNullOrBlank() }?.rawValue ?: ""
                    Log.i(TAG, "decode success count=${barcodes.size} len=${value.length}")
                    cleanupPhoto(file)
                    if (value.isEmpty()) {
                        result.error(
                            "no_qr",
                            "No QR code found in the photo. Hold steady, fill the frame, and try again — or enter the unlock code.",
                            null,
                        )
                    } else {
                        result.success(value)
                    }
                }
                .addOnFailureListener { error ->
                    Log.e(TAG, "ML Kit decode failed: ${error.message}", error)
                    cleanupPhoto(file)
                    result.error(
                        "decode",
                        error.message ?: "Could not read a QR code from the photo.",
                        null,
                    )
                }
        } catch (e: Exception) {
            Log.e(TAG, "decodeQrFromPhoto exception", e)
            cleanupPhoto(file)
            result.error("decode", e.message ?: "Could not read the photo", null)
        }
    }

    /** Downscale + EXIF-rotate so low-end devices do not OOM on 12MP JPEGs. */
    private fun loadBitmapForDecode(uri: Uri, file: File?): Bitmap? {
        return try {
            val path = file?.absolutePath
            val bounds = BitmapFactory.Options().apply { inJustDecodeBounds = true }
            if (path != null && File(path).exists()) {
                BitmapFactory.decodeFile(path, bounds)
            } else {
                contentResolver.openInputStream(uri)?.use {
                    BitmapFactory.decodeStream(it, null, bounds)
                }
            }
            var sample = 1
            val w = bounds.outWidth
            val h = bounds.outHeight
            while (w / sample > MAX_DECODE_EDGE || h / sample > MAX_DECODE_EDGE) {
                sample *= 2
            }
            val opts = BitmapFactory.Options().apply { inSampleSize = sample }
            var bitmap = if (path != null && File(path).exists()) {
                BitmapFactory.decodeFile(path, opts)
            } else {
                contentResolver.openInputStream(uri)?.use {
                    BitmapFactory.decodeStream(it, null, opts)
                }
            } ?: return null

            val rotation = readExifRotation(path, uri)
            if (rotation != 0) {
                val matrix = Matrix().apply { postRotate(rotation.toFloat()) }
                val rotated = Bitmap.createBitmap(bitmap, 0, 0, bitmap.width, bitmap.height, matrix, true)
                if (rotated != bitmap) bitmap.recycle()
                bitmap = rotated
            }
            Log.i(TAG, "bitmap for decode ${bitmap.width}x${bitmap.height} sample=$sample rot=$rotation")
            bitmap
        } catch (e: Exception) {
            Log.e(TAG, "loadBitmapForDecode failed", e)
            null
        }
    }

    private fun readExifRotation(path: String?, uri: Uri): Int {
        return try {
            val exif = when {
                path != null && File(path).exists() -> ExifInterface(path)
                else -> contentResolver.openInputStream(uri)?.use { ExifInterface(it) }
            } ?: return 0
            when (exif.getAttributeInt(ExifInterface.TAG_ORIENTATION, ExifInterface.ORIENTATION_NORMAL)) {
                ExifInterface.ORIENTATION_ROTATE_90 -> 90
                ExifInterface.ORIENTATION_ROTATE_180 -> 180
                ExifInterface.ORIENTATION_ROTATE_270 -> 270
                else -> 0
            }
        } catch (_: Exception) {
            0
        }
    }

    private fun cleanupPhoto(file: File?) {
        try {
            file?.delete()
        } catch (_: Exception) {
        }
        photoFile = null
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
        val pending = captureAfterPermission
        if (pending != null) {
            captureAfterPermission = null
            if (ok) launchSystemCamera(pending)
            else pending.error("permission_denied", "Camera permission denied", null)
        }
    }

    private fun setSecure(on: Boolean) {
        secureWanted = false
        window.clearFlags(WindowManager.LayoutParams.FLAG_SECURE)
    }
}
