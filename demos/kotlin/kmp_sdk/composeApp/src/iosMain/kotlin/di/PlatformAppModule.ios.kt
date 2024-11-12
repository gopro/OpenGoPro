package di

import androidx.datastore.core.DataStore
import androidx.datastore.preferences.core.Preferences
import data.dataStore
import org.koin.dsl.module

actual val platformModule = object : PlatformModule {

    override val module = module {
        single<DataStore<Preferences>> { dataStore() }
    }
}