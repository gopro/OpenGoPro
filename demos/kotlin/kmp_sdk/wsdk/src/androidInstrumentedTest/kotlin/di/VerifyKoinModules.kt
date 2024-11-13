package di

import gopro.CameraConnector
import gopro.GoProFacadeFactory
import org.junit.Test
import org.koin.core.annotation.KoinExperimentalAPI
import org.koin.test.verify.verify

//class VerifyKoinModules {
//    @OptIn(KoinExperimentalAPI::class)
//    @Test
//    fun `verify koin modules`() {
//        initTestWsdk().verify(
//            extraTypes = listOf(
//                GoProFacadeFactory::class,
//                CameraConnector::class,
//            )
//        )
//    }
//}