package domain.gopro

import entity.communicator.CommunicationType
import entity.network.IHttpsCredentials
import entity.operation.AccessPointState
import kotlinx.coroutines.flow.StateFlow

sealed class CohnState {

    data object Unprovisioned : CohnState() {
        override fun toString(): String = "Unprovisioned"
    }

    data class Provisioned(
        override val username: String,
        override val password: String,
        val ipAddress: String,
        override val certificates: List<String>
    ) : CohnState(), IHttpsCredentials {
        override fun toString(): String = "Provisioned"
    }
}

interface IGpDescriptor {
    val serialId: String

    val isBusy: StateFlow<Boolean>
    val isEncoding: StateFlow<Boolean>
    val isReady: StateFlow<Boolean>

    val accessPointState: StateFlow<AccessPointState>
    val cohnState: StateFlow<CohnState>

    val communicators: List<CommunicationType>
}

interface GpDescriptorManager {
    fun getDescriptor(): IGpDescriptor
    fun setAccessPointState(state: AccessPointState)
    fun setCohnState(state: CohnState)
}