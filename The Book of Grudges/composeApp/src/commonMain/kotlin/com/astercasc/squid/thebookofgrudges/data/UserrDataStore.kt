package com.astercasc.squid.thebookofgrudges.data

import com.astercasc.squid.thebookofgrudges.constant.EXAMPLE_TAG_1
import com.astercasc.squid.thebookofgrudges.constant.EXAMPLE_TAG_2
import com.astercasc.squid.thebookofgrudges.constant.TAG_PREFIX
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