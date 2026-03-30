package com.astercasc.squid.meowfitness.di

import com.astercasc.squid.meowfitness.data.SettingsWrapper
import org.koin.dsl.module

actual fun platformModule() = module {

    single { SettingsWrapper().createSettings() }

}