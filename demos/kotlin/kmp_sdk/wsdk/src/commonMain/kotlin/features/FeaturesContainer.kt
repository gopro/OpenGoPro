package features

import domain.api.IOperationMarshaller
import domain.data.ICameraRepository
import domain.gopro.GpDescriptorManager
import entity.connector.ICameraConnector
import gopro.GoProFacade
import gopro.IGoProFacadeFactory

interface IFeatureContext {
    val gopro: GoProFacade
    val gpDescriptorManager: GpDescriptorManager
    val cameraRepo: ICameraRepository
    val connector: ICameraConnector
    val facadeFactory: IGoProFacadeFactory
}

internal data class FeatureContext(
    override val gopro: GoProFacade,
    override val gpDescriptorManager: GpDescriptorManager,
    override val cameraRepo: ICameraRepository,
    override val connector: ICameraConnector,
    override val facadeFactory: IGoProFacadeFactory
) : IFeatureContext

class FeaturesContainer(featureContext: IFeatureContext) {
    val accessPoint = AccessPointFeature(featureContext)
    val cohn = CohnFeature(featureContext)
    val connectWifi = ConnectWifiFeature(featureContext)
}