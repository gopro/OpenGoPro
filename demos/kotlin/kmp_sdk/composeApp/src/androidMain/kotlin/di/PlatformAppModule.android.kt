package di

import androidx.datastore.core.DataStore
import androidx.datastore.preferences.core.Preferences
import data.dataStore
import org.koin.android.ext.koin.androidContext
import org.koin.dsl.module
import ui.components.AndroidImageRequestBuilder
import ui.components.ExoplayerStreamPlayer
import ui.components.AndroidVideoPlayer
import ui.components.IImageRequestBuilder
import ui.components.IStreamPlayer
import ui.components.IVideoPlayer
import ui.components.LibVlcStreamPlayer

actual val platformModule = object : PlatformModule {
    override val module = module {
        single<DataStore<Preferences>> { dataStore(androidContext()) }
        factory<IImageRequestBuilder> { AndroidImageRequestBuilder(androidContext()) }
//        factory<IStreamPlayer> { ExoplayerStreamPlayer(androidContext()) }
        factory<IStreamPlayer> { LibVlcStreamPlayer(androidContext()) }
        factory<IVideoPlayer> { AndroidVideoPlayer(androidContext()) }
    }
}