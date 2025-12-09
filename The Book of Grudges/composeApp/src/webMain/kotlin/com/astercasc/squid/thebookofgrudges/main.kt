package com.astercasc.squid.thebookofgrudges

import androidx.compose.ui.ExperimentalComposeUiApi
import androidx.compose.ui.window.ComposeViewport
import com.astercasc.squid.thebookofgrudges.di.KoinInit

@OptIn(ExperimentalComposeUiApi::class)
fun main() {
    KoinInit().init()
    ComposeViewport {
        App()
    }
}