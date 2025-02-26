/* TestBleAdvertisementParsing.kt/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Tue Feb 18 18:41:30 UTC 2025 */

package com.gopro.open_gopro.network

import com.gopro.open_gopro.domain.communicator.bleCommunicator.GpBleAdvertisement
import kotlin.test.Test
import kotlin.test.assertContentEquals
import kotlin.test.assertEquals
import vectors.scanResponseFea6ServiceData
import vectors.scanResponseManufData

class TestBleAdvertisementParsing {
  @OptIn(ExperimentalUnsignedTypes::class)
  @Test
  fun `parse service data`() {
    // GIVEN
    val builder = GpBleAdvertisement.Builder()

    // WHEN
    val gpAdvertisement =
        builder
            .name("name")
            .serviceData(scanResponseFea6ServiceData)
            .manufacturerData(scanResponseManufData)
            .build()

    // THEN
    with(gpAdvertisement) {
      assertEquals(1, cameraStatus)
      assertEquals(65, cameraId)
      assertEquals(0x2300, cameraCapability)
      assertContentEquals(ubyteArrayOf(0x99U, 0x64U, 0x26U, 0x61U, 0x21U, 0xe0U), idHash)
      assertEquals(15, mediaOffloadStatus)
      assertContentEquals(ubyteArrayOf(0x47U, 0x3bU, 0x28U, 0x2dU), macAddress)
      assertEquals("0053", serialNumber)
    }
  }
}
