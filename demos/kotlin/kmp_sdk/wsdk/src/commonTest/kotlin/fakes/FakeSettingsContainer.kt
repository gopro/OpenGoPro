package fakes

import entity.network.BleNotification
import kotlinx.coroutines.CoroutineDispatcher
import operation.SettingsContainer

class FakeSettingsContainer(
    val settingsContainer: SettingsContainer,
    private val marshaller: FakeOperationMarshaller
) {
    suspend fun sendNextBleMessage() = marshaller.sendNextBleMessage()
}

fun buildFakeSettingsContainer(responses: List<List<BleNotification>> = listOf(), dispatcher: CoroutineDispatcher): FakeSettingsContainer =
    FakeOperationMarshaller(responses, dispatcher).let { marshaller ->
        FakeSettingsContainer(
            SettingsContainer(marshaller),
            marshaller
        )
    }