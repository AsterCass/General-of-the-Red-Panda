package com.astercasc.squid.thebookofgrudges.data

import com.astercasc.squid.thebookofgrudges.constant.enums.GrudgeLevel
import kotlinx.serialization.Serializable

@Serializable
data class GrudgeCell(
    var id: Long = 0L,
    var title: String = "",
    var description: String = "",
    var level : GrudgeLevel = GrudgeLevel.ONE,
    var referCount : Int = 0,
    var tags : List<GrudgeTag> = listOf(),
    var obj : GrudgeObj? = null,
    var createTime : Long = 0L,
)

@Serializable
data class GrudgeObj(
    var id: Long = 0L,
    var name: String = "",
)

@Serializable
data class GrudgeTag(
    var id: Long = 0L,
    var name: String = "",
)