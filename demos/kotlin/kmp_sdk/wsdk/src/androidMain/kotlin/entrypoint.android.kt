import android.content.Context
import java.lang.ref.WeakReference

// https://stackoverflow.com/questions/76669135/using-context-in-kmm-shared-library-manually/77378735
actual class WsdkAppContext {

    private var value: WeakReference<Context?>? = null

    fun set(context: Context) {
        value = WeakReference(context)
    }

    fun get(): Context =
        value?.get() ?: throw Exception("Context has not been set.")
}
