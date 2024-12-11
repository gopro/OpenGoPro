package com.gopro.open_gopro.domain.data

import com.gopro.open_gopro.GoProId
import com.gopro.open_gopro.entity.network.IHttpsCredentials

internal data class WifiCredentials(
    val ssid: String,
    val password: String
)

internal interface ICameraRepository {
    suspend fun addHttpsCredentials(id: GoProId, credentials: IHttpsCredentials)
    suspend fun getHttpsCredentials(id: GoProId): Result<IHttpsCredentials>
    suspend fun removeHttpsCredentials(id: GoProId)

    suspend fun addWifiCredentials(id: GoProId, ssid: String, password: String)
    suspend fun getWifiCredentials(id: GoProId): Result<WifiCredentials>
    suspend fun removeWifiCredentials(id: GoProId)
}