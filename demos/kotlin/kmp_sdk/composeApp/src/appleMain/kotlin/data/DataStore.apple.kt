/* DataStore.apple.kt/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Tue Feb 18 18:41:27 UTC 2025 */

package data

import androidx.datastore.core.DataStore
import androidx.datastore.preferences.core.Preferences
import kotlinx.cinterop.ExperimentalForeignApi
import platform.Foundation.NSDocumentDirectory
import platform.Foundation.NSFileManager
import platform.Foundation.NSURL
import platform.Foundation.NSUserDomainMask

@OptIn(ExperimentalForeignApi::class)
fun dataStore(): DataStore<Preferences> =
    createDataStore(
        producePath = {
          val documentDirectory: NSURL? =
              NSFileManager.defaultManager.URLForDirectory(
                  directory = NSDocumentDirectory,
                  inDomain = NSUserDomainMask,
                  appropriateForURL = null,
                  create = false,
                  error = null,
              )
          requireNotNull(documentDirectory).path + "/$dataStoreFileName"
        })
