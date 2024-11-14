package gopro

import domain.api.IOperationMarshaller
import entity.constants.Fps
import entity.constants.Resolution
import entity.constants.SettingId
import operation.queries.Setting

class SettingsContainer internal constructor (marshaller: IOperationMarshaller) {
    val resolution = Setting(SettingId.RESOLUTION, Resolution, marshaller)
    val fps = Setting(SettingId.FPS, Fps, marshaller)
}