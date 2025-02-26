/* GpBleAdvertisement.kt/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Tue Feb 18 18:41:29 UTC 2025 */

package com.gopro.open_gopro.domain.communicator.bleCommunicator

import com.gopro.open_gopro.GoProId

@OptIn(ExperimentalUnsignedTypes::class)
internal data class GpBleAdvertisement(
    val id: GoProId,
    val cameraStatus: Int,
    val cameraId: Int,
    val cameraCapability: Int,
    val idHash: UByteArray,
    val mediaOffloadStatus: Int,
    val macAddress: UByteArray,
    val serialNumber: String,
) {
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
              // TODO parse further
              GpBleAdvertisement(
                  cameraStatus = manufacturerData[1].toInt(),
                  cameraId = manufacturerData[2].toInt(),
                  cameraCapability =
                      manufacturerData[3].toLong().shl(8).or(manufacturerData[4].toLong()).toInt(),
                  idHash = manufacturerData.slice(5..10).toByteArray().toUByteArray(),
                  mediaOffloadStatus = manufacturerData[11].toInt(),
                  id = GoProId(name),
                  macAddress = serviceData.slice(0..3).toByteArray().toUByteArray(),
                  serialNumber = serviceData.slice(4..7).toByteArray().decodeToString())
            }
          }
        } ?: throw Exception("Missing service data, manufacturer data, or name.")
  }
}
