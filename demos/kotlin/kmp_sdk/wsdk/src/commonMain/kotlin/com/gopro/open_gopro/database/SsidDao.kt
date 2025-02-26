/* SsidDao.kt/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Tue Feb 18 18:41:29 UTC 2025 */

package com.gopro.open_gopro.database

import androidx.room.Dao
import androidx.room.Delete
import androidx.room.Entity
import androidx.room.Insert
import androidx.room.OnConflictStrategy
import androidx.room.PrimaryKey
import androidx.room.Query

@Entity
internal data class SsidDbEntry(
    @PrimaryKey(autoGenerate = false) val serialId: String,
    val ssid: String,
    val password: String
)

@Dao
internal interface SsidDao {
  @Insert(onConflict = OnConflictStrategy.REPLACE) suspend fun insert(credentials: SsidDbEntry)

  @Query("SELECT * FROM SsidDbEntry WHERE serialId in (:ids)")
  suspend fun loadAll(vararg ids: String): List<SsidDbEntry>

  @Query("SELECT COUNT(*) as count FROM SsidDbEntry") suspend fun count(): Int

  @Delete(entity = SsidDbEntry::class) suspend fun delete(serialId: SerialIdDb)
}
