/* http.kt/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Tue Feb 18 18:41:29 UTC 2025 */

package com.gopro.open_gopro.domain.network

import com.gopro.open_gopro.entity.network.IHttpsCredentials
import io.ktor.client.HttpClient
import io.ktor.client.request.HttpRequestBuilder
import io.ktor.client.statement.HttpResponse

internal interface IHttpClientProvider {
  fun provideBaseClient(credentials: IHttpsCredentials?): HttpClient
}

internal interface IHttpApi {
  suspend fun get(client: HttpClient, requestBuilder: HttpRequestBuilder.() -> Unit): HttpResponse

  suspend fun post(client: HttpClient, requestBuilder: HttpRequestBuilder.() -> Unit): HttpResponse
}
