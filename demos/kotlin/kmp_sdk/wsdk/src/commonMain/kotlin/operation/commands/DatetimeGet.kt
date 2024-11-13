package operation.commands

import domain.api.BaseOperation
import domain.communicator.BleCommunicator
import domain.communicator.HttpCommunicator
import domain.communicator.bleCommunicator.ResponseId
import entity.communicator.CommandId
import entity.operation.DateTimeHttpResponse
import entity.operation.GpDatetime
import extensions.toBoolean
import extensions.toLocalDateTime
import extensions.toUtcOffset
import io.ktor.client.call.body
import io.ktor.http.path
import kotlinx.datetime.LocalDateTime
import kotlinx.datetime.Month
import kotlinx.datetime.UtcOffset


@OptIn(ExperimentalUnsignedTypes::class)
internal class DatetimeGet : BaseOperation<GpDatetime>("Get Datetime") {
    override suspend fun execute(communicator: BleCommunicator): Result<GpDatetime> =
        communicator.executeTlvCommand(
            CommandId.GET_DATE_TIME,
            ResponseId.Command(CommandId.GET_DATE_TIME)
        ).map {
            GpDatetime(
                datetime = it.slice(1..7).toUByteArray().toLocalDateTime(),
                utcOffset = it.slice(8..9).toUByteArray().toUtcOffset(),
                isDaylightSavingsTime = it[10].toBoolean()
            )
        }

    override suspend fun execute(communicator: HttpCommunicator): Result<GpDatetime> =
        communicator.get { url { path("gopro/camera/get_date_time") } }.map { response ->
            val dateTimeHttp: DateTimeHttpResponse = response.body()
            var year: Int
            var month: Int
            var day: Int
            dateTimeHttp.date.split("_").let { parts ->
                year = parts[0].toInt()
                month = parts[1].toInt()
                day = parts[2].toInt()
            }
            var hour: Int
            var minute: Int
            var second: Int
            dateTimeHttp.time.split("_").let { parts ->
                hour = parts[0].toInt()
                minute = parts[1].toInt()
                second = parts[2].toInt()
            }
            GpDatetime(
                datetime = LocalDateTime(
                    year = year,
                    month = Month(month),
                    dayOfMonth = day,
                    hour = hour,
                    minute = minute,
                    second = second
                ),
                utcOffset = UtcOffset(minutes = dateTimeHttp.tzone),
                isDaylightSavingsTime = dateTimeHttp.dst.toBoolean()
            )
        }

}
