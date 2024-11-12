package entity.operation

import kotlinx.serialization.SerialName
import kotlinx.serialization.Serializable

@Serializable
data class HardwareInfo(
    @SerialName("model_number") val  modelNumber: String,
    @SerialName("model_name") val modelName: String,
    @SerialName("firmware_version") val firmwareVersion: String,
    @SerialName("serial_number") val serialNumber: String,
    @SerialName("ap_ssid") val apSsid: String,
    @SerialName("ap_mac_addr") val apMacAddress: String
)