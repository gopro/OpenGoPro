package domain.network

import kotlinx.coroutines.flow.Flow

internal data class DnsScanResult(
    val ipAddress: String,
    val serviceName: String
)

internal interface IDnsApi {
    suspend fun scan(serviceType: String): Result<Flow<DnsScanResult>>
}