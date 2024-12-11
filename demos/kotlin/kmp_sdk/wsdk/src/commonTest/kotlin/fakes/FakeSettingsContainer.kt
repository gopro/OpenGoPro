package fakes

import com.gopro.open_gopro.entity.network.ble.BleNotification
import com.gopro.open_gopro.gopro.SettingsContainer
import kotlinx.coroutines.CoroutineDispatcher

internal class FakeSettingsContainer(
    val settingsContainer: SettingsContainer,
    private val marshaller: FakeOperationMarshaller
) {
    val spies = marshaller.fakeBleApi.spies
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