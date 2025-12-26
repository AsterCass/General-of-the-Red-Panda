# The Book of Grudges

English | [中文](README_zh.md)

## Introduction

### Browser Version URLs:

* https://www.astercasc.com/apps/grudgesWasmJs/ (Note: the first load may take a little while as the core package and fonts are being loaded.)
* Backup URL (use this if some older browsers cannot access the address above): https://www.astercasc.com/apps/grudgesJs/

## Platforms Support

| Android | IOS | Desktop/JVM | Web |
|:-------:|:---:|:-----------:|:---:|
|    √    |  √  |      √      |  √  |


## Screenshots

todo

## Run Project

### Android

Open project in Android Studio and run

### Desktop

Run command `./gradlew :composeApp:run`

Release `./gradlew packageDistributionForCurrentOS`

### Web

Run command `./gradlew :composeApp:jsBrowserDevelopmentRun` or `./gradlew :composeApp:wasmJsBrowserDevelopmentRun`

Release `./gradlew jsBrowserDistribution` or `./gradlew wasmJsBrowserDistribution`

### IOS

[Run your application on iOS](https://www.jetbrains.com/help/kotlin-multiplatform-dev/multiplatform-create-first-app.html#run-your-application-on-ios)

#### TIPS 

* If you encounter `nw_proxy_resolver_create_parsed_array [C5.1 proxy pac] Evaluation error: NSURLErrorDomain: -1004`, please disable the proxy on your iPhone or the computer where the simulator is running

## Tech Stack

- [Kotlin Multiplatform](https://kotlinlang.org/lp/multiplatform/)
- [Compose Multiplatform](https://www.jetbrains.com/lp/compose-multiplatform/)
- [Kotlin Coroutines](https://github.com/Kotlin/kotlinx.coroutines)
- [Koin](https://insert-koin.io/)
- [Voyager](https://github.com/adrielcafe/voyager)
- [Multiplatform Setting](https://github.com/russhwolf/multiplatform-settings)