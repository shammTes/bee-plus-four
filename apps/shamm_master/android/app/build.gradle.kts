import java.util.Properties

plugins {
    id("com.android.application")
    // The Flutter Gradle Plugin must be applied after the Android and Kotlin Gradle plugins.
    id("dev.flutter.flutter-gradle-plugin")
}

// Release signing: env vars or android/key.properties (never committed; the key lives outside git).
//   MASTER_KEYSTORE=/path/master-release.jks MASTER_KEYSTORE_PASSWORD=… MASTER_KEY_ALIAS=master MASTER_KEY_PASSWORD=…
val keyProps = Properties().apply {
    val f = rootProject.file("key.properties")
    if (f.exists()) f.inputStream().use { load(it) }
}
fun sign(env: String, prop: String): String? = System.getenv(env)?.takeIf { it.isNotEmpty() } ?: keyProps.getProperty(prop)
val storePath = sign("MASTER_KEYSTORE", "storeFile")

android {
    namespace = "com.shamm.master"
    compileSdk = flutter.compileSdkVersion
    ndkVersion = flutter.ndkVersion

    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }

    defaultConfig {
        // Own app ID: installs next to Bee Seller, Four (com.four.student) and Winner.
        applicationId = "com.shamm.master"
        minSdk = flutter.minSdkVersion
        targetSdk = flutter.targetSdkVersion
        versionCode = flutter.versionCode
        versionName = flutter.versionName
    }

    signingConfigs {
        if (storePath != null && file(storePath).exists()) {
            create("release") {
                storeFile = file(storePath)
                storePassword = sign("MASTER_KEYSTORE_PASSWORD", "storePassword")
                keyAlias = sign("MASTER_KEY_ALIAS", "keyAlias")
                keyPassword = sign("MASTER_KEY_PASSWORD", "keyPassword")
            }
        }
    }

    buildTypes {
        release {
            signingConfig = signingConfigs.findByName("release") ?: signingConfigs.getByName("debug")
            isMinifyEnabled = true
            isShrinkResources = true
            proguardFiles(getDefaultProguardFile("proguard-android-optimize.txt"), "proguard-rules.pro")
        }
    }
}

kotlin {
    compilerOptions {
        jvmTarget = org.jetbrains.kotlin.gradle.dsl.JvmTarget.JVM_17
    }
}

flutter {
    source = "../.."
}

dependencies {
    // Same scanner stack as Four: bundled (offline) ML Kit barcode model + CameraX live preview.
    implementation("com.google.mlkit:barcode-scanning:17.3.0")
    implementation("androidx.camera:camera-camera2:1.4.2")
    implementation("androidx.camera:camera-lifecycle:1.4.2")
    implementation("androidx.camera:camera-view:1.4.2")
    implementation("androidx.core:core-ktx:1.13.1")
    implementation("androidx.activity:activity-ktx:1.9.3")
}
