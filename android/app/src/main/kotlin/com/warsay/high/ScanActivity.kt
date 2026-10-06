package com.warsay.high

import android.Manifest
import android.annotation.SuppressLint
import android.app.Activity
import android.content.Intent
import android.content.pm.PackageManager
import android.graphics.Canvas
import android.graphics.Color
import android.graphics.Paint
import android.graphics.RectF
import android.graphics.drawable.GradientDrawable
import android.os.Bundle
import android.os.SystemClock
import android.util.Log
import android.util.Size
import android.util.TypedValue
import android.view.Gravity
import android.view.MotionEvent
import android.view.View
import android.view.ViewGroup
import android.view.WindowManager
import android.widget.FrameLayout
import android.widget.LinearLayout
import android.widget.TextView
import androidx.activity.ComponentActivity
import androidx.activity.OnBackPressedCallback
import androidx.activity.result.contract.ActivityResultContracts
import androidx.camera.core.Camera
import androidx.camera.core.CameraSelector
import androidx.camera.core.ExperimentalGetImage
import androidx.camera.core.FocusMeteringAction
import androidx.camera.core.ImageAnalysis
import androidx.camera.core.ImageProxy
import androidx.camera.core.Preview
import androidx.camera.core.resolutionselector.ResolutionSelector
import androidx.camera.core.resolutionselector.ResolutionStrategy
import androidx.camera.lifecycle.ProcessCameraProvider
import androidx.camera.view.PreviewView
import androidx.core.content.ContextCompat
import androidx.core.view.ViewCompat
import androidx.core.view.WindowInsetsCompat
import com.google.mlkit.vision.barcode.BarcodeScanner
import com.google.mlkit.vision.barcode.BarcodeScannerOptions
import com.google.mlkit.vision.barcode.BarcodeScanning
import com.google.mlkit.vision.barcode.ZoomSuggestionOptions
import com.google.mlkit.vision.barcode.common.Barcode
import com.google.mlkit.vision.common.InputImage
import com.google.mlkit.vision.text.TextRecognition
import com.google.mlkit.vision.text.TextRecognizer
import com.google.mlkit.vision.text.latin.TextRecognizerOptions
import java.util.concurrent.ExecutorService
import java.util.concurrent.Executors
import java.util.concurrent.TimeUnit
import java.util.concurrent.atomic.AtomicBoolean

/**
 * In-app unlock scanner (same process as Flutter, so the result can never be lost to the OS
 * killing a background app). CameraX preview + continuous analysis with bundled ML Kit:
 *  1. QR / Data Matrix / Aztec / PDF417 barcode (with ML Kit auto-zoom when the code is small)
 *  2. Text recognition of the printed unlock code — the current Bee Seller (Compose) shows the
 *     code as TEXT, not as a QR image, so reading the text is what makes scanning work.
 *     Text candidates are accepted only when the HMAC verifies ([UnlockCodeRecovery]).
 * Torch toggle, zoom button, tap-to-focus. Logcat tag: HighSecure
 *
 * Result extras: payload, via ("qr" | "text"), frames, nonBee (last non-unlock QR, redacted),
 * sawCodeText, error, message.
 */
class ScanActivity : ComponentActivity() {
    companion object {
        private const val TAG = "HighSecure"
        const val EXTRA_DEVICE_ID = "deviceId"
        const val EXTRA_PAYLOAD = "payload"
        const val EXTRA_VIA = "via"
        const val EXTRA_FRAMES = "frames"
        const val EXTRA_NON_BEE = "nonBee"
        const val EXTRA_SAW_TEXT = "sawCodeText"
        const val EXTRA_ERROR = "error"
        const val EXTRA_MESSAGE = "message"
        /** Run text recognition at most this often (ms) — keeps low-end phones responsive. */
        private const val TEXT_EVERY_MS = 350L
    }

    private var deviceId: String? = null
    private lateinit var previewView: PreviewView
    private lateinit var status: TextView
    private lateinit var torchBtn: TextView
    private lateinit var zoomBtn: TextView
    private var camera: Camera? = null
    private var cameraProvider: ProcessCameraProvider? = null
    private var analysisExecutor: ExecutorService? = null
    private var barcodeScanner: BarcodeScanner? = null
    private var textRecognizer: TextRecognizer? = null
    private val finished = AtomicBoolean(false)
    @Volatile private var frames = 0
    @Volatile private var lastTextAt = 0L
    @Volatile private var nonBee: String? = null
    @Volatile private var sawCodeText = false
    private var torchOn = false
    private var zoomStep = 0
    private val startedAt = SystemClock.elapsedRealtime()

    private val permissionLauncher =
        registerForActivityResult(ActivityResultContracts.RequestPermission()) { granted ->
            Log.i(TAG, "ScanActivity permission granted=$granted")
            if (granted) startCamera() else finishError("permission_denied", "Camera permission denied")
        }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        window.clearFlags(WindowManager.LayoutParams.FLAG_SECURE)
        window.addFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON)
        deviceId = intent.getStringExtra(EXTRA_DEVICE_ID)
        // Android 16 / targetSdk 36: onBackPressed() is no longer called; use the dispatcher.
        onBackPressedDispatcher.addCallback(this, object : OnBackPressedCallback(true) {
            override fun handleOnBackPressed() = finishCancelled()
        })
        buildUi()
        if (ContextCompat.checkSelfPermission(this, Manifest.permission.CAMERA) == PackageManager.PERMISSION_GRANTED) {
            startCamera()
        } else {
            permissionLauncher.launch(Manifest.permission.CAMERA)
        }
    }

    private fun dp(v: Float): Int =
        TypedValue.applyDimension(TypedValue.COMPLEX_UNIT_DIP, v, resources.displayMetrics).toInt()

    private fun pill(text: String, filled: Boolean): TextView = TextView(this).apply {
        this.text = text
        setTextColor(if (filled) Color.WHITE else Color.parseColor("#3E3129"))
        textSize = 15f
        typeface = android.graphics.Typeface.DEFAULT_BOLD
        gravity = Gravity.CENTER
        setPadding(dp(18f), dp(12f), dp(18f), dp(12f))
        background = GradientDrawable().apply {
            cornerRadius = dp(28f).toFloat()
            setColor(if (filled) Color.parseColor("#C24E32") else Color.parseColor("#FFFCF7"))
        }
        isClickable = true
        isFocusable = true
    }

    @SuppressLint("ClickableViewAccessibility")
    private fun buildUi() {
        val root = FrameLayout(this).apply { setBackgroundColor(Color.BLACK) }
        previewView = PreviewView(this).apply {
            implementationMode = PreviewView.ImplementationMode.COMPATIBLE
            scaleType = PreviewView.ScaleType.FILL_CENTER
        }
        root.addView(previewView, FrameLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.MATCH_PARENT))
        root.addView(FrameOverlay(this), FrameLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.MATCH_PARENT))

        val top = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            setPadding(dp(18f), dp(16f), dp(18f), dp(8f))
        }
        top.addView(TextView(this).apply {
            text = "Scan the Bee Seller unlock code"
            setTextColor(Color.WHITE)
            textSize = 19f
            typeface = android.graphics.Typeface.DEFAULT_BOLD
            gravity = Gravity.CENTER
        })
        status = TextView(this).apply {
            text = "Point at the QR or at the BEE1|… code text. Hold steady, about 15–25 cm away."
            setTextColor(Color.parseColor("#FFE7D4"))
            textSize = 14f
            gravity = Gravity.CENTER
            setPadding(0, dp(6f), 0, 0)
        }
        top.addView(status)
        root.addView(top, FrameLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.WRAP_CONTENT, Gravity.TOP))

        val bottom = LinearLayout(this).apply {
            orientation = LinearLayout.HORIZONTAL
            gravity = Gravity.CENTER
            setPadding(dp(12f), dp(8f), dp(12f), dp(20f))
        }
        torchBtn = pill("Light: off", false).apply { setOnClickListener { toggleTorch() } }
        zoomBtn = pill("Zoom 1×", false).apply { setOnClickListener { cycleZoom() } }
        val cancel = pill("Cancel", true).apply { setOnClickListener { finishCancelled() } }
        val lp = { LinearLayout.LayoutParams(0, ViewGroup.LayoutParams.WRAP_CONTENT, 1f).apply { setMargins(dp(5f), 0, dp(5f), 0) } }
        bottom.addView(torchBtn, lp())
        bottom.addView(zoomBtn, lp())
        bottom.addView(cancel, lp())
        root.addView(bottom, FrameLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.WRAP_CONTENT, Gravity.BOTTOM))

        // Edge-to-edge (targetSdk 35+): keep controls clear of status / navigation bars.
        ViewCompat.setOnApplyWindowInsetsListener(root) { _, insets ->
            val bars = insets.getInsets(WindowInsetsCompat.Type.systemBars() or WindowInsetsCompat.Type.displayCutout())
            top.setPadding(dp(18f), dp(16f) + bars.top, dp(18f), dp(8f))
            bottom.setPadding(dp(12f), dp(8f), dp(12f), dp(20f) + bars.bottom)
            insets
        }

        previewView.setOnTouchListener { v, ev ->
            if (ev.action == MotionEvent.ACTION_UP) {
                focusAt(ev.x, ev.y)
                v.performClick()
            }
            true
        }
        setContentView(root)
    }

    private fun setStatus(msg: String) {
        runOnUiThread { if (!finished.get()) status.text = msg }
    }

    private fun startCamera() {
        val future = ProcessCameraProvider.getInstance(this)
        future.addListener({
            try {
                val provider = future.get()
                cameraProvider = provider
                bindUseCases(provider)
            } catch (e: Exception) {
                Log.e(TAG, "ScanActivity camera provider failed", e)
                finishError("camera", "Camera could not start: ${e.message ?: e.javaClass.simpleName}")
            }
        }, ContextCompat.getMainExecutor(this))
    }

    private fun bindUseCases(provider: ProcessCameraProvider) {
        val selector = when {
            provider.hasCamera(CameraSelector.DEFAULT_BACK_CAMERA) -> CameraSelector.DEFAULT_BACK_CAMERA
            provider.hasCamera(CameraSelector.DEFAULT_FRONT_CAMERA) -> CameraSelector.DEFAULT_FRONT_CAMERA
            else -> {
                finishError("no_camera", "This phone reports no camera.")
                return
            }
        }
        val resolution = ResolutionSelector.Builder()
            .setResolutionStrategy(
                ResolutionStrategy(Size(1280, 720), ResolutionStrategy.FALLBACK_RULE_CLOSEST_HIGHER_THEN_LOWER),
            )
            .build()
        val preview = Preview.Builder().setResolutionSelector(resolution).build().also {
            it.setSurfaceProvider(previewView.surfaceProvider)
        }
        val analysis = ImageAnalysis.Builder()
            .setResolutionSelector(resolution)
            .setBackpressureStrategy(ImageAnalysis.STRATEGY_KEEP_ONLY_LATEST)
            .build()
        val exec = Executors.newSingleThreadExecutor()
        analysisExecutor = exec

        val zoomCallback = ZoomSuggestionOptions.ZoomCallback { ratio ->
            val cam = camera
            if (cam == null) {
                false
            } else {
                val max = cam.cameraInfo.zoomState.value?.maxZoomRatio ?: 1f
                val r = ratio.coerceIn(1f, max)
                Log.i(TAG, "ScanActivity auto-zoom -> $r")
                cam.cameraControl.setZoomRatio(r)
                true
            }
        }
        val zoomOptions = ZoomSuggestionOptions.Builder(zoomCallback).setMaxSupportedZoomRatio(4f).build()
        barcodeScanner = BarcodeScanning.getClient(
            BarcodeScannerOptions.Builder()
                .setBarcodeFormats(
                    Barcode.FORMAT_QR_CODE,
                    Barcode.FORMAT_DATA_MATRIX,
                    Barcode.FORMAT_AZTEC,
                    Barcode.FORMAT_PDF417,
                )
                .setZoomSuggestionOptions(zoomOptions)
                .build(),
        )
        textRecognizer = if (OcrSupport.available) {
            try {
                TextRecognition.getClient(TextRecognizerOptions.DEFAULT_OPTIONS)
            } catch (e: Throwable) {
                Log.e(TAG, "text recognizer unavailable", e)
                null
            }
        } else {
            null
        }
        analysis.setAnalyzer(exec) { proxy -> analyze(proxy) }

        try {
            provider.unbindAll()
            camera = provider.bindToLifecycle(this, selector, preview, analysis)
            val maxZoom = camera?.cameraInfo?.zoomState?.value?.maxZoomRatio ?: 1f
            Log.i(TAG, "ScanActivity camera bound selector=$selector maxZoom=$maxZoom hasFlash=${camera?.cameraInfo?.hasFlashUnit()}")
            if (camera?.cameraInfo?.hasFlashUnit() != true) torchBtn.visibility = View.GONE
            // Start centred focus once so phones without continuous AF still focus on the code.
            previewView.post { focusAt(previewView.width / 2f, previewView.height / 2f) }
        } catch (e: Exception) {
            Log.e(TAG, "ScanActivity bindToLifecycle failed", e)
            finishError("camera", "Camera could not start: ${e.message ?: e.javaClass.simpleName}")
        }
    }

    @androidx.annotation.OptIn(markerClass = [ExperimentalGetImage::class])
    private fun analyze(proxy: ImageProxy) {
        if (finished.get()) {
            proxy.close()
            return
        }
        val media = proxy.image
        if (media == null) {
            proxy.close()
            return
        }
        frames++
        val image = InputImage.fromMediaImage(media, proxy.imageInfo.rotationDegrees)
        val scanner = barcodeScanner
        if (scanner == null) {
            proxy.close()
            return
        }
        scanner.process(image)
            .addOnSuccessListener(analysisExecutor!!) { barcodes ->
                val values = barcodes.mapNotNull { b ->
                    b.rawValue?.trim()?.takeIf { it.isNotEmpty() }
                        ?: b.displayValue?.trim()?.takeIf { it.isNotEmpty() }
                        ?: b.rawBytes?.let { String(it, Charsets.UTF_8).trim() }?.takeIf { it.isNotEmpty() }
                }
                val bee = values.firstOrNull { it.contains("BEE1", ignoreCase = true) }
                if (bee != null) {
                    Log.i(TAG, "ScanActivity QR hit frame=$frames len=${bee.length} preview=${redact(bee)}")
                    proxy.close()
                    finishOk(bee, "qr")
                    return@addOnSuccessListener
                }
                if (values.isNotEmpty()) {
                    val v = values.first()
                    // A QR that recovers to a valid code after cleaning still counts.
                    val rec = UnlockCodeRecovery.recover(v, deviceId)
                    if (rec != null) {
                        proxy.close()
                        finishOk(rec.payload, "qr")
                        return@addOnSuccessListener
                    }
                    if (nonBee != v) Log.i(TAG, "ScanActivity non-unlock QR len=${v.length} preview=${redact(v)}")
                    nonBee = v
                    setStatus("That QR is not a Bee Seller unlock code (it says “${redact(v)}”). Point at the seller’s unlock code.")
                }
                maybeText(image, proxy)
            }
            .addOnFailureListener(analysisExecutor!!) { e ->
                Log.w(TAG, "ScanActivity barcode frame failed: ${e.message}")
                maybeText(image, proxy)
            }
    }

    /** Text pass (throttled). Always closes [proxy]. */
    private fun maybeText(image: InputImage, proxy: ImageProxy) {
        val rec = textRecognizer
        val now = SystemClock.elapsedRealtime()
        if (finished.get() || rec == null || now - lastTextAt < TEXT_EVERY_MS) {
            proxy.close()
            return
        }
        lastTextAt = now
        rec.process(image)
            .addOnSuccessListener(analysisExecutor!!) { text ->
                val raw = text.text
                if (raw.isNotBlank() && UnlockCodeRecovery.looksLikeCode(raw)) {
                    if (!sawCodeText) Log.i(TAG, "ScanActivity code text visible frame=$frames chars=${raw.length}")
                    sawCodeText = true
                    // Try the whole text, then line-joined blocks (reading order can vary).
                    val joined = text.textBlocks.joinToString("\n") { b -> b.lines.joinToString("") { it.text } }
                    val hit = UnlockCodeRecovery.recover(raw, deviceId)
                        ?: UnlockCodeRecovery.recover(joined, deviceId)
                    if (hit != null) {
                        Log.i(TAG, "ScanActivity TEXT hit layout=${hit.layout} frame=$frames preview=${redact(hit.payload)}")
                        proxy.close()
                        finishOk(hit.payload, "text")
                        return@addOnSuccessListener
                    }
                    setStatus("Code text seen — move closer so the whole BEE1|… code fills the box, and hold still.")
                } else if (frames % 40 == 0 && nonBee == null) {
                    val secs = (SystemClock.elapsedRealtime() - startedAt) / 1000
                    setStatus("Looking… (${secs}s) Point at the Bee Seller QR or BEE1|… code. Tap the screen to focus; use Light in a dark room.")
                }
                proxy.close()
            }
            .addOnFailureListener(analysisExecutor!!) { e ->
                Log.w(TAG, "ScanActivity text frame failed: ${e.message}")
                proxy.close()
            }
    }

    private fun toggleTorch() {
        val cam = camera ?: return
        torchOn = !torchOn
        cam.cameraControl.enableTorch(torchOn)
        torchBtn.text = if (torchOn) "Light: on" else "Light: off"
    }

    private fun cycleZoom() {
        val cam = camera ?: return
        val max = cam.cameraInfo.zoomState.value?.maxZoomRatio ?: 1f
        val steps = floatArrayOf(1f, 2f, 3f).filter { it <= max + 0.01f }
        zoomStep = (zoomStep + 1) % steps.size
        val z = steps[zoomStep]
        cam.cameraControl.setZoomRatio(z)
        zoomBtn.text = "Zoom ${z.toInt()}×"
    }

    private fun focusAt(x: Float, y: Float) {
        val cam = camera ?: return
        try {
            val point = previewView.meteringPointFactory.createPoint(x, y)
            val action = FocusMeteringAction.Builder(point, FocusMeteringAction.FLAG_AF or FocusMeteringAction.FLAG_AE)
                .setAutoCancelDuration(4, TimeUnit.SECONDS)
                .build()
            cam.cameraControl.startFocusAndMetering(action)
        } catch (e: Exception) {
            Log.d(TAG, "focusAt failed: ${e.message}")
        }
    }

    private fun baseResult(): Intent = Intent().apply {
        putExtra(EXTRA_FRAMES, frames)
        putExtra(EXTRA_SAW_TEXT, sawCodeText)
        nonBee?.let { putExtra(EXTRA_NON_BEE, redact(it)) }
    }

    private fun finishOk(payload: String, via: String) {
        if (!finished.compareAndSet(false, true)) return
        runOnUiThread {
            setResult(Activity.RESULT_OK, baseResult().putExtra(EXTRA_PAYLOAD, payload).putExtra(EXTRA_VIA, via))
            finish()
        }
    }

    private fun finishCancelled() {
        if (!finished.compareAndSet(false, true)) return
        Log.i(TAG, "ScanActivity cancelled frames=$frames sawCodeText=$sawCodeText nonBee=${nonBee?.let { redact(it) }}")
        runOnUiThread {
            setResult(Activity.RESULT_CANCELED, baseResult())
            finish()
        }
    }

    private fun finishError(code: String, message: String) {
        if (!finished.compareAndSet(false, true)) return
        Log.e(TAG, "ScanActivity error code=$code msg=$message")
        runOnUiThread {
            setResult(Activity.RESULT_CANCELED, baseResult().putExtra(EXTRA_ERROR, code).putExtra(EXTRA_MESSAGE, message))
            finish()
        }
    }

    override fun onDestroy() {
        finished.set(true)
        try { cameraProvider?.unbindAll() } catch (_: Exception) {}
        try { barcodeScanner?.close() } catch (_: Exception) {}
        try { textRecognizer?.close() } catch (_: Exception) {}
        analysisExecutor?.shutdown()
        super.onDestroy()
    }

    private fun redact(raw: String): String {
        val t = raw.trim()
        if (t.length <= 16) return t
        val parts = t.split("|")
        return if (parts.size >= 4 && parts[0].equals("BEE1", true)) {
            "BEE1|${parts[1]}|${parts[2]}|…(${t.length})"
        } else {
            "${t.take(16)}…(${t.length})"
        }
    }

    /** Dims the edges and draws a framing box so users know where to put the code. */
    private class FrameOverlay(ctx: android.content.Context) : View(ctx) {
        private val dim = Paint().apply { color = Color.argb(110, 0, 0, 0) }
        private val stroke = Paint(Paint.ANTI_ALIAS_FLAG).apply {
            color = Color.parseColor("#FFC9A3")
            style = Paint.Style.STROKE
            strokeWidth = 6f
        }
        override fun onDraw(canvas: Canvas) {
            super.onDraw(canvas)
            val w = width.toFloat()
            val h = height.toFloat()
            val side = minOf(w, h) * 0.82f
            val left = (w - side) / 2
            val topY = (h - side) / 2.2f
            val box = RectF(left, topY, left + side, topY + side * 0.8f)
            canvas.drawRect(0f, 0f, w, box.top, dim)
            canvas.drawRect(0f, box.bottom, w, h, dim)
            canvas.drawRect(0f, box.top, box.left, box.bottom, dim)
            canvas.drawRect(box.right, box.top, w, box.bottom, dim)
            canvas.drawRoundRect(box, 28f, 28f, stroke)
        }
    }
}
