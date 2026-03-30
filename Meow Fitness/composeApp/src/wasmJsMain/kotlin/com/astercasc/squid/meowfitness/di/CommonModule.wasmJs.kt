package com.astercasc.squid.meowfitness.di

import com.astercasc.squid.meowfitness.data.SettingsWrapper
import org.koin.core.module.Module
import org.koin.dsl.module

actual fun platformModule(): Module = module {
    single { SettingsWrapper().createSettings() }
}