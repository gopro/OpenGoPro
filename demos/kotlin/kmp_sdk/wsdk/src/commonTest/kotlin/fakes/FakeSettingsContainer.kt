package fakes

import entity.network.ble.BleNotification
import gopro.SettingsContainer
import kotlinx.coroutines.CoroutineDispatcher

internal class FakeSettingsContainer(
    val settingsContainer: SettingsContainer,
    private val marshaller: FakeOperationMarshaller
) {
    suspend fun sendNextBleMessage() = marshaller.sendNextBleMessage()
}

internal fun buildFakeSettingsContainer(
    responses: List<List<BleNotification>> = listOf(),
    dispatcher: CoroutineDispatcher
): FakeSettingsContainer =
    FakeOperationMarshaller(responses, dispatcher).let { marshaller ->
        FakeSettingsContainer(
            SettingsContainer(marshaller),
            marshaller
        )
    }