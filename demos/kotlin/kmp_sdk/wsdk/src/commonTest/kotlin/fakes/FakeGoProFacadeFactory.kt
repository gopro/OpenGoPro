package fakes

import FakeWifiApi
import domain.gopro.IGoProFactory
import gopro.GoProFactory
import kotlinx.coroutines.CoroutineDispatcher

fun buildFakeGoPro(dispatcher: CoroutineDispatcher): IGoProFactory =
    GoProFactory(
        dispatcher = dispatcher,
        cameraRepository = FakeCameraRepo(),
        cameraConnector = FakeCameraConnector(),
        bleApi = FakeBleApi(listOf(), dispatcher),
        httpApi = buildFakeHttpCommunicator(dispatcher).api,
        wifiApi = FakeWifiApi(dispatcher),
        httpClientProvider = FakeHttpClientProvider
    )

