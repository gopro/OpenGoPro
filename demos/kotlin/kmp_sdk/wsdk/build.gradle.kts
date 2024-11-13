import org.jetbrains.dokka.gradle.DokkaTaskPartial
import org.jetbrains.kotlin.gradle.ExperimentalKotlinGradlePluginApi
import org.jetbrains.kotlin.gradle.dsl.JvmTarget

plugins {
    alias(libs.plugins.kotlinMultiplatform)
    alias(libs.plugins.androidLibrary)
    alias(libs.plugins.ksp)
    alias(libs.plugins.room)
    alias(libs.plugins.serialization)
    alias(libs.plugins.dokka)
}

val pbandkVersion by extra("0.16.0")

kotlin {
    androidTarget {
        @OptIn(ExperimentalKotlinGradlePluginApi::class)
        compilerOptions {
            jvmTarget.set(JvmTarget.JVM_11)
        }
    }

    jvm("desktop")

    iosX64()
    iosArm64()
    iosSimulatorArm64()

    sourceSets {
        val desktopMain by getting

        commonMain.dependencies {
            implementation(projects.domain)

            // DI
            api(libs.koin.core)
            implementation(libs.koin.compose) // TODO do we need this
            implementation(libs.koin.compose.viewmodel) // TODO do we need this?

            // Logging
            implementation(libs.kermit)

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
            implementation("pro.streem.pbandk:pbandk-runtime:$pbandkVersion")

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
        iosMain.dependencies {
            api(libs.ktor.client.darwin)
        }
        desktopMain.dependencies {
            api(libs.ktor.client.okhttp)
        }
    }
}

android {
    namespace = "gopro.open_gopro.network"
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

    add("kspAndroid", libs.androidx.room.compiler)
    add("kspIosSimulatorArm64", libs.androidx.room.compiler)
    add("kspIosX64", libs.androidx.room.compiler)
    add("kspIosArm64", libs.androidx.room.compiler)
}


tasks.withType<DokkaTaskPartial>().configureEach {
    dokkaSourceSets {
        configureEach {
            includes.from("ModuleDocumentation.md")
        }
    }
}