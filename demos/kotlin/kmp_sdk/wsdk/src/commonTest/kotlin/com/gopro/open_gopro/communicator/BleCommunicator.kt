/* BleCommunicator.kt/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Tue Feb 18 18:41:30 UTC 2025 */

package com.gopro.open_gopro.communicator

import com.gopro.open_gopro.BleError
import com.gopro.open_gopro.domain.communicator.bleCommunicator.ResponseId
import com.gopro.open_gopro.domain.communicator.bleCommunicator.decipherResponse
import com.gopro.open_gopro.entity.communicator.ActionId
import com.gopro.open_gopro.entity.communicator.CommandId
import com.gopro.open_gopro.entity.communicator.FeatureId
import com.gopro.open_gopro.entity.communicator.QueryId
import com.gopro.open_gopro.entity.network.ble.BleNotification
import com.gopro.open_gopro.entity.network.ble.GpUuid
import com.gopro.open_gopro.operations.SettingId
import fakes.BleApiSpy
import fakes.buildFakeBleCommunicator
import fakes.buildResponse
import kotlin.test.Test
import kotlin.test.assertEquals
import kotlin.test.assertTrue
import kotlinx.coroutines.ExperimentalCoroutinesApi
import kotlinx.coroutines.test.UnconfinedTestDispatcher
import kotlinx.coroutines.test.runTest
import vectors.genericProtoResponseSuccessPayload
import vectors.getSettingResponsePayload
import vectors.setSettingResponsePayload
import vectors.setShutterRequestMessage
import vectors.setShutterResponseMessage
import vectors.setShutterResponsePayload

@OptIn(ExperimentalUnsignedTypes::class, ExperimentalCoroutinesApi::class)
class TestBleCommunicator {

  @Test
  fun `decipher protobuf response`() {
    // WHEN
    val actionId = ActionId.SET_CAMERA_CONTROL_RSP
    val featureId = FeatureId.COMMAND
    val response =
        buildResponse(
            GpUuid.CQ_COMMAND_RESP,
            ubyteArrayOf(featureId.value, actionId.value) + genericProtoResponseSuccessPayload)
    // GIVEN
    val id = decipherResponse(response)

    // THEN
    assertTrue { id is ResponseId.Protobuf }
    assertEquals((id as ResponseId.Protobuf).featureId, featureId)
    assertEquals(id.actionId, actionId)
  }

  @Test
  fun `decipher command response`() {
    // WHEN
    val commandId = CommandId.SET_SHUTTER
    val response = buildResponse(GpUuid.CQ_COMMAND_RESP, setShutterResponsePayload)

    // GIVEN
    val id = decipherResponse(response)

    // THEN
    assertTrue { id is ResponseId.Command }
    assertEquals((id as ResponseId.Command).id, commandId)
  }

  @Test
  fun `decipher set setting response`() {
    // WHEN
    val settingId = SettingId.VIDEO_RESOLUTION
    val response = buildResponse(GpUuid.CQ_SETTINGS_RESP, setSettingResponsePayload)

    // GIVEN
    val id = decipherResponse(response)

    // THEN
    assertTrue { id is ResponseId.Setting }
    assertEquals((id as ResponseId.Setting).id, settingId)
  }

  @Test
  fun `decipher query setting response`() {
    // WHEN
    val queryId = QueryId.GET_SETTING_VALUES
    val response = buildResponse(GpUuid.CQ_QUERY_RESP, getSettingResponsePayload)

    // GIVEN
    val id = decipherResponse(response)

    // THEN
    assertTrue { id is ResponseId.Query }
    assertEquals((id as ResponseId.Query).id, queryId)
  }

  @Test
  fun `execute tlv command succeeds`() = runTest {
    // GIVEN
    val id = CommandId.SET_SHUTTER
    val arguments = listOf(ubyteArrayOf(1U))
    val fakeCommunicator =
        buildFakeBleCommunicator(
            listOf(
                listOf(
                    BleNotification(GpUuid.CQ_COMMAND_RESP.toUuid(), setShutterResponseMessage))),
            UnconfinedTestDispatcher())

    // WHEN
    val response =
        fakeCommunicator.communicator.executeTlvCommand(
            id, ResponseId.Command(CommandId.SET_SHUTTER), arguments)

    // THEN
    assertTrue { response.isSuccess }
    assertTrue { response.getOrThrow().contentEquals(ubyteArrayOf()) }
    assertEquals(fakeCommunicator.spies.size, 1)
    assertEquals(
        fakeCommunicator.spies.first() as BleApiSpy.Write,
        BleApiSpy.Write(
            fakeCommunicator.connection.device,
            GpUuid.CQ_COMMAND.toUuid(),
            setShutterRequestMessage))
  }

  @Test
  fun `tlv command timeout`() = runTest {
    // GIVEN
    val id = CommandId.SET_SHUTTER
    val arguments = listOf(ubyteArrayOf(1U))
    val fakeCommunicator = buildFakeBleCommunicator(listOf(), UnconfinedTestDispatcher())

    // WHEN
    val response =
        fakeCommunicator.communicator.executeTlvCommand(
            id, ResponseId.Command(CommandId.SET_SHUTTER), arguments)

    // THEN
    assertTrue { response.isFailure }
    assertTrue { response.exceptionOrNull() is BleError }
  }

  @Test
  fun `tlv write characteristic fails`() = runTest {
    // GIVEN
    val id = CommandId.SET_SHUTTER
    val arguments = listOf(ubyteArrayOf(1U))
    val fakeCommunicator = buildFakeBleCommunicator(listOf(), UnconfinedTestDispatcher())

    // WHEN
    fakeCommunicator.api.shouldWriteSucceed = false
    val response =
        fakeCommunicator.communicator.executeTlvCommand(
            id, ResponseId.Command(CommandId.SET_SHUTTER), arguments)

    // THEN
    assertTrue { response.isFailure }
    assertTrue { response.exceptionOrNull() is BleError }
  }
}
