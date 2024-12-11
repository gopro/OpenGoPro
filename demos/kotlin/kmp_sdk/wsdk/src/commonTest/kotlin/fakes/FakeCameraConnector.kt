package fakes

import com.gopro.open_gopro.domain.connector.ICameraConnector
import com.gopro.open_gopro.entity.connector.ConnectionDescriptor
import com.gopro.open_gopro.entity.connector.ConnectionRequestContext
import com.gopro.open_gopro.entity.connector.NetworkType
import com.gopro.open_gopro.entity.connector.ScanResult
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