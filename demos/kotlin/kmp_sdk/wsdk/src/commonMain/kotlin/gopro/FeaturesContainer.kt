package gopro

import domain.connector.ICameraConnector
import domain.gopro.GpDescriptorManager
import domain.gopro.IGoProFactory
import features.AccessPointFeature
import features.CohnFeature
import features.ConnectWifiFeature

internal interface IFeatureContext {
    val gopro: GoPro
    val gpDescriptorManager: GpDescriptorManager
    val connector: ICameraConnector
    val facadeFactory: IGoProFactory
}

internal data class FeatureContext(
    override val gopro: GoPro,
    override val gpDescriptorManager: GpDescriptorManager,
    override val connector: ICameraConnector,
    override val facadeFactory: IGoProFactory
) : IFeatureContext

class FeaturesContainer internal constructor(featureContext: IFeatureContext) {
    val accessPoint = AccessPointFeature(featureContext)
    val cohn = CohnFeature(featureContext)
    val connectWifi = ConnectWifiFeature(featureContext)
}