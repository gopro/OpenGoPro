package fakes

import com.gopro.open_gopro.GoProId
import com.gopro.open_gopro.gopro.GoPro
import kotlinx.coroutines.CoroutineDispatcher

class FakeGoProProvider {
    fun getGoPro(serialId: String, dispatcher: CoroutineDispatcher): GoPro {
        return GoPro(GoProId(serialId))
    }
}