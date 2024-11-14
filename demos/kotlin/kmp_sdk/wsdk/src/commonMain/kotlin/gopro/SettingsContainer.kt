package gopro

import domain.api.IOperationMarshaller
import entity.queries.Fps
import entity.queries.Resolution
import entity.queries.SettingId
import domain.queries.Setting

class SettingsContainer internal constructor (marshaller: IOperationMarshaller) {
    val resolution = Setting(SettingId.RESOLUTION, Resolution, marshaller)
    val fps = Setting(SettingId.FPS, Fps, marshaller)
}