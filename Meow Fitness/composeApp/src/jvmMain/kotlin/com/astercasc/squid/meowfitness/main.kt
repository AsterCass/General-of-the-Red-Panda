package com.astercasc.squid.meowfitness

import androidx.compose.ui.res.painterResource
import androidx.compose.ui.window.Window
import androidx.compose.ui.window.application
import com.astercasc.squid.meowfitness.di.KoinInit
import org.koin.core.Koin


lateinit var koin: Koin


fun main() = application {

    koin = KoinInit().init()

    Window(
        onCloseRequest = ::exitApplication,
        icon = painterResource("logo.png"),
        title = "喵喵健身",
    ) {
        App()
    }
}