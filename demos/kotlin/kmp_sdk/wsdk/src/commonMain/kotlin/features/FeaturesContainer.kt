package features

import domain.api.IOperationMarshaller
import domain.data.ICameraRepository
import domain.gopro.GpDescriptorManager
import domain.gopro.IGpDescriptor
import entity.connector.ICameraConnector
import gopro.CameraConnector
import gopro.GoProFacadeFactory
import operation.CommandsContainer
import operation.SettingsContainer
import operation.StatusesContainer

// TODO let's see how these evolve. It might make more sense to just put them in the
// commands container.

interface IFeatureContext {
    val serialId: String
    val marshaller: IOperationMarshaller
    val commands: CommandsContainer
    val settings: SettingsContainer
    val statuses: StatusesContainer
    val descriptor: IGpDescriptor
    val gpDescriptorManager: GpDescriptorManager
    val cameraRepo: ICameraRepository
    val connector: ICameraConnector
    val facadeFactory: GoProFacadeFactory
}

data class FeatureContext(
    override val marshaller: IOperationMarshaller,
    override val commands: CommandsContainer,
    override val settings: SettingsContainer,
    override val statuses: StatusesContainer,
    override val gpDescriptorManager: GpDescriptorManager,
    override val cameraRepo: ICameraRepository,
    override val connector: ICameraConnector,
    override val facadeFactory: GoProFacadeFactory
) : IFeatureContext {
    override val descriptor: IGpDescriptor get() = gpDescriptorManager.getDescriptor()
    override val serialId get() = descriptor.serialId
}

class FeaturesContainer(featureContext: FeatureContext) {
    val accessPoint = AccessPointFeature(featureContext)
    val cohn = CohnFeature(featureContext)
    val connectWifi = ConnectWifiFeature(featureContext)
}