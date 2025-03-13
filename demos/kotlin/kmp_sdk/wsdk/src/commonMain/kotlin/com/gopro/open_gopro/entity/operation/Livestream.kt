/* Livestream.kt/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Tue Feb 18 18:41:29 UTC 2025 */

package com.gopro.open_gopro.operations

import kotlinx.serialization.SerialName
import kotlinx.serialization.Serializable

enum class LivestreamResolution(val value: Int) {
  RES_480(4),
  RES_720(7),
  RES_1080(12);

  companion object {
    fun fromValue(value: Int) = LivestreamResolution.entries.first { it.value == value }
  }
}

enum class LivestreamFov(val value: Int) {
  WIDE(0),
  SUPERVIEW(3),
  LINEAR(4);

  companion object {
    fun fromValue(value: Int) = LivestreamFov.entries.first { it.value == value }
  }
}

enum class LivestreamError(val value: Int) {
  NONE(0),
  NETWORK(1),
  CREATESTREAM(2),
  OUTOFMEMORY(3),
  INPUTSTREAM(4),
  INTERNET(5),
  OSNETWORK(6),
  SELECTEDNETWORKTIMEOUT(7),
  SSL_HANDSHAKE(8),
  CAMERA_BLOCKED(9),
  UNKNOWN(10),
  SD_CARD_FULL(40),
  SD_CARD_REMOVED(41);

  companion object {
    fun fromValue(value: Int?): LivestreamError? =
        LivestreamError.entries.firstOrNull { it.value == value }
  }
}

fun LivestreamError.isOk(): Boolean =
    when (this) {
      LivestreamError.NONE -> true

      LivestreamError.UNKNOWN,
      LivestreamError.NETWORK,
      LivestreamError.CREATESTREAM,
      LivestreamError.OUTOFMEMORY,
      LivestreamError.INPUTSTREAM,
      LivestreamError.INTERNET,
      LivestreamError.OSNETWORK,
      LivestreamError.SELECTEDNETWORKTIMEOUT,
      LivestreamError.SSL_HANDSHAKE,
      LivestreamError.CAMERA_BLOCKED,
      LivestreamError.SD_CARD_FULL,
      LivestreamError.SD_CARD_REMOVED -> false
    }

enum class LivestreamState(val value: Int) {
  IDLE(0),
  CONFIG(1),
  READY(2),
  STREAMING(3),
  COMPLETE_STAY_ON(4),
  FAILED_STAY_ON(5),
  RECONNECTING(6),
  UNAVAILABLE(7);

  companion object {
    fun fromValue(value: Int?): LivestreamState? =
        LivestreamState.entries.firstOrNull { it.value == value }
  }
}

fun LivestreamState.isOk(): Boolean =
    when (this) {
      LivestreamState.IDLE,
      LivestreamState.CONFIG,
      LivestreamState.READY,
      LivestreamState.STREAMING,
      LivestreamState.COMPLETE_STAY_ON,
      LivestreamState.RECONNECTING -> true

      LivestreamState.FAILED_STAY_ON,
      LivestreamState.UNAVAILABLE -> false
    }

@Serializable
data class LivestreamConfigurationRequest(
    val url: String,
    @SerialName("encode") val shouldEncode: Boolean? = null,
    @SerialName("window_size") val resolution: LivestreamResolution? = null,
    @SerialName("minimum_bitrate") val minimumBitrate: Int? = null,
    @SerialName("maximum_bitrate") val maximumBitrate: Int? = null,
    @SerialName("starting_bitrate") val startingBitRate: Int? = null,
    @SerialName("lens") val fov: LivestreamFov? = null,
    @SerialName("cert") val certificate: ByteArray? = null
)

@Serializable
data class LivestreamStatus(
    @SerialName("liveStreamError") val error: LivestreamError?,
    @SerialName("liveStreamStatus") val status: LivestreamState?,
    @SerialName("liveStreamBitrate") val bitRate: Int?,
    @SerialName("liveStreamMaximumStreamBitrate") val maxBitrate: Int?,
    @SerialName("liveStreamMinimumStreamBitrate") val minBitrate: Int?,
    @SerialName("liveStreamEncodeSupported") val isEncodingSupported: Boolean?,
    @SerialName("liveStreamEncode") val isEncoding: Boolean?,
    @SerialName("live_stream_lens_supported") val isLensSupported: Boolean?,
    @SerialName("liveStreamMaxLensUnsupported") val isMaxLensSupported: Boolean?,
    @SerialName("liveStreamLensSupportedArray") val supportedFov: List<LivestreamFov>,
    @SerialName("liveStreamWindowSizeSupportedArray")
    val supportedResolution: List<LivestreamResolution>,
    @SerialName("liveStreamProtuneSupported") val isProtuneSupported: Boolean?
)

fun LivestreamStatus.isOk(): Boolean = (this.status?.isOk() ?: true) && (this.error?.isOk() ?: true)
