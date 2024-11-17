package data

import androidx.room.RoomDatabase
import database.AppDatabase
import database.IDatabaseProvider

// https://developer.android.com/kotlin/multiplatform/room
internal class AppleDatabaseProvider() : IDatabaseProvider {
    override fun provideDatabase(): RoomDatabase.Builder<AppDatabase> {
        TODO()
    }
}