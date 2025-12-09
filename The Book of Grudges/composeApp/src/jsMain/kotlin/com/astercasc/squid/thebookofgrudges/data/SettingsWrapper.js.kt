package com.astercasc.squid.thebookofgrudges.data

import com.russhwolf.settings.Settings
import com.russhwolf.settings.StorageSettings

actual class SettingsWrapper {
    actual fun createSettings(): Settings {
        return StorageSettings()
    }
}