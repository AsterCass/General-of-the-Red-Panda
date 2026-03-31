package com.astercasc.squid.meowfitness.ui

import androidx.compose.foundation.background
import androidx.compose.foundation.isSystemInDarkTheme
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.FabPosition
import androidx.compose.material3.Scaffold
import androidx.compose.runtime.Composable
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import cafe.adriel.voyager.core.screen.Screen
import cafe.adriel.voyager.core.screen.ScreenKey
import cafe.adriel.voyager.core.screen.uniqueScreenKey
import cafe.adriel.voyager.navigator.LocalNavigator
import cafe.adriel.voyager.navigator.currentOrThrow
import com.astercasc.squid.meowfitness.constant.enums.ViewEnum
import com.astercasc.squid.meowfitness.data.DataStorageManager
import com.astercasc.squid.meowfitness.data.model.GlobalDataModel
import com.astercasc.squid.meowfitness.ui.components.MainAppBar
import com.astercasc.squid.meowfitness.utils.LocalBgBrush
import meowfitness.composeapp.generated.resources.Res
import meowfitness.composeapp.generated.resources.home_title
import org.jetbrains.compose.resources.stringResource
import org.koin.compose.koinInject

object HomeScreenObj : Screen {

    override val key: ScreenKey = "${ViewEnum.VIEW_HOME.code}$uniqueScreenKey"

    @Composable
    override fun Content() {
        HomeScreen()
    }

}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun HomeScreen() {

    // inject
    val globalDataModel : GlobalDataModel = koinInject()
    val dataStorageManager: DataStorageManager = koinInject()
    val navigator = LocalNavigator.currentOrThrow
    val scope = rememberCoroutineScope()
    val isDark = isSystemInDarkTheme()


    Scaffold(
        topBar = {
            MainAppBar(stringResource(Res.string.home_title))
    }, bottomBar = {}, floatingActionButton = {}, floatingActionButtonPosition = FabPosition.Start
    ) { padding ->

        Box(
            modifier = Modifier.fillMaxSize().padding(padding)
                .then(if (isDark) Modifier else Modifier.background(brush = LocalBgBrush.current))
        ) {
            // 主内容

            LazyColumn(
                modifier = Modifier
                    .padding(horizontal = 12.dp).fillMaxSize(),
                verticalArrangement = Arrangement.spacedBy(8.dp)
            ) {
                item {
                    Spacer(Modifier.height(18.dp))
                }



                item {
                    Spacer(Modifier.height(75.dp))
                }

            }



        }
    }


}

