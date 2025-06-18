/* build.gradle.kts/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Tue Feb 18 18:41:27 UTC 2025 */

import org.jetbrains.kotlin.gradle.ExperimentalKotlinGradlePluginApi
import org.jetbrains.kotlin.gradle.dsl.JvmTarget

plugins {
  alias(libs.plugins.kotlinMultiplatform)
  alias(libs.plugins.androidApplication)
  alias(libs.plugins.jetbrainsCompose)
  alias(libs.plugins.compose.compiler)
  alias(libs.plugins.license)
  alias(libs.plugins.format)
}

kotlin {
  androidTarget {
    @OptIn(ExperimentalKotlinGradlePluginApi::class)
    compilerOptions { jvmTarget.set(JvmTarget.JVM_17) }
  }

  //    jvm("desktop")

  listOf(iosX64(), iosArm64(), iosSimulatorArm64()).forEach { iosTarget ->
    iosTarget.binaries.framework {
      baseName = "ComposeApp"
      isStatic = true
    }
  }

  sourceSets {
    //        val desktopMain by getting
    val androidUnitTest by getting

    commonMain.dependencies {
      implementation(projects.wsdk)

      // UI
      implementation(compose.runtime)
      implementation(compose.foundation)
      implementation(compose.material3)
      implementation(compose.ui)
      implementation(compose.components.resources)
      implementation(compose.components.uiToolingPreview)

      implementation(libs.androidx.lifecycle.viewmodel)
      implementation(libs.androidx.lifecycle.runtime.compose)

      // DI
      api(libs.koin.core)
      implementation(libs.koin.compose)
      implementation(libs.koin.compose.viewmodel)

      // Logging
      implementation(libs.kermit)

      // Navigation
      implementation(libs.navigation.compose)

      // Datastore
      implementation(libs.datastore)
      implementation(libs.datastore.preferences)

      // Coil
      implementation(libs.coil.compose.core)
      implementation(libs.coil.compose)
      implementation(libs.coil.mp)
      implementation(libs.coil.network.ktor)
    }
    //        desktopMain.dependencies {
    //            implementation(compose.desktop.currentOs)
    //            implementation(libs.kotlinx.coroutines.swing)
    //        }
    androidMain.dependencies {
      implementation(libs.androidx.activity.compose)
      // DI
      implementation(libs.koin.android)
      implementation(libs.koin.androidx.compose)
      // VLC
      implementation(libs.libvlc.all)
      // Exoplayer
      implementation(libs.exoplayer.base)
      implementation(libs.exoplayer.ui)
      implementation(libs.exoplayer.rtsp)
    }
    androidUnitTest.dependencies {
      implementation(libs.junit)
      implementation(libs.koin.test)
    }
  }
}

android {
  namespace = "gopro.open_gopro"
  compileSdk = libs.versions.android.compileSdk.get().toInt()

  sourceSets["main"].manifest.srcFile("src/androidMain/AndroidManifest.xml")
  sourceSets["main"].res.srcDirs("src/androidMain/res")
  sourceSets["main"].resources.srcDirs("src/commonMain/resources")

  defaultConfig {
    applicationId = "gopro.open_gopro.compose_app"
    minSdk = libs.versions.android.minSdk.get().toInt()
    targetSdk = libs.versions.android.targetSdk.get().toInt()
    versionCode = 1
    versionName = "1.0"
  }
  packaging { resources { excludes += "/META-INF/{AL2.0,LGPL2.1}" } }
  buildTypes { getByName("release") { isMinifyEnabled = false } }
  compileOptions {
    sourceCompatibility = JavaVersion.VERSION_17
    targetCompatibility = JavaVersion.VERSION_17
  }
  buildFeatures { compose = true }
  dependencies {
    debugImplementation(compose.uiTooling)
    debugImplementation(compose.preview)
    debugImplementation(libs.ui.tooling.preview)
  }
}

// compose.desktop {
//    application {
//        mainClass = "gopro.open_gopro.MainKt"
//
//        nativeDistributions {
//            targetFormats(TargetFormat.Dmg, TargetFormat.Msi, TargetFormat.Deb)
//            packageName = "gopro.open_gopro"
//            packageVersion = "1.0.0"
//        }
//    }
// }

licenseReport {
  // Generate reports
  generateCsvReport = true
  generateHtmlReport = true
  generateJsonReport = false
  generateTextReport = true

  // Copy reports - These options are ignored for Java projects
  copyCsvReportToAssets = false
  copyHtmlReportToAssets = false
  copyJsonReportToAssets = false
  copyTextReportToAssets = false
  useVariantSpecificAssetDirs = false

  // Ignore licenses for certain artifact patterns
  //    ignoredPatterns = []

  // Show versions in the report - default is false
  showVersions = true
}
