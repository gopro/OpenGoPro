/* CameraRepository.kt/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Tue Feb 18 18:41:29 UTC 2025 */

package com.gopro.open_gopro.database

import co.touchlab.kermit.Logger
import com.gopro.open_gopro.GoProId
import com.gopro.open_gopro.domain.data.ICameraRepository
import com.gopro.open_gopro.domain.data.WifiCredentials
import com.gopro.open_gopro.entity.network.HttpsCredentials
import com.gopro.open_gopro.entity.network.IHttpsCredentials
import com.gopro.open_gopro.operations.jsonDefault
import kotlinx.serialization.encodeToString

private val logger = Logger.withTag("CameraRepository")

internal class CameraRepository(appDatabase: AppDatabase) : ICameraRepository {
  private val certificatesDao = appDatabase.certificatesDao()
  private val httpsCredentialsDao = appDatabase.httpsCredentialsDao()
  private val ssidDao = appDatabase.ssidDao()

  override suspend fun addHttpsCredentials(id: GoProId, credentials: IHttpsCredentials) {
    certificatesDao.insert(
        CertificatesDbEntry(
            serialId = id.partialSerial,
            certificates = jsonDefault.encodeToString(CertificatesForDb(credentials.certificates))))
    httpsCredentialsDao.insert(
        HttpsCredentialsDbEntry(
            serialId = id.partialSerial,
            username = credentials.username,
            password = credentials.password))
  }

  override suspend fun getHttpsCredentials(id: GoProId): Result<IHttpsCredentials> {
    val certificates =
        jsonDefault
            .decodeFromString<CertificatesForDb>(
                certificatesDao.loadAll(id.partialSerial).first().certificates)
            .certificates
            .onEach { logger.d(it) }
    val credentials =
        httpsCredentialsDao.loadAll(id.partialSerial).first().also { logger.d(it.toString()) }
    return Result.success(
        HttpsCredentials(
            username = credentials.username,
            password = credentials.password,
            certificates = certificates))
  }

  override suspend fun removeHttpsCredentials(id: GoProId) {
    certificatesDao.delete(SerialIdDb(id.partialSerial))
    httpsCredentialsDao.delete(SerialIdDb(id.partialSerial))
  }

  override suspend fun addWifiCredentials(id: GoProId, ssid: String, password: String) {
    ssidDao.insert(SsidDbEntry(id.partialSerial, ssid, password))
  }

  override suspend fun getWifiCredentials(id: GoProId): Result<WifiCredentials> =
      ssidDao.loadAll(id.partialSerial).first().let {
        Result.success(WifiCredentials(it.ssid, it.password))
      }

  override suspend fun removeWifiCredentials(id: GoProId) {
    ssidDao.delete(SerialIdDb(id.partialSerial))
  }
}
