# Copied from Four (shammTes/bee-plus-four android/app/proguard-rules.pro).
# ML Kit finds its components (barcode, vision-common) by instantiating every ComponentRegistrar listed in the
# manifest through reflection. The consumer rule shipped by firebase-components is
# `-keep class * implements ComponentRegistrar` with no member list, and in R8 full mode (default since AGP 8)
# that no longer keeps the no-arg constructor. R8 then removes BarcodeRegistrar.<init>(), ML Kit registers
# nothing, and BarcodeScanning.getClient() throws a NullPointerException as soon as the scanner opens.
-keep class * implements com.google.firebase.components.ComponentRegistrar {
    void <init>();
}
-keep class com.shamm.master.ScanActivity { *; }
