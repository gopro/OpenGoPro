package gopro

import domain.api.IOperationMarshaller
import domain.queries.Setting
import entity.queries.Fps
import entity.queries.Resolution
import entity.queries.SettingId

/**
 * Container for all per-setting-ID wrappers
 *
 * Note! This is a very small subset of the supported settings. TODO these need to be
 * automatically generated.
 *
 * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html)
 *
 * @param marshaller
 */
class SettingsContainer internal constructor(marshaller: IOperationMarshaller) {
    /**
     * Video Resolution
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#video-resolution-2)
     */
    val resolution = Setting(SettingId.RESOLUTION, Resolution, marshaller)

    /**
     * Frames per Second
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#frames-per-second-3)
     */
    val fps = Setting(SettingId.FPS, Fps, marshaller)
}