package com.astercasc.squid.thebookofgrudges.data

import androidx.compose.ui.graphics.Color
import com.astercasc.squid.thebookofgrudges.constant.enums.GrudgeLevelEnum
import kotlinx.serialization.Serializable

@Serializable
data class GrudgeCell(
    var id: Long = 0L,
    var title: String = "",
    var description: String = "",
    var level : GrudgeLevelEnum = GrudgeLevelEnum.ONE,
    var referCount : Int = 0,
    var tags : List<GrudgeTag> = listOf(),
    var objs : List<GrudgeObj> = listOf(),
    var createTime : Long = 0L,
)

@Serializable
data class GrudgeObj(
    var id: Long = 0L,
    var name: String = "",
    var color: Color = Color.Black,
)

@Serializable
data class GrudgeTag(
    var id: Long = 0L,
    var name: String = "",
    var color: Color = Color.Black,
)