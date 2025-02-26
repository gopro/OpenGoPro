/* GpBleResponse.kt/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Tue Feb 18 18:41:29 UTC 2025 */

package com.gopro.open_gopro.domain.communicator.bleCommunicator

import com.gopro.open_gopro.entity.network.ble.GpUuid
import com.gopro.open_gopro.util.extensions.pow

internal enum class GpBleMessageHeaderMask(val value: UByte) {
  Header(0b01100000U),
  Continuation(0b10000000U),
  GenLength(0b00011111U),
  ExtByte0(0b00011111U),
}

internal enum class GpBleMessageHeader(val value: UByte) {
  GENERAL(0b00U),
  EXT_13(0b01U),
  EXT_16(0b10U),
  RESERVED(0b11U);

  companion object {
    private val valueMap: Map<UByte, GpBleMessageHeader> by lazy {
      entries.associateBy { it.value }
    }

    fun fromValue(value: Int) = valueMap.getValue(value.toUByte())
  }
}

@OptIn(ExperimentalUnsignedTypes::class)
internal sealed interface GpBleMessageState {
  fun accumulate(data: UByteArray)

  data class Idle(private val message: AccumulatedGpBleResponse) : GpBleMessageState {
    override fun accumulate(data: UByteArray) {
      var buf = data
      if (data.first().and(GpBleMessageHeaderMask.Continuation.value) ==
          GpBleMessageHeaderMask.Continuation.value) {
        throw Exception("Received continuation packet in Idle state.")
      }
      var bytesRemaining = 0
      when (GpBleMessageHeader.fromValue(
          (buf.first() and GpBleMessageHeaderMask.Header.value).toInt() shr 5)) {
        GpBleMessageHeader.GENERAL -> {
          bytesRemaining = buf[0].and(GpBleMessageHeaderMask.GenLength.value).toInt()
          buf = buf.drop(1).toUByteArray()
        }

        GpBleMessageHeader.EXT_13 -> {
          bytesRemaining =
              ((buf[0].and(GpBleMessageHeaderMask.ExtByte0.value).toLong() shl 8) or
                      buf[1].toLong())
                  .toInt()
          buf = buf.drop(2).toUByteArray()
        }

        GpBleMessageHeader.EXT_16 -> {
          bytesRemaining = ((buf[1].toLong() shl 8) or buf[2].toLong()).toInt()
          buf = buf.drop(3).toUByteArray()
        }

        GpBleMessageHeader.RESERVED -> {
          throw Exception("Unexpected RESERVED header")
        }
      }
      bytesRemaining -= buf.size
      if (bytesRemaining == 0) {
        message.changeState(Received(message, buf, data))
      } else {
        message.changeState(Accumulating(message, buf, data, bytesRemaining))
      }
    }
  }

  data class Accumulating(
      private val message: AccumulatedGpBleResponse,
      private var payload: UByteArray,
      private var rawBytes: UByteArray,
      private var bytesRemaining: Int
  ) : GpBleMessageState {
    override fun accumulate(data: UByteArray) {
      rawBytes += data
      if (data.first().and(GpBleMessageHeaderMask.Continuation.value) !=
          GpBleMessageHeaderMask.Continuation.value) {
        throw Exception("Received start packet in accumulation state")
      }
      // Pop the header byte
      data.drop(1).toUByteArray().let {
        payload += it
        bytesRemaining -= it.size
      }
      if (bytesRemaining == 0) {
        message.changeState(Received(message, payload, rawBytes))
      }
    }
  }

  data class Received(
      private val message: AccumulatedGpBleResponse,
      val payload: UByteArray,
      val rawBytes: UByteArray
  ) : GpBleMessageState {
    override fun accumulate(data: UByteArray) {
      throw Exception("Attempted to accumulate an already received packet.")
    }
  }
}

@OptIn(ExperimentalUnsignedTypes::class)
internal interface IGpBleResponse {
  val uuid: GpUuid
  val payload: UByteArray
  val id: ResponseId
}

@OptIn(ExperimentalUnsignedTypes::class)
internal class AccumulatedGpBleResponse(override val uuid: GpUuid) : IGpBleResponse {
  private var state: GpBleMessageState = GpBleMessageState.Idle(this)

  internal fun changeState(state: GpBleMessageState) {
    this.state = state
  }

  val isReceived
    get() = state is GpBleMessageState.Received

  override val id: ResponseId by lazy {
    state.let {
      when (it) {
        is GpBleMessageState.Received -> decipherResponse(this)
        else -> throw Exception("Message is not yet received.")
      }
    }
  }
  val rawBytes: UByteArray
    get() =
        state.let {
          when (it) {
            is GpBleMessageState.Received -> it.rawBytes
            else -> throw Exception("Message is not yet received.")
          }
        }

  override val payload: UByteArray
    get() =
        state.let {
          when (it) {
            is GpBleMessageState.Received -> it.payload
            else -> throw Exception("Message is not yet received.")
          }
        }

  fun accumulate(data: UByteArray) {
    state.accumulate(data)
  }
}

@OptIn(ExperimentalUnsignedTypes::class)
internal fun UByteArray.bleFragment(packetSize: Int): Iterator<UByteArray> {
  val data = this
  return iterator {
    var header: UByteArray =
        if (data.size < (2.pow(13) - 1)) {
          val byte0 = data.size.toLong().and(0xFFL).toUByte()
          val byte1 =
              GpBleMessageHeader.EXT_13.value
                  .toLong()
                  .shl(5)
                  .or(
                      data.size
                          .toLong()
                          .and(GpBleMessageHeaderMask.ExtByte0.value.toLong().shl(8))
                          .shr(8))
                  .toUByte()
          ubyteArrayOf(byte1, byte0)
        } else if (data.size < (2.pow(16) - 1)) {
          val byte0 = data.size.toLong().and(0x0000FFL).toUByte()
          val byte1 = (data.size.toLong().and(0x00FF00L).shr(8)).toUByte()
          val byte2 =
              GpBleMessageHeader.EXT_16.value
                  .toLong()
                  .shl(5)
                  .or(
                      data.size
                          .toLong()
                          .and(GpBleMessageHeaderMask.ExtByte0.value.toLong().shl(16))
                          .shr(16))
                  .toUByte()
          ubyteArrayOf(byte2, byte1, byte0)
        } else {
          throw Exception("Protocol does not support messages larger than 2^16 -1 bytes.")
        }

    var buf = data
    while (buf.isNotEmpty()) {
      val payloadSize = kotlin.math.min(packetSize - header.size, buf.size)
      yield(header + buf.take(payloadSize))
      buf = buf.drop(payloadSize).toUByteArray()
      header = ubyteArrayOf(0x80U) // Continuation for all but the first packet
    }
  }
}
