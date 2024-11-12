package database

import androidx.room.Dao
import androidx.room.Delete
import androidx.room.Entity
import androidx.room.Insert
import androidx.room.OnConflictStrategy
import androidx.room.PrimaryKey
import androidx.room.Query

@Entity
data class HttpsCredentialsDbEntry(
    @PrimaryKey(autoGenerate = false) val serialId: String,
    val username: String,
    val password: String,
)

@Dao
interface HttpsCredentialsDao {
    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insert(credentials: HttpsCredentialsDbEntry)

    @Query("SELECT * FROM HttpsCredentialsDbEntry WHERE serialId in (:ids)")
    suspend fun loadAll(vararg ids: String): List<HttpsCredentialsDbEntry>

    @Query("SELECT COUNT(*) as count FROM HttpsCredentialsDbEntry")
    suspend fun count(): Int

    @Delete(entity = HttpsCredentialsDbEntry::class)
    suspend fun delete(serialId: SerialIdDb)
}
