package fakes

import domain.data.ICameraRepository
import domain.data.WifiCredentials
import entity.connector.GoProId
import entity.network.HttpsCredentials
import entity.network.IHttpsCredentials

internal class FakeCameraRepo : ICameraRepository {
    override suspend fun addHttpsCredentials(id: GoProId, credentials: IHttpsCredentials) {

    }

    override suspend fun getHttpsCredentials(id: GoProId): Result<IHttpsCredentials> {
        return Result.success(
            HttpsCredentials(
                certificates = listOf("certificate1"),
                password = "password",
                username = "username"
            )
        )
    }

    override suspend fun removeHttpsCredentials(id: GoProId) {

    }

    override suspend fun addWifiCredentials(id: GoProId, ssid: String, password: String) {
        TODO("Not yet implemented")
    }

    override suspend fun getWifiCredentials(id: GoProId): Result<WifiCredentials> {
        TODO("Not yet implemented")
    }

    override suspend fun removeWifiCredentials(id: GoProId) {
        TODO("Not yet implemented")
    }
}