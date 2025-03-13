/* CertificatesDao.kt/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Tue Feb 18 18:41:29 UTC 2025 */

package com.gopro.open_gopro.database

import androidx.room.Dao
import androidx.room.Delete
import androidx.room.Entity
import androidx.room.Insert
import androidx.room.OnConflictStrategy
import androidx.room.PrimaryKey
import androidx.room.Query
import kotlinx.serialization.Serializable

// TODO this should be a one-to-many. I'm using this JSON serialization hack since I don't know
// anything about databases

@Serializable internal data class CertificatesForDb(val certificates: List<String>)

@Entity
internal data class CertificatesDbEntry(
    @PrimaryKey(autoGenerate = false) val serialId: String,
    val certificates: String
)

@Dao
internal interface CertificatesDao {
  @Insert(onConflict = OnConflictStrategy.REPLACE)
  suspend fun insert(credentials: CertificatesDbEntry)

  @Query("SELECT * FROM CertificatesDbEntry WHERE serialId in (:ids)")
  suspend fun loadAll(vararg ids: String): List<CertificatesDbEntry>

  @Query("SELECT COUNT(*) as count FROM CertificatesDbEntry") suspend fun count(): Int

  @Delete(entity = CertificatesDbEntry::class) suspend fun delete(serialId: SerialIdDb)
}
