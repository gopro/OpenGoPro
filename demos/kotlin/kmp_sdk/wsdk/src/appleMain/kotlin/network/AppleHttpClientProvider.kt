package network

import domain.network.IHttpClientProvider
import entity.network.IHttpsCredentials
import io.ktor.client.HttpClient

internal class AppleHttpClientProvider: IHttpClientProvider {
    override fun provideBaseClient(credentials: IHttpsCredentials?): HttpClient {
        TODO("Not yet implemented")
    }
}