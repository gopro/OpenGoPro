import di.WsdkIsolatedKoinContext
import entity.connector.ICameraConnector
import gopro.CameraConnector
import gopro.GoProFacadeFactory
import gopro.IGoProFacadeFactory
import org.koin.dsl.KoinAppDeclaration

object Wsdk {
    // https://medium.com/@gusakov.giorgi/using-koin-dependency-injection-in-library-sdk-7be76291ecad
    fun getCameraConnector(config: KoinAppDeclaration? = null): ICameraConnector =
        WsdkIsolatedKoinContext.getWsdkKoinApp(config).koin.get()

    fun getGoProFacadeFactory(config: KoinAppDeclaration? = null): IGoProFacadeFactory =
        WsdkIsolatedKoinContext.getWsdkKoinApp(config).koin.get()
}