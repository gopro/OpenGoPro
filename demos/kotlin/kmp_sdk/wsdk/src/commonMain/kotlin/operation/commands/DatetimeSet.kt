package operation.commands

import domain.api.BaseOperation
import domain.communicator.BleCommunicator
import domain.communicator.HttpCommunicator
import domain.communicator.bleCommunicator.ResponseId
import entity.communicator.CommandId
import util.extensions.toInt
import util.extensions.toUByte
import util.extensions.toUByteArray
import io.ktor.client.call.body
import io.ktor.http.path
import kotlinx.datetime.LocalDateTime
import kotlinx.datetime.UtcOffset
import kotlinx.datetime.number


@OptIn(ExperimentalUnsignedTypes::class)
internal class DatetimeSet(
    val datetime: LocalDateTime,
    val utcOffset: UtcOffset,
    val isDaylightSavings: Boolean
) :
    BaseOperation<Unit>("Set Datetime") {
    override suspend fun execute(communicator: BleCommunicator): Result<Unit> =
        communicator.executeTlvCommand(
            CommandId.SET_DATE_TIME,
            ResponseId.Command(CommandId.SET_DATE_TIME),
            listOf(
                datetime.toUByteArray() + utcOffset.toUByteArray() + ubyteArrayOf(isDaylightSavings.toUByte())
            ),
        ).map { }

    override suspend fun execute(communicator: HttpCommunicator): Result<Unit> =
        communicator.get {
            url {
                path("gopro/camera/set_date_time")
                parameters.append(
                    "date",
                    "${datetime.year}_${datetime.month.number}_${datetime.dayOfMonth}"
                )
                parameters.append("time", "${datetime.hour}_${datetime.minute}_${datetime.second}")
                parameters.append("tzone", (utcOffset.totalSeconds / 60).toString())
                parameters.append("dst", isDaylightSavings.toInt().toString())
            }
        }.map { it.body() }
}
