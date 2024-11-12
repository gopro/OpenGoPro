package database

import androidx.room.Dao
import androidx.room.Delete
import androidx.room.Entity
import androidx.room.Insert
import androidx.room.OnConflictStrategy
import androidx.room.PrimaryKey
import androidx.room.Query
import kotlinx.serialization.Serializable

// TODO this should be a one-to-many. I'm using this JSON serialization hack since I don't know anything about databases

@Serializable
data class CertificatesForDb(
    val certificates: List<String>
)


@Entity
data class CertificatesDbEntry(
    @PrimaryKey(autoGenerate = false) val serialId: String,
    val certificates: String
)

@Dao
interface CertificatesDao {
    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insert(credentials: CertificatesDbEntry)

    @Query("SELECT * FROM CertificatesDbEntry WHERE serialId in (:ids)")
    suspend fun loadAll(vararg ids: String): List<CertificatesDbEntry>

    @Query("SELECT COUNT(*) as count FROM CertificatesDbEntry")
    suspend fun count(): Int

    @Delete(entity = CertificatesDbEntry::class)
    suspend fun delete(serialId: SerialIdDb)
}
