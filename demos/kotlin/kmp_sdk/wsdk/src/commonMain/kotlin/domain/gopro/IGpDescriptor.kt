package domain.gopro

import entity.communicator.CommunicationType
import entity.network.IHttpsCredentials
import entity.operation.AccessPointState
import entity.operation.CohnState
import kotlinx.coroutines.flow.StateFlow

interface IGpDescriptor {
    val serialId: String

    val isBusy: StateFlow<Boolean>
    val isEncoding: StateFlow<Boolean>
    val isReady: StateFlow<Boolean>

    val accessPointState: StateFlow<AccessPointState>
    val cohnState: StateFlow<CohnState>

    val communicators: List<CommunicationType>
}

internal interface GpDescriptorManager {
    fun getDescriptor(): IGpDescriptor
    fun setAccessPointState(state: AccessPointState)
    fun setCohnState(state: CohnState)
}