/* RootNavGraph.kt/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Tue Feb 18 18:41:27 UTC 2025 */

package navigation

import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.navigation.NavHostController
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.rememberNavController
import org.koin.compose.koinInject
import org.koin.compose.viewmodel.koinViewModel
import org.koin.core.annotation.KoinExperimentalAPI
import presenter.AccessPointViewModel
import presenter.CameraChooserViewModel
import presenter.CameraViewModel
import presenter.CohnViewModel
import presenter.LivestreamViewModel
import presenter.MediaViewModel
import presenter.SettingsViewModel
import presenter.WebcamViewModel
import ui.common.Screen
import ui.screens.CameraScreen
import ui.screens.HomeScreen
import ui.screens.connected.AccessPointScreen
import ui.screens.connected.CohnScreen
import ui.screens.connected.LivestreamScreen
import ui.screens.connected.MediaScreen
import ui.screens.connected.SettingsScreen
import ui.screens.connected.WebcamScreen

@OptIn(KoinExperimentalAPI::class)
@Composable
fun RootNavGraph(
    navController: NavHostController = rememberNavController(),
    modifier: Modifier = Modifier,
) {
  NavHost(
      navController = navController,
      startDestination = Screen.Home.route,
  ) {
    // Home (Camera Chooser)
    composable(route = Screen.Home.route) {
      HomeScreen(
          navController,
          koinInject<CameraChooserViewModel>(),
          modifier,
      )
    }
    // Connected Camera
    composable(route = Screen.Camera.route) {
      CameraScreen(
          navController,
          listOf(
              Screen.Settings,
              Screen.Media,
              Screen.Webcam,
              Screen.AccessPoint,
              Screen.Livestream,
              Screen.Cohn),
          koinViewModel<CameraViewModel>(),
          modifier,
      )
    }
    // Connected Camera sub-routes
    composable(route = Screen.Settings.route) {
      SettingsScreen(
          navController,
          koinInject<SettingsViewModel>(),
          modifier,
      )
    }
    composable(route = Screen.Media.route) {
      MediaScreen(
          navController,
          koinInject<MediaViewModel>(),
          modifier,
      )
    }
    composable(route = Screen.Webcam.route) {
      WebcamScreen(
          navController,
          koinInject<WebcamViewModel>(),
          modifier,
      )
    }
    composable(route = Screen.Livestream.route) {
      LivestreamScreen(
          navController,
          koinInject<LivestreamViewModel>(),
          modifier,
      )
    }
    composable(route = Screen.AccessPoint.route) {
      AccessPointScreen(
          navController,
          koinInject<AccessPointViewModel>(),
          modifier,
      )
    }
    composable(route = Screen.Cohn.route) {
      CohnScreen(
          navController,
          koinInject<CohnViewModel>(),
          modifier,
      )
    }
  }
}
