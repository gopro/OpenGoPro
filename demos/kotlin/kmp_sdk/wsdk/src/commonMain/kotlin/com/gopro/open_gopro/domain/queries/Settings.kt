package com.gopro.open_gopro.domain.queries

import com.gopro.open_gopro.domain.api.BaseOperation
import com.gopro.open_gopro.domain.api.IOperationMarshaller
import com.gopro.open_gopro.domain.communicator.BleCommunicator
import com.gopro.open_gopro.domain.communicator.bleCommunicator.ResponseId
import com.gopro.open_gopro.entity.communicator.CommunicationType
import com.gopro.open_gopro.entity.communicator.GpStatus
import com.gopro.open_gopro.entity.communicator.QueryId
import com.gopro.open_gopro.entity.queries.IUByteArrayCompanion
import com.gopro.open_gopro.entity.queries.IValuedEnum
import com.gopro.open_gopro.entity.queries.SettingId
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.map
import kotlinx.coroutines.flow.onStart
import com.gopro.open_gopro.util.extensions.toUByteArray

@OptIn(ExperimentalUnsignedTypes::class)
internal class UByteArrayEnumTransformer<T>(
    private val companion: IUByteArrayCompanion<T>
) where T : Enum<T>, T : IValuedEnum<*> {
    fun toUByteArray(value: T): UByteArray =
        if (value.value is UByte) {
            ubyteArrayOf(value.value as UByte)
        } else if (value.value is ULong) {
            (value.value as ULong).toUByteArray()
        } else {
            throw Exception("Only Enums of value type UByte and ULong can be converted to UByteArray")
        }

    fun fromUByteArray(data: UByteArray): T = companion.fromUByteArray(data)
}

/**
 * A per-setting ID wrapper to perform all setting queries
 *
 * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html)
 *
 * @param T Setting data type
 * @property settingId Setting ID
 * @property marshaller operation marshaller to marshal the queries
 *
 * @param enum Enum data type
 */
@OptIn(ExperimentalUnsignedTypes::class)
class Setting<T> internal constructor(
    private val settingId: SettingId,
    enum: IUByteArrayCompanion<T>,
    private val marshaller: IOperationMarshaller,
) where T : Enum<T>, T : IValuedEnum<*> {
    private val byteTransformer = UByteArrayEnumTransformer(enum)

    private inner class SetSettingValue(private val value: T) :
        BaseOperation<Unit>("Set Setting Value::${settingId.name}") {
        override suspend fun execute(communicator: BleCommunicator): Result<Unit> =
            communicator.executeSetting(
                settingId, byteTransformer.toUByteArray(value)
            ).map {
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
            communicator.executeQuery(QueryId.GET_SETTING_VALUES, settingId)
                .map { byteTransformer.fromUByteArray(it) }
    }

    private inner class GetSettingCapabilities :
        BaseOperation<List<T>>("Get Setting Capabilities::${settingId.name}") {

        override suspend fun execute(communicator: BleCommunicator): Result<List<T>> =
            communicator.executeQuery(QueryId.GET_SETTING_CAPABILITIES, settingId)
                .map { listOf(byteTransformer.fromUByteArray(TODO())) }
    }

    private inner class RegisterForSettingValueUpdates :
        BaseOperation<Flow<T>>("Register Setting Value Updates::${settingId.name}") {

        override suspend fun execute(communicator: BleCommunicator): Result<Flow<T>> {
            // Send initial query OTA to register and store current value for later returning
            val currentValue =
                communicator.executeQuery(QueryId.REGISTER_SETTING_VALUE_UPDATES, settingId).fold(
                    onFailure = { return Result.failure(it) },
                    onSuccess = { byteTransformer.fromUByteArray(it) },
                )

            // Now actually register to receive notifications
            return communicator.registerUpdate(
                ResponseId.QuerySetting(QueryId.ASYNC_SETTING_VALUE_NOTIFICATION, settingId)
            ).map { flow ->
                flow.map { byteTransformer.fromUByteArray(it.payload) }
                    .onStart { emit(currentValue) }
            }
        }
    }

    private inner class UnregisterForSettingValueUpdates :
        BaseOperation<Unit>("Unregister Setting Value Updates::${settingId.name}") {

        override suspend fun execute(communicator: BleCommunicator): Result<Unit> =
            communicator.executeQuery(QueryId.UNREGISTER_SETTING_VALUE_UPDATES, settingId).map { }
    }

    private inner class RegisterForSettingCapabilityUpdates :
        BaseOperation<Flow<List<T>>>("Register Setting Capability Updates::${settingId.name}") {

        override suspend fun execute(communicator: BleCommunicator): Result<Flow<List<T>>> {
            val initialCapabilities = communicator.executeQuery(
                QueryId.REGISTER_SETTING_CAPABILITY_UPDATES, settingId
            ).fold(
                onSuccess = { it.map { byte -> byteTransformer.fromUByteArray(ubyteArrayOf(byte)) } },
                onFailure = { return Result.failure(it) },
            )

            // Now actually register to receive notifications
            return communicator.registerUpdate(
                ResponseId.QuerySetting(QueryId.ASYNC_SETTING_CAPABILITY_NOTIFICATION, settingId)
            ).map { flow ->
                flow.map {
                    it.payload.map { byte -> byteTransformer.fromUByteArray(ubyteArrayOf(byte)) }
                }.onStart { emit(initialCapabilities) }
            }
        }
    }

    private inner class UnregisterForSettingCapabilityUpdates :
        BaseOperation<Unit>("Unregister Setting Capability Updates::${settingId.name}") {

        override suspend fun execute(communicator: BleCommunicator): Result<Unit> =
            communicator.executeQuery(QueryId.UNREGISTER_SETTING_CAPABILITY_UPDATES, settingId)
                .map { }
    }

    /**
     * Set the setting to a desired value
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#set-setting)
     *
     * @param value value to set
     */
    suspend fun setValue(value: T): Result<Unit> =
        marshaller.marshal(SetSettingValue(value)) { useCommunicator { _, _ -> CommunicationType.BLE } }

    /**
     * Get the current setting value
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/query.html#get-setting-values)
     *
     * @return current setting value
     */
    suspend fun getValue(): Result<T> =
        marshaller.marshal(GetSettingValue()) { useCommunicator { _, _ -> CommunicationType.BLE } }

    /**
     * Get the current setting's capabilities
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/query.html#get-setting-capabilities)
     *
     * @return setting capabilities
     */
    suspend fun getCapabilities(): Result<List<T>> =
        marshaller.marshal(GetSettingCapabilities()) { useCommunicator { _, _ -> CommunicationType.BLE } }

    /**
     * Register for setting value updates
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/query.html#register-for-setting-value-updates)
     *
     * @return continuous setting value updates
     */
    suspend fun registerValueUpdates(): Result<Flow<T>> =
        marshaller.marshal(RegisterForSettingValueUpdates()) { useCommunicator { _, _ -> CommunicationType.BLE } }

    suspend fun unregisterValueUpdates(): Result<Unit> =
        marshaller.marshal(UnregisterForSettingValueUpdates()) { useCommunicator { _, _ -> CommunicationType.BLE } }

    /**
     * Register for setting capability updates
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/query.html#register-for-setting-capability-updates)
     *
     * @return list of currently available setting options
     */
    suspend fun registerCapabilityUpdates(): Result<Flow<List<T>>> =
        marshaller.marshal(RegisterForSettingCapabilityUpdates()) { useCommunicator { _, _ -> CommunicationType.BLE } }

    suspend fun unregisterCapabilityUpdates(): Result<Unit> =
        marshaller.marshal(UnregisterForSettingCapabilityUpdates()) { useCommunicator { _, _ -> CommunicationType.BLE } }
}
