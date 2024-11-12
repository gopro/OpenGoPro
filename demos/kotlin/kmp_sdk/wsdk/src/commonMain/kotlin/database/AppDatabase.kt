package database

import androidx.room.ConstructedBy
import androidx.room.Database
import androidx.room.RoomDatabase
import androidx.room.RoomDatabaseConstructor

data class SerialIdDb(
    val serialId: String
)

@Database(
    entities = [
        HttpsCredentialsDbEntry::class,
        CertificatesDbEntry::class,
        SsidDbEntry::class
    ],
    version = 1
)
@ConstructedBy(AppDatabaseConstructor::class)
abstract class AppDatabase : RoomDatabase() {
    abstract fun httpsCredentialsDao(): HttpsCredentialsDao
    abstract fun certificatesDao(): CertificatesDao
    abstract fun ssidDao(): SsidDao
}

// The Room compiler generates the `actual` implementations.
@Suppress("NO_ACTUAL_FOR_EXPECT")
expect object AppDatabaseConstructor : RoomDatabaseConstructor<AppDatabase> {
    override fun initialize(): AppDatabase
}

internal const val dbFileName = "ogp_wsdk.db"

interface IDatabaseProvider {
    fun provideDatabase(): RoomDatabase.Builder<AppDatabase>
}