#include <jni.h>

extern const unsigned char termux_bootstrap_zip_start[];
extern const unsigned char termux_bootstrap_zip_end[];

JNIEXPORT jbyteArray JNICALL Java_com_termux_app_TermuxInstaller_getZip(JNIEnv *env, __attribute__((__unused__)) jobject This)
{
    // Dynamically calculate the pointer position and exact byte size
    const jbyte *blob = (const jbyte *)termux_bootstrap_zip_start;
    jsize blob_size = (jsize)(termux_bootstrap_zip_end - termux_bootstrap_zip_start);

    jbyteArray ret = (*env)->NewByteArray(env, blob_size);
    (*env)->SetByteArrayRegion(env, ret, 0, blob_size, blob);
    return ret;
}
