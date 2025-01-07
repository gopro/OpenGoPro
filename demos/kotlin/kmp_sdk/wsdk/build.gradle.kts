import com.vanniktech.maven.publish.SonatypeHost
import org.jetbrains.dokka.base.DokkaBase
import org.jetbrains.dokka.base.DokkaBaseConfiguration
import org.jetbrains.kotlin.gradle.ExperimentalKotlinGradlePluginApi
import org.jetbrains.kotlin.gradle.dsl.JvmTarget
import com.jaredsburrows.license.LicensePlugin

plugins {
    alias(libs.plugins.kotlinMultiplatform)
    alias(libs.plugins.androidLibrary)
    alias(libs.plugins.ksp)
    alias(libs.plugins.room)
    alias(libs.plugins.serialization)
    alias(libs.plugins.dokka)
    alias(libs.plugins.license)
    alias(libs.plugins.publish)
}

kotlin {
    androidTarget {
        @OptIn(ExperimentalKotlinGradlePluginApi::class)
        compilerOptions {
            jvmTarget.set(JvmTarget.JVM_11)
        }
        publishLibraryVariants("release")
    }

    listOf(
        iosX64(),
        iosArm64(),
        iosSimulatorArm64()
    ).forEach {
        it.binaries.framework {
            baseName = "openGoPro"
            isStatic = true
        }
    }

    sourceSets {
        // https://kotlinlang.org/docs/multiplatform-android-layout.html#move-source-files
        val commonTest by getting
        val androidInstrumentedTest by getting
        val androidUnitTest by getting

        commonMain.dependencies {
            // DI
            api(libs.koin.core)
            implementation(libs.koin.compose)
            implementation(libs.koin.compose.viewmodel)

            // Logging
            implementation(libs.kermit)

            // Dates
            api(libs.kotlinx.datetime)

            // Concurrency / Streams
            implementation(libs.kotlinx.coroutines)

            // Ktor - Http Stack
            implementation(libs.ktor.client.core)
            implementation(libs.ktor.client.logging)
            implementation(libs.ktor.client.negotiation)
            implementation(libs.ktor.client.auth)
            implementation(libs.ktor.json)

            // JSON serialization
            implementation(libs.kotlinx.serialization.json)

            // Kable
            implementation(libs.kable.core)
            implementation(libs.kable.exceptions)
            implementation(libs.khronicle)

            // Uuid
            implementation(libs.uuid)

            // Protobuf run-time
            implementation(libs.pbandk.runtime)

            // Version data structure
            implementation(libs.version)

            // Datetime
            implementation(libs.kotlinx.datetime)

            // Room
            implementation(libs.androidx.room.runtime)
            implementation(libs.sqlite.bundled)
        }
        commonTest.dependencies {
            implementation(libs.kotlin.test)
            implementation(libs.kotlinx.coroutines.test)
            implementation(libs.ktor.mock)
            implementation(libs.koin.test)
        }
        androidMain.dependencies {
            // DI
            implementation(libs.koin.android)
            implementation(libs.koin.androidx.compose)
            api(libs.ktor.client.okhttp)
        }
        appleMain.dependencies {
            api(libs.ktor.client.darwin)
        }
    }
}

android {
    namespace = "com.gopro.open_gopro"
    compileSdk = libs.versions.android.compileSdk.get().toInt()
    defaultConfig {
        minSdk = libs.versions.android.minSdk.get().toInt()
        testInstrumentationRunner = "androidx.test.runner.AndroidJUnitRunner"
    }
    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_11
        targetCompatibility = JavaVersion.VERSION_11
    }
}

room {
    schemaDirectory("$projectDir/schemas")
}

dependencies {
    testImplementation(libs.junit)
    // https://touchlab.co/understanding-and-configuring-your-kmm-test-suite
    androidTestImplementation(libs.kotlin.test)
    androidTestImplementation(libs.kotlinx.coroutines.test)
    androidTestImplementation(libs.core.ktx)
    androidTestImplementation(libs.androidx.test.junit)
    androidTestImplementation(libs.androidx.junit.ktx)
    androidTestImplementation(libs.androidx.espresso.core)
    androidTestImplementation(libs.mockito.android)
    androidTestImplementation(libs.koin.test.junit4)

    add("kspAndroid", libs.androidx.room.compiler)
    add("kspIosSimulatorArm64", libs.androidx.room.compiler)
    add("kspIosX64", libs.androidx.room.compiler)
    add("kspIosArm64", libs.androidx.room.compiler)
}

buildscript {
    dependencies {
        classpath(libs.dokka.base)
    }
}

tasks.dokkaHtml {
    pluginConfiguration<DokkaBase, DokkaBaseConfiguration> {
        customAssets = listOf(
            file("../docs/assets/logo-icon.svg"),
//            file("../docs/assets/my-style.css")
        )
    }
    dokkaSourceSets {
        configureEach {
            moduleName.set("Open GoPro SDK")
            includes.from("../docs/sdk_documentation.md")

//            suppressInheritedMembers = true
//            documentedVisibilities.set(
//                setOf(
//                    DokkaConfiguration.Visibility.PUBLIC,
//                    DokkaConfiguration.Visibility.PROTECTED
//                )
//            )
        }
    }
}

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

tasks.register<Copy>("copyLicenseReport") {
    val reportDir = layout.buildDirectory.dir("reports/licenses")
    group = "reporting"
    description = "Copy Generated License Reports to top level of repo"
    from(reportDir)
    into(rootDir)
}

//tasks.getByName("licenseReleaseReport").finalizedBy

mavenPublishing {
    // Define coordinates for the published artifact
    coordinates(
        groupId = "io.github.tcamise-gpsw", // TODO move to GoPro once possible
        artifactId = "open-gopro",
        version = "0.1.0"
    )

    // Configure POM metadata for the published artifact
    pom {
        name.set("Open GoPro KMP SDK")
        description.set("n interface for the user to exercise the Open GoPro Bluetooth Low Energy (BLE) and Wi-Fi / USB HTTP API's")
        inceptionYear.set("2024")
        url.set("tcamise-gpsw")

        licenses {
            license {
                name.set("MIT")
                url.set("https://opensource.org/licenses/MIT")
            }
        }

        // Specify developers information
        developers {
            developer {
                id.set("tcamise-gpsw")
                name.set("Tim Camise")
                email.set("tcamise@gopro.com")
            }
        }

        // Specify SCM information
        scm {
            url.set("https://github.com/gopro/OpenGoPro")
        }
    }

    // Configure publishing to Maven Central
    publishToMavenCentral(SonatypeHost.CENTRAL_PORTAL)

    // Enable GPG signing for all publications
    signAllPublications()
}