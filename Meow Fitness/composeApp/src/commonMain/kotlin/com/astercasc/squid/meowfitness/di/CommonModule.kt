package com.astercasc.squid.meowfitness.di


import com.astercasc.squid.meowfitness.data.DataStorageManager
import com.astercasc.squid.meowfitness.data.model.GlobalDataModel
import com.russhwolf.settings.ExperimentalSettingsApi
import org.koin.core.module.Module
import org.koin.dsl.module

@OptIn(ExperimentalSettingsApi::class)
fun commonModule() = module {

    //global
    single<GlobalDataModel> {
        GlobalDataModel(dataStorageManager = get())
    }

    //common


    //db
    single<DataStorageManager> {
        DataStorageManager(settings = get())
    }

}

expect fun platformModule(): Module