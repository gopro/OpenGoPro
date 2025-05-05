/* BleCommands.kt/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Tue Feb 18 18:41:30 UTC 2025 */

@file:OptIn(ExperimentalCoroutinesApi::class)

package com.gopro.open_gopro.operations

import com.gopro.open_gopro.domain.communicator.BleCommunicator
import com.gopro.open_gopro.domain.communicator.bleCommunicator.bleFragment
import com.gopro.open_gopro.entity.communicator.ActionId
import com.gopro.open_gopro.entity.communicator.FeatureId
import com.gopro.open_gopro.entity.network.ble.GpUuid
import com.gopro.open_gopro.gopro.CameraInternalError
import com.gopro.open_gopro.operations.commands.AccessPointGetScanResults
import com.gopro.open_gopro.operations.commands.AccessPointScan
import com.gopro.open_gopro.operations.commands.ConnectNewAccessPoint
import com.gopro.open_gopro.operations.commands.ConnectProvisionedAccessPoint
import com.gopro.open_gopro.operations.commands.DatetimeGet
import com.gopro.open_gopro.operations.commands.GetHardwareInfo
import com.gopro.open_gopro.operations.commands.KeepAlive
import com.gopro.open_gopro.operations.commands.LivestreamConfigure
import com.gopro.open_gopro.operations.commands.LivestreamGetStatus
import com.gopro.open_gopro.operations.commands.PresetGetInfo
import com.gopro.open_gopro.operations.commands.SetCameraControl
import com.gopro.open_gopro.operations.commands.SetShutter
import com.gopro.open_gopro.util.extensions.toLocalDateTime
import com.gopro.open_gopro.util.extensions.toUByteArray
import com.gopro.open_gopro.util.extensions.toUtcOffset
import fakes.BleApiSpy
import fakes.buildFakeBleCommunicator
import fakes.toBleNotificationList
import kotlin.test.Test
import kotlin.test.assertContentEquals
import kotlin.test.assertEquals
import kotlin.test.assertFalse
import kotlin.test.assertNull
import kotlin.test.assertTrue
import kotlinx.coroutines.ExperimentalCoroutinesApi
import kotlinx.coroutines.flow.take
import kotlinx.coroutines.launch
import kotlinx.coroutines.test.UnconfinedTestDispatcher
import kotlinx.coroutines.test.runTest
import kotlinx.datetime.UtcOffset
import pbandk.ExperimentalProtoJson
import pbandk.json.encodeToJsonString
import vectors.completeNotifyPresetStatus
import vectors.connectAccessPointComplete
import vectors.connectAccessPointFailureSuccess
import vectors.connectAccessPointOngoing
import vectors.connectNewAccessPointResponseSuccess
import vectors.dateTimeResponsePayload
import vectors.finalApScanNotification
import vectors.genericProtoResponseSuccessPayload
import vectors.getApScanResultsResponse
import vectors.getLivestreamStatusNoti1
import vectors.getLivestreamStatusNoti2
import vectors.getLivestreamStatusNoti3
import vectors.getLivestreamStatusResponse1
import vectors.getPresetStatusInitialResponse
import vectors.getPresetStatusPartialResponse1
import vectors.getPresetStatusPartialResponse2
import vectors.hardwareInfoResponsePayload
import vectors.initialApScanResponse
import vectors.initialApScanResponseFailure
import vectors.intermediateApScanNotification
import vectors.keepAliveResponsePayload
import vectors.localDateTimeBytes
import vectors.localDateTimeVector
import vectors.mockHardwareInfo
import vectors.setShutterResponsePayload
import vectors.unregisterLivestreamStatusRequest
import vectors.unregisterPresetInfoRequest
import vectors.utcOffsetBytes
import vectors.utcOffsetVector

@OptIn(ExperimentalUnsignedTypes::class)
class TestBleCommands {

  @Test
  fun `keep alive`() = runTest {
    // GIVEN
    val operation = KeepAlive()
    val fakeCommunicator =
        buildFakeBleCommunicator(
            listOf(keepAliveResponsePayload.toBleNotificationList(GpUuid.CQ_SETTINGS_RESP)),
            UnconfinedTestDispatcher())

    // WHEN
    val result = operation.execute(fakeCommunicator.communicator)

    // THEN
    assertTrue { result.isSuccess }
    assertEquals(1, fakeCommunicator.spies.size)
    when (val spy = fakeCommunicator.spies.first()) {
      is BleApiSpy.Write -> {
        assertEquals(GpUuid.CQ_SETTINGS.toUuid(), spy.uuid)
        assertContentEquals(ubyteArrayOf(32U, 0x03U, 0x5bU, 0x01U, 0x42U), spy.requestData)
      }

      else -> assertTrue { false }
    }
  }

  @Test
  fun `set shutter`() = runTest {
    // GIVEN
    val operation = SetShutter(true)
    val fakeCommunicator =
        buildFakeBleCommunicator(
            listOf(setShutterResponsePayload.toBleNotificationList(GpUuid.CQ_COMMAND_RESP)),
            UnconfinedTestDispatcher())

    // WHEN
    val result = operation.execute(fakeCommunicator.communicator)

    // THEN
    assertTrue { operation.shutter }
    assertTrue { result.isSuccess }
    assertEquals(result.getOrThrow(), Unit)
  }

  @OptIn(ExperimentalCoroutinesApi::class)
  @Test
  fun `set camera control status via BLE`() = runTest {
    // GIVEN
    val operation = SetCameraControl(CameraControlStatus.EXTERNAL)
    val responsePayload =
        ubyteArrayOf(FeatureId.COMMAND.value, ActionId.SET_CAMERA_CONTROL_RSP.value) +
            genericProtoResponseSuccessPayload
    val fakeCommunicator =
        buildFakeBleCommunicator(
            listOf(responsePayload.toBleNotificationList(GpUuid.CQ_COMMAND_RESP)),
            UnconfinedTestDispatcher())

    // WHEN
    val result = operation.execute(fakeCommunicator.communicator)

    // THEN
    assertEquals(operation.status, CameraControlStatus.EXTERNAL)
    assertTrue { result.isSuccess }
    assertEquals(result.getOrThrow(), Unit)
  }

  @OptIn(ExperimentalCoroutinesApi::class)
  @Test
  fun `set livestream mode via BLE`() = runTest {
    // GIVEN
    val livestreamRequest =
        LivestreamConfigurationRequest(
            fov = LivestreamFov.WIDE,
            resolution = LivestreamResolution.RES_480,
            shouldEncode = true,
            minimumBitrate = 0,
            maximumBitrate = 100,
            startingBitRate = 50,
            url = "rtmp://livestream/test")
    val operation = LivestreamConfigure(livestreamRequest)
    val responsePayload =
        ubyteArrayOf(FeatureId.COMMAND.value, ActionId.SET_LIVESTREAM_MODE_RSP.value) +
            genericProtoResponseSuccessPayload
    val fakeCommunicator =
        buildFakeBleCommunicator(
            listOf(responsePayload.toBleNotificationList(GpUuid.CQ_COMMAND_RESP)),
            UnconfinedTestDispatcher())

    // WHEN
    val result = operation.execute(fakeCommunicator.communicator)

    // THEN
    assertEquals(operation.request.fov, LivestreamFov.WIDE)
    assertEquals(operation.request.resolution, LivestreamResolution.RES_480)
    assertEquals(operation.request.shouldEncode, true)
    assertEquals(operation.request.minimumBitrate, 0)
    assertEquals(operation.request.maximumBitrate, 100)
    assertEquals(operation.request.startingBitRate, 50)
    assertEquals(operation.request.url, "rtmp://livestream/test")
    assertTrue { result.isSuccess }
    assertEquals(result.getOrThrow(), Unit)
  }

  @Test
  fun `get hardware info`() = runTest {
    // GIVEN
    val operation = GetHardwareInfo()
    val fakeCommunicator =
        buildFakeBleCommunicator(
            listOf(hardwareInfoResponsePayload.toBleNotificationList(GpUuid.CQ_COMMAND_RESP)),
            UnconfinedTestDispatcher())

    // WHEN
    val result = operation.execute(fakeCommunicator.communicator)

    // THEN
    assertTrue { result.isSuccess }
    assertEquals(result.getOrThrow(), mockHardwareInfo)
  }

  @Test
  fun `scan for access points succeeds`() = runTest {
    // GIVEN
    val operation = AccessPointScan()
    val fakeCommunicator =
        buildFakeBleCommunicator(
            listOf(
                initialApScanResponse.toBleNotificationList(GpUuid.CN_NET_MGMT_RESP),
                intermediateApScanNotification.toBleNotificationList(GpUuid.CN_NET_MGMT_RESP),
                intermediateApScanNotification.toBleNotificationList(GpUuid.CN_NET_MGMT_RESP),
                intermediateApScanNotification.toBleNotificationList(GpUuid.CN_NET_MGMT_RESP),
                finalApScanNotification.toBleNotificationList(GpUuid.CN_NET_MGMT_RESP),
            ),
            UnconfinedTestDispatcher())
    val scanResponses = mutableListOf<ApScanResult>()

    // WHEN
    val result = operation.execute(fakeCommunicator.communicator)
    val collector = launch { result.getOrThrow().collect { scanResponses += it } }
    launch { fakeCommunicator.sendNextBleMessage() }.join()
    launch { fakeCommunicator.sendNextBleMessage() }.join()
    launch { fakeCommunicator.sendNextBleMessage() }.join()
    launch { fakeCommunicator.sendNextBleMessage() }.join()
    collector.join()

    // THEN
    assertTrue { result.isSuccess }
    assertEquals(4, scanResponses.size)
    assertEquals(scanResponses.last().scanId, 9)
  }

  @Test
  fun `scan for access points sends failure status`() = runTest {
    // GIVEN
    val operation = AccessPointScan()
    val fakeCommunicator =
        buildFakeBleCommunicator(
            listOf(initialApScanResponseFailure.toBleNotificationList(GpUuid.CN_NET_MGMT_RESP)),
            UnconfinedTestDispatcher())

    // WHEN
    val result = operation.execute(fakeCommunicator.communicator)

    // THEN
    assertTrue { result.isFailure }
  }

  @Test
  fun `get ap scan results`() = runTest {
    // GIVEN
    val operation = AccessPointGetScanResults(0, 1)
    val fakeCommunicator =
        buildFakeBleCommunicator(
            listOf(getApScanResultsResponse.toBleNotificationList(GpUuid.CN_NET_MGMT_RESP)),
            UnconfinedTestDispatcher())

    // WHEN
    val response = operation.execute(fakeCommunicator.communicator)

    // THEN
    assertTrue { response.isSuccess }
    response.getOrThrow().let {
      assertEquals(3, it.size)
      it[0].run {
        assertEquals("zero", this.ssid)
        assertEquals(0, this.signalFrequencyMhz)
        assertEquals(0, this.signalStrengthBars)
        assertTrue { this.isOpen }
        assertFalse { this.isAuthenticated }
        assertFalse { this.isAssociated }
        assertFalse { this.isConfigured }
        assertFalse { this.isBestSsid }
      }
      it[1].run {
        assertEquals("one", this.ssid)
        assertEquals(1, this.signalFrequencyMhz)
        assertEquals(1, this.signalStrengthBars)
        assertFalse { this.isOpen }
        assertTrue { this.isAuthenticated }
        assertFalse { this.isConfigured }
        assertFalse { this.isAssociated }
        assertFalse { this.isBestSsid }
      }
      it[2].run {
        assertEquals("two", this.ssid)
        assertEquals(2, this.signalFrequencyMhz)
        assertEquals(2, this.signalStrengthBars)
        assertFalse { this.isOpen }
        assertTrue { this.isAuthenticated }
        assertTrue { this.isAssociated }
        assertTrue { this.isConfigured }
        assertTrue { this.isBestSsid }
      }
    }
  }

  @Test
  fun `connect to new access point succeeds`() = runTest {
    // GIVEN
    val operation = ConnectNewAccessPoint(ssid = "ssid", password = "password")
    val fakeCommunicator =
        buildFakeBleCommunicator(
            listOf(
                connectNewAccessPointResponseSuccess.toBleNotificationList(GpUuid.CN_NET_MGMT_RESP),
                connectAccessPointOngoing.toBleNotificationList(GpUuid.CN_NET_MGMT_RESP),
                connectAccessPointComplete.toBleNotificationList(GpUuid.CN_NET_MGMT_RESP),
            ),
            UnconfinedTestDispatcher())
    val stateUpdates = mutableListOf<AccessPointState>()

    // WHEN
    val result = operation.execute(fakeCommunicator.communicator)
    val collector = launch { result.getOrThrow().collect { stateUpdates += it } }
    launch { fakeCommunicator.sendNextBleMessage() }.join() // ongoing
    launch { fakeCommunicator.sendNextBleMessage() }.join() // complete
    collector.join()

    // THEN
    assertTrue { result.isSuccess }
    assertEquals(3, stateUpdates.size)
    assertTrue { stateUpdates[0] is AccessPointState.InProgress }
    assertTrue { stateUpdates[1] is AccessPointState.InProgress }
    assertTrue { stateUpdates[2] is AccessPointState.Connected }
  }

  @Test
  fun `connect to provisioned access point fails`() = runTest {
    // GIVEN
    val operation = ConnectProvisionedAccessPoint(ssid = "ssid")
    val fakeCommunicator =
        buildFakeBleCommunicator(
            listOf(
                connectAccessPointFailureSuccess.toBleNotificationList(GpUuid.CN_NET_MGMT_RESP),
                connectAccessPointOngoing.toBleNotificationList(GpUuid.CN_NET_MGMT_RESP),
                connectAccessPointComplete.toBleNotificationList(GpUuid.CN_NET_MGMT_RESP),
            ),
            UnconfinedTestDispatcher())

    // WHEN
    val result = operation.execute(fakeCommunicator.communicator)

    // THEN
    assertTrue { result.isFailure }
    assertTrue { result.exceptionOrNull() is CameraInternalError }
  }

  @Test
  fun `get livestream status`() = runTest {
    // GIVEN
    val operation = LivestreamGetStatus()
    val fakeCommunicator =
        buildFakeBleCommunicator(
            listOf(
                getLivestreamStatusResponse1.toBleNotificationList(GpUuid.CQ_COMMAND_RESP),
                getLivestreamStatusNoti1.toBleNotificationList(GpUuid.CQ_COMMAND_RESP),
                getLivestreamStatusNoti2.toBleNotificationList(GpUuid.CQ_COMMAND_RESP),
                getLivestreamStatusNoti3.toBleNotificationList(GpUuid.CQ_COMMAND_RESP),
            ),
            UnconfinedTestDispatcher())
    val statuses = mutableListOf<LivestreamStatus>()

    // WHEN
    val result = operation.execute(fakeCommunicator.communicator)
    val collector = launch { result.getOrThrow().take(4).collect { statuses += it } }
    launch { fakeCommunicator.sendNextBleMessage() }.join() // 2
    launch { fakeCommunicator.sendNextBleMessage() }.join() // 3
    launch { fakeCommunicator.sendNextBleMessage() }.join() // 4
    collector.join()

    // THEN
    assertTrue { result.isSuccess }
    assertEquals(4, statuses.size)
    assertEquals(1, statuses[0].bitRate)
    assertEquals(2, statuses[1].bitRate)
    assertEquals(3, statuses[2].bitRate)
    assertEquals(4, statuses[3].bitRate)
    assertEquals(2, fakeCommunicator.spies.size)
    // Ensure unregister was sent after flow completion
    (fakeCommunicator.spies.last() as BleApiSpy.Write).let {
      assertEquals(GpUuid.CQ_QUERY.toUuid(), it.uuid)
      assertContentEquals(
          unregisterLivestreamStatusRequest.bleFragment(BleCommunicator.MAX_PACKET_LENGTH).next(),
          it.requestData)
    }
  }

  @OptIn(ExperimentalProtoJson::class)
  @Test
  fun `test protobuf to json`() = runTest {
    // GIVEN
    val presetInfoProto = completeNotifyPresetStatus

    // WHEN
    val presetInfoSerializedAsStr = presetInfoProto.encodeToJsonString()
    // TODO remove this
    println(presetInfoSerializedAsStr)

    val presetInfoDeserialized =
        jsonFromProto.decodeFromString<PresetInfo>(presetInfoSerializedAsStr)

    // THEN
    assertTrue {
      presetInfoDeserialized.presetGroupArray?.first()?.presets?.first()?.isFixed == true
    }
  }

  @Test
  fun `get preset info`() = runTest {
    // GIVEN
    val operation = PresetGetInfo()
    val fakeCommunicator =
        buildFakeBleCommunicator(
            listOf(
                getPresetStatusInitialResponse.toBleNotificationList(GpUuid.CQ_QUERY_RESP),
                getPresetStatusPartialResponse1.toBleNotificationList(GpUuid.CQ_QUERY_RESP),
                getPresetStatusPartialResponse2.toBleNotificationList(GpUuid.CQ_QUERY_RESP),
            ),
            UnconfinedTestDispatcher())
    val infos = mutableListOf<PresetInfo>()

    // WHEN
    val result = operation.execute(fakeCommunicator.communicator)
    val collector = launch { result.getOrThrow().take(3).collect { infos += it } }
    launch { fakeCommunicator.sendNextBleMessage() }.join() // partial1
    launch { fakeCommunicator.sendNextBleMessage() }.join() // partial2
    collector.join()

    // THEN
    assertTrue { result.isSuccess }
    assertEquals(3, infos.size)
    // Ensure unregister was sent after flow completion
    assertEquals(2, fakeCommunicator.spies.size)
    assertEquals("cheese", infos[0].presetGroupArray?.first()?.presets?.first()?.customName)
    assertEquals(
        EnumPresetGroupIcon.PRESET_GROUP_TIMELAPSE_ICON_ID,
        infos[1].presetGroupArray?.first()?.icon)
    assertNull(infos[2].presetGroupArray!!.first().presets)
    (fakeCommunicator.spies.last() as BleApiSpy.Write).let {
      assertEquals(GpUuid.CQ_QUERY.toUuid(), it.uuid)
      assertContentEquals(
          unregisterPresetInfoRequest.bleFragment(BleCommunicator.MAX_PACKET_LENGTH).next(),
          it.requestData)
    }
  }

  @Test
  fun `convert datetime to ubytearray`() = runTest {
    // GIVEN
    val datetime = localDateTimeVector

    // WHEN
    val byteRequest = datetime.toUByteArray()

    // THEN
    assertContentEquals(localDateTimeBytes, byteRequest)
  }

  @Test
  fun `convert ubytearray to datetime`() = runTest {
    // GIVEN
    val byteRequest = localDateTimeBytes

    // WHEN
    val datetime = byteRequest.toLocalDateTime()

    // THEN
    assertEquals(localDateTimeVector, datetime)
  }

  @Test
  fun `convert utcOffset to ubytearray`() = runTest {
    // GIVEN
    val utcOffset = UtcOffset(hours = -2)

    // WHEN
    val byteRequest = utcOffset.toUByteArray()

    // THEN
    assertContentEquals(ubyteArrayOf(0xFFU, 0x88U), byteRequest)
  }

  @Test
  fun `convert ubytearray to utcOffset`() = runTest {
    // GIVEN
    val byteRequest = utcOffsetBytes

    // WHEN
    val utcOffset = byteRequest.toUtcOffset()

    // THEN
    assertEquals(utcOffsetVector, utcOffset)
  }

  @Test
  fun `get date time`() = runTest {
    // GIVEN
    val operation = DatetimeGet()
    val fakeCommunicator =
        buildFakeBleCommunicator(
            listOf(dateTimeResponsePayload.toBleNotificationList(GpUuid.CQ_COMMAND_RESP)),
            UnconfinedTestDispatcher())

    // WHEN
    val result = operation.execute(fakeCommunicator.communicator)

    // THEN
    assertTrue { result.isSuccess }
    with(result.getOrThrow()) {
      assertEquals(localDateTimeVector, datetime)
      assertEquals(utcOffsetVector, utcOffset)
      assertEquals(true, isDaylightSavingsTime)
    }
  }
}
