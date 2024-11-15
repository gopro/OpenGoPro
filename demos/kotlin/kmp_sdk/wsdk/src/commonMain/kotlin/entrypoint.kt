import di.buildPackageModules
import domain.connector.ICameraConnector
import domain.gopro.IGoProFactory
import entity.connector.ConnectionRequestContext
import entity.connector.GoProId
import entity.connector.NetworkType
import entity.connector.ScanResult
import kotlinx.coroutines.CoroutineDispatcher
import kotlinx.coroutines.flow.Flow
import org.koin.core.Koin
import org.koin.core.KoinApplication
import org.koin.core.module.Module
import org.koin.dsl.koinApplication

expect class WsdkAppContext

// https://insert-koin.io/docs/reference/koin-core/context-isolation
// https://medium.com/@gusakov.giorgi/using-koin-dependency-injection-in-library-sdk-7be76291ecad
internal object WsdkIsolatedKoinContext {

    private var koinApp: KoinApplication? = null
    internal var koinModules: Module? = null

    fun init(dispatcher: CoroutineDispatcher, appContext: WsdkAppContext) {
        koinModules = buildPackageModules(dispatcher, appContext)
        koinApp = koinApplication { modules(koinModules!!) }
    }

    fun getWsdkKoinApp(): Koin =
        koinApp?.koin ?: throw Exception("WSDK has not yet been initialized")
}

// TODO how / should we handle multiple SDK's
class Wsdk(dispatcher: CoroutineDispatcher, appContext: WsdkAppContext) {
    init {
        WsdkIsolatedKoinContext.init(dispatcher, appContext)
    }

    private val goProFactory: IGoProFactory = WsdkIsolatedKoinContext.getWsdkKoinApp().get()
    private val cameraConnector: ICameraConnector = WsdkIsolatedKoinContext.getWsdkKoinApp().get()

    suspend fun discover(vararg networkTypes: NetworkType): Flow<ScanResult> =
        cameraConnector.discover(*networkTypes)

    suspend fun connect(
        target: ScanResult,
        connectionRequestContext: ConnectionRequestContext? = null
    ): Result<GoProId> = cameraConnector.connect(target, connectionRequestContext).map {
        goProFactory.storeConnection(it)
        it.id
    }

    suspend fun getGoPro(id: GoProId) = goProFactory.getGoPro(id)
}