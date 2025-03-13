/* Preferences.kt/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Tue Feb 18 18:41:27 UTC 2025 */

package data

import androidx.datastore.core.DataStore
import androidx.datastore.preferences.core.Preferences
import androidx.datastore.preferences.core.edit
import androidx.datastore.preferences.core.stringPreferencesKey
import com.gopro.open_gopro.GoProId
import kotlinx.coroutines.flow.first
import kotlinx.coroutines.flow.map

interface IAppPreferences {
  suspend fun getConnectedDevice(): GoProId?

  suspend fun setConnectedDevice(id: GoProId): Preferences
}

class IAppPreferencesImpl(
    private val dataStore: DataStore<Preferences>,
) : IAppPreferences {

  private companion object {
    private const val PREFS_TAG_KEY = "IAppPreferences"
    private const val CONNECTED_DEVICE = "connectedDevice"
  }

  private val connectedDeviceKey = stringPreferencesKey("$PREFS_TAG_KEY$CONNECTED_DEVICE")

  override suspend fun getConnectedDevice(): GoProId? =
      dataStore.data.map { it[connectedDeviceKey] }.first()?.let { id -> GoProId(id) }

  override suspend fun setConnectedDevice(id: GoProId) =
      dataStore.edit { it[connectedDeviceKey] = id.partialSerial }
}
