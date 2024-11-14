package fakes

import gopro.GoPro
import kotlinx.coroutines.CoroutineDispatcher

class FakeGoProProvider {
    fun getGoPro(serialId: String, dispatcher: CoroutineDispatcher): GoPro {
        return GoPro(serialId = serialId)
    }
}