/* GpBleAdvertisement.kt/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Tue Feb 18 18:41:29 UTC 2025 */

package com.gopro.open_gopro.domain.communicator.bleCommunicator

import co.touchlab.kermit.Logger
import com.gopro.open_gopro.GoProId
import com.gopro.open_gopro.util.extensions.toBoolean
import kotlin.experimental.and

private val logger = Logger.withTag("GpBleAdvertisement")

internal val cameraIdMap =
    mapOf(
        55 to "C344",
        57 to "C346",
        58 to "C347",
        60 to "C349",
        62 to "C350",
        64 to "C352",
        65 to "C353",
    )

@OptIn(ExperimentalUnsignedTypes::class)
internal data class GpBleAdvertisement(
    val name: String,
    val schemaVersion: Int,
    val processorState: Boolean,
    val wifiApState: Boolean,
    val peripheralPairingState: Boolean,
    val centralRoleEnabled: Boolean,
    val isNewMediaAvailable: Boolean,
    val cameraId: Int,
    val supportsCnc: Boolean,
    val supportsBleMetadata: Boolean,
    val supportsWidebandAudio: Boolean,
    val supportsConcurrentMasterSlave: Boolean,
    val supportsOnboarding: Boolean,
    val supportsNewMediaAvailable: Boolean,
    val idHash: UByteArray,
    val isMediaUploadNewMediaAvailable: Boolean,
    val isMediaUploadAvailable: Boolean,
    val isMediaUploadBatteryOk: Boolean,
    val isMediaUploadSdCardOk: Boolean,
    val isMediaUploadBusy: Boolean,
    val isMediaUploadPaused: Boolean,
    val apMacAddress: UByteArray,
    val partialSerialNumber: String,
) {
  val serialNumber: String
    get() {
      val first4 =
          cameraIdMap.getOrElse(cameraId) {
            logger.w("Invalid camera ID ==> $cameraId")
            "XXXX"
          }
      var middle6 = idHash.toByteArray().decodeToString()
      if ("\uFFFD" in middle6) middle6 = "XXXXXX"
      return "$first4$middle6$partialSerialNumber"
    }

  val id: GoProId = GoProId(serialNumber.takeLast(4))

  class Builder {
    private var _name: String? = null
    private var _manufacturerData: ByteArray? = null
    private var _serviceData: ByteArray? = null

    fun name(name: String?) = this.apply { _name = name }

    fun manufacturerData(manufacturerData: ByteArray?) =
        this.apply { _manufacturerData = manufacturerData }

    fun serviceData(serviceData: ByteArray?) = this.apply { _serviceData = serviceData }

    fun build() =
        _manufacturerData?.let { manufacturerData ->
          _serviceData?.let { serviceData ->
            _name?.let { name ->
              GpBleAdvertisement(
                  // Name from scan response data
                  name = name,
                  // Schema version from advertising data manufacturer data
                  schemaVersion = manufacturerData[0].toInt(),
                  // Camera status from advertising data manufacturer data
                  processorState = manufacturerData[1].and(0x01.toByte()).toBoolean(),
                  wifiApState = manufacturerData[1].and(0x02.toByte()).toBoolean(),
                  peripheralPairingState = manufacturerData[1].and(0x04.toByte()).toBoolean(),
                  centralRoleEnabled = manufacturerData[1].and(0x08.toByte()).toBoolean(),
                  isNewMediaAvailable = manufacturerData[1].and(0x10.toByte()).toBoolean(),
                  // Camera ID from advertising data manufacturer data
                  cameraId = manufacturerData[2].toInt(),
                  // Camera capabilities from advertising data manufacturer data
                  supportsCnc = manufacturerData[3].and(0x01.toByte()).toBoolean(),
                  supportsBleMetadata = manufacturerData[3].and(0x02.toByte()).toBoolean(),
                  supportsWidebandAudio = manufacturerData[3].and(0x04.toByte()).toBoolean(),
                  supportsConcurrentMasterSlave =
                      manufacturerData[3].and(0x08.toByte()).toBoolean(),
                  supportsOnboarding = manufacturerData[3].and(0x10.toByte()).toBoolean(),
                  supportsNewMediaAvailable = manufacturerData[3].and(0x20.toByte()).toBoolean(),
                  // ID Hash from advertising data manufacturer's data
                  idHash = manufacturerData.slice(5..10).toByteArray().toUByteArray(),
                  // Media offload status from advertising data manufacturer's data
                  isMediaUploadAvailable = manufacturerData[11].and(0x10.toByte()).toBoolean(),
                  isMediaUploadNewMediaAvailable =
                      manufacturerData[11].and(0x20.toByte()).toBoolean(),
                  isMediaUploadBatteryOk = manufacturerData[11].and(0x40.toByte()).toBoolean(),
                  isMediaUploadSdCardOk = manufacturerData[11].and(0x80.toByte()).toBoolean(),
                  isMediaUploadBusy = manufacturerData[11].and(0x10.toByte()).toBoolean(),
                  isMediaUploadPaused = manufacturerData[11].and(0x20.toByte()).toBoolean(),
                  // MAC address from scan response service data
                  apMacAddress = serviceData.slice(0..3).toByteArray().toUByteArray(),
                  // Partial serial number from scan response service data
                  partialSerialNumber = serviceData.slice(4..7).toByteArray().decodeToString())
            }
          }
        } ?: throw Exception("Missing service data, manufacturer data, or name.")
  }
}
