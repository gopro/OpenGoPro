package gopro

import Wsdk
import WsdkIsolatedKoinContext
import co.touchlab.kermit.Logger
import domain.communicator.BleCommunicator
import domain.communicator.HttpCommunicator
import domain.communicator.ICommunicator
import domain.connector.ICameraConnector
import domain.gopro.GpDescriptorManager
import domain.gopro.IGoProFactory
import domain.gopro.IGpDescriptor
import entity.communicator.CommunicationType
import entity.connector.GoProId
import entity.operation.AccessPointState
import entity.operation.CohnState
import kotlinx.coroutines.CoroutineDispatcher
import kotlinx.coroutines.CoroutineExceptionHandler
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.delay
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.combine
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch
import kotlinx.datetime.Clock
import kotlinx.datetime.Instant
import kotlinx.datetime.LocalDateTime
import kotlinx.datetime.TimeZone
import kotlinx.datetime.offsetAt
import kotlinx.datetime.toLocalDateTime
import operation.GpMarshaller
import kotlin.time.DurationUnit
import kotlin.time.toDuration

private val logger = Logger.withTag("GoPro")
private const val TRACE_LOG = false

private fun traceLog(message: String) = if (TRACE_LOG) logger.d(message) else {
}

/**
 * Top level interface to communicate with a connected GoPro.
 *
 * Should be retrieved from [Wsdk.getGoPro]
 *
 * @property id identifier of connected GoPro
 */
class GoPro internal constructor(override val id: GoProId) : IGpDescriptor {
    private val cameraConnector: ICameraConnector = WsdkIsolatedKoinContext.getWsdkKoinApp().get()
    private val dispatcher: CoroutineDispatcher = WsdkIsolatedKoinContext.getWsdkKoinApp().get()
    private val facadeFactory: IGoProFactory =
        WsdkIsolatedKoinContext.getWsdkKoinApp().get()

    private val operationMarshaller = GpMarshaller(this)

    private val coroutineExceptionHandler = CoroutineExceptionHandler { _, throwable ->
        logger.e("Caught exception in coroutine:", throwable)
    }

    private val scope = CoroutineScope(dispatcher + coroutineExceptionHandler)

    private val gpDescriptorManager = object : GpDescriptorManager {
        override fun getDescriptor(): IGpDescriptor = this@GoPro

        override fun setAccessPointState(state: AccessPointState) =
            _accessPointState.update { state }

        override fun setCohnState(state: CohnState) = _cohnState.update { state }
    }

    override val communicators: List<CommunicationType>
        get() = operationMarshaller.communicators

    /**
     * Container delegate to access all camera commands
     */
    val commands = CommandsContainer(operationMarshaller)

    /**
     * Container delegate to access all camera settings
     */
    val settings = SettingsContainer(operationMarshaller)

    /**
     * Container delegate to access all camera statuses
     */
    val statuses = StatusesContainer(operationMarshaller)

    /**
     * Container delegate to access all camera features
     */
    val features = FeaturesContainer(
        FeatureContext(
            this,
            this.gpDescriptorManager,
            cameraConnector,
            facadeFactory
        )
    )

    private val _isBusy: MutableStateFlow<Boolean> = MutableStateFlow(true)
    override val isBusy: StateFlow<Boolean> get() = _isBusy
    private val _isEncoding: MutableStateFlow<Boolean> = MutableStateFlow(true)
    override val isEncoding: StateFlow<Boolean> get() = _isEncoding

    private val _isReady: MutableStateFlow<Boolean> = MutableStateFlow(true)
    override val isReady: StateFlow<Boolean> get() = _isReady

    private val _accessPointState: MutableStateFlow<AccessPointState> =
        MutableStateFlow(AccessPointState.Disconnected)
    override val accessPointState: StateFlow<AccessPointState> get() = _accessPointState

    private val _cohnState: MutableStateFlow<CohnState> = MutableStateFlow(CohnState.Unprovisioned)
    override val cohnState: StateFlow<CohnState> = _cohnState

    private var isInitialized = false

    internal fun unbindCommunicator(communicator: ICommunicator<*>) {
        operationMarshaller.removeCommunicator(communicator)
        if (communicator.communicationType == CommunicationType.BLE) {
            // Clear this so we restart state management if / when BLE connects again.
            isInitialized = false
        }
    }

    private fun initializeStateManagement(communicator: ICommunicator<*>) {
        logger.d("Setting up GoPro state management.")
        when (communicator) {
            is BleCommunicator -> {
                logger.d("Setting up BLE state management")
                // Start collecting read statuses
                scope.launch {
                    statuses.isBusy.registerValueUpdate().onSuccess { (currentValue, flow) ->
                        _isBusy.update { currentValue }
                        flow.collect { isBusy ->
                            traceLog("isBusy update: $isBusy")
                            _isBusy.update { isBusy }
                        }
                    }
                }
                scope.launch {
                    statuses.isEncoding.registerValueUpdate().onSuccess { (currentValue, flow) ->
                        _isEncoding.update { currentValue }
                        flow.collect { isEncoding ->
                            traceLog("isEncoding update: $isEncoding")
                            _isEncoding.update { isEncoding }
                        }
                    }
                }
                // Mux into isReady
                scope.launch {
                    isBusy.combine(isEncoding) { isBusy, isEncoding ->
                        (!isBusy) && (!isEncoding)
                    }.collect { isReady ->
                        _isReady.update { isReady }
                        traceLog("isReady update: $isReady")
                    }
                }
                // Send keep alive
                scope.launch {
                    while (true) {
                        delay(KEEP_ALIVE_INTERVAL)
                        commands.sendKeepAlive().onFailure {
                            logger.w("Failed to send keep alive.")
                        }
                    }
                }
                // Register for COHN status updates
                scope.launch {
                    features.cohn.getCohnStatus().collect { gpDescriptorManager.setCohnState(it) }
                }
            }

            is HttpCommunicator -> {
                // TODO this needs to be handled differently depending on whether or not there is a BLE communicator
                _isReady.update { true }
            }

            else -> {
                logger.w("Can not manage GoPro state on non-BLE communicator.")
            }
        }
    }

    private fun setDateTime() {
        logger.d("Setting DateTime")
        val currentMoment: Instant = Clock.System.now()
        val datetimeInSystemZone: LocalDateTime =
            currentMoment.toLocalDateTime(TimeZone.currentSystemDefault())
        val utcOffset = TimeZone.currentSystemDefault().offsetAt(currentMoment)
        scope.launch {
            commands.setDateTime(datetimeInSystemZone, utcOffset, false)
        }
    }

    internal suspend fun bindCommunicator(communicator: ICommunicator<*>) {
        // If the communicator was already bound, we don't need to do any configuration.
        if (!(operationMarshaller.bindCommunicator(communicator))) return

        if (!isInitialized) {
            initializeStateManagement(communicator)
            setDateTime()
            isInitialized = true
        }
    }

    internal companion object {
        val KEEP_ALIVE_INTERVAL = 28.toDuration(DurationUnit.SECONDS)
    }
}
