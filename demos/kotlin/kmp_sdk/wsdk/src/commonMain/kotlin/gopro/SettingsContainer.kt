package gopro

import domain.api.IOperationMarshaller
import entity.constants.Fps
import entity.constants.Resolution
import entity.constants.SettingId
import operation.queries.SettingFacade

class SettingsContainer internal constructor (marshaller: IOperationMarshaller) {
    val resolution = SettingFacade(SettingId.RESOLUTION, Resolution, marshaller)
    val fps = SettingFacade(SettingId.FPS, Fps, marshaller)
}