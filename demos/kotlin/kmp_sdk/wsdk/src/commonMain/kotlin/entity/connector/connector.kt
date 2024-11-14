package entity.connector

import entity.network.BleDevice
import entity.network.IHttpsCredentials

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
    val serialId: String // Last 4 digits of serial number
    val networkType: NetworkType

    data class Ble(override val serialId: String, val id: String, val name: String) :
        ScanResult {
        override val networkType = NetworkType.BLE
    }

    data class Wifi(override val serialId: String, val ssid: String) : ScanResult {
        override val networkType = NetworkType.WIFI_AP
    }

    data class Dns(
        override val serialId: String, val ipAddress: String,
        override val networkType: NetworkType
    ) : ScanResult
}

sealed interface ConnectionDescriptor {
    val serialId: String // Last 4 digits of serial number

    data class Ble(
        override val serialId: String,
        val device: BleDevice
    ) : ConnectionDescriptor

    data class Http(
        override val serialId: String,
        val ipAddress: String,
        val ssid: String? = null,
        val port: Int? = null,
        val credentials: IHttpsCredentials? = null
    ) : ConnectionDescriptor
}
