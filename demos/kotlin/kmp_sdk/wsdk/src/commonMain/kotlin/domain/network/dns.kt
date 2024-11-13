package domain.network

import entity.connector.ConnectionDescriptor
import entity.network.HttpsCredentials
import kotlinx.coroutines.flow.Flow

data class DnsScanResult(
    val ipAddress: String,
    val serviceName: String
)

interface IDnsApi {
    suspend fun scan(serviceType: String): Result<Flow<domain.network.DnsScanResult>>
}