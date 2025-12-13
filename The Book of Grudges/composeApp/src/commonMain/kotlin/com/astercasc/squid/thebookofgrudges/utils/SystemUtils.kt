package com.astercasc.squid.thebookofgrudges.utils

import androidx.compose.runtime.Composable
import androidx.compose.runtime.staticCompositionLocalOf
import androidx.compose.ui.graphics.Brush
import org.jetbrains.compose.resources.stringResource
import thebookofgrudges.composeapp.generated.resources.*


@Composable
fun getStringByName(key: String): String {
    val res = StringResourceRegistry.map[key] ?: Res.string.none
    return stringResource(res)
}


val LocalBgBrush = staticCompositionLocalOf<Brush> {
    error("Res not found")
}

object StringResourceRegistry {
    val map = mapOf(
        "app_name" to Res.string.app_name,
        "none" to Res.string.none,

        "grudge_one" to Res.string.grudge_one,
        "grudge_one_desc" to Res.string.grudge_one_desc,

        "grudge_two" to Res.string.grudge_two,
        "grudge_two_desc" to Res.string.grudge_two_desc,

        "grudge_three" to Res.string.grudge_three,
        "grudge_three_desc" to Res.string.grudge_three_desc,

        "grudge_four" to Res.string.grudge_four,
        "grudge_four_desc" to Res.string.grudge_four_desc,

        "grudge_five" to Res.string.grudge_five,
        "grudge_five_desc" to Res.string.grudge_five_desc,

        "grudge_six" to Res.string.grudge_six,
        "grudge_six_desc" to Res.string.grudge_six_desc,

        "grudge_seven" to Res.string.grudge_seven,
        "grudge_seven_desc" to Res.string.grudge_seven_desc,

        "grudge_eight" to Res.string.grudge_eight,
        "grudge_eight_desc" to Res.string.grudge_eight_desc,

        "grudge_nine" to Res.string.grudge_nine,
        "grudge_nine_desc" to Res.string.grudge_nine_desc,

        "grudge_ten" to Res.string.grudge_ten,
        "grudge_ten_desc" to Res.string.grudge_ten_desc,
    )
}
