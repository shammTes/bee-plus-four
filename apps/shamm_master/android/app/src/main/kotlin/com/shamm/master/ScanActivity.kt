package com.shamm.master

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
import java.util.concurrent.Executor
import java.util.concurrent.ExecutorService
import java.util.concurrent.RejectedExecutionException
import java.util.concurrent.Executors
import java.util.concurrent.TimeUnit
import java.util.concurrent.atomic.AtomicBoolean

/**
 * Shamm Master QR scanner. Copied from Four's working in-app scanner (CameraX + bundled ML Kit barcode,
 * auto-zoom, torch, tap-to-focus, late-callback-safe executor) without the text-recognition pass, so the
 * APK stays small and it runs well on low-end phones. Returns the first QR text it sees; Dart decides
 * whether it is a Seller ID or a top-up code. Needs the R8 keep rule in proguard-rules.pro.
 *
 * Extras in: title, hint. Result extras: payload, frames, error, message.
 */
class ScanActivity : ComponentActivity() {
    companion object {
        /** elapsedRealtime of the last successful onCreate — MainActivity's "did it open?" watchdog reads it. */
        @Volatile @JvmStatic var createdAt = 0L
        private const val TAG = "ShammScan"
        const val EXTRA_TITLE = "title"
        const val EXTRA_HINT = "hint"
        const val EXTRA_PAYLOAD = "payload"
        const val EXTRA_VIA = "via"
        const val EXTRA_FRAMES = "frames"
        const val EXTRA_ERROR = "error"
        const val EXTRA_MESSAGE = "message"
    }

    private lateinit var previewView: PreviewView
    private lateinit var status: TextView
    private lateinit var torchBtn: TextView
    private lateinit var zoomBtn: TextView
    private var camera: Camera? = null
    private var cameraProvider: ProcessCameraProvider? = null
    private var analysisExecutor: ExecutorService? = null
    /**
     * ML Kit completes tasks on its own threads and then posts the listener to this executor. After
     * onDestroy shut the executor down, a late frame would throw RejectedExecutionException on an
     * ML Kit thread and kill the whole app — so late callbacks are dropped instead.
     */
    private val listenerExecutor = Executor { r ->
        val exec = analysisExecutor
        if (exec == null || exec.isShutdown) return@Executor
        try {
            exec.execute(r)
        } catch (_: RejectedExecutionException) {
        }
    }
    private var barcodeScanner: BarcodeScanner? = null
    private val finished = AtomicBoolean(false)
    @Volatile private var frames = 0
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
        createdAt = SystemClock.elapsedRealtime()
        Log.i(TAG, "ScanActivity onCreate sdk=${android.os.Build.VERSION.SDK_INT} abi=${android.os.Build.SUPPORTED_ABIS.firstOrNull()}")
        // Anything failing here must come back to the lock screen as an error, never a crash.
        try {
            window.clearFlags(WindowManager.LayoutParams.FLAG_SECURE)
            window.addFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON)
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
        } catch (e: Throwable) {
            Log.e(TAG, "ScanActivity onCreate failed", e)
            finishError("init", "Scanner screen failed: ${e.javaClass.simpleName}: ${e.message}")
        }
    }

    private fun dp(v: Float): Int =
        TypedValue.applyDimension(TypedValue.COMPLEX_UNIT_DIP, v, resources.displayMetrics).toInt()

    private fun pill(text: String, filled: Boolean): TextView = TextView(this).apply {
        this.text = text
        setTextColor(if (filled) Color.WHITE else Color.parseColor("#1F2937"))
        textSize = 15f
        typeface = android.graphics.Typeface.DEFAULT_BOLD
        gravity = Gravity.CENTER
        setPadding(dp(18f), dp(12f), dp(18f), dp(12f))
        background = GradientDrawable().apply {
            cornerRadius = dp(28f).toFloat()
            setColor(if (filled) Color.parseColor("#4F46E5") else Color.WHITE)
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
            text = intent.getStringExtra(EXTRA_TITLE) ?: "Scan a QR code"
            setTextColor(Color.WHITE)
            textSize = 19f
            typeface = android.graphics.Typeface.DEFAULT_BOLD
            gravity = Gravity.CENTER
        })
        status = TextView(this).apply {
            text = intent.getStringExtra(EXTRA_HINT) ?: "Hold the QR inside the box, about 15–25 cm away."
            setTextColor(Color.parseColor("#E0E7FF"))
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
        val future = try {
            ProcessCameraProvider.getInstance(this)
        } catch (e: Throwable) {
            Log.e(TAG, "ScanActivity CameraX init failed", e)
            finishError("camera", "Camera could not start: ${e.message ?: e.javaClass.simpleName}")
            return
        }
        future.addListener({
            try {
                val provider = future.get()
                cameraProvider = provider
                bindUseCases(provider)
            } catch (e: Throwable) {
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
        barcodeScanner = try { BarcodeScanning.getClient(
            BarcodeScannerOptions.Builder()
                .setBarcodeFormats(
                    Barcode.FORMAT_QR_CODE,
                    Barcode.FORMAT_DATA_MATRIX,
                    Barcode.FORMAT_AZTEC,
                    Barcode.FORMAT_PDF417,
                )
                .setZoomSuggestionOptions(zoomOptions)
                .build(),
        ) } catch (e: Throwable) {
            // e.g. ML Kit components stripped by R8: report it so Dart falls back to photo scan (ZXing).
            Log.e(TAG, "ScanActivity ML Kit barcode client failed", e)
            finishError("mlkit", "QR reader could not start: ${e.javaClass.simpleName}: ${e.message}")
            return
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
        } catch (e: Throwable) {
            Log.e(TAG, "ScanActivity bindToLifecycle failed", e)
            finishError("camera", "Camera could not start: ${e.message ?: e.javaClass.simpleName}")
        }
    }

    private fun analyze(proxy: ImageProxy) {
        try {
            analyzeFrame(proxy)
        } catch (e: Throwable) {
            Log.e(TAG, "ScanActivity frame failed", e)
            try { proxy.close() } catch (_: Throwable) {}
        }
    }

    @androidx.annotation.OptIn(markerClass = [ExperimentalGetImage::class])
    private fun analyzeFrame(proxy: ImageProxy) {
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
        if (frames == 1) Log.i(TAG, "ScanActivity first frame ${proxy.width}x${proxy.height} rot=${proxy.imageInfo.rotationDegrees}")
        val image = InputImage.fromMediaImage(media, proxy.imageInfo.rotationDegrees)
        val scanner = barcodeScanner
        if (scanner == null) {
            proxy.close()
            return
        }
        scanner.process(image)
            .addOnSuccessListener(listenerExecutor) { barcodes ->
                val values = barcodes.mapNotNull { b ->
                    b.rawValue?.trim()?.takeIf { it.isNotEmpty() }
                        ?: b.displayValue?.trim()?.takeIf { it.isNotEmpty() }
                        ?: b.rawBytes?.let { String(it, Charsets.UTF_8).trim() }?.takeIf { it.isNotEmpty() }
                }
                val v = values.firstOrNull()
                if (v != null) {
                    Log.i(TAG, "ScanActivity QR hit frame=$frames len=${v.length}")
                    proxy.close()
                    finishOk(v, "qr")
                    return@addOnSuccessListener
                }
                if (frames % 60 == 0) {
                    val secs = (SystemClock.elapsedRealtime() - startedAt) / 1000
                    setStatus("Looking… (${secs}s) Tap the screen to focus. Use Light in a dark room.")
                }
                proxy.close()
            }
            .addOnFailureListener(listenerExecutor) { e ->
                Log.w(TAG, "ScanActivity barcode frame failed: ${e.message}")
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
            Log.i(TAG, "focusAt failed: ${e.message}")
        }
    }

    private fun baseResult(): Intent = Intent().apply {
        putExtra(EXTRA_FRAMES, frames)
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
        Log.i(TAG, "ScanActivity cancelled frames=$frames ")
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
        analysisExecutor?.shutdown()
        super.onDestroy()
    }

    /** Dims the edges and draws a framing box so users know where to put the code. */
    private class FrameOverlay(ctx: android.content.Context) : View(ctx) {
        private val dim = Paint().apply { color = Color.argb(110, 0, 0, 0) }
        private val stroke = Paint(Paint.ANTI_ALIAS_FLAG).apply {
            color = Color.parseColor("#A5B4FC")
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
