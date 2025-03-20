/* TestBleAdvertisementParsing.kt/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Tue Feb 18 18:41:30 UTC 2025 */

package com.gopro.open_gopro.network

import com.gopro.open_gopro.domain.communicator.bleCommunicator.GpBleAdvertisement
import kotlin.test.Test
import kotlin.test.assertContentEquals
import kotlin.test.assertEquals
import kotlin.test.assertFalse
import kotlin.test.assertTrue
import vectors.advResponseManufData
import vectors.scanResponseFea6ServiceData

@OptIn(ExperimentalUnsignedTypes::class)
class TestBleAdvertisementParsing {
  @Test
  fun `parse advertisement`() {
    // GIVEN
    val builder = GpBleAdvertisement.Builder()
    val serviceData = scanResponseFea6ServiceData.copyOf()
    val manuData = advResponseManufData.copyOf()

    // WHEN
    val gpAdvertisement =
        builder.name("name").serviceData(serviceData).manufacturerData(manuData).build()

    // THEN
    with(gpAdvertisement) {
      assertEquals(name, "name")
      assertEquals(schemaVersion, 2)
      assertTrue { processorState }
      assertFalse { wifiApState }
      assertFalse { peripheralPairingState }
      assertFalse { centralRoleEnabled }
      assertFalse { isNewMediaAvailable }
      assertEquals(65, cameraId)
      assertTrue { supportsCnc }
      assertTrue { supportsBleMetadata }
      assertFalse { supportsWidebandAudio }
      assertFalse { supportsConcurrentMasterSlave }
      assertFalse { supportsOnboarding }
      assertTrue { supportsNewMediaAvailable }
      assertContentEquals(ubyteArrayOf(0x99U, 0x64U, 0x26U, 0x61U, 0x21U, 0xe0U), idHash)
      assertFalse { isMediaUploadAvailable }
      assertFalse { isMediaUploadNewMediaAvailable }
      assertFalse { isMediaUploadBatteryOk }
      assertFalse { isMediaUploadSdCardOk }
      assertFalse { isMediaUploadBusy }
      assertFalse { isMediaUploadPaused }
      assertContentEquals(ubyteArrayOf(0x47U, 0x3bU, 0x28U, 0x2dU), apMacAddress)
      assertEquals("0053", partialSerialNumber)
      assertEquals(serialNumber, "C353XXXXXX0053")
    }
  }

  @Test
  fun `parse advertisement invalid model id`() {
    // GIVEN
    val builder = GpBleAdvertisement.Builder()
    val serviceData = scanResponseFea6ServiceData.copyOf()
    val manuData = advResponseManufData.copyOf()
    manuData[2] = 0xFF.toByte()

    // WHEN
    val gpAdvertisement =
        builder.name("name").serviceData(serviceData).manufacturerData(manuData).build()

    // THEN
    with(gpAdvertisement) {
      assertEquals(name, "name")
      assertEquals(schemaVersion, 2)
      assertTrue { processorState }
      assertFalse { wifiApState }
      assertFalse { peripheralPairingState }
      assertFalse { centralRoleEnabled }
      assertFalse { isNewMediaAvailable }
      assertEquals(-1, cameraId)
      assertTrue { supportsCnc }
      assertTrue { supportsBleMetadata }
      assertFalse { supportsWidebandAudio }
      assertFalse { supportsConcurrentMasterSlave }
      assertFalse { supportsOnboarding }
      assertTrue { supportsNewMediaAvailable }
      assertContentEquals(ubyteArrayOf(0x99U, 0x64U, 0x26U, 0x61U, 0x21U, 0xe0U), idHash)
      assertFalse { isMediaUploadAvailable }
      assertFalse { isMediaUploadNewMediaAvailable }
      assertFalse { isMediaUploadBatteryOk }
      assertFalse { isMediaUploadSdCardOk }
      assertFalse { isMediaUploadBusy }
      assertFalse { isMediaUploadPaused }
      assertContentEquals(ubyteArrayOf(0x47U, 0x3bU, 0x28U, 0x2dU), apMacAddress)
      assertEquals("0053", partialSerialNumber)
      assertEquals(serialNumber, "XXXXXXXXXX0053")
    }
  }
}
