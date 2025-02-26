/* FakeGoProFacade.kt/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Tue Feb 18 18:41:30 UTC 2025 */

package fakes

import com.gopro.open_gopro.GoProId
import com.gopro.open_gopro.gopro.GoPro
import kotlinx.coroutines.CoroutineDispatcher

class FakeGoProProvider {
  fun getGoPro(serialId: String, dispatcher: CoroutineDispatcher): GoPro {
    return GoPro(GoProId(serialId))
  }
}
