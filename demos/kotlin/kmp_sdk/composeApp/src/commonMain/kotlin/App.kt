import androidx.compose.foundation.layout.padding
import androidx.compose.material3.MaterialTheme
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import coil3.annotation.ExperimentalCoilApi
import coil3.compose.setSingletonImageLoaderFactory
import navigation.RootNavGraph
import org.jetbrains.compose.ui.tooling.preview.Preview
import org.koin.compose.KoinContext
import ui.common.getAsyncImageLoader

@OptIn(ExperimentalCoilApi::class)
@Composable
@Preview
fun App() {
    MaterialTheme {
        KoinContext {
            setSingletonImageLoaderFactory { getAsyncImageLoader(it) }
            RootNavGraph(
                modifier = Modifier.padding(20.dp),
            )
        }
    }
}