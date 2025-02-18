package com.gopro.open_gopro.di

import com.gopro.open_gopro.OgpSdkAppContext
import androidx.sqlite.driver.bundled.BundledSQLiteDriver
import com.gopro.open_gopro.database.AppDatabase
import com.gopro.open_gopro.database.CameraRepository
import com.gopro.open_gopro.database.IDatabaseProvider
import com.gopro.open_gopro.domain.data.ICameraRepository
import kotlinx.coroutines.CoroutineDispatcher
import org.koin.core.module.Module
import org.koin.dsl.module

internal interface OgpSdkPlatformModule {
    val module: Module
}

internal expect fun buildOgpSdkPlatformModule(appContext: OgpSdkAppContext): OgpSdkPlatformModule

private fun getRoomDatabase(
    provider: IDatabaseProvider,
    dispatcher: CoroutineDispatcher
): AppDatabase = provider.provideDatabase()
    .setDriver(BundledSQLiteDriver())
    .setQueryCoroutineContext(dispatcher)
    .build()

internal fun buildOgpSdkPlatformModules(appContext: OgpSdkAppContext) = module {
    includes(buildOgpSdkPlatformModule(appContext).module)

    // Note! We can't create HTTP engine / client singletons because they can be created dynamically
    // for various https credentials at run-time.

    single<AppDatabase> { getRoomDatabase(get(), get()) }
    single<ICameraRepository> { CameraRepository(get()) }
}