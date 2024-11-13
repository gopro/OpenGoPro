package di

import gopro.CameraConnector
import gopro.IGoProFacadeFactory
import org.junit.Test
import org.koin.core.annotation.KoinExperimentalAPI
import org.koin.test.verify.verify

class VerifyKoinModules {

    @OptIn(KoinExperimentalAPI::class)
    @Test
    fun `verify koin modules`() {
        buildAppModule().verify(
            extraTypes = listOf(
                IGoProFacadeFactory::class,
                CameraConnector::class,
            )
        )
    }
}