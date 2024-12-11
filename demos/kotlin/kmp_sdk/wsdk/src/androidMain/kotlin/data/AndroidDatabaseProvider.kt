package data

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
        return Room.databaseBuilder<AppDatabase>(
            context = appContext,
            name = dbFile.absolutePath
        )
    }
}