/* Tutorial7CameraMediaList.kt/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Mon Mar  6 17:45:15 UTC 2023 */

package com.example.open_gopro_tutorial.tutorials

import androidx.annotation.RequiresPermission
import com.example.open_gopro_tutorial.AppContainer
import com.example.open_gopro_tutorial.util.GOPRO_BASE_URL
import com.example.open_gopro_tutorial.util.prettyJson
import kotlinx.serialization.encodeToString
import kotlinx.serialization.json.jsonArray
import kotlinx.serialization.json.jsonObject
import timber.log.Timber
import java.io.File

class Tutorial7CameraMediaList(number: Int, name: String, prerequisites: List<Prerequisite>) :
    Tutorial(number, name, prerequisites) {
    @RequiresPermission(allOf = ["android.permission.BLUETOOTH_SCAN", "android.permission.BLUETOOTH_CONNECT"])
    override suspend fun perform(appContainer: AppContainer): File? {
        val wifi = appContainer.wifi

        // Get the media list
        val response = wifi.get(GOPRO_BASE_URL + "gopro/media/list")
        Timber.i("Complete media list: ${prettyJson.encodeToString(response)}")

        // Get a list of file names from the media list JSON response
        val fileList =
            response["media"]?.jsonArray?.first()?.jsonObject?.get("fs")?.jsonArray?.map { mediaEntry ->
                mediaEntry.jsonObject["n"]
            }?.map { it.toString().replace("\"", "") }
        Timber.i("Files in media list: ${prettyJson.encodeToString(fileList)}")

        // Find a .jpg
        val photo = fileList?.firstOrNull { it.endsWith(ignoreCase = true, suffix = "jpg") }
            ?: throw Exception("Not able to find a .jpg in the media list")
        Timber.i("Found a photo: $photo")

        // Download the photo
        Timber.i("Downloading photo: $photo...")
        return wifi.getFile(
            GOPRO_BASE_URL + "videos/DCIM/100GOPRO/$photo", appContainer.applicationContext
        )
    }
}