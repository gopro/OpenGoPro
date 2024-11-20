package domain.gopro

import entity.communicator.CommunicationType
import entity.connector.GoProId
import entity.operation.AccessPointState
import entity.operation.CohnState
import kotlinx.coroutines.flow.StateFlow

/**
 * Properties of a connectd GoPro
 */
interface IGpDescriptor {
    /**
     * Identifier of connected GoPro
     */
    val id: GoProId

    /**
     * Is the camera busy performing an operation?
     *
     * @see [Busy Status](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#busy-8)
     */
    val isBusy: StateFlow<Boolean>

    /**
     * Is the camera currently encoding?
     *
     * @see [Encoding Status](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#encoding-10)
     */
    val isEncoding: StateFlow<Boolean>

    /**
     * Is the camera ready to communicate?
     *
     * That is, is both [isBusy] and [isEncoding] are false
     *
     * @see [Camera Readiness](https://gopro.github.io/OpenGoPro/ble/protocol/state_management.html#camera-readiness)
     */
    val isReady: StateFlow<Boolean>

    /**
     * State of the camera connecting to an Access Point
     *
     * That is, the camera will be operating in STA mode.
     *
     * @see [gopro.features.AccessPointFeature]
     */
    val accessPointState: StateFlow<AccessPointState>

    /**
     * State of COHN provisioning
     *
     * @see [gopro.features.CohnFeature]
     */
    val cohnState: StateFlow<CohnState>

    /**
     * List of currently available communicators by [CommunicationType]
     */
    val communicators: List<CommunicationType>

    /**
     * IP Address of connected device. Null if not HTTP connection is available.
     */
    val ipAddress: String?
}

internal interface GpDescriptorManager {
    fun getDescriptor(): IGpDescriptor
    fun setAccessPointState(state: AccessPointState)
    fun setCohnState(state: CohnState)
}