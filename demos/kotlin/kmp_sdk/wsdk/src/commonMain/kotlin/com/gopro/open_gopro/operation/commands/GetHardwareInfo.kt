/* GetHardwareInfo.kt/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Tue Feb 18 18:41:28 UTC 2025 */

package com.gopro.open_gopro.operations.commands

import com.gopro.open_gopro.domain.api.BaseOperation
import com.gopro.open_gopro.domain.communicator.BleCommunicator
import com.gopro.open_gopro.domain.communicator.HttpCommunicator
import com.gopro.open_gopro.domain.communicator.bleCommunicator.ResponseId
import com.gopro.open_gopro.entity.communicator.CommandId
import com.gopro.open_gopro.operations.HardwareInfo
import com.gopro.open_gopro.util.extensions.decodeToString
import io.ktor.client.call.body
import io.ktor.http.path

@OptIn(ExperimentalUnsignedTypes::class)
internal class GetHardwareInfo : BaseOperation<HardwareInfo>("Get Hardware Info") {
  override suspend fun execute(communicator: BleCommunicator): Result<HardwareInfo> =
      communicator
          .executeTlvCommand(
              CommandId.GET_HARDWARE_INFO,
              ResponseId.Command(CommandId.GET_HARDWARE_INFO),
          )
          .map { parseBleCommunicatorResponse(it) }

  override suspend fun execute(communicator: HttpCommunicator): Result<HardwareInfo> =
      communicator.get { url { path("gopro/camera/info") } }.map { it.body() }
}

@OptIn(ExperimentalUnsignedTypes::class)
internal fun parseBleCommunicatorResponse(response: UByteArray): HardwareInfo {
  var buf = response.toList()

  val modelNumberLen = buf.first().toInt()
  buf = buf.drop(1)
  val modelNumber = buf.slice(0..<modelNumberLen).toUByteArray().decodeToString()
  buf = buf.drop(modelNumberLen)

  val modelNameLen = buf.first().toInt()
  buf = buf.drop(1)
  val modelName = buf.slice(0..<modelNameLen).toUByteArray().decodeToString()
  buf = buf.drop(modelNameLen)

  val deprecatedLen = buf.first().toInt()
  buf = buf.drop(1 + deprecatedLen)

  val firmwareVersionLen = buf.first().toInt()
  buf = buf.drop(1)
  val firmwareVersion = buf.slice(0..<firmwareVersionLen).toUByteArray().decodeToString()
  buf = buf.drop(firmwareVersionLen)

  val serialNumberLen = buf.first().toInt()
  buf = buf.drop(1)
  val serialNumber = buf.slice(0..<serialNumberLen).toUByteArray().decodeToString()
  buf = buf.drop(serialNumberLen)

  val apSsidLen = buf.first().toInt()
  buf = buf.drop(1)
  val apSsid = buf.slice(0..<apSsidLen).toUByteArray().decodeToString()
  buf = buf.drop(apSsidLen)

  val apMacAddressLen = buf.first().toInt()
  buf = buf.drop(1)
  val apMacAddress = buf.slice(0..<apMacAddressLen).toUByteArray().decodeToString()

  return HardwareInfo(modelNumber, modelName, firmwareVersion, serialNumber, apSsid, apMacAddress)
}
