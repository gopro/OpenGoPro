/* Tutorial.kt/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Mon Mar  6 17:45:15 UTC 2023 */

package com.example.open_gopro_tutorial.tutorials

import com.example.open_gopro_tutorial.AppContainer
import java.io.File

abstract class Tutorial(
    private val number: Int, private val name: String, prerequisites: List<Prerequisite>
) {
    enum class Prerequisite {
        BLE_CONNECTED, WIFI_CONNECTED
    }

    val requiresBle = Prerequisite.BLE_CONNECTED in prerequisites
    val requiresWifi = Prerequisite.WIFI_CONNECTED in prerequisites

    override fun toString(): String {
        return "Tutorial $number: $name"
    }

    abstract suspend fun perform(appContainer: AppContainer): File?
}

val Tutorials = listOf(
    Tutorial1ConnectBle(1, "Connect BLE", emptyList()),
    Tutorial2SendBleCommands(2, "Send BLE Commands", listOf(Tutorial.Prerequisite.BLE_CONNECTED)),
    Tutorial3ParseBleTlvResponses(3, "Parse BLE TLV Responses", listOf(Tutorial.Prerequisite.BLE_CONNECTED)),
    Tutorial4BleQueries(4, "BLE Queries", listOf(Tutorial.Prerequisite.BLE_CONNECTED)),
    Tutorial5ConnectWifi(5, "Connect Wifi", listOf(Tutorial.Prerequisite.BLE_CONNECTED)),
    Tutorial6SendWifiCommands(6, "Send Wifi Commands",listOf(Tutorial.Prerequisite.WIFI_CONNECTED)),
    Tutorial7CameraMediaList(7, "Camera Media List", listOf(Tutorial.Prerequisite.WIFI_CONNECTED))
)