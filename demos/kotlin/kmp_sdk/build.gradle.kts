import org.jetbrains.dokka.DokkaConfiguration
import org.jetbrains.dokka.gradle.DokkaTask
import org.jetbrains.dokka.gradle.DokkaTaskPartial
import java.net.URL

plugins {
    // this is necessary to avoid the plugins to be loaded multiple times
    // in each subproject's classloader
    alias(libs.plugins.androidApplication) apply false
    alias(libs.plugins.androidLibrary) apply false
    alias(libs.plugins.jetbrainsCompose) apply false
    alias(libs.plugins.compose.compiler) apply false
    alias(libs.plugins.kotlinMultiplatform) apply false
    alias(libs.plugins.serialization) apply false
    alias(libs.plugins.protobuf) apply false
    alias(libs.plugins.ksp) apply false
    alias(libs.plugins.room) apply false

    alias(libs.plugins.license) apply false
    alias(libs.plugins.dokka)

}

tasks.withType<DokkaTaskPartial>().configureEach {
    dokkaSourceSets.configureEach {
        documentedVisibilities.set(
            setOf(
                DokkaConfiguration.Visibility.PUBLIC,
                DokkaConfiguration.Visibility.PROTECTED
            )
        )

        // TODO what is this?
        // Read docs for more details: https://kotlinlang.org/docs/dokka-gradle.html#source-link-configuration
        sourceLink {
            val exampleDir =
                "https://github.com/Kotlin/dokka/tree/master/examples/gradle/dokka-multimodule-example"

            localDirectory.set(rootProject.projectDir)
            remoteUrl.set(URL(exampleDir))
            remoteLineSuffix.set("#L")
        }
    }
}

// Configures only the parent MultiModule task,
// this will not affect subprojects
tasks.dokkaHtmlMultiModule {
    moduleName.set("Open GoPro")
    includes.from("TopLevelDocumentation.md")
}