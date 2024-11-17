package ui.components

import android.content.Context
import coil3.request.ImageRequest

class AndroidImageRequestBuilder(private val context: Context) : IImageRequestBuilder {
    override fun fromBinary(data: ByteArray): ImageRequest =
        ImageRequest.Builder(context).data(data).build()

    override fun fromNetwork(url: String): ImageRequest =
        ImageRequest.Builder(context).data(url).build()
}