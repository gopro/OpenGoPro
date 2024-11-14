package gopro

import domain.connector.ICameraConnector
import domain.gopro.GpDescriptorManager
import domain.gopro.IGoProFacadeFactory
import features.AccessPointFeature
import features.CohnFeature
import features.ConnectWifiFeature

internal interface IFeatureContext {
    val gopro: GoProFacade
    val gpDescriptorManager: GpDescriptorManager
    val connector: ICameraConnector
    val facadeFactory: IGoProFacadeFactory
}

internal data class FeatureContext(
    override val gopro: GoProFacade,
    override val gpDescriptorManager: GpDescriptorManager,
    override val connector: ICameraConnector,
    override val facadeFactory: IGoProFacadeFactory
) : IFeatureContext

class FeaturesContainer internal constructor(featureContext: IFeatureContext) {
    val accessPoint = AccessPointFeature(featureContext)
    val cohn = CohnFeature(featureContext)
    val connectWifi = ConnectWifiFeature(featureContext)
}