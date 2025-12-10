package com.astercasc.squid.thebookofgrudges.utils

import androidx.compose.ui.graphics.Color
import kotlinx.datetime.LocalDateTime
import kotlinx.datetime.TimeZone
import kotlinx.datetime.format.FormatStringsInDatetimeFormats
import kotlinx.datetime.format.byUnicodePattern
import kotlinx.datetime.toLocalDateTime
import kotlin.time.ExperimentalTime
import kotlin.time.Instant

@OptIn(ExperimentalTime::class, FormatStringsInDatetimeFormats::class)
fun formatTimestamp(timestampMillis: Long): String {
    val instant = Instant.fromEpochMilliseconds(timestampMillis * 1000)
    val zone = TimeZone.currentSystemDefault()
    val localDT = instant.toLocalDateTime(zone)
    val formatter = LocalDateTime.Format {
        byUnicodePattern("yyyy-MM-dd HH:mm")
    }
    return formatter.format(localDT)

}

/**
 * 在给定范围 [minValue, maxValue] 内，对两个颜色做线性插值。
 *
 * @param color1    起始颜色（输入 value = minValue 时返回）
 * @param color2    目标颜色（输入 value = maxValue 时返回）
 * @param value     当前进度值
 * @param minValue  最小值（例如 0）
 * @param maxValue  最大值（例如 10、100）
 */
fun interColorRange(
    color1: Color,
    color2: Color,
    value: Float,
    minValue: Float,
    maxValue: Float
): Color {
    val t = when {
        maxValue == minValue -> 0f // 防止除零
        else -> ((value - minValue) / (maxValue - minValue)).coerceIn(0f, 1f)
    }

    return Color(
        red = color1.red + (color2.red - color1.red) * t,
        green = color1.green + (color2.green - color1.green) * t,
        blue = color1.blue + (color2.blue - color1.blue) * t,
        alpha = color1.alpha + (color2.alpha - color1.alpha) * t
    )
}