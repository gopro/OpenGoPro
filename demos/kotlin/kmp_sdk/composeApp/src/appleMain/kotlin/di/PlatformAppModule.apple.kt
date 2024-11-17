package di

import WsdkAppContext
import androidx.datastore.core.DataStore
import androidx.datastore.preferences.core.Preferences
import data.dataStore
import org.koin.core.module.Module
import org.koin.dsl.module

actual fun buildPlatformModules(appContext: WsdkAppContext): Module = module {
    single<DataStore<Preferences>> { dataStore() }
}
