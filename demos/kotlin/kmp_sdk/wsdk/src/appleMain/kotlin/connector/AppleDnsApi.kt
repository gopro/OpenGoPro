package connector

import co.touchlab.kermit.Logger
import domain.network.DnsScanResult
import domain.network.IDnsApi
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