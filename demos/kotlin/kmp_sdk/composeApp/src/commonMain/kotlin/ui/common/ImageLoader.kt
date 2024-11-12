package ui.common

import coil3.ImageLoader
import coil3.PlatformContext
import coil3.request.crossfade
import coil3.util.DebugLogger

// https://fastly.picsum.photos/id/686/200/300.jpg?hmac=KpugvfnM7VFRRbf_yihA6yObvfaWEJEEXeeFEqmVegQ

fun getAsyncImageLoader(context: PlatformContext): ImageLoader =
    ImageLoader.Builder(context).crossfade(true).logger(DebugLogger()).build()