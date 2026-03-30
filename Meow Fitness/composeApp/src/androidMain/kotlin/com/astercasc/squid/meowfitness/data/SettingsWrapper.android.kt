package com.astercasc.squid.meowfitness.data

import android.content.Context
import com.russhwolf.settings.Settings
import com.russhwolf.settings.SharedPreferencesSettings
import org.koin.core.component.KoinComponent
import org.koin.core.component.inject


actual class SettingsWrapper() : KoinComponent {

    private val context: Context by inject()

    actual fun createSettings(): Settings {
        return SharedPreferencesSettings(
            context.getSharedPreferences(
                "meow_fitness_settings", Context.MODE_PRIVATE
            )
        )
    }

}