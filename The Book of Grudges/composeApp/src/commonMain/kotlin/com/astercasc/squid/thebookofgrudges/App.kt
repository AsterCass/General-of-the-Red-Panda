package com.astercasc.squid.thebookofgrudges

import androidx.compose.animation.AnimatedVisibility
import androidx.compose.foundation.Image
import androidx.compose.foundation.background
import androidx.compose.foundation.isSystemInDarkTheme
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.safeContentPadding
import androidx.compose.material3.Button
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.material3.darkColorScheme
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import com.astercasc.squid.thebookofgrudges.theme.AppTypography
import com.astercasc.squid.thebookofgrudges.theme.darkScheme
import com.astercasc.squid.thebookofgrudges.theme.lightScheme
import org.jetbrains.compose.resources.painterResource
import org.jetbrains.compose.ui.tooling.preview.Preview

import thebookofgrudges.composeapp.generated.resources.Res
import thebookofgrudges.composeapp.generated.resources.compose_multiplatform

@Composable
fun App() {

    val  darkTheme: Boolean = isSystemInDarkTheme()
    val colorScheme = if(darkTheme) darkScheme else lightScheme

    MaterialTheme(
        colorScheme = colorScheme,
        typography = AppTypography,
    ) {


        var showContent by remember { mutableStateOf(false) }
        Column(
            modifier = Modifier
                .safeContentPadding()
                .fillMaxSize(),
            horizontalAlignment = Alignment.CenterHorizontally,
        ) {
            Button(onClick = { showContent = !showContent }) {
                Text("Click me!")
            }
            AnimatedVisibility(showContent) {
                Column(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalAlignment = Alignment.CenterHorizontally,
                ) {
                    Image(painterResource(Res.drawable.compose_multiplatform), null)
                }
            }
        }


    }
}