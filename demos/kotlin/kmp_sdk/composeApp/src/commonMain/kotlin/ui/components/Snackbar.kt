package ui.components

import androidx.compose.material3.SnackbarHostState
import androidx.compose.runtime.Composable
import androidx.compose.runtime.CompositionLocalProvider
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.staticCompositionLocalOf
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.launch

interface SnackbarController {
    val snackbarHostState: SnackbarHostState
    fun showMessage(message: String)
}

fun SnackbarController(
    snackbarHostState: SnackbarHostState, coroutineScope: CoroutineScope
): SnackbarController = SnackbarControllerImpl(
    snackbarHostState = snackbarHostState, coroutineScope = coroutineScope
)

@Composable
fun ProvideSnackbarController(
    snackbarHostState: SnackbarHostState,
    coroutineScope: CoroutineScope,
    content: @Composable () -> Unit
) {
    CompositionLocalProvider(
        LocalSnackbarController provides SnackbarController(snackbarHostState, coroutineScope),
        content = content
    )
}

@Composable
fun SnackbarMessageHandler(
    snackbarMessage: String?,
    onDismissSnackbar: () -> Unit = {},
    snackbarController: SnackbarController = LocalSnackbarController.current
) {
    if (snackbarMessage == null) return

    LaunchedEffect(snackbarMessage, onDismissSnackbar) {
        snackbarController.showMessage(message = snackbarMessage)
        onDismissSnackbar()
    }
}

private class SnackbarControllerImpl(
    override val snackbarHostState: SnackbarHostState,
    private val coroutineScope: CoroutineScope
) : SnackbarController {
    override fun showMessage(message: String) {
        coroutineScope.launch {
            snackbarHostState.showSnackbar(message)
        }
    }
}

val LocalSnackbarController = staticCompositionLocalOf<SnackbarController> {
    error("No SnackbarController provided.")
}