package di

import org.koin.core.KoinApplication
import org.koin.dsl.KoinAppDeclaration
import org.koin.dsl.koinApplication

// Get a Context for your Koin instance
object WsdkIsolatedKoinContext {

    private val koinApp = koinApplication {
        modules(packageModule)
    }

    fun getWsdkKoinApp(config: KoinAppDeclaration?): KoinApplication {
        config?.invoke(koinApp)
        return koinApp
    }
}