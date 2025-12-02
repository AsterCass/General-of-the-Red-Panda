package com.astercasc.squid.thebookofgrudges.constant.enums


enum class GrudgeLevel(
    val level: Int,
    val title: String,
    val desc: String,
) {
    ONE(1, "grudge_one", "grudge_one_desc"),
    TWO(2, "grudge_two", "grudge_two_desc"),
    THREE(3, "grudge_three", "grudge_three_desc"),
    FOUR(4, "grudge_four", "grudge_four_desc"),
    FIVE(5, "grudge_five", "grudge_five_desc"),
    SIX(6, "grudge_six", "grudge_six_desc"),
    SEVEN(7, "grudge_seven", "grudge_seven_desc"),
    EIGHT(8, "grudge_eight", "grudge_eight_desc"),
    NINE(9, "grudge_nine", "grudge_nine_desc"),
    TEN(10, "grudge_ten", "grudge_ten_desc"),


    ;

    companion object {
        fun getEnumByCode(level: Int): GrudgeLevel {
            var ret = ONE
            for (thisEnum in GrudgeLevel.entries) {
                if (thisEnum.level == level) {
                    ret = thisEnum
                    break
                }
            }
            return ret
        }
    }
}

