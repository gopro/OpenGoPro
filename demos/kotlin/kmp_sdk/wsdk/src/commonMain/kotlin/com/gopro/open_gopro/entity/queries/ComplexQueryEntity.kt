/* ComplexQueryEntity.kt/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Mon Apr 21 22:23:55 UTC 2025 */

package com.gopro.open_gopro.entity.queries

import com.gopro.open_gopro.operations.IUByteArrayCompanion
import com.gopro.open_gopro.util.extensions.toBoolean
import com.gopro.open_gopro.util.extensions.toInt
import com.gopro.open_gopro.util.extensions.toUByte

internal object ComplexQueryEntity {
  data class ScheduledCapture(
      val hour: Int,
      val minute: Int,
      val is24hour: Boolean,
      val isEnabled: Boolean
  ) {
    companion object : IUByteArrayCompanion<ScheduledCapture> {
      private val hourMask = (0x1FU).toUByte()
      private val minuteMask = (0xFCU).toUByte()
      private val is24HourMask = (0x02U).toUByte()
      private val isEnabledMask = (0x01U).toUByte()

      @OptIn(ExperimentalUnsignedTypes::class)
      override fun fromUByteArray(value: UByteArray) =
          // Payload is the last 2 bytes
          value.takeLast(2).let {
            val hour = it[0] and hourMask
            val minute = (it[1] and minuteMask).toLong() shr 2
            val is24Hour = (it[1] and is24HourMask).toLong() shr 1
            val isEnabled = it[1] and isEnabledMask
            ScheduledCapture(
                hour = hour.toInt(),
                minute = minute.toInt(),
                is24hour = is24Hour.toInt().toBoolean(),
                isEnabled = isEnabled.toInt().toBoolean())
          }

      @OptIn(ExperimentalUnsignedTypes::class)
      override fun toUByteArray(value: ScheduledCapture): UByteArray {
        val hourField = value.hour.toLong()
        val minuteField = value.minute.toLong() shl 2
        val is24HourField = value.is24hour.toInt().toLong() shl 1
        val isEnabledField = value.isEnabled.toInt().toLong()
        return ubyteArrayOf(
            0U, 0U, hourField.toUByte(), (minuteField or is24HourField or isEnabledField).toUByte())
      }
    }
  }
}
