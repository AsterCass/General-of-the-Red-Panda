package com.astercasc.squid.meowfitness.data

import com.russhwolf.settings.Settings


expect class SettingsWrapper {
    fun createSettings(): Settings
}