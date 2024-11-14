package operation.queries

import domain.api.BaseOperation
import domain.api.IOperationMarshaller
import domain.communicator.BleCommunicator
import domain.communicator.bleCommunicator.ResponseId
import entity.communicator.CommunicationType
import entity.communicator.GpStatus
import entity.communicator.QueryId
import entity.constants.IUByteEnumCompanion
import entity.constants.SettingId
import entity.constants.UByteEnum
import extensions.toUByteArray
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.map

internal class UByteEnumTransformer<T>(
    private val companion: IUByteEnumCompanion<T>,
    private val settingId: SettingId
) where T : Enum<T>, T : UByteEnum {
    fun toUByte(value: T): UByte = value.value
    fun fromUByte(data: UByte): T = companion.fromUByte(data)
}

@OptIn(ExperimentalUnsignedTypes::class)
class SettingFacade<T> internal constructor(
    private val settingId: SettingId,
    enum: IUByteEnumCompanion<T>,
    private val marshaller: IOperationMarshaller,
) where T : Enum<T>, T : UByteEnum {
    private val byteTransformer = UByteEnumTransformer(enum, settingId)

    // TODO lazy init these classes

    private inner class SetSettingValue(private val value: T) :
        BaseOperation<Boolean>("Set Setting Value::${settingId.name}") {
        override suspend fun execute(communicator: BleCommunicator): Result<Boolean> =
            communicator.executeSetting(
                settingId,
                byteTransformer.toUByte(value).toUByteArray()
            ).map { GpStatus.isSuccess(it.last()) }
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
        BaseOperation<Pair<T, Flow<T>>>("Register Setting Value Updates::${settingId.name}") {

        override suspend fun execute(communicator: BleCommunicator): Result<Pair<T, Flow<T>>> {
            // Send initial query OTA to register and store current value for later returning
            val currentValue =
                communicator.executeQuery(QueryId.REGISTER_SETTING_VALUE_UPDATES, settingId)
                    .fold(
                        onFailure = { return Result.failure(it) },
                        onSuccess = { byteTransformer.fromUByte(it.first()) },
                    )

            // Now actually register to receive notifications
            return communicator.registerUpdate(
                ResponseId.QuerySetting(
                    QueryId.ASYNC_SETTING_VALUE_NOTIFICATION,
                    settingId
                )
            ).map { flow ->
                currentValue to flow.map { byteTransformer.fromUByte(it.payload.last()) }
            }
        }
    }

    suspend fun setValue(value: T): Result<Boolean> =
        marshaller.marshal(SetSettingValue(value)) { useCommunicator { _, _ -> CommunicationType.BLE } }

    suspend fun getValue(): Result<T> =
        marshaller.marshal(GetSettingValue()) { useCommunicator { _, _ -> CommunicationType.BLE } }

    suspend fun getCapabilities(): Result<List<T>> =
        marshaller.marshal(GetSettingCapabilities()) { useCommunicator { _, _ -> CommunicationType.BLE } }

    suspend fun registerValueUpdate(): Result<Pair<T, Flow<T>>> =
        marshaller.marshal(RegisterForSettingValueUpdates()) { useCommunicator { _, _ -> CommunicationType.BLE } }

    suspend fun registerCapabilityUpdates(): Result<Flow<T>> = TODO()
}
