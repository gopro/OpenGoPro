package fakes

import FakeWifiApi
import domain.gopro.IGoProFactory
import gopro.GoProFactory
import kotlinx.coroutines.CoroutineDispatcher

internal fun buildFakeGoPro(dispatcher: CoroutineDispatcher): IGoProFactory =
    GoProFactory(
        dispatcher = dispatcher,
        bleApi = FakeBleApi(listOf(), dispatcher),
        httpApi = buildFakeHttpCommunicator(dispatcher).api,
        wifiApi = FakeWifiApi(dispatcher),
        httpClientProvider = FakeHttpClientProvider
    )

