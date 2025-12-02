package com.astercasc.squid.thebookofgrudges

import androidx.compose.foundation.isSystemInDarkTheme
import androidx.compose.material3.MaterialTheme
import androidx.compose.runtime.Composable
import cafe.adriel.voyager.navigator.CurrentScreen
import cafe.adriel.voyager.navigator.Navigator
import com.astercasc.squid.thebookofgrudges.theme.AppTypography
import com.astercasc.squid.thebookofgrudges.theme.darkScheme
import com.astercasc.squid.thebookofgrudges.theme.lightScheme
import com.astercasc.squid.thebookofgrudges.ui.HomeScreenObj


@Composable
fun App() {

    val  darkTheme: Boolean = isSystemInDarkTheme()
    val colorScheme = if(darkTheme) darkScheme else lightScheme

    Navigator(HomeScreenObj) { _ ->
        MaterialTheme(
            colorScheme = colorScheme,
            typography = AppTypography,
        ) {
            CurrentScreen()
        }
    }


}