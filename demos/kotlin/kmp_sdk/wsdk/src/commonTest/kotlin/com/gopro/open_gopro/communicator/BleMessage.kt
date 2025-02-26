/* BleMessage.kt/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Tue Feb 18 18:41:30 UTC 2025 */

package com.gopro.open_gopro.communicator

import com.gopro.open_gopro.domain.communicator.BleCommunicator
import com.gopro.open_gopro.domain.communicator.bleCommunicator.AccumulatedGpBleResponse
import com.gopro.open_gopro.domain.communicator.bleCommunicator.bleFragment
import com.gopro.open_gopro.entity.network.ble.GpUuid
import com.gopro.open_gopro.util.extensions.toUByteArray
import kotlin.test.Test
import kotlin.test.assertEquals
import kotlin.test.assertFalse
import kotlin.test.assertTrue
import vectors.complexBleWriteResponse
import vectors.hardwareInfoResponsePayload
import vectors.setShutterRequestMessage
import vectors.setShutterRequestPayload
import vectors.setShutterResponseMessage

@OptIn(ExperimentalUnsignedTypes::class)
class TestBleMessage {
  @Test
  fun `accumulate single packet BLE message`() {
    // GIVEN
    val message = AccumulatedGpBleResponse(GpUuid.CQ_COMMAND)

    // WHEN
    message.accumulate(setShutterResponseMessage)

    // THEN
    assertTrue { message.isReceived }
    assertTrue { message.payload.contentEquals(ubyteArrayOf(1U, 0U)) }
    assertTrue { message.rawBytes.contentEquals(setShutterResponseMessage) }
  }

  @Test
  fun `accumulate multi packet BLE message`() {
    // GIVEN
    val message = AccumulatedGpBleResponse(GpUuid.CQ_COMMAND)

    // WHEN
    complexBleWriteResponse.chunked(BleCommunicator.MAX_PACKET_LENGTH).let { chunked ->
      chunked.forEach { chunk ->
        message.accumulate(chunk.toUByteArray())
        if (chunked.indexOf(chunk) < chunked.lastIndex) {
          assertFalse { message.isReceived }
        }
      }
    }

    // THEN
    assertTrue { message.isReceived }
    assertEquals(message.payload.size, 370)
  }

  @Test
  fun `fragment single 13 bit length message`() {
    // GIVEN
    val payload = setShutterRequestPayload

    // WHEN
    val packets = payload.bleFragment(BleCommunicator.MAX_PACKET_LENGTH).asSequence().toList()

    // THEN
    assertEquals(packets.size, 1)
    assertTrue { packets.first().contentEquals(setShutterRequestMessage) }
  }

  @Test
  fun `fragment multiple 13 bit length message`() {
    // GIVEN
    val payload = (0..1023).toList().toUByteArray() // 2^10 - 1

    // WHEN
    val packets = payload.bleFragment(BleCommunicator.MAX_PACKET_LENGTH).asSequence().toList()

    // THEN
    assertEquals(packets.size, 54)
    assertTrue {
      packets
          .first()
          .take(5)
          .toUByteArray()
          .contentEquals(ubyteArrayOf(0x024U, 0x00U, 0x00U, 0x01U, 0x02U))
    }
    // Ensure continuation is set on all but first packet
    packets.drop(1).forEach { assertEquals(0x80U, it.first().and(0x80U)) }
  }

  @Test
  fun `fragment 16 bit length message`() {
    // GIVEN
    val payload = (0..16383).toList().toUByteArray() // 2^14 - 1

    // WHEN
    val packets = payload.bleFragment(BleCommunicator.MAX_PACKET_LENGTH).asSequence().toList()

    // THEN
    assertEquals(packets.size, 863)
    assertTrue {
      packets
          .first()
          .take(6)
          .toUByteArray()
          .contentEquals(ubyteArrayOf(0x40U, 0x40U, 0x00U, 0x00U, 0x01U, 0x02U))
    }
  }

  @Test
  fun `accumulate get hardware info`() {
    // GIVEN
    val message = AccumulatedGpBleResponse(GpUuid.CQ_COMMAND_RESP)

    // WHEN
    hardwareInfoResponsePayload
        .bleFragment(BleCommunicator.MAX_PACKET_LENGTH)
        .asSequence()
        .forEach { message.accumulate(it) }

    // THEN
    assertTrue { message.isReceived }
  }
}
