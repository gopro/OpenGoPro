/* connector.kt/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Tue Feb 18 18:41:29 UTC 2025 */

package com.gopro.open_gopro

import com.gopro.open_gopro.entity.network.IHttpsCredentials
import com.gopro.open_gopro.entity.network.ble.BleDevice

/** Represents server (50x) and client (40x) errors. */
class HttpError(code: Int, errorMessage: String) :
    Exception("HTTP failed with status $code: $errorMessage")

/** Represent IOExceptions and connectivity issues. */
class NetworkError(message: String) : Exception("Http Network Error: $message")

class BleError(errorMessage: String) : Exception(errorMessage)

class DeviceNotFound(deviceId: String) : Exception("$deviceId not found")

/**
 * The identifier of a connected GoPro
 *
 * This is used throughout the SDK to identify / retrieve GoPro's.
 *
 * @property partialSerial the last four digits of the GoPro's serial number
 */
data class GoProId(val partialSerial: String) {
  /** Display's GoPro XXXX where XXXX is the [partialSerial] */
  override fun toString() = "GoPro $partialSerial"
}

enum class NetworkType {
  BLE,
  WIFI_WLAN,
  WIFI_AP,
  USB
}

/** Per-network-type additional connection request information. */
sealed interface ConnectionRequestContext {
  /**
   * Wi-Fi connection request information to connect to a password-protected SSID
   *
   * @property password password to use for connecting to the SSID
   */
  data class Wifi(val password: String) : ConnectionRequestContext
}

/** Network-type-specific GoPro device discovery results */
sealed interface ScanResult {
  /** ID of discovered Gopro device */
  val id: GoProId

  /** Network type of the [ScanResult] */
  val networkType: NetworkType

  /**
   * A GoPro scan result discovered via BLE (i.e. a BLE advertisement)
   *
   * @property id ID of discovered Gopro device
   * @property bleId BLE-specific identifier
   * @property name human-readable name of BLE advertisement
   */
  data class Ble(override val id: GoProId, val bleId: String, val name: String) : ScanResult {
    override val networkType = NetworkType.BLE
  }

  /**
   * A GoPro discovered from a Wi-Fi SSID scan
   *
   * @property id ID of discovered Gopro device
   * @property ssid SSID of Wi-Fi scan
   */
  data class Wifi(override val id: GoProId, val ssid: String) : ScanResult {
    override val networkType = NetworkType.WIFI_AP
  }

  /**
   * A GoPro discovered from DNS scanning
   *
   * @property id ID of discovered Gopro device
   * @property ipAddress IP Address of DNS scan
   * @property networkType network type of DNS scan ([NetworkType.WIFI_WLAN] or [NetworkType.USB])
   */
  data class Dns(
      override val id: GoProId,
      val ipAddress: String,
      override val networkType: NetworkType
  ) : ScanResult
}

internal sealed interface ConnectionDescriptor {
  val id: GoProId

  data class Ble(override val id: GoProId, val device: BleDevice) : ConnectionDescriptor

  data class Http(
      override val id: GoProId,
      val ipAddress: String,
      val ssid: String? = null,
      val port: Int? = null,
      val credentials: IHttpsCredentials? = null
  ) : ConnectionDescriptor
}
