/* MainScreen.kt/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Mon Mar  6 17:45:14 UTC 2023 */

package com.example.open_gopro_tutorial.ui

import androidx.compose.foundation.Image
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.material.*
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.rounded.BluetoothConnected
import androidx.compose.material.icons.rounded.BluetoothDisabled
import androidx.compose.material.icons.rounded.Wifi
import androidx.compose.material.icons.rounded.WifiOff
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.tooling.preview.datasource.LoremIpsum
import androidx.compose.ui.unit.dp
import coil.compose.rememberAsyncImagePainter
import com.example.open_gopro_tutorial.*
import com.example.open_gopro_tutorial.network.Bluetooth
import com.example.open_gopro_tutorial.tutorials.Tutorial
import com.example.open_gopro_tutorial.tutorials.Tutorials
import com.example.open_gopro_tutorial.ui.theme.OpenGoProTutorialTheme
import com.google.accompanist.permissions.ExperimentalPermissionsApi
import com.google.accompanist.permissions.rememberMultiplePermissionsState
import java.io.File

@OptIn(ExperimentalPermissionsApi::class)
@Composable
fun MainScreen(mainViewModel: MainViewModel) {
    val uiState by mainViewModel.uiState.collectAsState()

    val permissionsState = rememberMultiplePermissionsState(Bluetooth.permissionsNeeded)
    if (!permissionsState.allPermissionsGranted) {
        Column(modifier=Modifier.padding(15.dp)) {
            Text("Bluetooth is needed for this app. Please grant the permission.")
            Button(onClick = {
                permissionsState.launchMultiplePermissionRequest()
            }) {
                Text("Request permission")
            }
        }
    } else {
        // All permissions are granted. Compose per-state screen.
        MainScreen(
            uiState = uiState, onTutorialSelect = mainViewModel::onTutorialSelect
        )
    }
}

@Composable
fun MainScreen(
    uiState: MainUiState, onTutorialSelect: (Tutorial?) -> Unit
) {
    Column(
        horizontalAlignment = Alignment.CenterHorizontally,
        modifier = Modifier.padding(6.dp).fillMaxWidth()
    ) {
        when (uiState) {
            is MainUiState.Idle -> TutorialSelectionScreen(
                uiState.bleConnected,
                uiState.wifiConnected,
                uiState.tutorials,
                onTutorialSelect
            )
            is MainUiState.TutorialSelected -> TutorialInProgressScreen(
                uiState.bleConnected,
                uiState.wifiConnected,
                uiState.activeTutorial,
                uiState.logEntries,
                uiState.inProgress,
                uiState.media,
                onTutorialSelect
            )
        }
    }
}

@Composable
fun TutorialSelectionScreen(
    ble: Boolean, wifi: Boolean, tutorials: List<Tutorial>, onTutorialSelect: (Tutorial?) -> Unit
) {
    Column(horizontalAlignment = Alignment.CenterHorizontally) {
        Header(ble, wifi, "Open GoPro Tutorials")
        // Filter out tutorials that are not currently available
        TutorialDropDown(tutorials, onTutorialSelect)
    }

}

@Composable
fun TutorialInProgressScreen(
    ble: Boolean,
    wifi: Boolean,
    activeTutorial: Tutorial,
    logEntries: List<String>,
    inProgress: Boolean,
    media: File?,
    onTutorialSelect: (Tutorial?) -> Unit,
) {
    Column(horizontalAlignment = Alignment.CenterHorizontally) {
        Header(ble, wifi, activeTutorial.toString())
        Row {
            if (inProgress) CircularProgressIndicator()
            Spacer(modifier = Modifier.width(40.dp))
            Button(onClick = { onTutorialSelect(null) }) {
                Text("Exit Tutorial")
            }
        }
        Divider(modifier = Modifier.height(5.dp))
        media?.let {
            Text("File received from camera:")
            Image(
                painter = rememberAsyncImagePainter(model = it),
                contentDescription = "File from camera"
            )
        } ?: run {
            ScrollableLog(logEntries)
        }
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun TutorialDropDown(tutorials: List<Tutorial>, onTutorialSelect: (Tutorial) -> Unit) {
    var expanded by remember { mutableStateOf(false) }
    var selection by remember { mutableStateOf(tutorials.first()) }
    Column(horizontalAlignment = Alignment.CenterHorizontally) {
        ExposedDropdownMenuBox(expanded = expanded, onExpandedChange = { expanded = !expanded }) {
            TextField(value = selection.toString(),
                modifier = Modifier.menuAnchor(),
                onValueChange = {},
                readOnly = true,
                trailingIcon = { ExposedDropdownMenuDefaults.TrailingIcon(expanded = expanded) })
            ExposedDropdownMenu(expanded = expanded, onDismissRequest = { expanded = false }) {
                tutorials.forEach { tutorial ->
                    DropdownMenuItem(onClick = {
                        expanded = false
                        selection = tutorial
                    }, text = { Text(text = tutorial.toString()) })
                }
            }
        }
        Button(onClick = { onTutorialSelect(selection) }) {
            Text("Perform")
        }
    }
}

@Composable
fun Header(ble: Boolean, wifi: Boolean, tutorial: String) {
    Column {
        Row {
            Text("BLE: ")
            Spacer(modifier = Modifier.width(3.dp))
            Icon(
                if (ble) Icons.Rounded.BluetoothConnected else Icons.Rounded.BluetoothDisabled,
                "Bluetooth Status",
                tint = Color.Blue
            )
            Spacer(modifier = Modifier.width(10.dp))
            Text("Wifi: ")
            Spacer(modifier = Modifier.width(3.dp))
            Icon(
                if (wifi) Icons.Rounded.Wifi else Icons.Rounded.WifiOff,
                "Wifi Status",
                tint = Color.Green
            )
        }
        Text(tutorial)
    }
}

@Composable
fun ScrollableLog(entries: List<String>) {
    LazyColumn {
        entries.forEach { entry ->
            item {
                Text(entry, style = MaterialTheme.typography.bodySmall)
                Divider(modifier = Modifier.height(2.dp))
            }
        }
    }
}

/**
 * Previews
 */

@Preview
@Composable
fun PreviewTutorialSelectionScreen() {
    OpenGoProTutorialTheme {
        Surface(modifier = Modifier.fillMaxWidth()) {
            TutorialSelectionScreen(ble = false, wifi = true, tutorials = Tutorials) {}
        }
    }
}

@Preview
@Composable
fun PreviewTutorialSelected() {
    OpenGoProTutorialTheme {
        Surface(modifier = Modifier.fillMaxWidth()) {
            TutorialInProgressScreen(
                ble = false,
                wifi = true,
                activeTutorial = Tutorials.first(),
                inProgress = true,
                media = null,
                logEntries = LoremIpsum().values.joinToString().lines()
            ) {}
        }
    }
}