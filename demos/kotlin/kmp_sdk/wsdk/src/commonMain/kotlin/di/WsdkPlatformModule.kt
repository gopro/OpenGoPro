package di

import WsdkAppContext
import androidx.sqlite.driver.bundled.BundledSQLiteDriver
import database.AppDatabase
import database.CameraRepository
import database.IDatabaseProvider
import domain.data.ICameraRepository
import kotlinx.coroutines.CoroutineDispatcher
import org.koin.core.module.Module
import org.koin.dsl.module

internal interface WsdkPlatformModule {
    val module: Module
}

internal expect fun buildWsdkPlatformModule(appContext: WsdkAppContext): WsdkPlatformModule

private fun getRoomDatabase(
    provider: IDatabaseProvider,
    dispatcher: CoroutineDispatcher
): AppDatabase = provider.provideDatabase()
    .setDriver(BundledSQLiteDriver())
    .setQueryCoroutineContext(dispatcher)
    .build()

internal fun buildWsdkPlatformModules(appContext: WsdkAppContext) = module {
    includes(buildWsdkPlatformModule(appContext).module)

    // Note! We can't create HTTP engine / client singletons because they can be created dynamically
    // for various https credentials at run-time.

    single<AppDatabase> { getRoomDatabase(get(), get()) }
    single<ICameraRepository> { CameraRepository(get()) }
}