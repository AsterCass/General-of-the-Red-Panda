package com.astercasc.squid.meowfitness.data

import com.astercasc.squid.meowfitness.constant.*
import com.astercasc.squid.meowfitness.data.DataStorageManager.Companion.USER_GRU_LIST
import com.astercasc.squid.meowfitness.data.DataStorageManager.Companion.USER_OBJ_LIST
import com.astercasc.squid.meowfitness.data.DataStorageManager.Companion.USER_TAG_LIST
import com.astercasc.squid.meowfitness.data.model.GlobalDataModel
import kotlin.random.Random
import kotlin.random.nextUInt
import kotlin.time.Clock
import kotlin.time.ExperimentalTime

// tag
fun initTagList(dataStorageManager: DataStorageManager): List<GrudgeTag> {
    val listStr = dataStorageManager.getString(USER_TAG_LIST)
    return if (listStr.isBlank()) {
        listOf(
            EXAMPLE_TAG_1,
            EXAMPLE_TAG_2,
        )
    } else {
        commonJson.decodeFromString<List<GrudgeTag>>(listStr)
    }
}

@OptIn(ExperimentalTime::class)
fun addNewTag(
    globalDataModel: GlobalDataModel,
    dataStorageManager: DataStorageManager,
    name: String
) {
    globalDataModel.addTag(
        GrudgeTag(
            id = "${TAG_PREFIX}${Clock.System.now().epochSeconds}${Random.nextUInt()}",
            name = name,
            color = 0UL,
            createTime = Clock.System.now().epochSeconds
        )
    )
    dataStorageManager.setString(USER_TAG_LIST, commonJson.encodeToString(globalDataModel.tagList.value))
}

fun deleteTag(
    globalDataModel: GlobalDataModel,
    dataStorageManager: DataStorageManager,
    id: String
) {
    globalDataModel.removeTag(id)
    dataStorageManager.setString(USER_TAG_LIST, commonJson.encodeToString(globalDataModel.tagList.value))
}

// obj

fun initObjList(dataStorageManager: DataStorageManager): List<GrudgeObj> {
    val listStr = dataStorageManager.getString(USER_OBJ_LIST)
    return if (listStr.isBlank()) {
        listOf(
            EXAMPLE_OBJ_1,
        )
    } else {
        commonJson.decodeFromString<List<GrudgeObj>>(listStr)
    }
}

@OptIn(ExperimentalTime::class)
fun addNewObj(
    globalDataModel: GlobalDataModel,
    dataStorageManager: DataStorageManager,
    name: String
) {
    globalDataModel.addObj(
        GrudgeObj(
            id = "${OBJ_PREFIX}${Clock.System.now().epochSeconds}${Random.nextUInt()}",
            name = name,
            color = 0UL,
            createTime = Clock.System.now().epochSeconds
        )
    )
    dataStorageManager.setString(USER_OBJ_LIST, commonJson.encodeToString(globalDataModel.objList.value))
}

fun deleteObj(
    globalDataModel: GlobalDataModel,
    dataStorageManager: DataStorageManager,
    id: String
) {
    globalDataModel.removeObj(id)
    dataStorageManager.setString(USER_OBJ_LIST, commonJson.encodeToString(globalDataModel.objList.value))
}

// grudge

fun initGrudgeList(dataStorageManager: DataStorageManager): List<GrudgeCell> {
    val listStr = dataStorageManager.getString(USER_GRU_LIST)
    return if (listStr.isBlank()) {
        listOf()
    } else {
        commonJson.decodeFromString<List<GrudgeCell>>(listStr)
    }
}

@OptIn(ExperimentalTime::class)
fun addNewGru(
    globalDataModel: GlobalDataModel,
    dataStorageManager: DataStorageManager,
    title: String,
    description: String,
    level: Int,
) {
    globalDataModel.addGru(
        GrudgeCell(
            id = "${GRU_PREFIX}${Clock.System.now().epochSeconds}${Random.nextUInt()}",
            title = title,
            description = description,
            level = level,
            tags = globalDataModel.tagListSelectedNew.value,
            objs = globalDataModel.objListSelectedNew.value,
            createTime = Clock.System.now().epochSeconds,
            updateTime = Clock.System.now().epochSeconds,
        )
    )
    dataStorageManager.setString(USER_GRU_LIST, commonJson.encodeToString(globalDataModel.gruList.value))
}

@OptIn(ExperimentalTime::class)
fun editGru(
    globalDataModel: GlobalDataModel,
    dataStorageManager: DataStorageManager,
    title: String,
    description: String,
    level: Int,
    editGru: GrudgeCell,
) {
    globalDataModel.editGru(
        GrudgeCell(
            id = editGru.id,
            title = title,
            description = description,
            level = level,
            tags = globalDataModel.tagListSelectedEdit.value,
            objs = globalDataModel.objListSelectedEdit.value,
            createTime = editGru.createTime,
            updateTime = Clock.System.now().epochSeconds,
        )
    )
    dataStorageManager.setString(USER_GRU_LIST, commonJson.encodeToString(globalDataModel.gruList.value))
}

fun deleteGru(
    globalDataModel: GlobalDataModel,
    dataStorageManager: DataStorageManager,
    id: String
) {
    globalDataModel.removeGru(id)
    dataStorageManager.setString(USER_GRU_LIST, commonJson.encodeToString(globalDataModel.gruList.value))
}

fun addGruRef(
    globalDataModel: GlobalDataModel,
    dataStorageManager: DataStorageManager,
    id: String
) {
    globalDataModel.addGruRef(id)
    dataStorageManager.setString(USER_GRU_LIST, commonJson.encodeToString(globalDataModel.gruList.value))
}