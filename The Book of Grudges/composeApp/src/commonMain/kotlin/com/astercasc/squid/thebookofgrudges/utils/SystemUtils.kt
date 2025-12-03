package com.astercasc.squid.thebookofgrudges.utils

import androidx.compose.runtime.Composable
import org.jetbrains.compose.resources.stringResource
import thebookofgrudges.composeapp.generated.resources.Res
import thebookofgrudges.composeapp.generated.resources.app_name
import thebookofgrudges.composeapp.generated.resources.grudge_eight
import thebookofgrudges.composeapp.generated.resources.grudge_eight_desc
import thebookofgrudges.composeapp.generated.resources.grudge_five
import thebookofgrudges.composeapp.generated.resources.grudge_five_desc
import thebookofgrudges.composeapp.generated.resources.grudge_four
import thebookofgrudges.composeapp.generated.resources.grudge_four_desc
import thebookofgrudges.composeapp.generated.resources.grudge_nine
import thebookofgrudges.composeapp.generated.resources.grudge_nine_desc
import thebookofgrudges.composeapp.generated.resources.grudge_one
import thebookofgrudges.composeapp.generated.resources.grudge_one_desc
import thebookofgrudges.composeapp.generated.resources.grudge_seven
import thebookofgrudges.composeapp.generated.resources.grudge_seven_desc
import thebookofgrudges.composeapp.generated.resources.grudge_six
import thebookofgrudges.composeapp.generated.resources.grudge_six_desc
import thebookofgrudges.composeapp.generated.resources.grudge_ten
import thebookofgrudges.composeapp.generated.resources.grudge_ten_desc
import thebookofgrudges.composeapp.generated.resources.grudge_three
import thebookofgrudges.composeapp.generated.resources.grudge_three_desc
import thebookofgrudges.composeapp.generated.resources.grudge_two
import thebookofgrudges.composeapp.generated.resources.grudge_two_desc
import thebookofgrudges.composeapp.generated.resources.none


@Composable
fun getStringByName(key: String): String {
    val res = StringResourceRegistry.map[key] ?: Res.string.none
    return stringResource(res)
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
