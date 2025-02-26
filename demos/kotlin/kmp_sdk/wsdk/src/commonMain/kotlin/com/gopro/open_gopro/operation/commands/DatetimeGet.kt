/* DatetimeGet.kt/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Tue Feb 18 18:41:28 UTC 2025 */

package com.gopro.open_gopro.operations.commands

import com.gopro.open_gopro.domain.api.BaseOperation
import com.gopro.open_gopro.domain.communicator.BleCommunicator
import com.gopro.open_gopro.domain.communicator.HttpCommunicator
import com.gopro.open_gopro.domain.communicator.bleCommunicator.ResponseId
import com.gopro.open_gopro.entity.communicator.CommandId
import com.gopro.open_gopro.operations.DateTimeHttpResponse
import com.gopro.open_gopro.operations.GpDatetime
import com.gopro.open_gopro.util.extensions.toBoolean
import com.gopro.open_gopro.util.extensions.toLocalDateTime
import com.gopro.open_gopro.util.extensions.toUtcOffset
import io.ktor.client.call.body
import io.ktor.http.path
import kotlinx.datetime.LocalDateTime
import kotlinx.datetime.Month
import kotlinx.datetime.UtcOffset

@OptIn(ExperimentalUnsignedTypes::class)
internal class DatetimeGet : BaseOperation<GpDatetime>("Get Datetime") {
  override suspend fun execute(communicator: BleCommunicator): Result<GpDatetime> =
      communicator
          .executeTlvCommand(CommandId.GET_DATE_TIME, ResponseId.Command(CommandId.GET_DATE_TIME))
          .map {
            GpDatetime(
                datetime = it.slice(1..7).toUByteArray().toLocalDateTime(),
                utcOffset = it.slice(8..9).toUByteArray().toUtcOffset(),
                isDaylightSavingsTime = it[10].toBoolean())
          }

  override suspend fun execute(communicator: HttpCommunicator): Result<GpDatetime> =
      communicator
          .get { url { path("gopro/camera/get_date_time") } }
          .map { response ->
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
                datetime =
                    LocalDateTime(
                        year = year,
                        month = Month(month),
                        dayOfMonth = day,
                        hour = hour,
                        minute = minute,
                        second = second),
                utcOffset = UtcOffset(minutes = dateTimeHttp.tzone),
                isDaylightSavingsTime = dateTimeHttp.dst.toBoolean())
          }
}
