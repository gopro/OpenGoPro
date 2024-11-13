package entity.operation

import kotlinx.datetime.LocalDateTime
import kotlinx.datetime.UtcOffset
import kotlinx.serialization.Serializable

data class GpDatetime(
    val datetime: LocalDateTime,
    val utcOffset: UtcOffset,
    val isDaylightSavingsTime: Boolean
)

@Serializable
data class DateTimeHttpResponse(
    val date: String,
    val dst: Int,
    val time: String,
    val tzone: Int
)