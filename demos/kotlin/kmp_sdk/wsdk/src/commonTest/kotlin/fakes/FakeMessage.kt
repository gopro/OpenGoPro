package fakes

import domain.communicator.BleCommunicator
import domain.communicator.bleCommunicator.AccumulatedGpBleResponse
import domain.communicator.bleCommunicator.bleFragment
import entity.network.ble.GpUuid
import kotlin.test.assertTrue

@OptIn(ExperimentalUnsignedTypes::class)
internal fun buildResponse(uuid: GpUuid, payload: UByteArray): AccumulatedGpBleResponse {
    val response = AccumulatedGpBleResponse(uuid).also { response ->
        payload.bleFragment(BleCommunicator.MAX_PACKET_LENGTH).forEach {
            response.accumulate(it)
        }
    }
    assertTrue { response.isReceived }
    return response
}