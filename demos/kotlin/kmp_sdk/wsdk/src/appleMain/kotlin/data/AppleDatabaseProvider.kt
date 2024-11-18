package data

import androidx.room.Room
import androidx.room.RoomDatabase
import database.AppDatabase
import database.IDatabaseProvider
import kotlinx.cinterop.ExperimentalForeignApi
import platform.Foundation.NSDocumentDirectory
import platform.Foundation.NSFileManager
import platform.Foundation.NSUserDomainMask

// https://developer.android.com/kotlin/multiplatform/room
internal class AppleDatabaseProvider() : IDatabaseProvider {
    @OptIn(ExperimentalForeignApi::class)
    private fun documentDirectory(): String {
        val documentDirectory = NSFileManager.defaultManager.URLForDirectory(
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