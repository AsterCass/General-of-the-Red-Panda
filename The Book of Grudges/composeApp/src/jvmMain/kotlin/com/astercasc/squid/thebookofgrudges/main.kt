package com.astercasc.squid.thebookofgrudges

import androidx.compose.ui.window.Window
import androidx.compose.ui.window.application

fun main() = application {
    Window(
        onCloseRequest = ::exitApplication,
        title = "thebookofgrudges",
    ) {
        App()
    }
}