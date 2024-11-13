package domain.data

import entity.network.IHttpsCredentials

internal data class WifiCredentials(
    val ssid: String,
    val password: String
)

internal interface ICameraRepository {
    suspend fun addHttpsCredentials(serialId: String, credentials: IHttpsCredentials)
    suspend fun getHttpsCredentials(serialId: String): Result<IHttpsCredentials>
    suspend fun removeHttpsCredentials(serialId: String)

    suspend fun addWifiCredentials(serialId: String, ssid: String, password: String)
    suspend fun getWifiCredentials(serialId: String): Result<WifiCredentials>
    suspend fun removeWifiCredentials(serialId: String)
}