package fakes

import FakeWifiApi
import domain.gopro.IGoProFacadeFactory
import gopro.GoProFacadeFactory
import kotlinx.coroutines.CoroutineDispatcher

fun buildFakeGoProFacade(dispatcher: CoroutineDispatcher): IGoProFacadeFactory =
    GoProFacadeFactory(
        dispatcher = dispatcher,
        cameraRepository = FakeCameraRepo(),
        cameraConnector = FakeCameraConnector(),
        bleApi = FakeBleApi(listOf(), dispatcher),
        httpApi = buildFakeHttpCommunicator(dispatcher).api,
        wifiApi = FakeWifiApi(dispatcher),
        httpClientProvider = FakeHttpClientProvider
    )

