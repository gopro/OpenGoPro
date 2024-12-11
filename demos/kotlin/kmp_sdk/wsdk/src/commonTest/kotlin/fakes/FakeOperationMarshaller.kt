package fakes

import com.gopro.open_gopro.domain.api.IOperation
import com.gopro.open_gopro.domain.api.IOperationMarshaller
import com.gopro.open_gopro.domain.api.StrategyBuilder
import com.gopro.open_gopro.domain.communicator.BleCommunicator
import com.gopro.open_gopro.domain.communicator.ICommunicator
import com.gopro.open_gopro.entity.communicator.CommunicationType
import com.gopro.open_gopro.entity.connector.ConnectionDescriptor
import com.gopro.open_gopro.entity.connector.GoProId
import com.gopro.open_gopro.entity.network.ble.BleDevice
import com.gopro.open_gopro.entity.network.ble.BleNotification
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

    val fakeBleApi = FakeBleApi(responses, dispatcher)

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
                    GoProId("serialId"),
                    object : BleDevice {
                        override val id = "bleDeviceId"
                    }),
                dispatcher
            )
        )

    override val communicators: List<CommunicationType> = communicatorMap.keys.toList()
}