/* HardwareInfo.kt/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Tue Feb 18 18:41:29 UTC 2025 */

package com.gopro.open_gopro.operations

import kotlinx.serialization.SerialName
import kotlinx.serialization.Serializable

@Serializable
data class HardwareInfo(
    @SerialName("model_number") val modelNumber: String,
    @SerialName("model_name") val modelName: String,
    @SerialName("firmware_version") val firmwareVersion: String,
    @SerialName("serial_number") val serialNumber: String,
    @SerialName("ap_ssid") val apSsid: String,
    @SerialName("ap_mac_addr") val apMacAddress: String
)
