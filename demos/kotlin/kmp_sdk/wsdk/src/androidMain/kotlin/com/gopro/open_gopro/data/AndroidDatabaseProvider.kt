/* AndroidDatabaseProvider.kt/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Tue Feb 18 18:41:30 UTC 2025 */

package com.gopro.open_gopro.data

import android.content.Context
import androidx.room.Room
import androidx.room.RoomDatabase
import com.gopro.open_gopro.database.AppDatabase
import com.gopro.open_gopro.database.IDatabaseProvider

// https://developer.android.com/kotlin/multiplatform/room
internal class AndroidDatabaseProvider(private val context: Context) : IDatabaseProvider {
  override fun provideDatabase(): RoomDatabase.Builder<AppDatabase> {
    val appContext = context.applicationContext
    val dbFile = appContext.getDatabasePath("my_room.db")
    return Room.databaseBuilder<AppDatabase>(context = appContext, name = dbFile.absolutePath)
  }
}
