import di.buildPackageModules
import entity.connector.ICameraConnector
import gopro.IGoProFacadeFactory
import kotlinx.coroutines.CoroutineDispatcher
import org.koin.core.Koin
import org.koin.core.KoinApplication
import org.koin.core.module.Module
import org.koin.dsl.koinApplication

expect object AppContext

// https://insert-koin.io/docs/reference/koin-core/context-isolation
internal object WsdkIsolatedKoinContext {

    private var koinApp: KoinApplication? = null
    internal var koinModules: Module? = null

    fun init(dispatcher: CoroutineDispatcher, appContext: AppContext) {
        // TODO handle multiple inits

        koinModules = buildPackageModules(dispatcher, appContext).also { modules ->
            koinApp = koinApplication {
                modules(modules)
            }
        }
    }

    fun getWsdkKoinApp(): Koin? = koinApp?.koin
}

object Wsdk {
    // https://medium.com/@gusakov.giorgi/using-koin-dependency-injection-in-library-sdk-7be76291ecad

    fun init(dispatcher: CoroutineDispatcher, appContext: AppContext) =
        WsdkIsolatedKoinContext.init(dispatcher, appContext)

    fun getCameraConnector(): ICameraConnector =
        WsdkIsolatedKoinContext.getWsdkKoinApp()?.get()
            ?: throw Exception("Wsdk has not yet been initialized")

    fun getGoProFacadeFactory(): IGoProFacadeFactory =
        WsdkIsolatedKoinContext.getWsdkKoinApp()?.get()
            ?: throw Exception("Wsdk has not yet been initialized")
}