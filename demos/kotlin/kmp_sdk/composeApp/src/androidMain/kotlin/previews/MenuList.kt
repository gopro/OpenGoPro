/* MenuList.kt/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Tue Feb 18 18:41:27 UTC 2025 */

package previews

import androidx.compose.foundation.layout.Box
import androidx.compose.runtime.Composable
import androidx.compose.ui.tooling.preview.Preview
import ui.components.MenuListItem

@Composable
@Preview
private fun PreviewMenuListItem() {
  Box { MenuListItem("item") { println("clicked") } }
}
