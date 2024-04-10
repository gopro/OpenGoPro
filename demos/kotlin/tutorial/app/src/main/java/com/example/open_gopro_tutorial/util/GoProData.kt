/* GoProData.kt/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Mon Mar  6 17:45:14 UTC 2023 */

package com.example.open_gopro_tutorial.util

import java.util.UUID

const val GOPRO_UUID = "0000FEA6-0000-1000-8000-00805f9b34fb"
const val GOPRO_BASE_UUID = "b5f9%s-aa8d-11e3-9046-0002a5d5c51b"

enum class GoProUUID(val uuid: UUID) {
    WIFI_AP_PASSWORD(UUID.fromString(GOPRO_BASE_UUID.format("0003"))),
    WIFI_AP_SSID(UUID.fromString(GOPRO_BASE_UUID.format("0002"))),
    CQ_COMMAND(UUID.fromString(GOPRO_BASE_UUID.format("0072"))),
    CQ_COMMAND_RSP(UUID.fromString(GOPRO_BASE_UUID.format("0073"))),
    CQ_SETTING(UUID.fromString(GOPRO_BASE_UUID.format("0074"))),
    CQ_SETTING_RSP(UUID.fromString(GOPRO_BASE_UUID.format("0075"))),
    CQ_QUERY(UUID.fromString(GOPRO_BASE_UUID.format("0076"))),
    CQ_QUERY_RSP(UUID.fromString(GOPRO_BASE_UUID.format("0077")));

    companion object {
        private val uuidToGoProUUID: Map<UUID, GoProUUID> by lazy { GoProUUID.values().associateBy { it.uuid } }
        fun fromUuid(uuid: UUID): GoProUUID? = uuidToGoProUUID[uuid]
        fun <T> mapByUuid(valueCreator: ((GoProUUID) -> T)): MutableMap<GoProUUID, T> =
            values().associateWith { valueCreator(it) }.toMutableMap()
    }
}

const val GOPRO_BASE_URL = "http://10.5.5.9:8080/"