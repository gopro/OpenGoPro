/* FakeGoProFacadeFactory.kt/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Tue Feb 18 18:41:30 UTC 2025 */

package fakes

import FakeWifiApi
import com.gopro.open_gopro.domain.gopro.IGoProFactory
import com.gopro.open_gopro.gopro.GoProFactory
import kotlinx.coroutines.CoroutineDispatcher

internal fun buildFakeGoPro(dispatcher: CoroutineDispatcher): IGoProFactory =
    GoProFactory(
        dispatcher = dispatcher,
        bleApi = FakeBleApi(listOf(), dispatcher),
        httpApi = buildFakeHttpCommunicator(dispatcher).api,
        wifiApi = FakeWifiApi(dispatcher),
        httpClientProvider = FakeHttpClientProvider)
