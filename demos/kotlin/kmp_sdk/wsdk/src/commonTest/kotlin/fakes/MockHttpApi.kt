/* MockHttpApi.kt/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Tue Feb 18 18:41:30 UTC 2025 */

package fakes

import com.gopro.open_gopro.domain.network.IHttpApi
import io.ktor.client.HttpClient
import io.ktor.client.request.HttpRequestBuilder
import io.ktor.client.request.get
import io.ktor.client.request.post
import io.ktor.client.statement.HttpResponse

data class HttpSpy(val request: HttpRequestBuilder)

class FakeHttpApi : IHttpApi {
  val spies = mutableListOf<HttpSpy>()

  override suspend fun get(
      client: HttpClient,
      requestBuilder: HttpRequestBuilder.() -> Unit
  ): HttpResponse {
    spies += HttpSpy(HttpRequestBuilder().apply(requestBuilder))
    return client.get(requestBuilder)
  }

  override suspend fun post(
      client: HttpClient,
      requestBuilder: HttpRequestBuilder.() -> Unit
  ): HttpResponse {
    spies += HttpSpy(HttpRequestBuilder().apply(requestBuilder))
    return client.post(requestBuilder)
  }
}
