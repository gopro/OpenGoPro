/* datetime.kt/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Tue Feb 18 18:41:29 UTC 2025 */

package com.gopro.open_gopro.util.extensions

import kotlinx.datetime.LocalDateTime
import kotlinx.datetime.Month
import kotlinx.datetime.UtcOffset
import kotlinx.datetime.number

@OptIn(ExperimentalUnsignedTypes::class)
internal fun LocalDateTime.toUByteArray(): UByteArray =
    ubyteArrayOf(
        this.year.and(0xFF00).shr(8).toUByte(), // year msb
        this.year.and(0xFF).toUByte(), // year lsb
        this.month.number.toUByte(),
        this.dayOfMonth.toUByte(),
        this.hour.toUByte(),
        this.minute.toUByte(),
        this.second.toUByte())

@OptIn(ExperimentalUnsignedTypes::class)
internal fun UByteArray.toLocalDateTime(): LocalDateTime =
    LocalDateTime(
        hour = this[4].toInt(),
        minute = this[5].toInt(),
        second = this[6].toInt(),
        year = this[0].toInt().shl(8).or(this[1].toInt()),
        month = Month(this[2].toInt()),
        dayOfMonth = this[3].toInt(),
    )

@OptIn(ExperimentalUnsignedTypes::class)
internal fun UtcOffset.toUByteArray(): UByteArray =
    (this.totalSeconds / 60).let {
      ubyteArrayOf(it.and(0xFF00).shr(8).toUByte(), it.and(0xFF).toUByte())
    }

@OptIn(ExperimentalUnsignedTypes::class)
internal fun UByteArray.toUtcOffset(): UtcOffset =
    // Use short to get 2's complement version
    UtcOffset(minutes = this[0].toInt().shl(8).or(this[1].toInt()).toShort().toInt())
