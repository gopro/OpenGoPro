package com.gopro.open_gopro.connector

import co.touchlab.kermit.Logger
import com.gopro.open_gopro.domain.network.DnsScanResult
import com.gopro.open_gopro.domain.network.IDnsApi
import kotlinx.coroutines.CoroutineDispatcher
import kotlinx.coroutines.flow.Flow

private val logger = Logger.withTag("AndroidDnsApi")

internal class AppleDnsApi(
    dispatcher: CoroutineDispatcher
) : IDnsApi {
    override suspend fun scan(serviceType: String): Result<Flow<DnsScanResult>> {
        TODO("Not yet implemented")
    }
}