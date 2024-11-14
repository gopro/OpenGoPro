package di

import org.koin.compose.viewmodel.dsl.viewModel
import org.koin.compose.viewmodel.dsl.viewModelOf
import org.koin.dsl.module
import presenter.AccessPointViewModel
import presenter.CameraChooserViewModel
import presenter.CameraViewModel
import presenter.CohnViewModel
import presenter.LivestreamViewModel
import presenter.MediaViewModel
import presenter.NetworkBrowserViewModel
import presenter.WebcamViewModel

val cameraScreenModule = module {
    viewModel { CameraViewModel(get(), get()) }
}

val cameraChooserScreenModule = module {
    viewModel { CameraChooserViewModel(get(), get()) }
}

val mediaScreenModule = module {
    viewModel { MediaViewModel(get(), get()) }
}

val webcamScreenModule = module {
    viewModel { WebcamViewModel(get(), get()) }
}

val livestreamScreenModule = module {
    viewModel { LivestreamViewModel(get(), get()) }
}

val accessPointModule = module {
    viewModelOf(::AccessPointViewModel)
}

val cohnModule = module {
    viewModel { CohnViewModel(get(), get()) }
}

val screenModules = listOf(
    cameraScreenModule,
    mediaScreenModule,
    cameraChooserScreenModule,
    webcamScreenModule,
    accessPointModule,
    livestreamScreenModule,
    cohnModule
)
