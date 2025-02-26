/* AppleHttpClientProvider.kt/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Tue Feb 18 18:41:30 UTC 2025 */

package com.gopro.open_gopro.network

import com.gopro.open_gopro.domain.network.IHttpClientProvider
import com.gopro.open_gopro.entity.network.IHttpsCredentials
import io.ktor.client.HttpClient

internal class AppleHttpClientProvider : IHttpClientProvider {
  override fun provideBaseClient(credentials: IHttpsCredentials?): HttpClient {
    TODO("Not yet implemented")
  }
}
