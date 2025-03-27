/* entrypoint.kt/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Tue Feb 18 18:41:28 UTC 2025 */

package com.gopro.open_gopro

import co.touchlab.kermit.Logger
import com.gopro.open_gopro.di.buildPackageModules
import com.gopro.open_gopro.domain.connector.ICameraConnector
import com.gopro.open_gopro.domain.gopro.IGoProFactory
import com.gopro.open_gopro.gopro.GoPro
import kotlinx.coroutines.CoroutineDispatcher
import kotlinx.coroutines.flow.Flow
import org.koin.core.Koin
import org.koin.core.KoinApplication
import org.koin.core.context.startKoin
import org.koin.core.error.KoinApplicationAlreadyStartedException
import org.koin.core.module.Module
import org.koin.dsl.koinApplication

/** Platform-specific context needed to initialize the OGP SDK */
expect class OgpSdkAppContext

private val logger = Logger.withTag("OGP SDK")

// https://insert-koin.io/docs/reference/koin-core/context-isolation
// https://medium.com/@gusakov.giorgi/using-koin-dependency-injection-in-library-sdk-7be76291ecad
internal object OgpSdkIsolatedKoinContext {
  private data class InitArguments(
      val dispatcher: CoroutineDispatcher,
      val appContext: OgpSdkAppContext
  )

  private var initArguments: InitArguments? = null

  private val koinApp: KoinApplication by lazy {
    koinApplication { modules(koinModules) }
        .also { app ->
          try {
            startKoin(app)
            logger.d("Started KOIN from OGP SDK since it was not running.")
          } catch (_: KoinApplicationAlreadyStartedException) {
            logger.d("Not starting Koin from OGP SDK since it was already started")
          }
        }
  }
  internal val koinModules: Module by lazy {
    initArguments?.let { args -> buildPackageModules(args.dispatcher, args.appContext) }
        ?: throw Exception("OGP SDK has not been initialized")
  }

  fun init(dispatcher: CoroutineDispatcher, appContext: OgpSdkAppContext) {
    initArguments = InitArguments(dispatcher, appContext)
  }

  fun getOgpSdkKoinApp(): Koin = koinApp.koin
}

/**
 * The top level SDK interface
 *
 * The client should use this class to discover, connect, and retrieve [GoPro] objects
 * > TODO currently multiple instances of OGP SDK are not supported and have not been tested.
 *
 * ```
 * // Initialize OGP SDK
 * val ogpSdk = OgpSdk(dispatcher, appContext)
 *
 * coroutineScope.launch {
 *     // Discover and take the first device we find
 *     val target = ogpSdk.discover(NetworkType.BLE).first()
 *
 *     // Connect
 *     val goproId = ogpSdk.connect(target).getOrThrow()
 *
 *     // Now retrieve the gopro
 *     val gopro = ogpSdk.getGoPro(goproId)
 *
 *     // Set the shutter
 *     gopro.commands.setShutter(true)
 * }
 * ```
 *
 * @param dispatcher dispatcher that OGP SDK should use for coroutine scopes
 * @param appContext platform-specific application context
 */
class OgpSdk(dispatcher: CoroutineDispatcher, appContext: OgpSdkAppContext) {
  // TODO how / should we handle multiple SDK's
  init {
    OgpSdkIsolatedKoinContext.init(dispatcher, appContext)
  }

  private val goProFactory: IGoProFactory = OgpSdkIsolatedKoinContext.getOgpSdkKoinApp().get()
  private val cameraConnector: ICameraConnector = OgpSdkIsolatedKoinContext.getOgpSdkKoinApp().get()

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
      target: ScanResult,
      connectionRequestContext: ConnectionRequestContext? = null
  ): Result<GoProId> =
      cameraConnector.connect(target, connectionRequestContext).map {
        goProFactory.storeConnection(it)
        it.id
      }

  /**
   * Retrieve a connected GoPro instance
   *
   * The GoPro referenced by [id] must have first been connected with [connect]
   *
   * @param id
   * @return [GoPro] if a connection is found matching the [id]
   */
  suspend fun getGoPro(id: GoProId) = goProFactory.getGoPro(id)
}
