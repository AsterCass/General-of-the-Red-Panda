package com.astercasc.squid.thebookofgrudges.ui

import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.FabPosition
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import cafe.adriel.voyager.core.screen.Screen
import cafe.adriel.voyager.core.screen.ScreenKey
import cafe.adriel.voyager.core.screen.uniqueScreenKey
import com.astercasc.squid.thebookofgrudges.constant.enums.ViewEnum
import com.astercasc.squid.thebookofgrudges.ui.components.MainAppBar

object EditGrudgeTagObj : Screen {

    override val key: ScreenKey = "${ViewEnum.EDIT_GRU_TAG.code}$uniqueScreenKey"

    @Composable
    override fun Content() {
        EditGrudgeTag()
    }

}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun EditGrudgeTag() {


    Scaffold(
        topBar = {
            MainAppBar("todo title")
        }, bottomBar = {}, floatingActionButton = {}, floatingActionButtonPosition = FabPosition.Start
    ) { padding ->


        Box(modifier = Modifier.fillMaxSize().padding(padding)) {


            Text("Edit Grudge Tag")

        }
    }


}

