import org.jetbrains.compose.desktop.application.dsl.TargetFormat
import org.jetbrains.kotlin.gradle.ExperimentalWasmDsl
import org.jetbrains.kotlin.gradle.dsl.JvmTarget

plugins {
    alias(libs.plugins.kotlinMultiplatform)
    alias(libs.plugins.androidApplication)
    alias(libs.plugins.composeMultiplatform)
    alias(libs.plugins.composeCompiler)
    alias(libs.plugins.composeHotReload)


    kotlin("plugin.serialization") version "1.9.0"
}

kotlin {
    androidTarget {
        compilerOptions {
            jvmTarget.set(JvmTarget.JVM_11)
        }
    }

    listOf(
        iosArm64(),
        iosSimulatorArm64()
    ).forEach { iosTarget ->
        iosTarget.binaries.framework {
            baseName = "ComposeApp"
            isStatic = true
        }
    }

    jvm()

    js {
        browser()
        binaries.executable()
    }

    @OptIn(ExperimentalWasmDsl::class)
    wasmJs {
        browser()
        binaries.executable()
    }

    sourceSets {
        androidMain.dependencies {
            implementation(compose.preview)
            implementation(libs.androidx.activity.compose)
        }
        commonMain.dependencies {
            implementation(compose.runtime)
            implementation(compose.foundation)
            implementation(compose.material3)
            implementation(compose.materialIconsExtended)
            implementation(compose.ui)
            implementation(compose.components.resources)
            implementation(compose.components.uiToolingPreview)
            implementation(libs.androidx.lifecycle.viewmodelCompose)
            implementation(libs.androidx.lifecycle.runtimeCompose)
            implementation("org.jetbrains.kotlinx:kotlinx-serialization-json:1.9.0")
            implementation("org.jetbrains.kotlinx:kotlinx-datetime:0.7.1")

            //https://github.com/adrielcafe/voyager
            implementation(libs.voyager.navigator)
            implementation(libs.voyager.tabNavigator)
            implementation(libs.voyager.transitions)
            implementation(libs.voyager.koin)

            //https://github.com/russhwolf/multiplatform-settings
            //https://developer.android.com/jetpack/androidx/releases/datastore
            //https://developer.android.com/kotlin/multiplatform/datastore
            //implementation(libs.multiplatform.settings.coroutines)
            // 当前datastore 还不支持 wasmJs 和 js
            //implementation(libs.androidx.datastore)
            //implementaton(libs.androidx.datastore.preferences)
            //implementation(libs.multiplatform.settings.datastore)
            implementation(libs.multiplatform.settings)

            //https://github.com/InsertKoinIO/koin
            implementation(project.dependencies.platform("io.insert-koin:koin-bom:4.1.1"))
            implementation("io.insert-koin:koin-core")
            implementation("io.insert-koin:koin-compose")


        }
        commonTest.dependencies {
            implementation(libs.kotlin.test)
        }
        jvmMain.dependencies {
            implementation(compose.desktop.currentOs)
            implementation(libs.kotlinx.coroutinesSwing)
        }
    }
}

android {
    namespace = "com.astercasc.squid.meowfitness"
    compileSdk = libs.versions.android.compileSdk.get().toInt()

    defaultConfig {
        applicationId = "com.astercasc.squid.meowfitness"
        minSdk = libs.versions.android.minSdk.get().toInt()
        targetSdk = libs.versions.android.targetSdk.get().toInt()
        versionCode = 1
        versionName = "1.0"
    }
    packaging {
        resources {
            excludes += "/META-INF/{AL2.0,LGPL2.1}"
        }
    }
    buildTypes {
        getByName("release") {
            isMinifyEnabled = false
        }
    }
    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_11
        targetCompatibility = JavaVersion.VERSION_11
    }
}

dependencies {
    debugImplementation(compose.uiTooling)
}

//  ./gradlew packageReleaseDistribution
compose.desktop {
    application {
        mainClass = "com.astercasc.squid.meowfitness.MainKt"

        nativeDistributions {
            targetFormats(TargetFormat.Dmg, TargetFormat.Msi, TargetFormat.Deb)

            includeAllModules = true

            packageName = "Meow Fitness"
            packageVersion = "1.0.0"
            description = "Meow Fitness"
            copyright = "astercasc.com. All rights reserved."
            vendor = "Aster Casc"

            windows {
                menuGroup = "GotRP"
                iconFile.set(project.file("src/jvmMain/resources/logo.ico"))
                upgradeUuid = "a33226c1-436e-44e4-9f4a-f9fbc6fc0dde"
            }

        }
    }
}
