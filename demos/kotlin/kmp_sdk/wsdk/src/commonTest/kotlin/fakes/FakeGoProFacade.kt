package fakes

import gopro.GoProFacade
import kotlinx.coroutines.CoroutineDispatcher

class FakeGoProFacadeProvider {
    fun getGoProFacade(serialId: String, dispatcher: CoroutineDispatcher): GoProFacade {
        return GoProFacade(serialId = serialId)
    }
}