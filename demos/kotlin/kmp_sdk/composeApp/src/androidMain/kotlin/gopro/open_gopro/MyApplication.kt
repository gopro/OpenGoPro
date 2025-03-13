/* MyApplication.kt/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Tue Feb 18 18:41:28 UTC 2025 */

package gopro.open_gopro

import android.app.Application
import com.gopro.open_gopro.OgpSdkAppContext
import di.buildAppModule
import org.koin.android.ext.koin.androidLogger
import org.koin.core.context.startKoin
import org.koin.core.logger.Level

class MyApplication : Application() {
  // TODO try
  // https://insert-koin.io/docs/reference/koin-android/start#start-koin-with-androidx-startup-401

  override fun onCreate() {
    super.onCreate()
    val appContext = OgpSdkAppContext().apply { set(applicationContext) }
    startKoin {
      androidLogger(Level.WARNING)
      modules(buildAppModule(appContext = appContext))
    }
  }
}
