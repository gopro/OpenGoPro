import domain.communicator.BleCommunicator
import domain.communicator.bleCommunicator.bleFragment
import entity.queries.Resolution
import entity.network.BleNotification
import entity.network.GpUuid
import extensions.toTlvMap
import fakes.buildFakeSettingsContainer
import kotlinx.coroutines.ExperimentalCoroutinesApi
import kotlinx.coroutines.flow.onEach
import kotlinx.coroutines.flow.onStart
import kotlinx.coroutines.flow.take
import kotlinx.coroutines.launch
import kotlinx.coroutines.test.UnconfinedTestDispatcher
import kotlinx.coroutines.test.runTest
import vectors.asynchronousSettingValueUpdateMessage1
import vectors.asynchronousSettingValueUpdateMessage2
import vectors.getMultipleSettingsResponsePayload
import vectors.getSettingResponseMessage
import vectors.getSettingResponseMessage2
import vectors.getSettingResponseMessage3
import vectors.getSettingResponsePayload
import vectors.registerSettingValueResponseMessage
import vectors.setSettingResponseMessage
import kotlin.test.Test
import kotlin.test.assertEquals
import kotlin.test.assertTrue

// TODO check spies

@OptIn(ExperimentalUnsignedTypes::class, ExperimentalCoroutinesApi::class)
class TestSettings {

    @Test
    fun `set resolution`() = runTest {
        // GIVEN
        val responses = listOf(
            listOf(
                BleNotification(GpUuid.CQ_SETTINGS_RESP.toUuid(), setSettingResponseMessage)
            )
        )
        val fakeSettingsContainer = buildFakeSettingsContainer(responses, UnconfinedTestDispatcher())
        val setting = fakeSettingsContainer.settingsContainer.resolution

        // WHEN
        val result = setting.setValue(Resolution.RES_1080)

        // THEN
        assertTrue { result.isSuccess }
        assertTrue { result.getOrThrow() }
    }

    @Test
    fun `tlv to map extension`() {
        // GIVEN
        val data = getSettingResponsePayload.drop(2)

        // WHEN
        val tlvMap = data.toTlvMap()

        // THEN
        assertEquals(tlvMap.size, 1)
        assertEquals(tlvMap.getValue(2U).first(), 9U.toUByte())
    }

    @Test
    fun `get resolution`() = runTest {
        // GIVEN
        val responses =
            listOf(
                listOf(
                    BleNotification(
                        GpUuid.CQ_QUERY_RESP.toUuid(),
                        getSettingResponseMessage
                    )
                )
            )
        val fakeSettingsContainer = buildFakeSettingsContainer(responses, UnconfinedTestDispatcher())
        val setting = fakeSettingsContainer.settingsContainer.resolution

        // WHEN
        val result = setting.getValue()

        // THEN
        assertTrue { result.isSuccess }
        assertEquals(result.getOrThrow(), Resolution.RES_1080)
    }

    @Test
    fun `get multiple settings`() = runTest {
        // GIVEN
        val responses =
            listOf(
                getMultipleSettingsResponsePayload.bleFragment(BleCommunicator.MAX_PACKET_LENGTH)
                    .asSequence().map {
                        BleNotification(
                            GpUuid.CQ_QUERY_RESP.toUuid(),
                            it
                        )
                    }.toList()
            )
        val fakeSettingsContainer = buildFakeSettingsContainer(responses, UnconfinedTestDispatcher())
        val setting = fakeSettingsContainer.settingsContainer.resolution

        // WHEN
        val result = setting.getValue()
        // THEN
        assertTrue { result.isSuccess }
        assertEquals(result.getOrThrow(), Resolution.RES_1080)
    }

    @Test
    fun `multiple consecutive operations`() = runTest {
        // GIVEN
        val responses =
            listOf(
                listOf(BleNotification(GpUuid.CQ_QUERY_RESP.toUuid(), getSettingResponseMessage)),
                listOf(BleNotification(GpUuid.CQ_QUERY_RESP.toUuid(), getSettingResponseMessage2)),
                listOf(BleNotification(GpUuid.CQ_QUERY_RESP.toUuid(), getSettingResponseMessage3)),
            )
        val fakeSettingsContainer = buildFakeSettingsContainer(responses, UnconfinedTestDispatcher())
        val setting = fakeSettingsContainer.settingsContainer.resolution

        // WHEN / THEN
        var result = setting.getValue()
        assertTrue { result.isSuccess }
        assertEquals(result.getOrThrow(), Resolution.RES_1080)

        result = setting.getValue()
        assertTrue { result.isSuccess }
        assertEquals(result.getOrThrow(), Resolution.RES_720)

        result = setting.getValue()
        assertTrue { result.isSuccess }
        assertEquals(result.getOrThrow(), Resolution.RES_4K_4_3)
    }

    @Test
    fun `register resolution value updates`() = runTest {
        // GIVEN
        val responses = listOf(
            listOf(
                BleNotification(
                    GpUuid.CQ_QUERY_RESP.toUuid(),
                    registerSettingValueResponseMessage
                )
            ),
            listOf(
                BleNotification(
                    GpUuid.CQ_QUERY_RESP.toUuid(),
                    asynchronousSettingValueUpdateMessage1
                )
            ),
            listOf(
                BleNotification(
                    GpUuid.CQ_QUERY_RESP.toUuid(),
                    asynchronousSettingValueUpdateMessage1
                )
            ),
            listOf(
                BleNotification(
                    GpUuid.CQ_QUERY_RESP.toUuid(),
                    asynchronousSettingValueUpdateMessage2
                )
            ),
        )
        val fakeSettingsContainer = buildFakeSettingsContainer(responses, UnconfinedTestDispatcher())
        val setting = fakeSettingsContainer.settingsContainer.resolution
        var initialValue: Resolution? = null

        var messageCount = 0

        // WHEN
        val settingUpdates = mutableListOf<Resolution>()
        setting.registerValueUpdate()
            .onSuccess { (currentValue, flow) ->
                initialValue = currentValue
                flow
                    .take(3)
                    .onStart {
                        launch {
                            fakeSettingsContainer.sendNextBleMessage()
                            messageCount += 1
                        }
                    }
                    .onEach {
                        launch {
                            try {
                                messageCount += 1
                                // Minus one because of the original message sent from the write.
                                if (messageCount <= responses.size - 1) fakeSettingsContainer.sendNextBleMessage()
                            } catch (exc: Exception) {
                                println(exc)
                            }
                        }
                    }
                    .collect {
                        settingUpdates += it
                    }
            }
            .onFailure { assertTrue { false } }

        // THEN
        assertEquals(initialValue, Resolution.RES_1080)
        assertEquals(settingUpdates.size, 3)
        assertEquals(settingUpdates[0], Resolution.RES_1080)
        assertEquals(settingUpdates[1], Resolution.RES_1080)
        assertEquals(settingUpdates[2], Resolution.RES_720)
    }
}