package domain.communicator

import co.touchlab.kermit.Logger
import domain.network.IHttpApi
import domain.network.IHttpClientProvider
import entity.communicator.CommunicationType
import entity.connector.ConnectionDescriptor
import entity.exceptions.HttpError
import entity.exceptions.NetworkError
import entity.exceptions.SerializationError
import io.ktor.client.plugins.ClientRequestException
import io.ktor.client.plugins.ServerResponseException
import io.ktor.client.plugins.defaultRequest
import io.ktor.client.request.HttpRequestBuilder
import io.ktor.client.statement.HttpResponse
import io.ktor.client.statement.bodyAsText
import io.ktor.http.URLProtocol
import io.ktor.utils.io.errors.IOException
import kotlinx.coroutines.CoroutineDispatcher
import kotlinx.coroutines.CoroutineExceptionHandler
import kotlinx.coroutines.CoroutineScope
import kotlinx.serialization.SerializationException

private val logger = Logger.withTag("HttpCommunicator")

class HttpCommunicator(
    private val httpApi: IHttpApi,
    override val connection: ConnectionDescriptor.Http,
    httpClientProvider: IHttpClientProvider,
    dispatcher: CoroutineDispatcher
) : ICommunicator<ConnectionDescriptor.Http>() {

    private val client = httpClientProvider.provideBaseClient(connection.credentials).config {
        defaultRequest {
            host = connection.ipAddress
            connection.port?.let {
                port = it
            }
            url {
                protocol = connection.credentials?.let { URLProtocol.HTTPS } ?: URLProtocol.HTTP
            }
        }
    }


    // TODO how to cancel immediately when exception is found?
    private val coroutineExceptionHandler = CoroutineExceptionHandler { _, throwable ->
        logger.e("Caught exception in coroutine:", throwable)
    }

    // TODO is this correct? Do we need supervisorJob?
    val scope = CoroutineScope(dispatcher + coroutineExceptionHandler)

    override val communicationType = CommunicationType.HTTP

    // TODO
    override suspend fun setup() = true

    suspend fun get(requestBuilder: HttpRequestBuilder.() -> Unit): Result<HttpResponse> =
        try {
            Result.success(httpApi.get(client, requestBuilder))
        } catch (e: ClientRequestException) {
            Result.failure(HttpError(e.response.status.value, e.response.bodyAsText()))
        } catch (e: ServerResponseException) {
            Result.failure(HttpError(e.response.status.value, e.response.bodyAsText()))
        } catch (e: IOException) {
            Result.failure(NetworkError(e.message ?: ""))
        } catch (e: SerializationException) {
            Result.failure(SerializationError(e.message ?: ""))
        }

    suspend fun post(requestBuilder: HttpRequestBuilder.() -> Unit): Result<HttpResponse> =
        try {
            Result.success(httpApi.post(client, requestBuilder))
        } catch (e: ClientRequestException) {
            Result.failure(HttpError(e.response.status.value, e.response.bodyAsText()))
        } catch (e: ServerResponseException) {
            Result.failure(HttpError(e.response.status.value, e.response.bodyAsText()))
        } catch (e: IOException) {
            Result.failure(NetworkError(e.message ?: ""))
        } catch (e: SerializationException) {
            Result.failure(SerializationError(e.message ?: ""))
        }
}