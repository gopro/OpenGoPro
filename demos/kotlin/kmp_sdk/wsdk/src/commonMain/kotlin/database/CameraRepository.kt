package database

import co.touchlab.kermit.Logger
import domain.data.ICameraRepository
import domain.data.WifiCredentials
import entity.network.HttpsCredentials
import entity.network.IHttpsCredentials
import entity.operation.jsonDefault
import kotlinx.serialization.encodeToString

private val logger = Logger.withTag("CameraRepository")

internal class CameraRepository(appDatabase: AppDatabase) : ICameraRepository {
    private val certificatesDao = appDatabase.certificatesDao()
    private val httpsCredentialsDao = appDatabase.httpsCredentialsDao()
    private val ssidDao = appDatabase.ssidDao()

    override suspend fun addHttpsCredentials(serialId: String, credentials: IHttpsCredentials) {
        certificatesDao.insert(
            CertificatesDbEntry(
                serialId = serialId,
                certificates = jsonDefault.encodeToString(CertificatesForDb(credentials.certificates))
            )
        )
        httpsCredentialsDao.insert(
            HttpsCredentialsDbEntry(
                serialId = serialId,
                username = credentials.username,
                password = credentials.password
            )
        )
    }

    override suspend fun getHttpsCredentials(serialId: String): Result<IHttpsCredentials> {
        // TODO handle errors
        val certificates = jsonDefault.decodeFromString<CertificatesForDb>(
            certificatesDao.loadAll(serialId).first().certificates
        ).certificates.onEach { logger.d(it) }
        val credentials = httpsCredentialsDao.loadAll(serialId).first().also {
            logger.d(it.toString())
        }
        return Result.success(
            HttpsCredentials(
                username = credentials.username,
                password = credentials.password,
                certificates = certificates
            )
        )
    }

    override suspend fun removeHttpsCredentials(serialId: String) {
        certificatesDao.delete(SerialIdDb(serialId))
        httpsCredentialsDao.delete(SerialIdDb(serialId))
    }

    override suspend fun addWifiCredentials(serialId: String, ssid: String, password: String) {
        ssidDao.insert(SsidDbEntry(serialId, ssid, password))
    }

    override suspend fun getWifiCredentials(serialId: String): Result<WifiCredentials> =
        ssidDao.loadAll(serialId).first().let {
            Result.success(
                WifiCredentials(it.ssid, it.password)
            )
        }

    override suspend fun removeWifiCredentials(serialId: String) {
        ssidDao.delete(SerialIdDb(serialId))
    }
}