/* SimplifiedActivity.kt/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Tue Feb 18 18:41:30 UTC 2025 */

package gopro.open_gopro

import android.Manifest.permission.ACCESS_COARSE_LOCATION
import android.Manifest.permission.ACCESS_FINE_LOCATION
import android.Manifest.permission.ACCESS_WIFI_STATE
import android.Manifest.permission.BLUETOOTH_CONNECT
import android.Manifest.permission.BLUETOOTH_SCAN
import android.Manifest.permission.CHANGE_WIFI_STATE
import android.content.pm.PackageManager
import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.result.contract.ActivityResultContracts
import androidx.core.content.ContextCompat
import app
import com.gopro.open_gopro.OgpSdkAppContext

class SimplifiedActivity : ComponentActivity() {

  private val requestPermissionLauncher =
      registerForActivityResult(ActivityResultContracts.RequestMultiplePermissions()) { isGranted ->
        require(isGranted.all { it.value }) { "Failed to enable all required permissions." }
        startApp()
      }

  override fun onCreate(savedInstanceState: Bundle?) {
    super.onCreate(savedInstanceState)

    val permissions =
        arrayOf(
            BLUETOOTH_SCAN,
            BLUETOOTH_CONNECT,
            ACCESS_FINE_LOCATION,
            ACCESS_COARSE_LOCATION,
            ACCESS_WIFI_STATE,
            CHANGE_WIFI_STATE)

    if (permissions.all { isPermissionGranted(it) }) {
      startApp()
    }

    requestPermissionLauncher.launch(permissions)
  }

  private fun startApp() {
    val appContext = OgpSdkAppContext().apply { set(applicationContext) }
    app(appContext)
  }

  private fun isPermissionGranted(permission: String) =
      ContextCompat.checkSelfPermission(this, permission) == PackageManager.PERMISSION_GRANTED
}
