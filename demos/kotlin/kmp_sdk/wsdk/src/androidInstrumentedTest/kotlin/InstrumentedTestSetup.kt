import androidx.test.platform.app.InstrumentationRegistry
import domain.network.IDnsApi
import domain.network.IWifiApi
import kotlinx.coroutines.ExperimentalCoroutinesApi
import kotlinx.coroutines.test.UnconfinedTestDispatcher
import org.junit.Rule
import org.junit.rules.TestWatcher
import org.junit.runner.Description
import org.koin.core.context.GlobalContext.getKoinApplicationOrNull
import org.koin.core.context.loadKoinModules
import org.koin.core.context.startKoin
import org.koin.core.context.unloadKoinModules
import org.koin.core.module.Module
import org.koin.dsl.module
import org.koin.test.KoinTest
import org.koin.test.mock.MockProviderRule
import org.koin.test.mock.declareMock
import org.mockito.Mockito

open class AndroidInstrumentedKoinTest : KoinTest {
    @get:Rule
    val mockProvider = MockProviderRule.create { clazz ->
        Mockito.mock(clazz.java)
    }

    @get:Rule
    val koinTestRule = KoinTestRule(listOf(module {
        single<IWifiApi> { declareMock() }
        single<IDnsApi> { declareMock() }
    }))
}

@OptIn(ExperimentalCoroutinesApi::class)
class KoinTestRule(private val additionalModules: List<Module>? = null) : TestWatcher() {
    private val testModule: Module

    init {
        Wsdk.init(
            dispatcher = UnconfinedTestDispatcher(),
            appContext = WsdkAppContext().apply {
                set(InstrumentationRegistry.getInstrumentation().targetContext.applicationContext)
            })
        testModule = WsdkIsolatedKoinContext.koinModules!!
    }

    override fun starting(description: Description) {
        if (getKoinApplicationOrNull() == null) {
            startKoin {
                modules(testModule)
                additionalModules?.let { modules(it) }
            }
        } else {
            loadKoinModules(testModule)
            additionalModules?.let { loadKoinModules(it) }
        }
    }

    override fun finished(description: Description) {
        unloadKoinModules(testModule)
        additionalModules?.let { unloadKoinModules(it) }
    }
}
