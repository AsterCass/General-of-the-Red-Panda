package com.astercasc.squid.thebookofgrudges.data

import com.russhwolf.settings.ExperimentalSettingsApi
import com.russhwolf.settings.NSUserDefaultsSettings
import com.russhwolf.settings.Settings
import platform.Foundation.NSUserDefaults

actual class SettingsWrapper {
    @OptIn(ExperimentalSettingsApi::class)
    actual fun createSettings(): Settings {
        val delegate: NSUserDefaults = NSUserDefaults.standardUserDefaults
        return NSUserDefaultsSettings(delegate)
    }
}