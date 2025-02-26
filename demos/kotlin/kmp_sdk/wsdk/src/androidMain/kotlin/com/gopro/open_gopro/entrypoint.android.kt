/* entrypoint.android.kt/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Tue Feb 18 18:41:30 UTC 2025 */

package com.gopro.open_gopro

import android.content.Context
import java.lang.ref.WeakReference

// https://stackoverflow.com/questions/76669135/using-context-in-kmm-shared-library-manually/77378735
actual class OgpSdkAppContext {

  private var value: WeakReference<Context?>? = null

  fun set(context: Context) {
    value = WeakReference(context)
  }

  fun get(): Context = value?.get() ?: throw Exception("Context has not been set.")
}
