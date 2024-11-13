package domain.network

import kotlinx.coroutines.CoroutineDispatcher
import kotlinx.coroutines.flow.Flow

interface IWifiApi {
    val dispatcher: CoroutineDispatcher
    suspend fun setup()
    suspend fun scanForSsid(): Result<Flow<String>>
    suspend fun connect(ssid: String, password: String): Result<Unit>
    suspend fun disconnect(ssid: String): Result<Unit>
    fun receiveDisconnects(): Flow<String>
}