package com.astercasc.squid.thebookofgrudges

import androidx.compose.ui.window.ComposeUIViewController
import com.astercasc.squid.thebookofgrudges.di.KoinInit

fun MainViewController() = ComposeUIViewController(
    configure = {
        KoinInit().init()
    }
) { App() }