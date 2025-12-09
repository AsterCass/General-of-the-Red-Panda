package com.astercasc.squid.thebookofgrudges.data

import android.content.Context
import com.russhwolf.settings.Settings
import com.russhwolf.settings.SharedPreferencesSettings


actual class SettingsWrapper(private val context: Context) {


    actual fun createSettings(): Settings {
        return SharedPreferencesSettings(
            context.getSharedPreferences(
                "gru_settings", Context.MODE_PRIVATE
            )
        )
    }

}