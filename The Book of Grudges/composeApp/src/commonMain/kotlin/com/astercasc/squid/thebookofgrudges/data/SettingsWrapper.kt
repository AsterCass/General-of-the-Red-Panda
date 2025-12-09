package com.astercasc.squid.thebookofgrudges.data

import com.russhwolf.settings.Settings


expect class SettingsWrapper {
    fun createSettings(): Settings
}