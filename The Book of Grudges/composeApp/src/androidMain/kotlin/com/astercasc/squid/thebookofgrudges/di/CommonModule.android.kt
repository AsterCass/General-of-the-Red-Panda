package com.astercasc.squid.thebookofgrudges.di

import com.astercasc.squid.thebookofgrudges.data.SettingsWrapper
import org.koin.core.module.Module
import org.koin.dsl.module

actual fun platformModule(): Module = module {
    single {
        SettingsWrapper().createSettings()
    }
}