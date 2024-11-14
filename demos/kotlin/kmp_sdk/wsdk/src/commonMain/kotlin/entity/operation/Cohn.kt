package entity.operation

import entity.network.IHttpsCredentials
import entity.operation.proto.EnumCOHNNetworkState
import entity.operation.proto.EnumCOHNStatus
import kotlinx.serialization.Contextual
import kotlinx.serialization.SerialName
import kotlinx.serialization.Serializable

sealed class CohnState {

    data object Unprovisioned : CohnState() {
        override fun toString(): String = "Unprovisioned"
    }

    data class Provisioned(
        override val username: String,
        override val password: String,
        val ipAddress: String,
        override val certificates: List<String>
    ) : CohnState(), IHttpsCredentials {
        override fun toString(): String = "Provisioned"
    }
}

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
class CohnSettingRequest(
    @SerialName("cohn_active") val disableCohn: Boolean
)