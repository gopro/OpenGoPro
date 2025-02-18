package fakes

import com.gopro.open_gopro.domain.communicator.BleCommunicator
import com.gopro.open_gopro.domain.communicator.bleCommunicator.AccumulatedGpBleResponse
import com.gopro.open_gopro.domain.communicator.bleCommunicator.bleFragment
import com.gopro.open_gopro.entity.network.ble.GpUuid
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