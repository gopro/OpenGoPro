/* FakeMessage.kt/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Tue Feb 18 18:41:30 UTC 2025 */

package fakes

import com.gopro.open_gopro.domain.communicator.BleCommunicator
import com.gopro.open_gopro.domain.communicator.bleCommunicator.AccumulatedGpBleResponse
import com.gopro.open_gopro.domain.communicator.bleCommunicator.bleFragment
import com.gopro.open_gopro.entity.network.ble.GpUuid
import kotlin.test.assertTrue

@OptIn(ExperimentalUnsignedTypes::class)
internal fun buildResponse(uuid: GpUuid, payload: UByteArray): AccumulatedGpBleResponse {
  val response =
      AccumulatedGpBleResponse(uuid).also { response ->
        payload.bleFragment(BleCommunicator.MAX_PACKET_LENGTH).forEach { response.accumulate(it) }
      }
  assertTrue { response.isReceived }
  return response
}
