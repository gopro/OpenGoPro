package fakes

import com.gopro.open_gopro.domain.data.ICameraRepository
import com.gopro.open_gopro.domain.data.WifiCredentials
import com.gopro.open_gopro.entity.connector.GoProId
import com.gopro.open_gopro.entity.network.HttpsCredentials
import com.gopro.open_gopro.entity.network.IHttpsCredentials

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