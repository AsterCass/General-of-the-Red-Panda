package com.astercasc.squid.thebookofgrudges

import androidx.compose.foundation.isSystemInDarkTheme
import androidx.compose.material3.MaterialTheme
import androidx.compose.runtime.Composable
import cafe.adriel.voyager.navigator.Navigator
import cafe.adriel.voyager.transitions.SlideTransition
import com.astercasc.squid.thebookofgrudges.theme.appTypography
import com.astercasc.squid.thebookofgrudges.theme.darkScheme
import com.astercasc.squid.thebookofgrudges.theme.lightScheme
import com.astercasc.squid.thebookofgrudges.ui.HomeScreenObj



// https://chatgpt.com/c/69315080-1adc-8322-a187-4cec47046ccd
// https://claude.ai/chat/e56ac51b-edf2-4a66-ae1f-fa7e287adcfe
// https://www.iconfont.cn/search/index?searchType=icon&q=devil&page=1&fromCollection=-1
// https://m3.material.io/components/chips/specs
// https://fonts.google.com/icons
// https://voyager.adriel.cafe/transitions-api/
@Composable
fun App() {

    val  darkTheme: Boolean = isSystemInDarkTheme()
    val colorScheme = if(darkTheme) darkScheme else lightScheme

    Navigator(HomeScreenObj) { nav ->
        MaterialTheme(
            colorScheme = colorScheme,
            typography = appTypography(),
        ) {
            SlideTransition(nav)
        }
    }


}