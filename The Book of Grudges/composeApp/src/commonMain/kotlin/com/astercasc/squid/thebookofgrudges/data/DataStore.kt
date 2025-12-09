package com.astercasc.squid.thebookofgrudges.data

import androidx.compose.ui.input.key.Key.Companion.Settings
import org.koin.compose.koinInject

fun getNewTag(dataStorageManager: DataStorageManager) {
    println("================== New tag data: ${dataStorageManager.getString("abc")}")
}

fun setNewTag(dataStorageManager: DataStorageManager, name : String) {
  dataStorageManager.setString("abc", name)
}