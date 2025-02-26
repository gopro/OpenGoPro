/* PhotoDisplay.kt/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Tue Feb 18 18:41:27 UTC 2025 */

package ui.components

import androidx.compose.foundation.layout.Box
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import coil3.compose.AsyncImage
import coil3.request.ImageRequest
import org.koin.core.component.KoinComponent
import org.koin.core.component.inject

interface IImageRequestBuilder {
  fun fromBinary(data: ByteArray): ImageRequest

  fun fromNetwork(url: String): ImageRequest
}

object PhotoDisplay : KoinComponent {

  private val imageRequestBuilder: IImageRequestBuilder by inject()

  @Composable
  private fun PhotoBase(modifier: Modifier, imageRequest: ImageRequest) {
    // https://proandroiddev.com/coil-for-compose-multiplatform-5745ea76356f
    Box {
      AsyncImage(
          modifier = modifier,
          model = imageRequest,
          contentDescription = "TODO",
          onError = {
            // update state
          },
          onLoading = {
            // update state
          },
          onSuccess = {
            // update state
          })
    }
  }

  @Composable
  fun FromBinary(modifier: Modifier, data: ByteArray) =
      PhotoBase(modifier, imageRequestBuilder.fromBinary(data))

  @Composable
  fun FromNetwork(modifier: Modifier, url: String) =
      PhotoBase(modifier, imageRequestBuilder.fromNetwork(url))
}
