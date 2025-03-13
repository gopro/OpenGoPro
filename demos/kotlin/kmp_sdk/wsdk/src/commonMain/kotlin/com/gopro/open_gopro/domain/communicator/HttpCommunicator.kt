/* HttpCommunicator.kt/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Tue Feb 18 18:41:29 UTC 2025 */

package com.gopro.open_gopro.domain.communicator

import co.touchlab.kermit.Logger
import com.gopro.open_gopro.CommunicationType
import com.gopro.open_gopro.ConnectionDescriptor
import com.gopro.open_gopro.HttpError
import com.gopro.open_gopro.NetworkError
import com.gopro.open_gopro.domain.network.IHttpApi
import com.gopro.open_gopro.domain.network.IHttpClientProvider
import com.gopro.open_gopro.operations.SerializationError
import io.ktor.client.plugins.ClientRequestException
import io.ktor.client.plugins.ServerResponseException
import io.ktor.client.plugins.defaultRequest
import io.ktor.client.request.HttpRequestBuilder
import io.ktor.client.statement.HttpResponse
import io.ktor.client.statement.bodyAsText
import io.ktor.http.URLProtocol
import io.ktor.utils.io.errors.IOException
import kotlinx.coroutines.CoroutineDispatcher
import kotlinx.serialization.SerializationException

private val logger = Logger.withTag("HttpCommunicator")

internal class HttpCommunicator(
    private val httpApi: IHttpApi,
    override val connection: ConnectionDescriptor.Http,
    httpClientProvider: IHttpClientProvider,
    dispatcher: CoroutineDispatcher
) : ICommunicator<ConnectionDescriptor.Http>() {

  private val client =
      httpClientProvider.provideBaseClient(connection.credentials).config {
        defaultRequest {
          host = connection.ipAddress
          connection.port?.let { port = it }
          url { protocol = connection.credentials?.let { URLProtocol.HTTPS } ?: URLProtocol.HTTP }
        }
      }

  override val communicationType = CommunicationType.HTTP

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
