import co.touchlab.kermit.Logger
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
import org.koin.core.context.startKoin
import org.koin.core.error.ApplicationAlreadyStartedException
import org.koin.core.module.Module
import org.koin.dsl.koinApplication

expect class WsdkAppContext

private val logger = Logger.withTag("WSDK")

// https://insert-koin.io/docs/reference/koin-core/context-isolation
// https://medium.com/@gusakov.giorgi/using-koin-dependency-injection-in-library-sdk-7be76291ecad
internal object WsdkIsolatedKoinContext {
    private data class InitArguments(
        val dispatcher: CoroutineDispatcher, val appContext: WsdkAppContext
    )

    private var initArguments: InitArguments? = null

    private val koinApp: KoinApplication by lazy {
        koinApplication { modules(koinModules) }.also { app ->
            try {
                startKoin(app)
                logger.d("Started KOIN from WSDK since it was not running.")
            } catch (_: ApplicationAlreadyStartedException) {
                logger.d("Not starting Koin from WSDK since it was already started")
            }
        }
    }
    internal val koinModules: Module by lazy {
        initArguments?.let { args ->
            buildPackageModules(args.dispatcher, args.appContext)
        } ?: throw Exception("WSDK has not been initialized")
    }

    fun init(dispatcher: CoroutineDispatcher, appContext: WsdkAppContext) {
        initArguments = InitArguments(dispatcher, appContext)
    }

    fun getWsdkKoinApp(): Koin = koinApp.koin
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
        target: ScanResult, connectionRequestContext: ConnectionRequestContext? = null
    ): Result<GoProId> = cameraConnector.connect(target, connectionRequestContext).map {
        goProFactory.storeConnection(it)
        it.id
    }

    suspend fun getGoPro(id: GoProId) = goProFactory.getGoPro(id)
}