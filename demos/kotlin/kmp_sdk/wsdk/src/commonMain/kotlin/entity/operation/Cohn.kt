package entity.operation

import kotlinx.serialization.Contextual
import kotlinx.serialization.SerialName
import kotlinx.serialization.Serializable
import open_gopro.EnumCOHNNetworkState
import open_gopro.EnumCOHNStatus

@Serializable
data class CohnStatus(
    @SerialName("enabled") val isEnabled: Boolean? = null,
    @SerialName("ipaddress") val ipAddress: String? = null,
    @SerialName("macaddress") val macAddress: String? = null,
    val password: String? = null,
    val ssid: String? = null,
    val username: String? = null,
    @Contextual val state: EnumCOHNNetworkState? = null,
    @Contextual val status: EnumCOHNStatus? = null
)

@Serializable
data class CohnSettingRequest(
    @SerialName("cohn_active") val disableCohn: Boolean
)