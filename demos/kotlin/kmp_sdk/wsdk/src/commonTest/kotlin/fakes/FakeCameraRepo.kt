package fakes

import domain.data.ICameraRepository
import domain.data.WifiCredentials
import entity.network.HttpsCredentials
import entity.network.IHttpsCredentials

class FakeCameraRepo : ICameraRepository {
    override suspend fun addHttpsCredentials(serialId: String, credentials: IHttpsCredentials) {

    }

    override suspend fun getHttpsCredentials(serialId: String): Result<IHttpsCredentials> {
        return Result.success(
            HttpsCredentials(
                certificates = listOf("certificate1"),
                password = "password",
                username = "username"
            )
        )
    }

    override suspend fun removeHttpsCredentials(serialId: String) {

    }

    override suspend fun addWifiCredentials(serialId: String, ssid: String, password: String) {
        TODO("Not yet implemented")
    }

    override suspend fun getWifiCredentials(serialId: String): Result<WifiCredentials> {
        TODO("Not yet implemented")
    }

    override suspend fun removeWifiCredentials(serialId: String) {
        TODO("Not yet implemented")
    }
}