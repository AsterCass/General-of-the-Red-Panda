package com.astercasc.squid.meowfitness.data

import com.russhwolf.settings.Settings
import com.russhwolf.settings.set

class DataStorageManager(private val settings: Settings) {

    fun setString(key: String, value: String) {
        settings.set(key = key, value = value)
    }

    fun getString(key: String) = settings.getString(
        key = key,
        defaultValue = "",
    )

    companion object {
        const val FITNESS_LIST = "FITNESS_LIST"


    }

}