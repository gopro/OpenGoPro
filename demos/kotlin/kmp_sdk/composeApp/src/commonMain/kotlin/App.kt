/* App.kt/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Tue Feb 18 18:41:27 UTC 2025 */

import androidx.compose.foundation.layout.padding
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.SnackbarHostState
import androidx.compose.runtime.Composable
import androidx.compose.runtime.remember
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import coil3.annotation.ExperimentalCoilApi
import coil3.compose.setSingletonImageLoaderFactory
import navigation.RootNavGraph
import org.jetbrains.compose.ui.tooling.preview.Preview
import org.koin.compose.KoinContext
import ui.common.getAsyncImageLoader
import ui.components.ProvideSnackbarController

@OptIn(ExperimentalCoilApi::class)
@Composable
@Preview
fun App() {
  MaterialTheme {
    KoinContext {
      setSingletonImageLoaderFactory { getAsyncImageLoader(it) }

      val snackbarHostState = remember { SnackbarHostState() }
      val coroutineScope = rememberCoroutineScope()
      ProvideSnackbarController(snackbarHostState, coroutineScope) {
        RootNavGraph(
            modifier = Modifier.padding(20.dp),
        )
      }
    }
  }
}
