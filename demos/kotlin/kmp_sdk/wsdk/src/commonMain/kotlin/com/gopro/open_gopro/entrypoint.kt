package com.gopro.open_gopro

import co.touchlab.kermit.Logger
import com.gopro.open_gopro.di.buildPackageModules
import com.gopro.open_gopro.domain.connector.ICameraConnector
import com.gopro.open_gopro.domain.gopro.IGoProFactory
import com.gopro.open_gopro.entity.connector.ConnectionRequestContext
import com.gopro.open_gopro.entity.connector.GoProId
import com.gopro.open_gopro.entity.connector.NetworkType
import com.gopro.open_gopro.entity.connector.ScanResult
import com.gopro.open_gopro.gopro.GoPro
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

/**
 * The top level SDK interface
 *
 * The client should use this class to discover, connect, and retrieve [GoPro] objects
 *
 * TODO currently multiple instances of WSDK are not supported and have not been tested.
 *
 * ```
 * // Initialize WSDK
 * val wsdk = Wsdk(dispatcher, appContext)
 *
 * coroutineScope.launch {
 *     // Discover and take the first device we find
 *     val target = wsdk.discover(NetworkType.BLE).first()
 *
 *     // Connect
 *     val goproId = wsdk.connect(target).getOrThrow()
 *
 *     // Now retrieve the gopro
 *     val gopro = wsdk.getGoPro(goproId)
 *
 *     // Set the shutter
 *     gopro.commands.setShutter(true)
 * }
 * ```
 *
 * @param dispatcher dispatcher that WSDK should use for coroutine scopes
 * @param appContext platform-specific application context
 */
class Wsdk(dispatcher: CoroutineDispatcher, appContext: WsdkAppContext) {
    // TODO how / should we handle multiple SDK's
    init {
        WsdkIsolatedKoinContext.init(dispatcher, appContext)
    }

    private val goProFactory: IGoProFactory = WsdkIsolatedKoinContext.getWsdkKoinApp().get()
    private val cameraConnector: ICameraConnector = WsdkIsolatedKoinContext.getWsdkKoinApp().get()

    /**
     * Scan for available GoPro's on one or more network types
     *
     * @param networkTypes network types to scan on
     * @return flow of GoPro's discovered per-network
     */
    suspend fun discover(vararg networkTypes: NetworkType): Flow<ScanResult> =
        cameraConnector.discover(*networkTypes)

    /**
     * Establish a connection to a discovered GoPro
     *
     * @param target discovered GoPro to connect to
     * @param connectionRequestContext additional per-network-type connection request information
     * @return ID of connected GoPro
     */
    suspend fun connect(
        target: ScanResult, connectionRequestContext: ConnectionRequestContext? = null
    ): Result<GoProId> = cameraConnector.connect(target, connectionRequestContext).map {
        goProFactory.storeConnection(it)
        it.id
    }

    /**
     * Retrieve a connected GoPro instance
     *
     * The GoPro referenced by [id] must have first been connected with [connect]
     *
     * @param id
     */
    suspend fun getGoPro(id: GoProId) = goProFactory.getGoPro(id)
}