package com.gopro.open_gopro.network

import com.gopro.open_gopro.domain.network.IHttpClientProvider
import com.gopro.open_gopro.entity.network.IHttpsCredentials
import io.ktor.client.HttpClient

internal class AppleHttpClientProvider: IHttpClientProvider {
    override fun provideBaseClient(credentials: IHttpsCredentials?): HttpClient {
        TODO("Not yet implemented")
    }
}