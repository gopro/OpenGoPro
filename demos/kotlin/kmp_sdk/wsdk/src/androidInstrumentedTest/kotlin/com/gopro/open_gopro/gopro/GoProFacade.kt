/* GoProFacade.kt/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Tue Feb 18 18:41:30 UTC 2025 */

package com.gopro.open_gopro.gopro

import com.gopro.open_gopro.AndroidInstrumentedKoinTest
import com.gopro.open_gopro.entity.network.ble.BleNotification
import com.gopro.open_gopro.entity.network.ble.GpUuid
import fakes.FakeGoProProvider
import fakes.buildFakeBleCommunicator
import kotlin.test.Test
import kotlin.test.assertEquals
import kotlinx.coroutines.ExperimentalCoroutinesApi
import kotlinx.coroutines.flow.first
import kotlinx.coroutines.launch
import kotlinx.coroutines.test.UnconfinedTestDispatcher
import kotlinx.coroutines.test.runTest
import vectors.isBusyNotificationMessage
import vectors.isEncodingNotificationMessage
import vectors.isNotBusyNotificationMessage
import vectors.isNotEncodingNotificationMessage
import vectors.registerBusyResponseMessage
import vectors.registerEncodingResponseMessage

@OptIn(ExperimentalUnsignedTypes::class, ExperimentalCoroutinesApi::class)
class TestGoPro : AndroidInstrumentedKoinTest() {
  @Test
  fun `maintain ready state`() = runTest {
    // GIVEN
    // busy    : 1 -> 0 -> 1 -> 0 == 4 state change notifications
    // encoding: 1 -> 1 -> 0      == 2 state change notifications
    val responses =
        listOf(
            // Register responses
            listOf(BleNotification(GpUuid.CQ_QUERY_RESP.toUuid(), registerBusyResponseMessage)),
            listOf(BleNotification(GpUuid.CQ_QUERY_RESP.toUuid(), registerEncodingResponseMessage)),
            // Notification responses
            listOf(BleNotification(GpUuid.CQ_QUERY_RESP.toUuid(), isEncodingNotificationMessage)),
            listOf(BleNotification(GpUuid.CQ_QUERY_RESP.toUuid(), isNotBusyNotificationMessage)),
            listOf(BleNotification(GpUuid.CQ_QUERY_RESP.toUuid(), isBusyNotificationMessage)),
            listOf(
                BleNotification(GpUuid.CQ_QUERY_RESP.toUuid(), isNotEncodingNotificationMessage)),
            listOf(BleNotification(GpUuid.CQ_QUERY_RESP.toUuid(), isNotBusyNotificationMessage)),
        )
    val fakeCommunicator = buildFakeBleCommunicator(responses, UnconfinedTestDispatcher())
    val gopro = FakeGoProProvider().getGoPro("1234", UnconfinedTestDispatcher())

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

    launch { fakeCommunicator.sendNextBleMessage() }.join()
    launch { fakeCommunicator.sendNextBleMessage() }.join()
    launch { fakeCommunicator.sendNextBleMessage() }.join()
    launch { fakeCommunicator.sendNextBleMessage() }.join()
    launch { fakeCommunicator.sendNextBleMessage() }.join()

    // Wait to be ready
    println("Test waiting for gopro to be ready.")
    gopro.isReady.first { it }
    println("Test gopro is ready")
    checkBusyJob.cancel()
    checkEncodingJob.cancel()

    // THEN
    assertEquals(4, busyStates.size)
    assertEquals(2, encodingStates.size)
  }
}
