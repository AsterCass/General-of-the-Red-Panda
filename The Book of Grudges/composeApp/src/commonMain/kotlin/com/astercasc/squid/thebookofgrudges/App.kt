package com.astercasc.squid.thebookofgrudges

import androidx.compose.foundation.isSystemInDarkTheme
import androidx.compose.material3.MaterialTheme
import androidx.compose.runtime.Composable
import androidx.compose.runtime.CompositionLocalProvider
import androidx.compose.runtime.remember
import androidx.compose.ui.graphics.ImageShader
import androidx.compose.ui.graphics.ShaderBrush
import cafe.adriel.voyager.navigator.Navigator
import cafe.adriel.voyager.transitions.SlideTransition
import com.astercasc.squid.thebookofgrudges.theme.appTypography
import com.astercasc.squid.thebookofgrudges.theme.darkScheme
import com.astercasc.squid.thebookofgrudges.theme.lightScheme
import com.astercasc.squid.thebookofgrudges.ui.HomeScreenObj
import com.astercasc.squid.thebookofgrudges.utils.LocalBgBrush
import org.jetbrains.compose.resources.imageResource
import thebookofgrudges.composeapp.generated.resources.Res
import thebookofgrudges.composeapp.generated.resources.bg


@Composable
fun App() {

    // theme
    val darkTheme: Boolean = isSystemInDarkTheme()
    val colorScheme = if(darkTheme) darkScheme else lightScheme

    // bg
    val image = imageResource(Res.drawable.bg)
    val brush = remember {
        ShaderBrush(ImageShader(image))
    }

    CompositionLocalProvider(
        LocalBgBrush provides brush
    ) {
        Navigator(HomeScreenObj) { nav ->
            MaterialTheme(
                colorScheme = colorScheme,
                typography = appTypography(),
            ) {
                SlideTransition(nav)
            }
        }
    }




}