/* Routes.kt/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Tue Feb 18 18:41:27 UTC 2025 */

package ui.common

sealed interface ConnectedScreen {
  val route: String
}

sealed class Screen(val route: String) {
  data object Home : Screen("Home")

  data object CameraChooser : Screen("Camera Chooser")

  data object Camera : Screen("Connected Camera Control")

  data object Media : Screen("Media Access"), ConnectedScreen

  data object Webcam : Screen("Webcam Streaming"), ConnectedScreen

  data object AccessPoint : Screen("Access Point"), ConnectedScreen

  data object Livestream : Screen("Livestreaming"), ConnectedScreen

  data object Cohn : Screen("Camera on the Home Network"), ConnectedScreen

  data object Settings : Screen("Settings"), ConnectedScreen
}
