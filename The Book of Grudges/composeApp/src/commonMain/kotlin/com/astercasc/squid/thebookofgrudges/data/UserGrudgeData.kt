package com.astercasc.squid.thebookofgrudges.data

import com.astercasc.squid.thebookofgrudges.constant.enums.GrudgeLevelEnum
import kotlinx.serialization.Serializable
import kotlinx.serialization.json.Json


val commonJson = Json { ignoreUnknownKeys = true }

@Serializable
data class GrudgeCell(
    var id: String = "",
    var title: String = "",
    var description: String = "",
    var level : Int = 1,
    var referCount : Int = 0,
    var tags : List<GrudgeTag> = listOf(),
    var objs : List<GrudgeObj> = listOf(),
    var createTime : Long = 0L,
)

@Serializable
data class GrudgeObj(
    var id: String = "",
    var name: String = "",
    var color: ULong = 0UL,
    var createTime: Long = 0L,
)

@Serializable
data class GrudgeTag(
    var id: String = "",
    var name: String = "",
    var color: ULong = 0UL,
    var createTime: Long = 0L,
)