/* Settings.kt/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Tue Feb 18 18:41:30 UTC 2025 */

import com.gopro.open_gopro.domain.communicator.BleCommunicator
import com.gopro.open_gopro.domain.communicator.bleCommunicator.bleFragment
import com.gopro.open_gopro.entity.network.ble.BleNotification
import com.gopro.open_gopro.entity.network.ble.GpUuid
import com.gopro.open_gopro.operations.VideoResolution
import com.gopro.open_gopro.util.extensions.toTlvMap
import fakes.BleApiSpy
import fakes.buildFakeSettingsContainer
import kotlin.test.Test
import kotlin.test.assertContentEquals
import kotlin.test.assertEquals
import kotlin.test.assertTrue
import kotlinx.coroutines.ExperimentalCoroutinesApi
import kotlinx.coroutines.flow.onEach
import kotlinx.coroutines.flow.onStart
import kotlinx.coroutines.flow.take
import kotlinx.coroutines.launch
import kotlinx.coroutines.test.UnconfinedTestDispatcher
import kotlinx.coroutines.test.runTest
import vectors.asynchronousSettingValueUpdateMessage1
import vectors.asynchronousSettingValueUpdateMessage2
import vectors.getMultipleSettingsResponsePayload
import vectors.getSettingResponseMessage
import vectors.getSettingResponseMessage2
import vectors.getSettingResponseMessage3
import vectors.getSettingResponsePayload
import vectors.registerSettingValueResponseMessage
import vectors.setSettingResponseMessage
import vectors.setSettingResponseMessageFailure
import vectors.setSettingsRequestPayload

// TODO check spies

@OptIn(ExperimentalUnsignedTypes::class, ExperimentalCoroutinesApi::class)
class TestSettings {

  @Test
  fun `set resolution success`() = runTest {
    // GIVEN
    val responses =
        listOf(listOf(BleNotification(GpUuid.CQ_SETTINGS_RESP.toUuid(), setSettingResponseMessage)))
    val fakeSettingsContainer = buildFakeSettingsContainer(responses, UnconfinedTestDispatcher())
    val setting = fakeSettingsContainer.settingsContainer.videoResolution

    // WHEN
    val result = setting.setValue(VideoResolution.NUM_1080)

    // THEN
    assertTrue { result.isSuccess }
    assertEquals(1, fakeSettingsContainer.spies.size)
    when (val spy = fakeSettingsContainer.spies.first()) {
      is BleApiSpy.Write -> {
        assertEquals(GpUuid.CQ_SETTINGS.toUuid(), spy.uuid)
        assertContentEquals(setSettingsRequestPayload, spy.requestData)
      }

      else -> assertTrue { false }
    }
  }

  @Test
  fun `set resolution failure`() = runTest {
    // GIVEN
    val responses =
        listOf(
            listOf(
                BleNotification(
                    GpUuid.CQ_SETTINGS_RESP.toUuid(), setSettingResponseMessageFailure)))
    val fakeSettingsContainer = buildFakeSettingsContainer(responses, UnconfinedTestDispatcher())
    val setting = fakeSettingsContainer.settingsContainer.videoResolution

    // WHEN
    val result = setting.setValue(VideoResolution.NUM_1080)

    // THEN
    assertTrue { result.isFailure }
    assertEquals(1, fakeSettingsContainer.spies.size)
    when (val spy = fakeSettingsContainer.spies.first()) {
      is BleApiSpy.Write -> {
        assertEquals(GpUuid.CQ_SETTINGS.toUuid(), spy.uuid)
        assertContentEquals(setSettingsRequestPayload, spy.requestData)
      }

      else -> assertTrue { false }
    }
  }

  @Test
  fun `tlv to map extension`() {
    // GIVEN
    val data = getSettingResponsePayload.drop(2)

    // WHEN
    val tlvMap = data.toTlvMap()

    // THEN
    assertEquals(tlvMap.size, 1)
    assertContentEquals(tlvMap.getValue(2U).first(), ubyteArrayOf(9U))
  }

  @Test
  fun `get resolution`() = runTest {
    // GIVEN
    val responses =
        listOf(listOf(BleNotification(GpUuid.CQ_QUERY_RESP.toUuid(), getSettingResponseMessage)))
    val fakeSettingsContainer = buildFakeSettingsContainer(responses, UnconfinedTestDispatcher())
    val setting = fakeSettingsContainer.settingsContainer.videoResolution

    // WHEN
    val result = setting.getValue()

    // THEN
    assertTrue { result.isSuccess }
    assertEquals(result.getOrThrow(), VideoResolution.NUM_1080)
  }

  @Test
  fun `get multiple settings`() = runTest {
    // GIVEN
    val responses =
        listOf(
            getMultipleSettingsResponsePayload
                .bleFragment(BleCommunicator.MAX_PACKET_LENGTH)
                .asSequence()
                .map { BleNotification(GpUuid.CQ_QUERY_RESP.toUuid(), it) }
                .toList())
    val fakeSettingsContainer = buildFakeSettingsContainer(responses, UnconfinedTestDispatcher())
    val setting = fakeSettingsContainer.settingsContainer.videoResolution

    // WHEN
    val result = setting.getValue()
    // THEN
    assertTrue { result.isSuccess }
    assertEquals(result.getOrThrow(), VideoResolution.NUM_1080)
  }

  @Test
  fun `multiple consecutive operations`() = runTest {
    // GIVEN
    val responses =
        listOf(
            listOf(BleNotification(GpUuid.CQ_QUERY_RESP.toUuid(), getSettingResponseMessage)),
            listOf(BleNotification(GpUuid.CQ_QUERY_RESP.toUuid(), getSettingResponseMessage2)),
            listOf(BleNotification(GpUuid.CQ_QUERY_RESP.toUuid(), getSettingResponseMessage3)),
        )
    val fakeSettingsContainer = buildFakeSettingsContainer(responses, UnconfinedTestDispatcher())
    val setting = fakeSettingsContainer.settingsContainer.videoResolution

    // WHEN / THEN
    var result = setting.getValue()
    assertTrue { result.isSuccess }
    assertEquals(result.getOrThrow(), VideoResolution.NUM_1080)

    result = setting.getValue()
    assertTrue { result.isSuccess }
    assertEquals(result.getOrThrow(), VideoResolution.NUM_720)

    result = setting.getValue()
    assertTrue { result.isSuccess }
    assertEquals(result.getOrThrow(), VideoResolution.NUM_4K_4_3)
  }

  @Test
  fun `register resolution value updates`() = runTest {
    // GIVEN
    val responses =
        listOf(
            listOf(
                BleNotification(
                    GpUuid.CQ_QUERY_RESP.toUuid(), registerSettingValueResponseMessage)),
            listOf(
                BleNotification(
                    GpUuid.CQ_QUERY_RESP.toUuid(), asynchronousSettingValueUpdateMessage1)),
            listOf(
                BleNotification(
                    GpUuid.CQ_QUERY_RESP.toUuid(), asynchronousSettingValueUpdateMessage1)),
            listOf(
                BleNotification(
                    GpUuid.CQ_QUERY_RESP.toUuid(), asynchronousSettingValueUpdateMessage2)),
        )
    val fakeSettingsContainer = buildFakeSettingsContainer(responses, UnconfinedTestDispatcher())
    val setting = fakeSettingsContainer.settingsContainer.videoResolution
    var messageCount = 0

    // WHEN
    val settingUpdates = mutableListOf<VideoResolution>()
    setting
        .registerValueUpdates()
        .onSuccess { flow ->
          flow
              .take(4)
              .onStart {
                launch {
                  fakeSettingsContainer.sendNextBleMessage()
                  messageCount += 1
                }
              }
              .onEach {
                launch {
                  try {
                    messageCount += 1
                    // Minus one because of the original message sent from the write.
                    if (messageCount <= responses.size - 1)
                        fakeSettingsContainer.sendNextBleMessage()
                  } catch (exc: Exception) {
                    println(exc)
                  }
                }
              }
              .collect { settingUpdates += it }
        }
        .onFailure { assertTrue { false } }

    // THEN
    assertEquals(settingUpdates.size, 4)
    assertEquals(settingUpdates[0], VideoResolution.NUM_1080)
    assertEquals(settingUpdates[1], VideoResolution.NUM_1080)
    assertEquals(settingUpdates[2], VideoResolution.NUM_1080)
    assertEquals(settingUpdates[3], VideoResolution.NUM_720)
  }
}
