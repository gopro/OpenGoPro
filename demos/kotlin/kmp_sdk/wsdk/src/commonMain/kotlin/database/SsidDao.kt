package database

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
    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insert(credentials: SsidDbEntry)

    @Query("SELECT * FROM SsidDbEntry WHERE serialId in (:ids)")
    suspend fun loadAll(vararg ids: String): List<SsidDbEntry>

    @Query("SELECT COUNT(*) as count FROM SsidDbEntry")
    suspend fun count(): Int

    @Delete(entity = SsidDbEntry::class)
    suspend fun delete(serialId: SerialIdDb)
}
