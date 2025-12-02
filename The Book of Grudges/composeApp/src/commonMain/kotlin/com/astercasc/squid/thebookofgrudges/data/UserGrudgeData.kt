package com.astercasc.squid.thebookofgrudges.data

import kotlinx.serialization.Serializable

@Serializable
data class GrudgeCell(
    var id: String = "",
    var title: String = "",
    var description: String = "",
    var level : Int = 0,
    var referCount : Int = 0,
)