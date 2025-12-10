package com.astercasc.squid.thebookofgrudges.data

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
        const val USER_TAG_LIST = "USER_TAG_LIST"
        const val USER_OBJ_LIST = "USER_OBJ_LIST"
        const val USER_GRU_LIST = "USER_GRU_LIST"

    }

}