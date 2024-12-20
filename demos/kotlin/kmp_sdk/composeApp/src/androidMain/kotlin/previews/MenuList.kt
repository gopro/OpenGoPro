package previews

import androidx.compose.foundation.layout.Box
import androidx.compose.runtime.Composable
import androidx.compose.ui.tooling.preview.Preview
import ui.components.MenuListItem

@Composable
@Preview
private fun PreviewMenuListItem() {
    Box {
        MenuListItem("item") { println("clicked") }
    }
}