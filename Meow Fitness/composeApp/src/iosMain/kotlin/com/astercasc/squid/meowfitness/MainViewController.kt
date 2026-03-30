package com.astercasc.squid.meowfitness

import androidx.compose.ui.window.ComposeUIViewController
import com.astercasc.squid.meowfitness.di.KoinInit

fun MainViewController() = ComposeUIViewController(
    configure = {
        KoinInit().init()
    }
) { App() }