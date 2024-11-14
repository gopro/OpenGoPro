package entity.connector

import entity.network.BleDevice
import entity.network.IHttpsCredentials

data class GoProId(val partialSerial: String) {
    override fun toString() = "GoPro $partialSerial"
}

enum class NetworkType {
    BLE,
    WIFI_WLAN,
    WIFI_AP,
    USB
}

sealed interface ConnectionRequestContext {
    data class Wifi(val password: String) : ConnectionRequestContext
}

sealed interface ScanResult {
    val id: GoProId
    val networkType: NetworkType

    data class Ble(override val id: GoProId, val bleId: String, val name: String) :
        ScanResult {
        override val networkType = NetworkType.BLE
    }

    data class Wifi(override val id: GoProId, val ssid: String) : ScanResult {
        override val networkType = NetworkType.WIFI_AP
    }

    data class Dns(
        override val id: GoProId, val ipAddress: String,
        override val networkType: NetworkType
    ) : ScanResult
}

internal sealed interface ConnectionDescriptor {
    val id: GoProId

    data class Ble(
        override val id: GoProId,
        val device: BleDevice
    ) : ConnectionDescriptor

    data class Http(
        override val id: GoProId,
        val ipAddress: String,
        val ssid: String? = null,
        val port: Int? = null,
        val credentials: IHttpsCredentials? = null
    ) : ConnectionDescriptor
}
