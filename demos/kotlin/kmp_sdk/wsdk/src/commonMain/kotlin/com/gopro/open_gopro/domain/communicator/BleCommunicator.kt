/* BleCommunicator.kt/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Tue Feb 18 18:41:29 UTC 2025 */

package com.gopro.open_gopro.domain.communicator

import com.benasher44.uuid.Uuid
import com.gopro.open_gopro.BleError
import com.gopro.open_gopro.CommunicationType
import com.gopro.open_gopro.ConnectionDescriptor
import com.gopro.open_gopro.domain.communicator.bleCommunicator.AccumulatedGpBleResponse
import com.gopro.open_gopro.domain.communicator.bleCommunicator.IGpBleResponse
import com.gopro.open_gopro.domain.communicator.bleCommunicator.ResponseId
import com.gopro.open_gopro.domain.communicator.bleCommunicator.bleFragment
import com.gopro.open_gopro.domain.network.IBleApi
import com.gopro.open_gopro.entity.communicator.ActionId
import com.gopro.open_gopro.entity.communicator.CommandId
import com.gopro.open_gopro.entity.communicator.FeatureId
import com.gopro.open_gopro.entity.communicator.GpStatus
import com.gopro.open_gopro.entity.communicator.QueryId
import com.gopro.open_gopro.entity.network.ble.BleNotification
import com.gopro.open_gopro.entity.network.ble.GpUuid
import com.gopro.open_gopro.operations.ApiError
import com.gopro.open_gopro.operations.SettingId
import com.gopro.open_gopro.operations.StatusId
import com.gopro.open_gopro.util.GpCommonBase
import com.gopro.open_gopro.util.IGpCommonBase
import com.gopro.open_gopro.util.extensions.toPrettyHexString
import com.gopro.open_gopro.util.extensions.toTlvMap
import kotlin.time.DurationUnit
import kotlin.time.toDuration
import kotlinx.coroutines.CoroutineDispatcher
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

private data class ResponseFlowElement(val id: ResponseId, val result: Result<IGpBleResponse>)

@OptIn(ExperimentalUnsignedTypes::class)
internal class BleCommunicator(
    private val bleApi: IBleApi,
    override val connection: ConnectionDescriptor.Ble,
    dispatcher: CoroutineDispatcher
) :
    ICommunicator<ConnectionDescriptor.Ble>(),
    IGpCommonBase by GpCommonBase("BleCommunicator", dispatcher, shouldEnableTraceLog = true) {
  override val communicationType = CommunicationType.BLE

  private val device = connection.device
  private val notifications: Flow<BleNotification>
    get() = bleApi.notificationsForConnection(device).getOrThrow()

  private val accumulatingRespMap: MutableMap<GpUuid, AccumulatedGpBleResponse> = mutableMapOf()
  private val receivedResponses: MutableSharedFlow<ResponseFlowElement> =
      MutableSharedFlow(replay = 0)

  init {
    scope?.launch {
      notifications.collect { notification ->
        // Ignore any non-GoPro UUID's
        GpUuid.fromUuid(notification.uuid)?.let { uuid ->
          traceLog("3. Received notification on $uuid: ${notification.data.toPrettyHexString()}")
          // Retrieve or create new message per-UUID
          accumulatingRespMap
              .getOrPut(uuid) { AccumulatedGpBleResponse(uuid) }
              .run {
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
      is ResponseId.Query -> {
        // Setting and Status queries may contain multiple responses.
        // First slice response into map of setting / status
        response.payload
            .drop(2)
            .toTlvMap()
            // Map keys to setting / status ID
            .mapKeys { (key, _) ->
              if (responseId.isSetting) {
                ResponseId.QuerySetting(responseId.id, SettingId.fromUByteArray(ubyteArrayOf(key)))
              } else {
                ResponseId.QueryStatus(responseId.id, StatusId.fromUByteArray(ubyteArrayOf(key)))
              }
            }
            // At this point IDs are adapted to Setting or Status IDs
            .forEach { (adaptedId, values) ->
              // If it should be sliced, emit each value individually
              if (adaptedId.shouldBeSliced) {
                values.forEach { value ->
                  traceLog("4. Emitting accumulated response $adaptedId")
                  receivedResponses.emit(
                      ResponseFlowElement(
                          adaptedId,
                          Result.success(
                              object : IGpBleResponse {
                                override val uuid = response.uuid
                                override val payload = value
                                override val id = adaptedId
                              })))
                }
                // Otherwise emit values together
              } else {
                traceLog("4. Emitting accumulated response $adaptedId")
                receivedResponses.emit(
                    ResponseFlowElement(
                        adaptedId,
                        Result.success(
                            object : IGpBleResponse {
                              override val uuid = response.uuid
                              override val payload = values.flatten().toUByteArray()
                              override val id = adaptedId
                            })))
              }
            }
      }

      // Everything else just gets forwarded
      else -> {
        traceLog("4. Emitting accumulated response ${response.id}")
        receivedResponses.emit(ResponseFlowElement(response.id, Result.success(response)))
      }
    }
  }

  /**
   * Fragment data into BLE writes and wait to receive notification identified by response ID
   *
   * @param uuid UUID to write to
   * @param data payload to fragment and write
   * @param responseId response identifier to wait for
   * @return accumulated payload for relevant response Id. Null if any BLE write fails.
   */
  @OptIn(FlowPreview::class)
  private suspend fun writeCharacteristicReceiveNotification(
      uuid: GpUuid,
      data: UByteArray,
      responseId: ResponseId
  ): Result<UByteArray> {
    for (retry in 1..WRITE_RETRIES) {
      try {
        return receivedResponses
            .onSubscription {
              // Do this here to avoid potential race condition of SharedFlow emitting before
              // we started collecting.
              data.bleFragment(MAX_PACKET_LENGTH).forEach {
                traceLog("1. Writing to $uuid ==> ${data.toPrettyHexString()}")
                bleApi.writeCharacteristic(device, uuid.toUuid(), it).onFailure {
                  emit(
                      ResponseFlowElement(responseId, Result.failure(BleError("BLE write failed"))))
                }
              }
              traceLog("2. Waiting to receive response $responseId")
            }
            .timeout(WRITE_TIMEOUT)
            .catch { exception ->
              if (exception is TimeoutCancellationException) {
                "BLE Write / Receive Notification timeout of $WRITE_TIMEOUT"
                    .let {
                      logger.e(it)
                      emit(ResponseFlowElement(responseId, Result.failure(BleError(it))))
                    }
              } else {
                "Unexpected failure in BLE Write Char Receive Notification"
                    .let {
                      logger.e(it)
                      emit(ResponseFlowElement(responseId, Result.failure(BleError(it))))
                    }
              }
            }
            .first { response ->
              traceLog("5. Checking received response ${response.id} vs expected $responseId")
              (response.id == responseId) && response.id.shouldBeMatchedAsSynchronousResponse
            }
            .result
            .map { response ->
              traceLog("6. Returning accumulated response $responseId")
              response.payload
            }
      } catch (e: Exception) {
        logger.w("Retrying $retry")
      }
    }
    return Result.failure(BleError("Write tried after $WRITE_RETRIES retries"))
  }

  suspend fun executeTlvCommand(
      id: CommandId,
      responseId: ResponseId,
      arguments: List<UByteArray> = listOf(),
  ): Result<UByteArray> {
    val payload =
        ubyteArrayOf(id.value) +
            arguments.fold(ubyteArrayOf()) { acc, next -> acc + next.size.toUByte() + next }
    return writeCharacteristicReceiveNotification(GpUuid.CQ_COMMAND, payload, responseId)
        .fold(
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
            onFailure = { Result.failure(it) })
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
              responseId)
          .map {
            // Drop feature and action ID so as only to return the payload
            it.drop(2).toUByteArray().toByteArray()
          }

  suspend fun executeSetting(id: SettingId, data: UByteArray): Result<UByteArray> =
      writeCharacteristicReceiveNotification(
              GpUuid.CQ_SETTINGS,
              ubyteArrayOf(id.value, data.size.toUByte()) + data,
              ResponseId.Setting(id))
          .fold(
              onSuccess = {
                if (GpStatus.isSuccess(it.last())) {
                  Result.success(it)
                } else {
                  "Set setting failed with status: ${it.last()}"
                      .let { message ->
                        logger.e(message)
                        Result.failure(ApiError(message))
                      }
                }
              },
              onFailure = { Result.failure(it) })

  suspend fun executeQuery(queryId: QueryId, settingId: SettingId): Result<UByteArray> =
      writeCharacteristicReceiveNotification(
          GpUuid.CQ_QUERY,
          ubyteArrayOf(queryId.value, settingId.value),
          ResponseId.QuerySetting(queryId, settingId))

  suspend fun executeQuery(queryId: QueryId, statusId: StatusId): Result<UByteArray> =
      writeCharacteristicReceiveNotification(
          GpUuid.CQ_QUERY,
          ubyteArrayOf(queryId.value, statusId.value),
          ResponseId.QueryStatus(queryId, statusId))

  suspend fun readCharacteristic(uuid: Uuid): Result<UByteArray> =
      bleApi.readCharacteristic(device, uuid)

  fun registerUpdate(id: ResponseId): Result<Flow<IGpBleResponse>> {
    logger.d("Registering to receive updates for $id")
    return Result.success(
        receivedResponses
            .filter {
              (it.result.isSuccess) && (it.id == id) && (it.id.shouldBeForwardedAsNotification)
            }
            .map {
              it.result.getOrThrow().let { notification ->
                // Special protobuf handling to extract the payload.
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
            })
  }

  companion object {
    const val MAX_PACKET_LENGTH = 20
    const val WRITE_RETRIES = 5
    val WRITE_TIMEOUT = 15.toDuration(DurationUnit.SECONDS)
  }
}
