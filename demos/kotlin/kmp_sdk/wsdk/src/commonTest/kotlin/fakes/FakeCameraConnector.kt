package fakes

import domain.connector.ICameraConnector
import entity.connector.ConnectionDescriptor
import entity.connector.ConnectionRequestContext
import entity.connector.GoProId
import entity.connector.NetworkType
import entity.connector.ScanResult
import kotlinx.coroutines.flow.Flow

internal class FakeCameraConnector : ICameraConnector {
    override suspend fun discover(vararg networkTypes: NetworkType): Flow<ScanResult> {
        TODO("Not yet implemented")
    }

    override suspend fun connect(
        target: ScanResult,
        connectionRequestContext: ConnectionRequestContext?
    ): Result<ConnectionDescriptor> {
        TODO("Not yet implemented")
    }
}