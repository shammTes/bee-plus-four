package com.warsay.high

import android.os.Build

/** The bundled ML Kit text-recognition native lib ships for ARM only (see build.gradle.kts). */
object OcrSupport {
    val available: Boolean by lazy {
        val abi = Build.SUPPORTED_ABIS.firstOrNull().orEmpty()
        abi.startsWith("arm")
    }
}
