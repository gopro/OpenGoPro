/* Datetime.kt/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Tue Feb 18 18:41:29 UTC 2025 */

package com.gopro.open_gopro.operations

import kotlinx.datetime.LocalDateTime
import kotlinx.datetime.UtcOffset
import kotlinx.serialization.Serializable

data class GpDatetime(
    val datetime: LocalDateTime,
    val utcOffset: UtcOffset,
    val isDaylightSavingsTime: Boolean
)

@Serializable
data class DateTimeHttpResponse(val date: String, val dst: Int, val time: String, val tzone: Int)
