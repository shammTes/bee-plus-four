# ML Kit finds its components (barcode, text, vision-common) by instantiating every
# ComponentRegistrar listed in the manifest through reflection. The consumer rule shipped by
# firebase-components 16.1.0 is `-keep class * implements ComponentRegistrar` with no member list,
# and in R8 full mode (default since AGP 8) that no longer keeps the no-arg constructor. R8 then
# removed BarcodeRegistrar.<init>() etc., ML Kit registered nothing, and
# BarcodeScanning.getClient() threw a NullPointerException as soon as the unlock scanner opened.
-keep class * implements com.google.firebase.components.ComponentRegistrar {
    void <init>();
}

# Add-on resources (pdfrx / PDFium via package:jni, cryptography_flutter native AES-GCM). Their consumer rules
# already cover this; kept explicit because R8 full mode stripped reflective constructors before (see above).
-keep class com.github.dart_lang.jni.** { *; }
-keep class dev.dint.cryptography_flutter.** { *; }
