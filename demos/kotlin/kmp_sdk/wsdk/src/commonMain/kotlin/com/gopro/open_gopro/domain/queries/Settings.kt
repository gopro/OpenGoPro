/* Settings.kt/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Tue Feb 18 18:41:29 UTC 2025 */

package com.gopro.open_gopro.gopro

import com.gopro.open_gopro.CommunicationType
import com.gopro.open_gopro.domain.api.BaseOperation
import com.gopro.open_gopro.domain.api.IOperationMarshaller
import com.gopro.open_gopro.domain.communicator.BleCommunicator
import com.gopro.open_gopro.domain.communicator.bleCommunicator.ResponseId
import com.gopro.open_gopro.entity.communicator.GpStatus
import com.gopro.open_gopro.entity.communicator.QueryId
import com.gopro.open_gopro.operations.IUByteArrayCompanion
import com.gopro.open_gopro.operations.SettingId
import com.gopro.open_gopro.util.extensions.asInt64UB
import com.gopro.open_gopro.util.extensions.toUByteArray
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.map
import kotlinx.coroutines.flow.onStart

@ExperimentalUnsignedTypes
internal class ULongByteTransformer(private val length: Int) : IUByteArrayCompanion<ULong> {
  init {
    when (length) {
      1,
      4 -> {}
      else -> throw NotImplementedError("Only lengths 1 and 4 are supported")
    }
  }

  override fun fromUByteArray(value: UByteArray): ULong =
      when (value.size) {
        1 -> value.first().toULong()
        4 -> value.asInt64UB()
        else -> throw NotImplementedError("Only lengths 1 and 4 are supported")
      }

  override fun toUByteArray(value: ULong): UByteArray =
      when (length) {
        1 -> value.toUByteArray().first().toUByteArray()
        4 -> value.toUByteArray()
        else -> throw NotImplementedError("Only lengths 1 and 4 are supported")
      }
}

/**
 * A per-setting ID wrapper to perform all setting queries
 *
 * @param T Setting data type
 * @property settingId Setting ID
 * @property marshaller operation marshaller to marshal the queries
 * @param byteTransformer Enum data type
 * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html)
 */
@OptIn(ExperimentalUnsignedTypes::class)
class Setting<T : Any>
internal constructor(
    private val settingId: SettingId,
    private val byteTransformer: IUByteArrayCompanion<T>,
    private val marshaller: IOperationMarshaller,
) {
  private inner class SetSettingValue(private val value: T) :
      BaseOperation<Unit>("Set Setting Value::${settingId.name}") {
    override suspend fun execute(communicator: BleCommunicator): Result<Unit> =
        communicator.executeSetting(settingId, byteTransformer.toUByteArray(value)).map {
          GpStatus.fromUByte(it.last()).let { status ->
            if (status == GpStatus.SUCCESS) {
              Result.success(Unit)
            } else {
              Result.failure(Exception("Set setting failed with: $status"))
            }
          }
        }
  }

  private inner class GetSettingValue : BaseOperation<T>("Get Setting Value::${settingId.name}") {
    override suspend fun execute(communicator: BleCommunicator): Result<T> =
        communicator.executeQuery(QueryId.GET_SETTING_VALUES, settingId).map {
          byteTransformer.fromUByteArray(it)
        }
  }

  private inner class GetSettingCapabilities :
      BaseOperation<List<T>>("Get Setting Capabilities::${settingId.name}") {

    override suspend fun execute(communicator: BleCommunicator): Result<List<T>> =
        communicator.executeQuery(QueryId.GET_SETTING_CAPABILITIES, settingId).map {
          listOf(byteTransformer.fromUByteArray(TODO()))
        }
  }

  private inner class RegisterForSettingValueUpdates :
      BaseOperation<Flow<T>>("Register Setting Value Updates::${settingId.name}") {

    override suspend fun execute(communicator: BleCommunicator): Result<Flow<T>> {
      // Send initial query OTA to register and store current value for later returning
      val currentValue =
          communicator
              .executeQuery(QueryId.REGISTER_SETTING_VALUE_UPDATES, settingId)
              .fold(
                  onFailure = {
                    return Result.failure(it)
                  },
                  onSuccess = { byteTransformer.fromUByteArray(it) },
              )

      // Now actually register to receive notifications
      return communicator
          .registerUpdate(
              ResponseId.QuerySetting(QueryId.ASYNC_SETTING_VALUE_NOTIFICATION, settingId))
          .map { flow ->
            flow.map { byteTransformer.fromUByteArray(it.payload) }.onStart { emit(currentValue) }
          }
    }
  }

  private inner class UnregisterForSettingValueUpdates :
      BaseOperation<Unit>("Unregister Setting Value Updates::${settingId.name}") {

    override suspend fun execute(communicator: BleCommunicator): Result<Unit> =
        communicator.executeQuery(QueryId.UNREGISTER_SETTING_VALUE_UPDATES, settingId).map {}
  }

  private inner class RegisterForSettingCapabilityUpdates :
      BaseOperation<Flow<List<T>>>("Register Setting Capability Updates::${settingId.name}") {

    override suspend fun execute(communicator: BleCommunicator): Result<Flow<List<T>>> {
      val initialCapabilities =
          communicator
              .executeQuery(QueryId.REGISTER_SETTING_CAPABILITY_UPDATES, settingId)
              .fold(
                  onSuccess = {
                    it.map { byte -> byteTransformer.fromUByteArray(ubyteArrayOf(byte)) }
                  },
                  onFailure = {
                    return Result.failure(it)
                  },
              )

      // Now actually register to receive notifications
      return communicator
          .registerUpdate(
              ResponseId.QuerySetting(QueryId.ASYNC_SETTING_CAPABILITY_NOTIFICATION, settingId))
          .map { flow ->
            flow
                .map {
                  it.payload.map { byte -> byteTransformer.fromUByteArray(ubyteArrayOf(byte)) }
                }
                .onStart { emit(initialCapabilities) }
          }
    }
  }

  private inner class UnregisterForSettingCapabilityUpdates :
      BaseOperation<Unit>("Unregister Setting Capability Updates::${settingId.name}") {

    override suspend fun execute(communicator: BleCommunicator): Result<Unit> =
        communicator.executeQuery(QueryId.UNREGISTER_SETTING_CAPABILITY_UPDATES, settingId).map {}
  }

  /**
   * Set the setting to a desired value
   *
   * @param value value to set
   * @see
   *   [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#set-setting)
   */
  suspend fun setValue(value: T): Result<Unit> =
      marshaller.marshal(SetSettingValue(value)) {
        useCommunicator { _, _ -> CommunicationType.BLE }
      }

  /**
   * Get the current setting value
   *
   * @return current setting value
   * @see
   *   [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/query.html#get-setting-values)
   */
  suspend fun getValue(): Result<T> =
      marshaller.marshal(GetSettingValue()) { useCommunicator { _, _ -> CommunicationType.BLE } }

  /**
   * Get the current setting's capabilities
   *
   * @return setting capabilities
   * @see
   *   [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/query.html#get-setting-capabilities)
   */
  suspend fun getCapabilities(): Result<List<T>> =
      marshaller.marshal(GetSettingCapabilities()) {
        useCommunicator { _, _ -> CommunicationType.BLE }
      }

  /**
   * Register for setting value updates
   *
   * @return continuous setting value updates
   * @see
   *   [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/query.html#register-for-setting-value-updates)
   */
  suspend fun registerValueUpdates(): Result<Flow<T>> =
      marshaller.marshal(RegisterForSettingValueUpdates()) {
        useCommunicator { _, _ -> CommunicationType.BLE }
      }

  /**
   * Unregister for setting value updates
   *
   * @see
   *   [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/query.html#unregister-for-setting-value-updates)
   */
  suspend fun unregisterValueUpdates(): Result<Unit> =
      marshaller.marshal(UnregisterForSettingValueUpdates()) {
        useCommunicator { _, _ -> CommunicationType.BLE }
      }

  /**
   * Register for setting capability updates
   *
   * @return list of currently available setting options
   * @see
   *   [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/query.html#register-for-setting-capability-updates)
   */
  suspend fun registerCapabilityUpdates(): Result<Flow<List<T>>> =
      marshaller.marshal(RegisterForSettingCapabilityUpdates()) {
        useCommunicator { _, _ -> CommunicationType.BLE }
      }

  /**
   * Unregister for setting capability updates
   *
   * @see
   *   [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/query.html#unregister-for-setting-capability-updates)
   */
  suspend fun unregisterCapabilityUpdates(): Result<Unit> =
      marshaller.marshal(UnregisterForSettingCapabilityUpdates()) {
        useCommunicator { _, _ -> CommunicationType.BLE }
      }
}
