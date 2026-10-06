package com.warsay.high

import android.content.Context
import android.util.Log
import java.io.File
import java.text.SimpleDateFormat
import java.util.ArrayDeque
import java.util.Date
import java.util.Locale

/**
 * Logcat tag HighSecure, plus the last [MAX] lines kept in memory so the lock screen can show a
 * "Scanner log" the user can screenshot. Also records an uncaught crash (with the log) to a small
 * file, so a scanner crash that kills the process is reported on the next start instead of the
 * app silently restarting.
 */
object HighLog {
    const val TAG = "HighSecure"
    private const val MAX = 30
    private const val CRASH_FILE = "high_scan_crash.txt"
    private const val OPEN_MARKER = "high_scan_open.txt"

    private val lines = ArrayDeque<String>(MAX + 1)
    private val clock = SimpleDateFormat("HH:mm:ss", Locale.US)
    @Volatile private var installed = false

    private fun add(level: Char, msg: String) {
        val line = "${clock.format(Date())} $level ${msg.take(300)}"
        synchronized(lines) {
            lines.addLast(line)
            while (lines.size > MAX) lines.removeFirst()
        }
    }

    fun i(msg: String) {
        Log.i(TAG, msg)
        add('I', msg)
    }

    fun w(msg: String) {
        Log.w(TAG, msg)
        add('W', msg)
    }

    fun e(msg: String, t: Throwable? = null) {
        if (t != null) Log.e(TAG, msg, t) else Log.e(TAG, msg)
        add('E', if (t != null) "$msg: ${t.javaClass.simpleName}: ${t.message}" else msg)
    }

    fun snapshot(): List<String> = synchronized(lines) { lines.toList() }

    /** Process-wide: write the crash + recent log to a file, then let Android's handler run. */
    fun installCrashCapture(context: Context) {
        if (installed) return
        installed = true
        val dir = context.applicationContext.filesDir
        val previous = Thread.getDefaultUncaughtExceptionHandler()
        Thread.setDefaultUncaughtExceptionHandler { thread, error ->
            try {
                add('E', "CRASH on ${thread.name}: ${error.javaClass.name}: ${error.message}")
                val stack = error.stackTrace.take(8).joinToString("\n") { "  at $it" }
                val cause = error.cause?.let { "\ncaused by ${it.javaClass.name}: ${it.message}" } ?: ""
                File(dir, CRASH_FILE).writeText(
                    "${error.javaClass.name}: ${error.message}$cause\n$stack\n--- log ---\n" + snapshot().joinToString("\n"),
                )
            } catch (_: Throwable) {
            }
            previous?.uncaughtException(thread, error)
        }
    }

    /** Marks that the in-app scanner is open; if the process dies before [scanClosed], the next start knows. */
    fun scanOpening(context: Context) {
        try { File(context.filesDir, OPEN_MARKER).writeText(System.currentTimeMillis().toString()) } catch (_: Throwable) {}
    }

    fun scanClosed(context: Context) {
        try { File(context.filesDir, OPEN_MARKER).delete() } catch (_: Throwable) {}
    }

    /**
     * Report left by the previous run: a crash (with stack + log), or "the scanner was open when
     * the app died". Returned once, then cleared. Null when the last run ended normally.
     */
    fun takeStartupReport(context: Context): Map<String, Any?>? {
        val dir = context.filesDir
        val crash = File(dir, CRASH_FILE)
        val marker = File(dir, OPEN_MARKER)
        val wasScanning = marker.exists()
        val crashText = try { if (crash.exists()) crash.readText() else null } catch (_: Throwable) { null }
        try { crash.delete() } catch (_: Throwable) {}
        try { marker.delete() } catch (_: Throwable) {}
        if (crashText == null && !wasScanning) return null
        val first = crashText?.lineSequence()?.firstOrNull()?.take(200)
        return mapOf(
            "code" to if (crashText != null) "crash" else "killed",
            "wasScanning" to wasScanning,
            "message" to first,
            "detail" to crashText?.take(4000),
        )
    }
}
