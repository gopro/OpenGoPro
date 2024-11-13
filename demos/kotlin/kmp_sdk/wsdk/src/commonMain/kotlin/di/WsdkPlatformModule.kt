package di

import AppContext
import Wsdk
import androidx.sqlite.driver.bundled.BundledSQLiteDriver
import database.AppDatabase
import database.CameraRepository
import database.IDatabaseProvider
import domain.data.ICameraRepository
import entity.network.IHttpsCredentials
import io.ktor.client.HttpClient
import io.ktor.client.engine.HttpClientEngine
import kotlinx.coroutines.CoroutineDispatcher
import org.koin.core.module.Module
import org.koin.dsl.module

internal interface WsdkPlatformModule {
    val module: Module
}

internal expect fun buildWsdkPlatformModule(appContext: AppContext): WsdkPlatformModule

private fun getRoomDatabase(
    provider: IDatabaseProvider,
    dispatcher: CoroutineDispatcher
): AppDatabase = provider.provideDatabase()
    .setDriver(BundledSQLiteDriver())
    .setQueryCoroutineContext(dispatcher)
    .build()

internal fun buildWsdkPlatformModules(appContext: AppContext) = module {
    includes(buildWsdkPlatformModule(appContext).module)

    // Note! We can't create HTTP engine / client singletons because they can be created dynamically
    // for various https credentials at run-time.

    single<AppDatabase> { getRoomDatabase(get(), get()) }
    single<ICameraRepository> { CameraRepository(get()) }
}