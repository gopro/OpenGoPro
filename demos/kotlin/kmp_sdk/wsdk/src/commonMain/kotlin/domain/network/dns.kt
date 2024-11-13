package domain.network

import entity.connector.ConnectionDescriptor
import entity.network.HttpsCredentials
import kotlinx.coroutines.flow.Flow

internal data class DnsScanResult(
    val ipAddress: String,
    val serviceName: String
)

internal interface IDnsApi {
    suspend fun scan(serviceType: String): Result<Flow<domain.network.DnsScanResult>>
}