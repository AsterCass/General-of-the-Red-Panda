package com.astercasc.squid.meowfitness

import androidx.compose.foundation.isSystemInDarkTheme
import androidx.compose.material3.MaterialTheme
import androidx.compose.runtime.Composable
import androidx.compose.runtime.CompositionLocalProvider
import androidx.compose.runtime.remember
import androidx.compose.ui.graphics.ImageShader
import androidx.compose.ui.graphics.ShaderBrush
import androidx.compose.ui.graphics.TileMode
import cafe.adriel.voyager.navigator.Navigator
import cafe.adriel.voyager.transitions.SlideTransition
import com.astercasc.squid.meowfitness.theme.appTypography
import com.astercasc.squid.meowfitness.theme.darkScheme
import com.astercasc.squid.meowfitness.theme.lightScheme
import com.astercasc.squid.meowfitness.ui.HomeScreenObj
import com.astercasc.squid.meowfitness.utils.LocalBgBrush
import org.jetbrains.compose.resources.imageResource
import meowfitness.composeapp.generated.resources.Res
import meowfitness.composeapp.generated.resources.bgl


@Composable
fun App() {

    // theme
    val darkTheme: Boolean = isSystemInDarkTheme()
    val colorScheme = if(darkTheme) darkScheme else lightScheme

    // bg
    val image = imageResource(Res.drawable.bgl)
    val brush = remember {
        ShaderBrush(
            ImageShader(
                image, TileMode.Mirror, TileMode.Mirror
            )
        )
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