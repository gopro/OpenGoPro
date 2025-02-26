/* PlatformAppModule.apple.kt/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Tue Feb 18 18:41:27 UTC 2025 */

package di

import androidx.datastore.core.DataStore
import androidx.datastore.preferences.core.Preferences
import com.gopro.open_gopro.OgpSdkAppContext
import data.dataStore
import org.koin.core.module.Module
import org.koin.dsl.module

actual fun buildPlatformModules(appContext: OgpSdkAppContext): Module = module {
  single<DataStore<Preferences>> { dataStore() }
}
