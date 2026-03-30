package com.astercasc.squid.meowfitness

import androidx.compose.ui.ExperimentalComposeUiApi
import androidx.compose.ui.window.ComposeViewport
import com.astercasc.squid.meowfitness.di.KoinInit

@OptIn(ExperimentalComposeUiApi::class)
fun main() {
    KoinInit().init()
    ComposeViewport {
        App()
    }
}