package fakes

import com.gopro.open_gopro.di.createHttpClient
import com.gopro.open_gopro.domain.communicator.BleCommunicator
import com.gopro.open_gopro.domain.communicator.HttpCommunicator
import com.gopro.open_gopro.domain.network.IHttpClientProvider
import com.gopro.open_gopro.ConnectionDescriptor
import com.gopro.open_gopro.GoProId
import com.gopro.open_gopro.entity.network.IHttpsCredentials
import com.gopro.open_gopro.entity.network.ble.BleDevice
import com.gopro.open_gopro.entity.network.ble.BleNotification
import com.gopro.open_gopro.entity.operation.PresetInfo
import com.gopro.open_gopro.entity.operation.jsonDefault
import com.gopro.open_gopro.entity.operation.serializeAsDefaultFromProto
import io.ktor.client.HttpClient
import io.ktor.client.engine.mock.MockEngine
import io.ktor.client.engine.mock.respond
import io.ktor.http.HttpHeaders
import io.ktor.http.HttpStatusCode
import io.ktor.http.headersOf
import io.ktor.utils.io.ByteReadChannel
import kotlinx.coroutines.CoroutineDispatcher
import kotlinx.serialization.encodeToString
import vectors.completeNotifyPresetStatus
import vectors.datetimeResponse
import vectors.mediaListJson
import vectors.mockMediaId
import vectors.mockOgpVersion
import vectors.photoMetadataJson
import vectors.webcamStatusResponseJson

internal data class FakeBleCommunicator(
    val communicator: BleCommunicator,
    val api: FakeBleApi,
    val connection: ConnectionDescriptor.Ble
) {
    val spies get() = api.spies
    suspend fun sendNextBleMessage() = api.sendNextMessage()
}

internal fun buildFakeBleCommunicator(
    responses: List<List<BleNotification>>,
    dispatcher: CoroutineDispatcher
): FakeBleCommunicator {
    val api = FakeBleApi(responses, dispatcher)
    val device = object : BleDevice {
        override val id = "bleDeviceId"
    }
    val communicator =
        BleCommunicator(api, ConnectionDescriptor.Ble(GoProId("serialId"), device), dispatcher)
    return FakeBleCommunicator(communicator, api, communicator.connection)
}

internal data class FakeHttpCommunicator(
    val communicator: HttpCommunicator,
    val api: FakeHttpApi,
    val connection: ConnectionDescriptor
) {
    val spies = api.spies
}

private val responseHeaders = headersOf(HttpHeaders.ContentType, "application/json")

private val mockEngine = MockEngine { request ->
    when (request.url.encodedPath) {
        "/com/gopro/open_gopro/gopro/media/last_captured" -> respond(
            content = ByteReadChannel(jsonDefault.encodeToString(mockMediaId)),
            status = HttpStatusCode.OK,
            headers = responseHeaders
        )

        "/com/gopro/open_gopro/gopro/camera/presets/get" -> {
            respond(
                content = ByteReadChannel(
                    serializeAsDefaultFromProto<PresetInfo>(
                        completeNotifyPresetStatus
                    )
                ),
                status = HttpStatusCode.OK,
                headers = responseHeaders
            )
        }

        "/com/gopro/open_gopro/gopro/version" -> respond(
            content = ByteReadChannel(jsonDefault.encodeToString(mockOgpVersion)),
            status = HttpStatusCode.OK,
            headers = responseHeaders
        )

        "/com/gopro/open_gopro/gopro/media/info" -> respond(
            content = ByteReadChannel(photoMetadataJson),
            status = HttpStatusCode.OK,
            headers = responseHeaders
        )

        "/com/gopro/open_gopro/gopro/media/list" -> respond(
            content = ByteReadChannel(mediaListJson),
            status = HttpStatusCode.OK,
            headers = responseHeaders
        )

        "/com/gopro/open_gopro/gopro/camera/get_date_time" -> respond(
            content = ByteReadChannel(jsonDefault.encodeToString(datetimeResponse)),
            status = HttpStatusCode.OK,
            headers = responseHeaders
        )

        "/com/gopro/open_gopro/gopro/webcam/status" -> respond(
            content = ByteReadChannel(webcamStatusResponseJson),
            status = HttpStatusCode.OK,
            headers = responseHeaders
        )

        // Empty successful responses
        "/com/gopro/open_gopro/gopro/livestream/setup",
        "/com/gopro/open_gopro/gopro/camera/control/set_ui_controller",
        "/gp/gpControl/command/storage/delete/group",
        "/com/gopro/open_gopro/gopro/camera/set_date_time",
        "/com/gopro/open_gopro/gopro/camera/presets/update_custom" -> respond(
            content = ByteReadChannel("{}"),
            status = HttpStatusCode.OK,
            headers = responseHeaders
        )

        else -> error("Unhandled ${request.url.encodedPath}")
    }
}

internal object FakeHttpClientProvider : IHttpClientProvider {
    override fun provideBaseClient(credentials: IHttpsCredentials?): HttpClient =
        createHttpClient(mockEngine)

}

internal fun buildFakeHttpCommunicator(dispatcher: CoroutineDispatcher): FakeHttpCommunicator {
    val api = FakeHttpApi()
    val communicator =
        HttpCommunicator(
            api,
            ConnectionDescriptor.Http(id = GoProId("serialId"), "ipAddress"),
            FakeHttpClientProvider,
            dispatcher
        )
    return FakeHttpCommunicator(communicator, api, communicator.connection)
}