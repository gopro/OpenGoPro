package gopro

import entity.network.BleNotification
import entity.network.GpUuid
import fakes.FakeGoProFacadeProvider
import fakes.buildFakeBleCommunicator
import kotlinx.coroutines.ExperimentalCoroutinesApi
import kotlinx.coroutines.flow.first
import kotlinx.coroutines.launch
import kotlinx.coroutines.test.UnconfinedTestDispatcher
import kotlinx.coroutines.test.runTest
import kotlinx.datetime.Clock
import kotlinx.datetime.Instant
import kotlinx.datetime.LocalDateTime
import kotlinx.datetime.TimeZone
import kotlinx.datetime.offsetAt
import kotlinx.datetime.toLocalDateTime
import org.koin.test.KoinTest
import vectors.isBusyNotificationMessage
import vectors.isEncodingNotificationMessage
import vectors.isNotBusyNotificationMessage
import vectors.isNotEncodingNotificationMessage
import vectors.registerBusyResponseMessage
import vectors.registerEncodingResponseMessage
import kotlin.test.Test
import kotlin.test.assertEquals

@OptIn(ExperimentalUnsignedTypes::class, ExperimentalCoroutinesApi::class)
class TestGoProFacade : KoinTest {
    @Test
    fun `maintain ready state`() = runTest {
        // GIVEN
        // busy    : 1 -> 0 -> 1 -> 0 == 4 state change notifications
        // encoding: 1 -> 1 -> 0      == 2 state change notifications
        val responses = listOf(
            // Register responses
            listOf(BleNotification(GpUuid.CQ_QUERY_RESP.toUuid(), registerBusyResponseMessage)),
            listOf(BleNotification(GpUuid.CQ_QUERY_RESP.toUuid(), registerEncodingResponseMessage)),
            // Notification responses
            listOf(BleNotification(GpUuid.CQ_QUERY_RESP.toUuid(), isEncodingNotificationMessage)),
            listOf(BleNotification(GpUuid.CQ_QUERY_RESP.toUuid(), isNotBusyNotificationMessage)),
            listOf(BleNotification(GpUuid.CQ_QUERY_RESP.toUuid(), isBusyNotificationMessage)),
            listOf(
                BleNotification(
                    GpUuid.CQ_QUERY_RESP.toUuid(),
                    isNotEncodingNotificationMessage
                )
            ),
            listOf(BleNotification(GpUuid.CQ_QUERY_RESP.toUuid(), isNotBusyNotificationMessage)),
        )
        val fakeCommunicator = buildFakeBleCommunicator(responses, UnconfinedTestDispatcher())
        val gopro = FakeGoProFacadeProvider().getGoProFacade("1234", UnconfinedTestDispatcher())

        val busyStates = mutableListOf<Boolean>()
        val encodingStates = mutableListOf<Boolean>()

        // WHEN / THEN
        val checkBusyJob = launch {
            gopro.isBusy.collect {
                busyStates += it
                println("Collected busy state ${busyStates.size} ==> $it")
            }
        }
        val checkEncodingJob = launch {
            gopro.isEncoding.collect {
                encodingStates += it
                println("Collected encoding state ${encodingStates.size} ==> $it")
            }
        }

        println("Test binding communicator")
        gopro.bindCommunicator(fakeCommunicator.communicator)
        println("Did I get here?")

        launch {
            fakeCommunicator.sendNextBleMessage()
        }.join()
        launch {
            fakeCommunicator.sendNextBleMessage()
        }.join()
        launch {
            fakeCommunicator.sendNextBleMessage()
        }.join()
        launch {
            fakeCommunicator.sendNextBleMessage()
        }.join()
        launch {
            fakeCommunicator.sendNextBleMessage()
        }.join()

        // Wait to be ready
        println("Test waiting for gopro to be ready.")
        gopro.isReady.first { it }
        checkBusyJob.cancel()
        checkEncodingJob.cancel()

        // THEN
        assertEquals(4, busyStates.size)
        assertEquals(2, encodingStates.size)
    }
}