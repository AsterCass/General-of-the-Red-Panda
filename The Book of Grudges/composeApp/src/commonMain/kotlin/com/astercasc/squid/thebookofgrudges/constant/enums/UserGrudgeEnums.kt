package com.astercasc.squid.thebookofgrudges.constant.enums

import org.jetbrains.compose.resources.StringResource
import thebookofgrudges.composeapp.generated.resources.*


enum class GrudgeLevelEnum(
    val level: Int,
    val title: String,
    val res: StringResource,
    val descRes: StringResource,
) {
    ONE(1, "grudge_one", Res.string.grudge_one, Res.string.grudge_one_desc),
    TWO(2, "grudge_two", Res.string.grudge_two, Res.string.grudge_two_desc),
    THREE(3, "grudge_three", Res.string.grudge_three, Res.string.grudge_three_desc),
    FOUR(4, "grudge_four", Res.string.grudge_four, Res.string.grudge_four_desc),
    FIVE(5, "grudge_five", Res.string.grudge_five, Res.string.grudge_five_desc),
    SIX(6, "grudge_six", Res.string.grudge_six, Res.string.grudge_six_desc),
    SEVEN(7, "grudge_seven", Res.string.grudge_seven, Res.string.grudge_seven_desc),
    EIGHT(8, "grudge_eight", Res.string.grudge_eight, Res.string.grudge_eight_desc),
    NINE(9, "grudge_nine", Res.string.grudge_nine, Res.string.grudge_nine_desc),
    TEN(10, "grudge_ten", Res.string.grudge_ten, Res.string.grudge_ten_desc),

    ;

    companion object {
        fun getEnumByCode(level: Int): GrudgeLevelEnum {
            var ret = ONE
            for (thisEnum in GrudgeLevelEnum.entries) {
                if (thisEnum.level == level) {
                    ret = thisEnum
                    break
                }
            }
            return ret
        }
    }
}

