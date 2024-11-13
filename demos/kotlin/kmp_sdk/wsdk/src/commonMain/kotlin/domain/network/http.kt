package domain.network

import entity.network.IHttpsCredentials
import io.ktor.client.HttpClient
import io.ktor.client.request.HttpRequestBuilder
import io.ktor.client.statement.HttpResponse

internal interface IHttpClientProvider {
    fun provideBaseClient(credentials: IHttpsCredentials?): HttpClient
}

internal interface IHttpApi {
    suspend fun get(client: HttpClient, requestBuilder: HttpRequestBuilder.() -> Unit): HttpResponse
    suspend fun post(
        client: HttpClient,
        requestBuilder: HttpRequestBuilder.() -> Unit
    ): HttpResponse
}