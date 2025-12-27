# The Book of Grudges

English | [中文](README_zh.md)

## Introduction

It doesn’t just help us record every little detail from daily life and work, ensuring that nothing ever goes wrong or gets overlooked when it’s time to serve a client—it also supports custom tags and service targets, making retrieval faster and more efficient.

We’ve also added a Grudge Level option, so keeping grudges is no longer monotonous and the intensity of our “service” is always under control.

Even more user-friendly, when searching records you can choose “1 by 1”, making it easy to operate with one hand on your phone and the other hand “serving,” while strictly following the core principle:
“Not a single thing that’s yours is missed; not a single thing that’s not yours is forced in.”

When client feedback fails to meet expectations, you can use “Remember +1” to log it, clearly distinguishing how fresh each old grudge still is.

And when you’re extremely satisfied with a client’s feedback, simply mark it as “Settled” to clear that service item.

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