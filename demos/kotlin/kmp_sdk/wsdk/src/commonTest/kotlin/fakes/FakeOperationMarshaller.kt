package fakes

import domain.api.IOperation
import domain.api.IOperationMarshaller
import domain.api.StrategyBuilder
import domain.communicator.BleCommunicator
import domain.communicator.ICommunicator
import entity.communicator.CommunicationType
import entity.connector.ConnectionDescriptor
import entity.network.BleDevice
import entity.network.BleNotification
import kotlinx.coroutines.CoroutineDispatcher

internal class FakeOperationMarshaller(
    responses: List<List<BleNotification>> = listOf(),
    dispatcher: CoroutineDispatcher,
) :
    IOperationMarshaller {
    override suspend fun <T : Any, O : IOperation<T>> marshal(
        operation: O,
        strategy: (StrategyBuilder<T, O>.() -> Unit)?
    ): Result<T> =
        operation.execute(communicatorMap.values.first())

    private val fakeBleApi = FakeBleApi(responses, dispatcher)

    suspend fun sendNextBleMessage() = fakeBleApi.sendNextMessage()

    override fun removeCommunicator(communicator: ICommunicator<*>) {
        TODO("Not yet implemented")
    }

    override suspend fun bindCommunicator(communicator: ICommunicator<*>): Boolean {
        TODO("Not yet implemented")
    }

    private val communicatorMap: MutableMap<CommunicationType, ICommunicator<*>> =
        mutableMapOf(
            CommunicationType.BLE to BleCommunicator(
                fakeBleApi,
                ConnectionDescriptor.Ble(
                    "serialId",
                    object : BleDevice {
                        override val serialId = "bleDeviceId"
                    }),
                dispatcher
            )
        )

    override val communicators: List<CommunicationType> = communicatorMap.keys.toList()
}