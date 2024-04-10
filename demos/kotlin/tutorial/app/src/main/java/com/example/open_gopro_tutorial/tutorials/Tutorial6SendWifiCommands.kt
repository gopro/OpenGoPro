/* Tutorial6SendWifiCommands.kt/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Mon Mar  6 17:45:14 UTC 2023 */

package com.example.open_gopro_tutorial.tutorials

import androidx.annotation.RequiresPermission
import com.example.open_gopro_tutorial.AppContainer
import com.example.open_gopro_tutorial.util.GOPRO_BASE_URL
import com.example.open_gopro_tutorial.util.prettyJson
import kotlinx.coroutines.delay
import kotlinx.serialization.encodeToString
import timber.log.Timber
import java.io.File

class Tutorial6SendWifiCommands(number: Int, name: String, prerequisites: List<Prerequisite>) :
    Tutorial(number, name, prerequisites) {
    @RequiresPermission(allOf = ["android.permission.BLUETOOTH_SCAN", "android.permission.BLUETOOTH_CONNECT"])
    override suspend fun perform(appContainer: AppContainer): File? {
        val wifi = appContainer.wifi

        // Get Camera State
        Timber.i("Getting camera state")
        var response = wifi.get(GOPRO_BASE_URL + "gopro/camera/state")
        Timber.i(prettyJson.encodeToString(response))

        // Load Preset Group
        Timber.i("Loading Video Preset Group")
        response = wifi.get(GOPRO_BASE_URL + "gopro/camera/presets/load?id=1000")
        Timber.i(prettyJson.encodeToString(response))

        // Set Shutter
        Timber.i("Setting Shutter On")
        response = wifi.get(GOPRO_BASE_URL + "gopro/camera/shutter/start")
        Timber.i(prettyJson.encodeToString(response))

        delay(4000)

        // Set Shutter
        Timber.i("Attempting to Set Shutter Off")
        response = wifi.get(GOPRO_BASE_URL + "gopro/camera/shutter/stop")
        Timber.i(prettyJson.encodeToString(response))

        delay(4000)

        // Set Resolution
        Timber.i("Setting Resolution to 1080")
        response = wifi.get(GOPRO_BASE_URL + "gopro/camera/setting?setting=2&option=9")
        Timber.i(prettyJson.encodeToString(response))

//        // Start Preview Stream
//        Timber.i("Start Livestream")
//        response = wifi.get(GOPRO_BASE_URL + "gopro/camera/stream/start")
//        Timber.i(prettyJson.encodeToString(response))

        return null
    }
}