package com.astercasc.squid.thebookofgrudges.di

import com.astercasc.squid.thebookofgrudges.data.SettingsWrapper
import org.koin.dsl.module

actual fun platformModule() = module {

    single { SettingsWrapper().createSettings() }

}