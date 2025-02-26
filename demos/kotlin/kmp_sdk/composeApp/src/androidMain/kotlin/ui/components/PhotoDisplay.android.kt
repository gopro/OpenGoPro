/* PhotoDisplay.android.kt/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Tue Feb 18 18:41:28 UTC 2025 */

package ui.components

import android.content.Context
import coil3.request.ImageRequest

class AndroidImageRequestBuilder(private val context: Context) : IImageRequestBuilder {
  override fun fromBinary(data: ByteArray): ImageRequest =
      ImageRequest.Builder(context).data(data).build()

  override fun fromNetwork(url: String): ImageRequest =
      ImageRequest.Builder(context).data(url).build()
}
