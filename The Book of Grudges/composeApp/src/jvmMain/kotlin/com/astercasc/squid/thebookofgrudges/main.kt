package com.astercasc.squid.thebookofgrudges

import androidx.compose.ui.window.Window
import androidx.compose.ui.window.application
import com.astercasc.squid.thebookofgrudges.di.KoinInit
import org.koin.core.Koin


lateinit var koin: Koin


fun main() = application {

    koin = KoinInit().init()

    Window(
        onCloseRequest = ::exitApplication,
        title = "thebookofgrudges",
    ) {
        App()
    }
}