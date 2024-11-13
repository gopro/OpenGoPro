import androidx.test.platform.app.InstrumentationRegistry
import kotlinx.coroutines.ExperimentalCoroutinesApi
import kotlinx.coroutines.test.UnconfinedTestDispatcher
import org.junit.rules.TestWatcher
import org.junit.runner.Description
import org.koin.core.context.GlobalContext.getKoinApplicationOrNull
import org.koin.core.context.loadKoinModules
import org.koin.core.context.startKoin
import org.koin.core.context.unloadKoinModules
import org.koin.core.module.Module

@OptIn(ExperimentalCoroutinesApi::class)
class KoinTestRule(private val additionalModules: List<Module>? = null) : TestWatcher() {
    private val testModule: Module

    init {
        AppContext.set(InstrumentationRegistry.getInstrumentation().targetContext.applicationContext)
        Wsdk.init(UnconfinedTestDispatcher(), AppContext)
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
