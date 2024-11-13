import com.google.protobuf.gradle.id
import org.jetbrains.dokka.gradle.DokkaTaskPartial
import org.jetbrains.kotlin.gradle.ExperimentalKotlinGradlePluginApi
import org.jetbrains.kotlin.gradle.dsl.JvmTarget

plugins {
    alias(libs.plugins.kotlinMultiplatform)
    alias(libs.plugins.androidLibrary)
    alias(libs.plugins.serialization)
    alias(libs.plugins.dokka)
//    id("com.google.protobuf") version "0.9.4"
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
    macosArm64()

    sourceSets {
        val desktopMain by getting

        commonMain.dependencies {
            // Logging
            implementation(libs.kermit)

            // Dates
            api(libs.kotlinx.datetime)

            implementation(libs.kotlinx.coroutines)

            // TODO use generic HTTP Request / Response interfaces to avoid explicit Ktor dependency?
            implementation(libs.ktor.client.core)
            implementation(libs.ktor.client.negotiation)
            implementation(libs.ktor.json)

            // JSON serialization
            implementation(libs.kotlinx.serialization.json)

            // UUID
            implementation(libs.uuid)

            // Protobuf run-time
            implementation("pro.streem.pbandk:pbandk-runtime:$pbandkVersion")

            // Room
            implementation(libs.androidx.room.runtime)
        }
        commonTest.dependencies {
            implementation(libs.kotlin.test)
        }
        androidMain.dependencies {
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
    namespace = "gopro.open_gopro.domain"
    compileSdk = libs.versions.android.compileSdk.get().toInt()
    defaultConfig {
        minSdk = libs.versions.android.minSdk.get().toInt()
    }
    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_11
        targetCompatibility = JavaVersion.VERSION_11
    }
}

tasks.withType<DokkaTaskPartial>().configureEach {
    dokkaSourceSets {
        configureEach {
            includes.from("ModuleDocumentation.md")
        }
    }
}