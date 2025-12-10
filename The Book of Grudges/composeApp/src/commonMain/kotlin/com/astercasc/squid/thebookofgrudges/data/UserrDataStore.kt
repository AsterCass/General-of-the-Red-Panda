package com.astercasc.squid.thebookofgrudges.data

import com.astercasc.squid.thebookofgrudges.constant.EXAMPLE_OBJ_1
import com.astercasc.squid.thebookofgrudges.constant.EXAMPLE_TAG_1
import com.astercasc.squid.thebookofgrudges.constant.EXAMPLE_TAG_2
import com.astercasc.squid.thebookofgrudges.constant.OBJ_PREFIX
import com.astercasc.squid.thebookofgrudges.constant.TAG_PREFIX
import com.astercasc.squid.thebookofgrudges.data.DataStorageManager.Companion.USER_OBJ_LIST
import com.astercasc.squid.thebookofgrudges.data.DataStorageManager.Companion.USER_TAG_LIST
import com.astercasc.squid.thebookofgrudges.data.model.GlobalDataModel
import kotlin.random.Random
import kotlin.random.nextUInt
import kotlin.time.Clock
import kotlin.time.ExperimentalTime

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

fun deleteTag(
    globalDataModel: GlobalDataModel,
    dataStorageManager: DataStorageManager,
    id: String
) {
    globalDataModel.removeTag(id)
    dataStorageManager.setString(USER_TAG_LIST, commonJson.encodeToString(globalDataModel.tagList.value))
}

fun deleteObj(
    globalDataModel: GlobalDataModel,
    dataStorageManager: DataStorageManager,
    id: String
) {
    globalDataModel.removeObj(id)
    dataStorageManager.setString(USER_OBJ_LIST, commonJson.encodeToString(globalDataModel.objList.value))
}