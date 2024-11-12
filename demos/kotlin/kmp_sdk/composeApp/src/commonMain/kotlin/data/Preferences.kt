package data

import androidx.datastore.core.DataStore
import androidx.datastore.preferences.core.Preferences
import androidx.datastore.preferences.core.edit
import androidx.datastore.preferences.core.stringPreferencesKey
import kotlinx.coroutines.flow.first
import kotlinx.coroutines.flow.map

interface IAppPreferences {
    suspend fun getConnectedDevice(): String?
    suspend fun setConnectedDevice(deviceId: String): Preferences
}

class IAppPreferencesImpl(
    private val dataStore: DataStore<Preferences>,
) : IAppPreferences {

    private companion object {
        private const val PREFS_TAG_KEY = "IAppPreferences"
        private const val CONNECTED_DEVICE = "connectedDevice"
    }

    private val connectedDeviceKey = stringPreferencesKey("$PREFS_TAG_KEY$CONNECTED_DEVICE")

    override suspend fun getConnectedDevice() =
        dataStore.data.map { it[connectedDeviceKey] }.first()

    override suspend fun setConnectedDevice(deviceId: String) =
        dataStore.edit { it[connectedDeviceKey] = deviceId }
}