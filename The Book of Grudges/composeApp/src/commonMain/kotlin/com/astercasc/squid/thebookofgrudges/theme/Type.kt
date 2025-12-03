package com.astercasc.squid.thebookofgrudges.theme

import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Typography
import androidx.compose.runtime.Composable
import androidx.compose.ui.text.font.FontFamily
import thebookofgrudges.composeapp.generated.resources.NotoSansSC_Regular
import thebookofgrudges.composeapp.generated.resources.Res

@Composable
fun appTypography(): Typography {

    val defaultFontFamily = FontFamily(
        org.jetbrains.compose.resources.Font(
            Res.font.NotoSansSC_Regular
        )
    )

    return Typography(
        labelSmall = MaterialTheme.typography.labelSmall.copy(
            fontFamily = defaultFontFamily,
        ),
        labelMedium = MaterialTheme.typography.labelMedium.copy(
            fontFamily = defaultFontFamily,
        ),
        labelLarge = MaterialTheme.typography.labelLarge.copy(
            fontFamily = defaultFontFamily,
        ),
        bodySmall = MaterialTheme.typography.bodySmall.copy(
            fontFamily = defaultFontFamily,
        ),
        bodyMedium = MaterialTheme.typography.bodyMedium.copy(
            fontFamily = defaultFontFamily,
        ),
        bodyLarge = MaterialTheme.typography.bodyLarge.copy(
            fontFamily = defaultFontFamily,
        ),
        titleSmall = MaterialTheme.typography.titleSmall.copy(
            fontFamily = defaultFontFamily,
        ),
        titleMedium = MaterialTheme.typography.titleMedium.copy(
            fontFamily = defaultFontFamily,
        ),
        titleLarge = MaterialTheme.typography.titleLarge.copy(
            fontFamily = defaultFontFamily,
        ),
        headlineSmall = MaterialTheme.typography.headlineSmall.copy(
            fontFamily = defaultFontFamily,
        ),
        headlineMedium = MaterialTheme.typography.headlineMedium.copy(
            fontFamily = defaultFontFamily,
        ),
        headlineLarge = MaterialTheme.typography.headlineLarge.copy(
            fontFamily = defaultFontFamily,
        ),

        )
}

