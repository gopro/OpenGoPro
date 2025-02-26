/* AppDatabase.kt/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Tue Feb 18 18:41:29 UTC 2025 */

package com.gopro.open_gopro.database

import androidx.room.ConstructedBy
import androidx.room.Database
import androidx.room.RoomDatabase
import androidx.room.RoomDatabaseConstructor

internal data class SerialIdDb(val serialId: String)

@Database(
    entities = [HttpsCredentialsDbEntry::class, CertificatesDbEntry::class, SsidDbEntry::class],
    version = 1)
@ConstructedBy(AppDatabaseConstructor::class)
internal abstract class AppDatabase : RoomDatabase() {
  abstract fun httpsCredentialsDao(): HttpsCredentialsDao

  abstract fun certificatesDao(): CertificatesDao

  abstract fun ssidDao(): SsidDao
}

// The Room compiler generates the `actual` implementations.
@Suppress("NO_ACTUAL_FOR_EXPECT")
internal expect object AppDatabaseConstructor : RoomDatabaseConstructor<AppDatabase> {
  override fun initialize(): AppDatabase
}

internal const val dbFileName = "ogp_sdk.db"

internal interface IDatabaseProvider {
  fun provideDatabase(): RoomDatabase.Builder<AppDatabase>
}
