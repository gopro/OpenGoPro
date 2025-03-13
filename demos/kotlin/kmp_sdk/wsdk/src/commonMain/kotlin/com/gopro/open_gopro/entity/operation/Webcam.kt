/* Webcam.kt/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Tue Feb 18 18:41:29 UTC 2025 */

package com.gopro.open_gopro.operations

import kotlinx.serialization.Contextual
import kotlinx.serialization.SerialName
import kotlinx.serialization.Serializable

interface IntEnum {
  val value: Int
}

interface IntEnumCompanion<T> {
  fun fromInt(value: Int): T
}

enum class WebcamResolution(val value: Int) {
  RES_480(4),
  RES_720(7),
  RES_1080(12)
}

enum class WebcamFov(val value: Int) {
  WIDE(0),
  NARROW(2),
  SUPERVIEW(3),
  LINEAR(4)
}

enum class WebcamProtocol(val value: String) {
  RTSP("RTSP"),
  TS("TS")
}

enum class WebcamError(override val value: Int) : IntEnum {
  NONE(0),
  SET_PRESET(1),
  SET_WINDOW_SIZE(2),
  EXEC_STREAM(3),
  SHUTTER(4),
  COM_TIMEOUT(5),
  INVALID_PARAM(6),
  UNAVAILABLE(7),
  EXIT(8);

  companion object : IntEnumCompanion<WebcamError> {
    override fun fromInt(value: Int) = WebcamError.entries.first { it.value == value }
  }
}

enum class WebcamStatus(override val value: Int) : IntEnum {
  OFF(0),
  IDLE(1),
  HIGH_POWER_PREVIEW(2),
  LOW_POWER_PREVIEW(3),
  STATUS_IS_UNAVAILABLE(4);

  fun isStreaming(): Boolean =
      when (this) {
        OFF,
        IDLE,
        STATUS_IS_UNAVAILABLE -> false
        else -> true
      }

  companion object : IntEnumCompanion<WebcamStatus> {
    override fun fromInt(value: Int) = WebcamStatus.entries.first { it.value == value }
  }
}

@Serializable
data class WebcamState(@Contextual val error: WebcamError, @Contextual val status: WebcamStatus)

@Serializable
data class WebcamInfo(
    @SerialName("max_lens_support") val isMaxLensSupported: Boolean,
    @SerialName("usb_3_1_compatible") val is31Compatible: Boolean,
    val version: Int
)
