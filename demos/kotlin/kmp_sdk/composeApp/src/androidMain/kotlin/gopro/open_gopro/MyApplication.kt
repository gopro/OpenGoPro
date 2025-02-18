package gopro.open_gopro

import com.gopro.open_gopro.OgpSdkAppContext
import android.app.Application
import di.buildAppModule
import org.koin.android.ext.koin.androidLogger
import org.koin.core.context.startKoin
import org.koin.core.logger.Level

class MyApplication : Application() {
    // TODO try https://insert-koin.io/docs/reference/koin-android/start#start-koin-with-androidx-startup-401

    override fun onCreate() {
        super.onCreate()
        val appContext = OgpSdkAppContext().apply { set(applicationContext) }
        startKoin {
            androidLogger(Level.WARNING)
            modules(buildAppModule(appContext = appContext))
        }
    }
}