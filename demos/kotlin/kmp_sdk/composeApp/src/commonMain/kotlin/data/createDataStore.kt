package data

import androidx.datastore.core.DataStore
import androidx.datastore.preferences.core.PreferenceDataStoreFactory
import androidx.datastore.preferences.core.Preferences
import okio.Path.Companion.toPath

// https://medium.com/arconsis/jetpack-preferences-datastore-in-kotlin-multiplatform-mobile-kmm-6bf046772217
// https://funkymuse.dev/posts/create-data-store-kmp/

/**
 * Gets the singleton DataStore instance, creating it if necessary.
 */
fun createDataStore(
    producePath: () -> String,
): DataStore<Preferences> = PreferenceDataStoreFactory.createWithPath(
    corruptionHandler = null,
    migrations = emptyList(),
    produceFile = { producePath().toPath() },
)

internal const val dataStoreFileName = "open_gopro.preferences_pb"
