package di

import WsdkAppContext
import androidx.datastore.core.DataStore
import androidx.datastore.preferences.core.Preferences
import data.dataStore
import org.koin.core.module.Module
import org.koin.dsl.module
import ui.components.AndroidImageRequestBuilder
import ui.components.AndroidVideoPlayer
import ui.components.IImageRequestBuilder
import ui.components.IStreamPlayer
import ui.components.IVideoPlayer
import ui.components.LibVlcStreamPlayer

actual fun buildPlatformModules(appContext: WsdkAppContext): Module = module {
    single<DataStore<Preferences>> { dataStore(appContext.get()) }
    factory<IImageRequestBuilder> { AndroidImageRequestBuilder(appContext.get()) }
//        factory<IStreamPlayer> { ExoplayerStreamPlayer(appContext.get()) }
    factory<IStreamPlayer> { LibVlcStreamPlayer(appContext.get()) }
    factory<IVideoPlayer> { AndroidVideoPlayer(appContext.get()) }
}

