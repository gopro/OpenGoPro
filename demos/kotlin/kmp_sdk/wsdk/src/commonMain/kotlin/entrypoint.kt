import di.buildPackageModules
import domain.connector.ICameraConnector
import domain.gopro.IGoProFacadeFactory
import kotlinx.coroutines.CoroutineDispatcher
import org.koin.core.Koin
import org.koin.core.KoinApplication
import org.koin.core.module.Module
import org.koin.dsl.koinApplication

expect class WsdkAppContext

// https://insert-koin.io/docs/reference/koin-core/context-isolation
internal object WsdkIsolatedKoinContext {

    private var koinApp: KoinApplication? = null
    internal var koinModules: Module? = null

    fun init(dispatcher: CoroutineDispatcher, appContext: WsdkAppContext) {
        // TODO handle multiple inits
        koinModules = buildPackageModules(dispatcher, appContext)
        koinApp = koinApplication { modules(koinModules!!) }
    }

    fun getWsdkKoinApp(): Koin =
        koinApp?.koin ?: throw Exception("WSDK has not yet been initialized")
}

object Wsdk {
    // https://medium.com/@gusakov.giorgi/using-koin-dependency-injection-in-library-sdk-7be76291ecad

    fun init(dispatcher: CoroutineDispatcher, appContext: WsdkAppContext) =
        WsdkIsolatedKoinContext.init(dispatcher, appContext)


    fun getCameraConnector(): ICameraConnector = WsdkIsolatedKoinContext.getWsdkKoinApp().get()

    fun getGoProFacadeFactory(): IGoProFacadeFactory =
        WsdkIsolatedKoinContext.getWsdkKoinApp().get()
}