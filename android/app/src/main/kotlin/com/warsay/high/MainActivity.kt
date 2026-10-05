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
import com.google.zxing.BinaryBitmap
import com.google.zxing.DecodeHintType
import com.google.zxing.MultiFormatReader
import com.google.zxing.RGBLuminanceSource
import com.google.zxing.common.HybridBinarizer
import com.google.zxing.BarcodeFormat
import io.flutter.embedding.android.FlutterFragmentActivity
import io.flutter.embedding.engine.FlutterEngine
import io.flutter.plugin.common.MethodChannel
import java.io.File
import java.util.EnumMap
import java.util.EnumSet
import java.util.concurrent.atomic.AtomicBoolean

/**
 * Unlock QR via the **system camera app** (ACTION_IMAGE_CAPTURE / TakePicture),
 * then robust on-device decode of the still photo:
 *   1) ML Kit barcode-scanning (file path + bitmap, multiple rotations)
 *   2) ZXing fallback (TRY_HARDER, rotations, inverted)
 *
 * Prefer payloads containing "BEE1|". Logcat tag: HighSecure
 */
class MainActivity : FlutterFragmentActivity() {
    companion object {
        private const val TAG = "HighSecure"
        private const val CHANNEL = "com.warsay.high/secure"
        /** Soft cap — keep enough pixels for dense unlock QR modules. */
        private const val MAX_DECODE_EDGE = 2400
        private const val MIN_PHOTO_BYTES = 2_048
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
            val bytes = file?.takeIf { it.exists() }?.length() ?: -1L
            Log.i(TAG, "TakePicture success=$success uri=$uri path=${file?.absolutePath} bytes=$bytes")
            if (pending == null) return@registerForActivityResult
            if (!success || uri == null) {
                cleanupPhoto(file)
                // Empty string = user cancelled — Dart shows a clear message.
                pending.success("")
                return@registerForActivityResult
            }
            if (bytes in 0 until MIN_PHOTO_BYTES) {
                Log.e(TAG, "photo too small/empty bytes=$bytes — camera may not have written FileProvider URI")
                cleanupPhoto(file)
                pending.error(
                    "decode",
                    "Camera did not save a usable photo. Try again, or enter the unlock code below.",
                    null,
                )
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
                    // Primary unlock path: system camera → still photo → ML Kit / ZXing QR.
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
        Log.i(TAG, "MethodChannel $CHANNEL ready (system-camera unlock, robust decode)")
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
            // Do NOT leave a 0-byte stub that some OEM cameras refuse to overwrite.
            val file = File(cacheDir, "unlock_qr_${System.currentTimeMillis()}.jpg")
            if (file.exists()) file.delete()
            // Touch empty file so FileProvider / some OEM cameras can open the Uri for write.
            file.parentFile?.mkdirs()
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

            Log.i(TAG, "launching system camera TakePicture uri=$uri path=${file.absolutePath}")
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
        val finished = AtomicBoolean(false)
        fun finishSuccess(value: String, via: String) {
            if (!finished.compareAndSet(false, true)) return
            Log.i(TAG, "unlock decode OK via=$via len=${value.length} preview=${redact(value)}")
            cleanupPhoto(file)
            result.success(value)
        }
        fun finishNoQr() {
            if (!finished.compareAndSet(false, true)) return
            Log.w(TAG, "unlock decode: no QR found after ML Kit + ZXing")
            cleanupPhoto(file)
            result.error(
                "no_qr",
                "No QR found — retake photo closer / better light",
                null,
            )
        }
        fun finishError(code: String, message: String) {
            if (!finished.compareAndSet(false, true)) return
            Log.e(TAG, "unlock decode error code=$code msg=$message")
            cleanupPhoto(file)
            result.error(code, message, null)
        }

        try {
            val path = file?.absolutePath
            val bytes = file?.takeIf { it.exists() }?.length() ?: -1L
            Log.i(TAG, "decodeQrFromPhoto begin path=$path bytes=$bytes uri=$uri")

            // Pass 1: ML Kit fromFilePath (auto EXIF) — often the most reliable for JPEGs.
            if (path != null && File(path).exists() && bytes >= MIN_PHOTO_BYTES) {
                try {
                    // Prefer the FileProvider content Uri (readable via ContentResolver).
                    val fromFile = InputImage.fromFilePath(this, uri)
                    runMlKit(fromFile, "fromFilePath") { value ->
                        if (value != null) {
                            finishSuccess(value, "mlkit-file")
                            true
                        } else {
                            // Continue to bitmap / rotation / ZXing passes.
                            continueDecodeAfterFileMiss(uri, file, ::finishSuccess, ::finishNoQr, ::finishError)
                            true
                        }
                    }
                    return
                } catch (e: Exception) {
                    Log.w(TAG, "fromFilePath InputImage failed: ${e.message}")
                }
            }
            continueDecodeAfterFileMiss(uri, file, ::finishSuccess, ::finishNoQr, ::finishError)
        } catch (e: Exception) {
            Log.e(TAG, "decodeQrFromPhoto exception", e)
            finishError("decode", e.message ?: "Could not read the photo")
        }
    }

    private fun continueDecodeAfterFileMiss(
        uri: Uri,
        file: File?,
        finishSuccess: (String, String) -> Unit,
        finishNoQr: () -> Unit,
        finishError: (String, String) -> Unit,
    ) {
        try {
            val base = loadBitmapForDecode(uri, file, maxEdge = MAX_DECODE_EDGE)
            if (base == null) {
                finishError("decode", "Could not read the photo from the camera.")
                return
            }
            Log.i(TAG, "bitmap ready ${base.width}x${base.height} for multi-pass decode")

            // Pass 2: ML Kit on EXIF-corrected bitmap + 90° rotations.
            tryMlKitRotations(base, 0) { mlValue ->
                if (mlValue != null) {
                    finishSuccess(mlValue, "mlkit-bitmap")
                    return@tryMlKitRotations
                }
                // Pass 3: ZXing on same bitmaps (and a higher-res retry if we downscaled hard).
                val zxingHit = tryZxingAll(base)
                if (zxingHit != null) {
                    finishSuccess(zxingHit, "zxing")
                    return@tryMlKitRotations
                }
                // Pass 4: if original file is large, try a higher-res bitmap once more with ZXing.
                val hi = if (file != null && file.length() > 400_000L) {
                    loadBitmapForDecode(uri, file, maxEdge = 3200)
                } else null
                if (hi != null && (hi.width != base.width || hi.height != base.height)) {
                    Log.i(TAG, "hi-res retry ${hi.width}x${hi.height}")
                    val hiZx = tryZxingAll(hi)
                    if (hiZx != null) {
                        if (hi != base) hi.recycle()
                        finishSuccess(hiZx, "zxing-hires")
                        return@tryMlKitRotations
                    }
                    // One more ML Kit pass on hi-res upright only.
                    try {
                        val image = InputImage.fromBitmap(hi, 0)
                        runMlKit(image, "hires-bitmap") { v ->
                            if (hi != base) hi.recycle()
                            if (v != null) finishSuccess(v, "mlkit-hires")
                            else finishNoQr()
                            true
                        }
                        return@tryMlKitRotations
                    } catch (e: Exception) {
                        if (hi != base) hi.recycle()
                        Log.w(TAG, "hires mlkit failed: ${e.message}")
                    }
                }
                finishNoQr()
            }
        } catch (e: Exception) {
            Log.e(TAG, "continueDecodeAfterFileMiss", e)
            finishError("decode", e.message ?: "Could not read the photo")
        }
    }

    private fun tryMlKitRotations(
        base: Bitmap,
        index: Int,
        done: (String?) -> Unit,
    ) {
        val angles = intArrayOf(0, 90, 180, 270)
        if (index >= angles.size) {
            done(null)
            return
        }
        val angle = angles[index]
        val bmp = if (angle == 0) base else rotateBitmap(base, angle)
        try {
            val image = InputImage.fromBitmap(bmp, 0)
            runMlKit(image, "bitmap-rot$angle") { value ->
                if (bmp != base) bmp.recycle()
                if (value != null) {
                    done(value)
                } else {
                    tryMlKitRotations(base, index + 1, done)
                }
                true
            }
        } catch (e: Exception) {
            if (bmp != base) bmp.recycle()
            Log.w(TAG, "mlkit rot=$angle failed: ${e.message}")
            tryMlKitRotations(base, index + 1, done)
        }
    }

    /**
     * @param onResult return true if this listener consumed the result (always true here).
     *                 Callback receives preferred raw value or null if none.
     */
    private fun runMlKit(
        image: InputImage,
        label: String,
        onResult: (String?) -> Boolean,
    ) {
        val options = BarcodeScannerOptions.Builder()
            .setBarcodeFormats(
                Barcode.FORMAT_QR_CODE,
                Barcode.FORMAT_AZTEC,
                Barcode.FORMAT_DATA_MATRIX,
            )
            .build()
        val scanner = BarcodeScanning.getClient(options)
        scanner.process(image)
            .addOnSuccessListener { barcodes ->
                val raws = barcodes.mapNotNull { b ->
                    val v = b.rawValue?.trim()?.takeIf { it.isNotEmpty() }
                        ?: b.displayValue?.trim()?.takeIf { it.isNotEmpty() }
                    v
                }
                Log.i(
                    TAG,
                    "ML Kit $label count=${barcodes.size} values=${raws.map { redact(it) }}",
                )
                val chosen = pickUnlockPayload(raws)
                try {
                    scanner.close()
                } catch (_: Exception) {
                }
                onResult(chosen)
            }
            .addOnFailureListener { error ->
                Log.e(TAG, "ML Kit $label failed: ${error.message}", error)
                try {
                    scanner.close()
                } catch (_: Exception) {
                }
                onResult(null)
            }
    }

    private fun tryZxingAll(base: Bitmap): String? {
        val angles = intArrayOf(0, 90, 180, 270)
        for (angle in angles) {
            val bmp = if (angle == 0) base else rotateBitmap(base, angle)
            try {
                val hit = decodeWithZxing(bmp, invert = false)
                    ?: decodeWithZxing(bmp, invert = true)
                if (hit != null) {
                    Log.i(TAG, "ZXing hit rot=$angle invert-tried len=${hit.length} preview=${redact(hit)}")
                    return hit
                }
            } finally {
                if (bmp != base && !bmp.isRecycled) {
                    try { bmp.recycle() } catch (_: Exception) {}
                }
            }
        }
        Log.i(TAG, "ZXing: no QR in any orientation")
        return null
    }

    private fun decodeWithZxing(bitmap: Bitmap, invert: Boolean): String? {
        return try {
            val w = bitmap.width
            val h = bitmap.height
            val pixels = IntArray(w * h)
            bitmap.getPixels(pixels, 0, w, 0, 0, w, h)
            if (invert) {
                for (i in pixels.indices) {
                    val c = pixels[i]
                    val r = 255 - ((c shr 16) and 0xff)
                    val g = 255 - ((c shr 8) and 0xff)
                    val b = 255 - (c and 0xff)
                    pixels[i] = (c and 0xff000000.toInt()) or (r shl 16) or (g shl 8) or b
                }
            }
            val source = RGBLuminanceSource(w, h, pixels)
            val bitmapBin = BinaryBitmap(HybridBinarizer(source))
            val hints = EnumMap<DecodeHintType, Any>(DecodeHintType::class.java)
            hints[DecodeHintType.TRY_HARDER] = true
            hints[DecodeHintType.POSSIBLE_FORMATS] = EnumSet.of(BarcodeFormat.QR_CODE)
            val reader = MultiFormatReader()
            reader.setHints(hints)
            val result = try {
                reader.decodeWithState(bitmapBin)
            } catch (_: Exception) {
                // Also try inverted binarizer path via a fresh reader on GlobalHistogram — skip.
                null
            } finally {
                reader.reset()
            }
            val text = result?.text?.trim().orEmpty()
            if (text.isEmpty()) null else text
        } catch (e: Exception) {
            Log.d(TAG, "zxing invert=$invert miss: ${e.message}")
            null
        }
    }

    /** Prefer Bee Seller / Flutter unlock payloads over incidental QR codes. */
    private fun pickUnlockPayload(values: List<String>): String? {
        if (values.isEmpty()) return null
        val bee = values.firstOrNull { it.contains("BEE1|") }
        if (bee != null) return bee
        return values.first()
    }

    private fun redact(raw: String): String {
        val t = raw.trim()
        if (t.length <= 16) return "***"
        // Keep layout visible, hide signature/nonce tail.
        val parts = t.split("|")
        return if (parts.size >= 4 && parts[0] == "BEE1") {
            "BEE1|${parts.getOrElse(1) {"?"}}|${parts.getOrElse(2) {"?"}}|…(redacted)"
        } else {
            "${t.take(12)}…(${t.length})"
        }
    }

    private fun rotateBitmap(src: Bitmap, degrees: Int): Bitmap {
        if (degrees % 360 == 0) return src
        val matrix = Matrix().apply { postRotate(degrees.toFloat()) }
        return Bitmap.createBitmap(src, 0, 0, src.width, src.height, matrix, true)
    }

    /** Downscale + EXIF-rotate so low-end devices do not OOM on 12MP JPEGs. */
    private fun loadBitmapForDecode(uri: Uri, file: File?, maxEdge: Int): Bitmap? {
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
            if (w <= 0 || h <= 0) {
                Log.e(TAG, "bitmap bounds invalid w=$w h=$h")
                return null
            }
            while (w / sample > maxEdge || h / sample > maxEdge) {
                sample *= 2
            }
            val opts = BitmapFactory.Options().apply {
                inSampleSize = sample
                inPreferredConfig = Bitmap.Config.ARGB_8888
            }
            var bitmap = if (path != null && File(path).exists()) {
                BitmapFactory.decodeFile(path, opts)
            } else {
                contentResolver.openInputStream(uri)?.use {
                    BitmapFactory.decodeStream(it, null, opts)
                }
            } ?: return null

            val rotation = readExifRotation(path, uri)
            if (rotation != 0) {
                val rotated = rotateBitmap(bitmap, rotation)
                if (rotated != bitmap) bitmap.recycle()
                bitmap = rotated
            }
            Log.i(
                TAG,
                "bitmap for decode ${bitmap.width}x${bitmap.height} sample=$sample rot=$rotation maxEdge=$maxEdge src=${w}x${h}",
            )
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
