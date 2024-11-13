package entity.network

import com.benasher44.uuid.Uuid
import com.benasher44.uuid.uuidFrom

private fun String.asGoProUuid(): Uuid =
    uuidFrom("b5f9${this.lowercase()}-aa8d-11e3-9046-0002a5d5c51b")

enum class GpUuid(private val base: String) {
    // GoPro Wifi Access Point Service
    S_WIFI_ACCESS_POINT("0001"),
    WAP_SSID("0002"),
    WAP_PASSWORD("0003"),
    WAP_POWER("0004"),
    WAP_STATE("0005"),
    WAP_CSI_PASSWORD("0006"),

    // GoPro Control & Query Service
    S_CONTROL_QUERY("0000fea6-0000-1000-8000-00805f9b34fb"),
    CQ_COMMAND("0072"),
    CQ_COMMAND_RESP("0073"),
    CQ_SETTINGS("0074"),
    CQ_SETTINGS_RESP("0075"),
    CQ_QUERY("0076"),
    CQ_QUERY_RESP("0077"),
    CQ_SENSOR("0078"),
    CQ_SENSOR_RESP("0079"),

    // GoPro Camera Management Service
    S_CAMERA_MANAGEMENT("0090"),
    CM_NET_MGMT_COMM("0091"),
    CN_NET_MGMT_RESP("0092");

    fun toUuid(): Uuid = if (this.base.length == 4) this.base.asGoProUuid() else uuidFrom(this.base)

    companion object {
        fun fromUuid(uuid: Uuid): GpUuid? = entries.firstOrNull { it.toUuid() == uuid }
    }
}

interface BleAdvertisement {
    val id: String // ID used to establish BLE connection from the advertisement.
    val name: String? // BLE Device name (i.e GP 1234). Global ID will come from the 4 digits.
}

interface BleDevice {
    val serialId: String
}

@OptIn(ExperimentalUnsignedTypes::class)
data class BleNotification(val uuid: Uuid, val data: UByteArray)

// TODO we don't need these (yet) but they will likely be useful at some point.
@OptIn(ExperimentalUnsignedTypes::class)
data class GpBleAdvertisement(
    val flags: List<Int>,
    val uuids: List<Uuid>,
    val manufacturingType: UByteArray,
    val companyId: Int,
    val cameraStatus: Int, // TODO parse this
    val cameraId: Int, // TODO parse this
    val cameraCapability: Int, // TODO parse this
    val idHash: UByteArray,
    val softtubesStatus: Int, // TODO parse this
) {
    companion object {
        fun fromUByteArray(bytes: UByteArray): GpBleAdvertisement = TODO()
    }
}

@OptIn(ExperimentalUnsignedTypes::class)
data class GpScanResponse(
    val name: String,
    val serviceUuid: Uuid,
    val macAddress: String,
    val serialNumber: String,
) {
    companion object {
        fun fromUByteArray(bytes: UByteArray): GpScanResponse = TODO()
    }
}