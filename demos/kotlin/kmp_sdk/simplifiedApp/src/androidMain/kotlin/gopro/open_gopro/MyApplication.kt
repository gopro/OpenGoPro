package gopro.open_gopro

import AppContext
import android.app.Application

class MyApplication : Application() {
    override fun onCreate() {
        super.onCreate()
        AppContext.set(applicationContext)
    }
}