import domain.network.IWifiApi
import kotlinx.coroutines.CoroutineDispatcher
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.flow

class FakeWifiApi(override val dispatcher: CoroutineDispatcher) : IWifiApi {
    override suspend fun setup() {
        TODO("Not yet implemented")
    }

    override suspend fun scanForSsid(): Result<Flow<String>> {
        TODO("Not yet implemented")
    }

    override suspend fun connect(ssid: String, password: String): Result<Unit> {
        TODO("Not yet implemented")
    }

    override suspend fun disconnect(ssid: String): Result<Unit> {
        TODO("Not yet implemented")
    }

    override fun receiveDisconnects(): Flow<String> =
        flow {

        }
}