package ui.common

sealed interface ConnectedScreen {
    val route: String
}

sealed class Screen(val route: String) {
    data object Home: Screen("Home")
    data object CameraChooser: Screen("Camera Chooser")
    data object Scratch: Screen("Scratch For Development")
    data object Camera: Screen("Connected Camera Control")
    data object Media: Screen("Media Access"), ConnectedScreen
    data object Webcam: Screen("Webcam Streaming"), ConnectedScreen
    data object AccessPoint: Screen("Access Point"), ConnectedScreen
    data object Livestream: Screen("Livestreaming"), ConnectedScreen
    data object Cohn: Screen("Cohn"), ConnectedScreen
}