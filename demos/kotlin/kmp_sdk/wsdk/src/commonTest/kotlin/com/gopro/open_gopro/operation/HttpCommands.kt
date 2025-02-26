/* HttpCommands.kt/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Tue Feb 18 18:41:30 UTC 2025 */

@file:OptIn(ExperimentalCoroutinesApi::class)

package com.gopro.open_gopro.operations

import com.gopro.open_gopro.operations.commands.DatetimeGet
import com.gopro.open_gopro.operations.commands.DatetimeSet
import com.gopro.open_gopro.operations.commands.GetOpenGoProVersion
import com.gopro.open_gopro.operations.commands.LivestreamConfigure
import com.gopro.open_gopro.operations.commands.MediaDeleteGrouped
import com.gopro.open_gopro.operations.commands.MediaGetLastCaptured
import com.gopro.open_gopro.operations.commands.MediaGetList
import com.gopro.open_gopro.operations.commands.MediaGetMetadata
import com.gopro.open_gopro.operations.commands.PresetGetInfo
import com.gopro.open_gopro.operations.commands.SetCameraControl
import com.gopro.open_gopro.operations.commands.UpdateCustomPresetIcon
import com.gopro.open_gopro.operations.commands.UpdateCustomPresetTitle
import com.gopro.open_gopro.operations.commands.WebcamGetState
import fakes.buildFakeHttpCommunicator
import io.ktor.client.utils.EmptyContent
import io.ktor.http.HttpMethod
import kotlin.test.Test
import kotlin.test.assertContentEquals
import kotlin.test.assertEquals
import kotlin.test.assertFalse
import kotlin.test.assertNull
import kotlin.test.assertTrue
import kotlinx.coroutines.ExperimentalCoroutinesApi
import kotlinx.coroutines.flow.single
import kotlinx.coroutines.launch
import kotlinx.coroutines.test.UnconfinedTestDispatcher
import kotlinx.coroutines.test.runTest
import kotlinx.serialization.encodeToString
import vectors.datetimeResponse
import vectors.localDateTimeVector
import vectors.mockHardwareInfo
import vectors.mockLivestreamRequest
import vectors.mockMediaId
import vectors.utcOffsetVector

class TestHttpCommands {
  @Test
  fun `parse http response`() {
    // GIVEN
    val jsonString = jsonDefault.encodeToString(mockHardwareInfo)

    // WHEN
    val hardwareInfo = jsonDefault.decodeFromString<HardwareInfo>(jsonString)

    // THEN
    assertEquals(hardwareInfo, mockHardwareInfo)
  }

  @Test
  fun `get last captured media file`() = runTest {
    // GIVEN
    val fakeCommunicator = buildFakeHttpCommunicator(UnconfinedTestDispatcher())
    val operation = MediaGetLastCaptured()

    // WHEN
    val response = operation.execute(fakeCommunicator.communicator)

    // THEN
    assertTrue { response.isSuccess }
    assertEquals(response.getOrThrow().filename, mockMediaId.filename)
    assertEquals(response.getOrThrow().folder, mockMediaId.folder)
    assertEquals(fakeCommunicator.spies.size, 1)
    fakeCommunicator.spies.first().let {
      assertEquals(it.request.method, HttpMethod.Get)
      assertTrue { it.request.url.parameters.isEmpty() }
    }
  }

  @Test
  fun `set camera control`() = runTest {
    // GIVEN
    val fakeCommunicator = buildFakeHttpCommunicator(UnconfinedTestDispatcher())
    val operation = SetCameraControl(CameraControlStatus.CAMERA)

    // WHEN
    val response = operation.execute(fakeCommunicator.communicator)

    // THEN
    assertTrue { response.isSuccess }
    assertEquals(response.getOrThrow(), Unit)
    assertEquals(fakeCommunicator.spies.size, 1)
    fakeCommunicator.spies.first().let { assertEquals(EmptyContent, it.request.body) }
  }

  @Test
  fun `get ogp version`() = runTest {
    // GIVEN
    val fakeCommunicator = buildFakeHttpCommunicator(UnconfinedTestDispatcher())
    val operation = GetOpenGoProVersion()

    // WHEN
    val response = operation.execute(fakeCommunicator.communicator)

    // THEN
    assertTrue { response.isSuccess }
    assertEquals(response.getOrThrow().major, 2)
    assertEquals(response.getOrThrow().minor, 0)
    assertEquals(fakeCommunicator.spies.size, 1)
    fakeCommunicator.spies.first().let { assertEquals(EmptyContent, it.request.body) }
  }

  @Test
  fun `set livestream mode`() = runTest {
    // GIVEN
    val fakeCommunicator = buildFakeHttpCommunicator(UnconfinedTestDispatcher())
    val operation = LivestreamConfigure(mockLivestreamRequest)

    // WHEN
    val response = operation.execute(fakeCommunicator.communicator)

    // THEN
    assertTrue { response.isSuccess }
    assertEquals(response.getOrThrow(), Unit)
    assertEquals(fakeCommunicator.spies.size, 1)
    fakeCommunicator.spies.first().let { assertEquals(it.request.body, mockLivestreamRequest) }
  }

  @Test
  fun `update custom icon`() = runTest {
    // GIVEN
    val fakeCommunicator = buildFakeHttpCommunicator(UnconfinedTestDispatcher())
    val operation = UpdateCustomPresetIcon(EnumPresetIcon.PRESET_ICON_BIKE)

    // WHEN
    val response = operation.execute(fakeCommunicator.communicator)

    // THEN
    assertTrue { response.isSuccess }
    assertEquals(response.getOrThrow(), Unit)
    assertEquals(fakeCommunicator.spies.size, 1)
    (fakeCommunicator.spies.first().request.body as UpdateCustomPresetRequest).let {
      assertEquals(EnumPresetIcon.PRESET_ICON_BIKE.value, it.iconId)
      assertNull(it.name)
      assertNull(it.titleId)
    }
  }

  @Test
  fun `update custom title id`() = runTest {
    // GIVEN
    val fakeCommunicator = buildFakeHttpCommunicator(UnconfinedTestDispatcher())
    val operation = UpdateCustomPresetTitle(EnumPresetTitle.PRESET_TITLE_BIKE)

    // WHEN
    val response = operation.execute(fakeCommunicator.communicator)

    // THEN
    assertTrue { response.isSuccess }
    assertEquals(response.getOrThrow(), Unit)
    assertEquals(fakeCommunicator.spies.size, 1)
    (fakeCommunicator.spies.first().request.body as UpdateCustomPresetRequest).let {
      assertEquals(EnumPresetTitle.PRESET_TITLE_BIKE.value, it.titleId)
      assertNull(it.name)
      assertNull(it.iconId)
    }
  }

  @Test
  fun `update custom title string`() = runTest {
    // GIVEN
    val fakeCommunicator = buildFakeHttpCommunicator(UnconfinedTestDispatcher())
    val operation = UpdateCustomPresetTitle("Cheese Title")

    // WHEN
    val response = operation.execute(fakeCommunicator.communicator)

    // THEN
    assertTrue { response.isSuccess }
    assertEquals(response.getOrThrow(), Unit)
    assertEquals(fakeCommunicator.spies.size, 1)
    (fakeCommunicator.spies.first().request.body as UpdateCustomPresetRequest).let {
      assertEquals(EnumPresetTitle.PRESET_TITLE_CUSTOM.value, it.titleId)
      assertEquals("Cheese Title", it.name)
      assertNull(it.iconId)
    }
  }

  @Test
  fun `test serialization of proto enums`() = runTest {
    val preset =
        WrappedPreset(
            icon = EnumPresetIcon.PRESET_ICON_BIKE,
            id = 0,
            mode = EnumFlatMode.FLAT_MODE_LOOPING,
            settings = listOf(),
            isFixed = true,
            titleId = EnumPresetTitle.PRESET_TITLE_BIKE,
            isUserDefined = true,
            isModified = true,
            titleNumber = 0)

    val serialized = jsonDefault.encodeToString(preset)

    val deserialized = jsonDefault.decodeFromString<WrappedPreset>(serialized)

    assertTrue { true }
    assertEquals(preset, deserialized)
  }

  @Test
  fun `get preset info`() = runTest {
    // GIVEN
    val fakeCommunicator = buildFakeHttpCommunicator(UnconfinedTestDispatcher())
    val operation = PresetGetInfo()
    var info: PresetInfo? = null

    // WHEN
    val response = operation.execute(fakeCommunicator.communicator)
    val collector = response.getOrThrow().let { launch { info = it.single() } }
    collector.join()

    // THEN
    assertTrue { response.isSuccess }
    assertTrue { info!!.presetGroupArray!!.first().presets!!.first().isFixed!! }
  }

  @Test
  fun `test media path in parameter`() = runTest {
    // GIVEN
    val fakeCommunicator = buildFakeHttpCommunicator(UnconfinedTestDispatcher())
    val group = MediaId("one/two", "file")
    val operation = MediaDeleteGrouped(group)

    // WHEN
    val response = operation.execute(fakeCommunicator.communicator)

    // THEN
    assertTrue { response.isSuccess }
    fakeCommunicator.spies.first().request.let {
      assertFalse { it.build().url.toString().contains("%") }
    }
  }

  @Test
  fun `get photo metadata`() = runTest {
    // GIVEN
    val fakeCommunicator = buildFakeHttpCommunicator(UnconfinedTestDispatcher())
    val file = MediaId("one/two", "file")
    val operation = MediaGetMetadata(file)

    // WHEN
    val response = operation.execute(fakeCommunicator.communicator)

    // THEN
    assertTrue { response.isSuccess }
    fakeCommunicator.spies.first().request.let {
      assertFalse { it.build().url.toString().contains("%") }
    }
    with(response.getOrThrow() as PhotoMediaMetadata) {
      assertFalse { isStabilized } // eis
      assertFalse { isHighDynamicRange!! } // hdr
      assertFalse { isWideDynamicRange!! } // wdr
    }
  }

  @Test
  fun `get media list`() = runTest {
    // GIVEN
    val fakeCommunicator = buildFakeHttpCommunicator(UnconfinedTestDispatcher())
    val operation = MediaGetList()

    // WHEN
    val response = operation.execute(fakeCommunicator.communicator)

    // THEN
    assertTrue { response.isSuccess }
    with(response.getOrThrow()) {
      assertEquals("3681934162299015560", id)
      assertEquals(1, media.size)
      with(media.first()) {
        assertEquals("100GOPRO", directory)
        assertEquals(6, files.size)
        with(files.last() as GroupedMediaListItem) {
          assertEquals("G0017061.JPG", filename) // n
          assertEquals(1, groupId) // g
          assertEquals(7061, firstGroupMemberId) // b
          assertEquals(7090, lastGroupMemberId) // l
          assertEquals(1729860144, creationTime) // cre
          assertEquals(1729860144, modifiedTime) // mod
          assertEquals(170856763, fileSize) // s
          assertEquals(GroupMediaItemType.BURST, groupType) // t
          assertContentEquals(listOf(), missingFileIds) // m

          assertNull(lowResVideoSize) // glrv
          assertNull(lowResFileSize) // ls
        }
      }
    }
  }

  @Test
  fun `get datetime`() = runTest {
    // GIVEN
    val fakeCommunicator = buildFakeHttpCommunicator(UnconfinedTestDispatcher())
    val operation = DatetimeGet()

    // WHEN
    val response = operation.execute(fakeCommunicator.communicator)

    // THEN
    assertTrue { response.isSuccess }
    with(response.getOrThrow()) {
      assertEquals(localDateTimeVector, datetime)
      assertEquals(utcOffsetVector, utcOffset)
      assertEquals(true, isDaylightSavingsTime)
    }
  }

  @Test
  fun `set datetime`() = runTest {
    // GIVEN
    val fakeCommunicator = buildFakeHttpCommunicator(UnconfinedTestDispatcher())
    val operation = DatetimeSet(localDateTimeVector, utcOffsetVector, true)

    // WHEN
    val response = operation.execute(fakeCommunicator.communicator)

    // THEN
    assertTrue { response.isSuccess }
    assertEquals(1, fakeCommunicator.spies.size)
    fakeCommunicator.spies.first().request.url.parameters.build().let {
      assertEquals(datetimeResponse.date, it["date"])
      assertEquals(datetimeResponse.time, it["time"])
      assertEquals(datetimeResponse.tzone.toString(), it["tzone"])
      assertEquals(datetimeResponse.dst.toString(), it["dst"])
    }
  }

  @Test
  fun `get webcam status`() = runTest {
    // GIVEN
    val fakeCommunicator = buildFakeHttpCommunicator(UnconfinedTestDispatcher())
    val operation = WebcamGetState()

    // WHEN
    val response = operation.execute(fakeCommunicator.communicator)

    // THEN
    assertTrue { response.isSuccess }
    with(response.getOrThrow()) {
      assertEquals(com.gopro.open_gopro.operations.WebcamStatus.OFF, status)
      assertEquals(com.gopro.open_gopro.operations.WebcamError.NONE, error)
    }
  }
}
