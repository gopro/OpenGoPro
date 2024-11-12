package domain.connector

import domain.data.ICameraRepository
import entity.connector.ConnectionDescriptor
import entity.connector.NetworkType
import entity.connector.ScanResult
import kotlinx.coroutines.flow.Flow

sealed interface ConnectionRequestContext {
    data class Wifi(val password: String) : ConnectionRequestContext
}

interface IConnector<S : ScanResult, C : ConnectionDescriptor> {
    val networkType: NetworkType
    val cameraRepo: ICameraRepository
    suspend fun scan(): Result<Flow<S>>
    suspend fun connect(target: S, request: ConnectionRequestContext? = null): Result<C>
    suspend fun disconnect(connection: C): Result<Unit>
    // TODO register listeners here?
}