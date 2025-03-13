/* AppleDatabaseProvider.kt/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Tue Feb 18 18:41:30 UTC 2025 */

package com.gopro.open_gopro.data

import androidx.room.Room
import androidx.room.RoomDatabase
import com.gopro.open_gopro.database.AppDatabase
import com.gopro.open_gopro.database.IDatabaseProvider
import kotlinx.cinterop.ExperimentalForeignApi
import platform.Foundation.NSDocumentDirectory
import platform.Foundation.NSFileManager
import platform.Foundation.NSUserDomainMask

// https://developer.android.com/kotlin/multiplatform/room
internal class AppleDatabaseProvider() : IDatabaseProvider {
  @OptIn(ExperimentalForeignApi::class)
  private fun documentDirectory(): String {
    val documentDirectory =
        NSFileManager.defaultManager.URLForDirectory(
            directory = NSDocumentDirectory,
            inDomain = NSUserDomainMask,
            appropriateForURL = null,
            create = false,
            error = null,
        )
    return requireNotNull(documentDirectory?.path)
  }

  override fun provideDatabase(): RoomDatabase.Builder<AppDatabase> {
    // TODO make the database file a constant in a shared location
    val dbFilePath = documentDirectory() + "/my_room.db"
    return Room.databaseBuilder<AppDatabase>(
        name = dbFilePath,
    )
  }
}
