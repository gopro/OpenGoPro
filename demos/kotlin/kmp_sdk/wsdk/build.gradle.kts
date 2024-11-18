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

// TODO how to to move to libs.versions.toml
// https://mvnrepository.com/artifact/com.google.protobuf/protoc
val protocVersion by extra("4.26.1")
// https://github.com/streem/pbandk/releases/tag/v0.16.0
val pbandkVersion by extra("0.16.0")

//dependencies {
//    implementation("pro.streem.pbandk:pbandk-runtime:$pbandkVersion")
//}

//protobuf {
//    generatedFilesBaseDir = "src"
//    protoc {
//        artifact = "com.google.protobuf:protoc:$protocVersion"
//    }
//    plugins {
//        id("pbandk") {
//            artifact = "pro.streem.pbandk:protoc-gen-pbandk-jvm:$pbandkVersion:jvm8@jar"
//        }
//    }
//    generateProtoTasks {
//        all().configureEach {
//            builtins {
//                java { }
//            }
//            plugins {
//                id("pbandk") {
//                    option("kotlin_package=ogp.pb")
//                }
//            }
//        }
//    }
//}

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

        // https://kotlinlang.org/docs/multiplatform-android-layout.html#move-source-files
        val commonTest by getting

        val androidInstrumentedTest by getting

        // https://slack-chats.kotlinlang.org/t/16139070/i-havee-to-admin-it-s-very-frustrating-that-there-is-no-stan
        // THis is not used currently
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
        appleMain.dependencies {
            api(libs.ktor.client.darwin)
        }
        desktopMain.dependencies {
            api(libs.ktor.client.okhttp)
        }
    }
}

android {
    namespace = "gopro.open_gopro.wsdk"
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


tasks.withType<DokkaTaskPartial>().configureEach {
    dokkaSourceSets {
        configureEach {
            includes.from("ModuleDocumentation.md")
            suppressInheritedMembers = true
        }
    }
}