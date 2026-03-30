# 喵喵健身

[English](README.md) | 中文

## 介绍


## 相关资源下载地址


## 浏览器版本地址：


## 平台支持

| Android | IOS | Desktop/JVM | Web |
|:-------:|:---:|:-----------:|:---:|
|    √    |  √  |      √      |  √  |

## 截图


## 运行项目

### 安卓

在Android Studio打开直接运行即可

### 桌面

执行命令`./gradlew :composeApp:run`

打包 `./gradlew packageDistributionForCurrentOS`

### 网页

执行命令 `./gradlew :composeApp:jsBrowserDevelopmentRun` 或 `./gradlew :composeApp:wasmJsBrowserDevelopmentRun`

打包 `./gradlew jsBrowserDistribution` 或 `./gradlew wasmJsBrowserDistribution`

### 苹果

[示例](https://www.jetbrains.com/help/kotlin-multiplatform-dev/multiplatform-create-first-app.html#run-your-application-on-ios)

#### 提示

* 如果遇到
  `nw_proxy_resolver_create_parsed_array [C5.1 proxy pac] Evaluation error: NSURLErrorDomain: -1004`
  请关闭苹果手机代理或者模拟器所在电脑的代理

## 技术栈

- [Kotlin Multiplatform](https://kotlinlang.org/lp/multiplatform/)
- [Compose Multiplatform](https://www.jetbrains.com/lp/compose-multiplatform/)
- [Kotlin Coroutines](https://github.com/Kotlin/kotlinx.coroutines)
- [Koin](https://insert-koin.io/)
- [Voyager](https://github.com/adrielcafe/voyager)
- [Multiplatform Setting](https://github.com/russhwolf/multiplatform-settings)