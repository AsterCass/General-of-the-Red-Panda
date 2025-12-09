package com.astercasc.squid.thebookofgrudges.utils

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