package domain.queries

import domain.api.BaseOperation
import domain.api.IOperationMarshaller
import domain.communicator.BleCommunicator
import domain.communicator.bleCommunicator.ResponseId
import entity.communicator.CommunicationType
import entity.communicator.GpStatus
import entity.communicator.QueryId
import entity.queries.IUByteEnumCompanion
import entity.queries.SettingId
import entity.queries.UByteEnum
import util.extensions.toUByteArray
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.map
import kotlinx.coroutines.flow.onStart

internal class UByteEnumTransformer<T>(
    private val companion: IUByteEnumCompanion<T>
) where T : Enum<T>, T : UByteEnum {
    fun toUByte(value: T): UByte = value.value
    fun fromUByte(data: UByte): T = companion.fromUByte(data)
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
    enum: IUByteEnumCompanion<T>,
    private val marshaller: IOperationMarshaller,
) where T : Enum<T>, T : UByteEnum {
    private val byteTransformer = UByteEnumTransformer(enum)

    private inner class SetSettingValue(private val value: T) :
        BaseOperation<Unit>("Set Setting Value::${settingId.name}") {
        override suspend fun execute(communicator: BleCommunicator): Result<Unit> =
            communicator.executeSetting(
                settingId,
                byteTransformer.toUByte(value).toUByteArray()
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
                .map { byteTransformer.fromUByte(it.first()) }
    }

    private inner class GetSettingCapabilities :
        BaseOperation<List<T>>("Get Setting Capabilities::${settingId.name}") {

        override suspend fun execute(communicator: BleCommunicator): Result<List<T>> =
            communicator.executeQuery(QueryId.GET_SETTING_CAPABILITIES, settingId)
                .map { listOf(byteTransformer.fromUByte(TODO())) }
    }

    private inner class RegisterForSettingValueUpdates :
        BaseOperation<Flow<T>>("Register Setting Value Updates::${settingId.name}") {

        override suspend fun execute(communicator: BleCommunicator): Result<Flow<T>> {
            // Send initial query OTA to register and store current value for later returning
            val currentValue =
                communicator.executeQuery(QueryId.REGISTER_SETTING_VALUE_UPDATES, settingId)
                    .fold(
                        onFailure = { return Result.failure(it) },
                        onSuccess = { byteTransformer.fromUByte(it.first()) },
                    )

            // Now actually register to receive notifications
            return communicator.registerUpdate(
                ResponseId.QuerySetting(QueryId.ASYNC_SETTING_VALUE_NOTIFICATION, settingId)
            ).map { flow ->
                flow
                    .map { byteTransformer.fromUByte(it.payload.last()) }
                    .onStart { emit(currentValue) }
            }
        }
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
    suspend fun registerValueUpdate(): Result<Flow<T>> =
        marshaller.marshal(RegisterForSettingValueUpdates()) { useCommunicator { _, _ -> CommunicationType.BLE } }

    // TODO Other queries here
}
