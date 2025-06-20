/* GoProFacade.kt/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Tue Feb 18 18:41:30 UTC 2025 */

package com.gopro.open_gopro.gopro

import co.touchlab.kermit.Logger
import com.gopro.open_gopro.CommunicationType
import com.gopro.open_gopro.GoProId
import com.gopro.open_gopro.OgpSdk
import com.gopro.open_gopro.OgpSdkIsolatedKoinContext
import com.gopro.open_gopro.domain.communicator.BleCommunicator
import com.gopro.open_gopro.domain.communicator.HttpCommunicator
import com.gopro.open_gopro.domain.communicator.ICommunicator
import com.gopro.open_gopro.domain.connector.ICameraConnector
import com.gopro.open_gopro.domain.gopro.IGoProFactory
import com.gopro.open_gopro.operations.AccessPointState
import com.gopro.open_gopro.operations.CohnState
import com.gopro.open_gopro.operations.GpMarshaller
import kotlin.time.DurationUnit
import kotlin.time.toDuration
import kotlinx.coroutines.CoroutineDispatcher
import kotlinx.coroutines.CoroutineExceptionHandler
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.delay
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.combine
import kotlinx.coroutines.flow.mapNotNull
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch
import kotlinx.datetime.Clock
import kotlinx.datetime.Instant
import kotlinx.datetime.LocalDateTime
import kotlinx.datetime.TimeZone
import kotlinx.datetime.offsetAt
import kotlinx.datetime.toLocalDateTime

private const val TRACE_LOG = true

/**
 * Top level interface to communicate with a connected GoPro.
 *
 * Should be retrieved from [OgpSdk.getGoPro]
 *
 * @property id identifier of connected GoPro
 */
class GoPro internal constructor(override val id: GoProId) : IGpDescriptor {
  private val logger = Logger.withTag(id.toString())

  private fun traceLog(message: String) = if (TRACE_LOG) logger.d(message) else {}

  private val cameraConnector: ICameraConnector = OgpSdkIsolatedKoinContext.getOgpSdkKoinApp().get()
  private val dispatcher: CoroutineDispatcher = OgpSdkIsolatedKoinContext.getOgpSdkKoinApp().get()
  private val facadeFactory: IGoProFactory = OgpSdkIsolatedKoinContext.getOgpSdkKoinApp().get()

  private val operationMarshaller = GpMarshaller(this)

  private val coroutineExceptionHandler = CoroutineExceptionHandler { _, throwable ->
    logger.e("Caught exception in coroutine:", throwable)
  }

  private val scope = CoroutineScope(dispatcher + coroutineExceptionHandler)

  override val communicators: List<CommunicationType>
    get() = operationMarshaller.communicators

  /** Container delegate to access all camera commands */
  val commands = CommandsContainer(operationMarshaller)

  /** Container delegate to access all camera settings */
  val settings = SettingsContainer(operationMarshaller)

  /** Container delegate to access all camera statuses */
  val statuses = StatusesContainer(operationMarshaller)

  /** Container delegate to access all camera features */
  val features = FeaturesContainer(FeatureContext(this, cameraConnector, facadeFactory, scope))

  private var _ipAddress: String? = null
  override val ipAddress: String?
    get() = _ipAddress

  private val _isBusy: MutableStateFlow<Boolean> = MutableStateFlow(true)
  override val isBusy: StateFlow<Boolean>
    get() = _isBusy

  private val _isEncoding: MutableStateFlow<Boolean> = MutableStateFlow(true)
  override val isEncoding: StateFlow<Boolean>
    get() = _isEncoding

  private val _isReady: MutableStateFlow<Boolean> = MutableStateFlow(true)
  override val isReady: StateFlow<Boolean>
    get() = _isReady

  override val accessPointState: StateFlow<AccessPointState> = features.accessPoint.state

  override val cohnState: StateFlow<CohnState> = features.cohn.state

  // TODO do we need network type instead of communication type?
  private val _disconnects = MutableStateFlow<CommunicationType?>(null)
  override val disconnects: Flow<CommunicationType>
    get() = _disconnects.mapNotNull { it }

  private var isInitialized = false

  override val isBleAvailable: Boolean
    get() = CommunicationType.BLE in communicators

  override val isHttpAvailable: Boolean
    get() = CommunicationType.HTTP in communicators

  internal fun unbindCommunicator(communicator: ICommunicator<*>) {
    operationMarshaller.removeCommunicator(communicator)
    if (communicator.communicationType == CommunicationType.BLE) {
      // Clear this so we restart state management if / when BLE connects again.
      isInitialized = false
    }
    scope.launch { _disconnects.emit(communicator.communicationType) }
  }

  private suspend fun initializeStateManagement(communicator: ICommunicator<*>) {
    logger.d("Setting up GoPro state management.")
    when (communicator) {
      is BleCommunicator -> {
        logger.d("Setting up BLE state management")
        // Start collecting read statuses
        scope.launch {
          statuses.busy.registerValueUpdate().onSuccess { flow ->
            flow.collect { isBusy ->
              traceLog("isBusy update: $isBusy")
              _isBusy.update { isBusy }
            }
          }
        }
        scope.launch {
          statuses.encoding.registerValueUpdate().onSuccess { flow ->
            flow.collect { isEncoding ->
              traceLog("isEncoding update: $isEncoding")
              _isEncoding.update { isEncoding }
            }
          }
        }
        // Mux into isReady
        scope.launch {
          isBusy
              .combine(isEncoding) { isBusy, isEncoding -> (!isBusy) && (!isEncoding) }
              .collect { isReady ->
                _isReady.update { isReady }
                traceLog("isReady update: $isReady")
              }
        }
        // Send keep alive
        scope.launch {
          while (true) {
            delay(KEEP_ALIVE_INTERVAL)
            commands.sendKeepAlive().onFailure { logger.w("Failed to send keep alive.") }
          }
        }
        commands.clearPairingScreen()
      }

      is HttpCommunicator -> {
        // TODO this needs to be handled differently depending on whether or not there is a BLE
        // communicator
        _isReady.update { true }
      }
    }
  }

  private suspend fun setDateTime() {
    logger.d("Setting DateTime")
    val currentMoment: Instant = Clock.System.now()
    val datetimeInSystemZone: LocalDateTime =
        currentMoment.toLocalDateTime(TimeZone.currentSystemDefault())
    val utcOffset = TimeZone.currentSystemDefault().offsetAt(currentMoment)
    commands.setDateTime(datetimeInSystemZone, utcOffset, false)
  }

  internal suspend fun bindCommunicator(communicator: ICommunicator<*>) {
    // If the communicator was already bound, we don't need to do any configuration.
    if (!(operationMarshaller.bindCommunicator(communicator))) return

    if (!isInitialized) {
      initializeStateManagement(communicator)
      setDateTime()
      commands.setThirdParty()
      isInitialized = true
    }

    // Per communicator initialization
    when (communicator) {
      is HttpCommunicator -> {
        // Update the IP address if relevant
        // TODO how to handle when there are multiple?
        _ipAddress = communicator.connection.ipAddress
      }

      is BleCommunicator -> {}
    }
  }

  internal companion object {
    val KEEP_ALIVE_INTERVAL = 3.toDuration(DurationUnit.SECONDS)
  }
}
