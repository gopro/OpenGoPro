package domain.communicator

import co.touchlab.kermit.Logger
import com.benasher44.uuid.Uuid
import domain.communicator.bleCommunicator.AccumulatedGpBleResponse
import domain.communicator.bleCommunicator.IGpBleResponse
import domain.communicator.bleCommunicator.ResponseId
import domain.communicator.bleCommunicator.bleFragment
import domain.network.IBleApi
import entity.communicator.ActionId
import entity.communicator.CommandId
import entity.communicator.CommunicationType
import entity.communicator.FeatureId
import entity.communicator.GpStatus
import entity.communicator.QueryId
import entity.connector.ConnectionDescriptor
import entity.queries.SettingId
import entity.queries.StatusId
import exceptions.BleError
import entity.network.ble.BleNotification
import entity.network.ble.GpUuid
import util.extensions.toPrettyHexString
import util.extensions.toTlvMap
import kotlinx.coroutines.CoroutineDispatcher
import kotlinx.coroutines.CoroutineExceptionHandler
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.FlowPreview
import kotlinx.coroutines.TimeoutCancellationException
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.MutableSharedFlow
import kotlinx.coroutines.flow.catch
import kotlinx.coroutines.flow.filter
import kotlinx.coroutines.flow.first
import kotlinx.coroutines.flow.map
import kotlinx.coroutines.flow.onSubscription
import kotlinx.coroutines.flow.timeout
import kotlinx.coroutines.launch
import kotlin.time.DurationUnit
import kotlin.time.toDuration

private val logger = Logger.withTag("BleCommunicator")
private const val TRACE_LOG = false

// TODO configure and inject
private fun traceLog(message: String) = if (TRACE_LOG) logger.d(message) else {
}

private data class ResponseFlowElement(
    val id: ResponseId,
    val result: Result<IGpBleResponse>
)

@OptIn(ExperimentalUnsignedTypes::class)
internal class BleCommunicator(
    private val bleApi: IBleApi,
    override val connection: ConnectionDescriptor.Ble,
    dispatcher: CoroutineDispatcher
) : ICommunicator<ConnectionDescriptor.Ble>() {
    private val device = connection.device
    override val communicationType = CommunicationType.BLE
    private val notifications: Flow<BleNotification>
        get() = bleApi.notificationsForConnection(device).getOrThrow()

    private val coroutineExceptionHandler = CoroutineExceptionHandler { _, throwable ->
        logger.e("Caught exception in coroutine:", throwable)
    }

    private val scope = CoroutineScope(dispatcher + coroutineExceptionHandler)

    private val accumulatingRespMap: MutableMap<GpUuid, AccumulatedGpBleResponse> = mutableMapOf()

    private val receivedResponses: MutableSharedFlow<ResponseFlowElement> =
        MutableSharedFlow(replay = 0)

    init {
        scope.launch {
            notifications.collect { notification ->
                // Ignore any non-GoPro UUID's
                GpUuid.fromUuid(notification.uuid)?.let { uuid ->
                    traceLog("3. Received notification on $uuid: ${notification.data.toPrettyHexString()}")
                    // Retrieve or create new message per-UUID
                    accumulatingRespMap.getOrPut(uuid) { AccumulatedGpBleResponse(uuid) }.run {
                        accumulate(notification.data)
                        if (isReceived) {
                            accumulatingRespMap.remove(uuid)
                            routeResponse(this)
                        }
                    }
                }
            }
        }
    }

    private suspend fun routeResponse(response: IGpBleResponse) {
        when (val responseId = response.id) {
            // Setting and Status queries may contain multiple responses so need to be muxed into those
            // responses here.
            is ResponseId.Query -> {
                if (responseId.isSetting()) {
                    response.payload.drop(2).toTlvMap().forEach { (settingId, settingValue) ->
                        traceLog("4. Emitting accumulated response $responseId")
                        val responseIdAsSetting = ResponseId.QuerySetting(
                            responseId.id,
                            SettingId.fromUByte(settingId)
                        )
                        receivedResponses.emit(
                            ResponseFlowElement(
                                responseIdAsSetting,
                                Result.success(object : IGpBleResponse {
                                    override val uuid = response.uuid
                                    override val payload = settingValue
                                    override val id = responseIdAsSetting
                                })
                            )
                        )
                    }
                } else if (responseId.isStatus()) {
                    response.payload.drop(2).toTlvMap().forEach { (statusId, statusValue) ->
                        traceLog("4. Emitting accumulated response $responseId")
                        val responseIdAsStatus = ResponseId.QueryStatus(
                            responseId.id,
                            StatusId.fromUByte(statusId)
                        )
                        receivedResponses.emit(
                            ResponseFlowElement(
                                responseIdAsStatus,
                                Result.success(object : IGpBleResponse {
                                    override val uuid = response.uuid
                                    override val payload = statusValue
                                    override val id = responseIdAsStatus
                                })
                            )
                        )
                    }
                } else {
                    throw Exception("It should be impossible for a query responseID to not be a setting or status.")
                }
            }

            // Everything else just gets forwarded
            else -> {
                traceLog("4. Emitting accumulated response $responseId")
                receivedResponses.emit(ResponseFlowElement(responseId, Result.success(response)))
            }
        }
    }

    /**
     * Fragment data into BLE writes and wait to receive notification identified by response ID
     *
     * @param uuid UUID to write to
     * @param data payload to fragment and write
     * @param responseId response identifier to wait for
     *
     * @return accumulated payload for relevant response Id. Null if any BLE write fails.
     */
    @OptIn(FlowPreview::class)
    private suspend fun writeCharacteristicReceiveNotification(
        uuid: GpUuid,
        data: UByteArray,
        responseId: ResponseId
    ): Result<UByteArray> =
        receivedResponses
            .onSubscription {
                // Do this here to avoid potential race condition of SharedFlow emitting before
                // we started collecting.
                data.bleFragment(MAX_PACKET_LENGTH).forEach {
                    traceLog("1. Writing to $uuid ==> ${data.toPrettyHexString()}")
                    bleApi.writeCharacteristic(device, uuid.toUuid(), it).onFailure {
                        emit(
                            ResponseFlowElement(
                                responseId,
                                Result.failure(BleError("BLE write failed"))
                            )
                        )
                    }
                }
                traceLog("2. Waiting to receive response $responseId")
            }
            .timeout(WRITE_TIMEOUT)
            .catch { exception ->
                if (exception is TimeoutCancellationException) {
                    "BLE Write / Receive Notification timeout of $WRITE_TIMEOUT".let {
                        logger.e(it)
                        emit(ResponseFlowElement(responseId, Result.failure(BleError(it))))
                    }
                } else {
                    "Unexpected failure in BLE Write Char Receive Notification".let {
                        logger.e(it)
                        emit(ResponseFlowElement(responseId, Result.failure(BleError(it))))
                    }
                }
            }
            .first { response ->
                traceLog("5. Checking received response ${response.id} vs expected $responseId")
                (response.id == responseId) && response.id.shouldBeMatchedAsSynchronousResponse()
            }.result.map { response ->
                traceLog("6. Returning accumulated response $responseId")
                response.payload
            }

    suspend fun executeTlvCommand(
        id: CommandId,
        responseId: ResponseId,
        arguments: List<UByteArray> = listOf(),
    ): Result<UByteArray> {
        val payload =
            ubyteArrayOf(id.value) + arguments.fold(ubyteArrayOf()) { acc, next ->
                acc + next.size.toUByte() + next
            }
        return writeCharacteristicReceiveNotification(
            GpUuid.CQ_COMMAND,
            payload,
            responseId
        ).fold(
            onSuccess = { response ->
                // Byte 0 == command ID. Byte 1 == status
                GpStatus.fromUByte(response[1]).let { status ->
                    if (status == GpStatus.SUCCESS) {
                        // Pop status
                        Result.success(response.drop(2).toUByteArray())
                    } else {
                        Result.failure(Exception("Received non-success status: $status"))
                    }
                }
            },
            onFailure = { Result.failure(it) }
        )
    }

    suspend fun executeProtobufCommand(
        featureId: FeatureId,
        actionId: ActionId,
        protobufPayload: ByteArray,
        responseId: ResponseId,
        uuid: GpUuid,
    ): Result<ByteArray> =
        writeCharacteristicReceiveNotification(
            uuid,
            ubyteArrayOf(featureId.value, actionId.value) + protobufPayload.toUByteArray(),
            responseId
        ).map {
            // Drop feature and action ID so as only to return the payload
            it.drop(2).toUByteArray().toByteArray()
        }

    suspend fun executeSetting(id: SettingId, data: UByteArray): Result<UByteArray> =
        // TODO check and extract status
        writeCharacteristicReceiveNotification(
            GpUuid.CQ_SETTINGS,
            ubyteArrayOf(id.value) + data,
            ResponseId.Setting(id)
        )

    suspend fun executeQuery(queryId: QueryId, settingId: SettingId): Result<UByteArray> =
        writeCharacteristicReceiveNotification(
            GpUuid.CQ_QUERY,
            ubyteArrayOf(queryId.value, settingId.value),
            ResponseId.QuerySetting(queryId, settingId)
        )

    suspend fun executeQuery(queryId: QueryId, statusId: StatusId): Result<UByteArray> =
        writeCharacteristicReceiveNotification(
            GpUuid.CQ_QUERY,
            ubyteArrayOf(queryId.value, statusId.value),
            ResponseId.QueryStatus(queryId, statusId)
        )

    suspend fun readCharacteristic(uuid: Uuid): Result<UByteArray> =
        bleApi.readCharacteristic(device, uuid)

    fun registerUpdate(id: ResponseId): Result<Flow<IGpBleResponse>> {
        logger.d("Registering to receive updates for $id")
        return Result.success(receivedResponses
            .filter {
                (it.result.isSuccess) && (it.id == id) && (it.id.shouldBeForwardedAsNotification())
            }
            .map {
                it.result.getOrThrow().let { notification ->
                    // Special protobuf handling to extract the payload.
                    // TODO this should be done somewhere more central.
                    if (notification.id is ResponseId.Protobuf) {
                        object : IGpBleResponse {
                            override val uuid = notification.uuid
                            override val payload = notification.payload.drop(2).toUByteArray()
                            override val id = notification.id
                        }
                    } else {
                        notification
                    }
                }
            }
        )
    }

    companion object {
        const val MAX_PACKET_LENGTH = 20
        val WRITE_TIMEOUT = 10.toDuration(DurationUnit.SECONDS)
    }
}

