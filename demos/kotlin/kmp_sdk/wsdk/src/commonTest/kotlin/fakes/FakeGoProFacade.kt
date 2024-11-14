package fakes

import entity.connector.GoProId
import gopro.GoPro
import kotlinx.coroutines.CoroutineDispatcher

class FakeGoProProvider {
    fun getGoPro(serialId: String, dispatcher: CoroutineDispatcher): GoPro {
        return GoPro(GoProId(serialId))
    }
}