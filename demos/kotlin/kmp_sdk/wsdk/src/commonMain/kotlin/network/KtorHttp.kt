package network

import co.touchlab.kermit.Logger
import domain.network.IHttpApi
import io.ktor.client.HttpClient
import io.ktor.client.request.HttpRequestBuilder
import io.ktor.client.request.get
import io.ktor.client.request.post
import io.ktor.client.statement.HttpResponse
import io.ktor.http.HttpMethod

private val logger = Logger.withTag("KtorHttp")

class KtorHttp : IHttpApi {
    private suspend fun robustlyPerformHttpOperation(operation: suspend () -> HttpResponse): HttpResponse {
        for (retry in (1..HTTP_RETRIES)) {
            try {
                return operation()
            } catch (e: Exception) {
                logger.e("HTTP Operation failed: ${e.message ?: ""}")
            }
        }
        throw Exception("Failed to perform HTTP operation after $HTTP_RETRIES retries")
    }


    override suspend fun get(
        client: HttpClient,
        requestBuilder: HttpRequestBuilder.() -> Unit
    ): HttpResponse =
        robustlyPerformHttpOperation { client.get(requestBuilder) }

    override suspend fun post(
        client: HttpClient,
        requestBuilder: HttpRequestBuilder.() -> Unit
    ): HttpResponse =
        robustlyPerformHttpOperation {
            client.post {
                HttpRequestBuilder().apply {
                    takeFrom(HttpRequestBuilder().apply(requestBuilder))
                    method = HttpMethod.Post // It defaults to GET so ensure this is an actual POST.
                }
            }
        }

    companion object {
        const val HTTP_RETRIES = 5
    }
}