package di

import com.gopro.open_gopro.OgpSdkAppContext
import androidx.datastore.core.DataStore
import androidx.datastore.preferences.core.Preferences
import data.dataStore
import org.koin.core.module.Module
import org.koin.dsl.module

actual fun buildPlatformModules(appContext: OgpSdkAppContext): Module = module {
    single<DataStore<Preferences>> { dataStore() }
}
