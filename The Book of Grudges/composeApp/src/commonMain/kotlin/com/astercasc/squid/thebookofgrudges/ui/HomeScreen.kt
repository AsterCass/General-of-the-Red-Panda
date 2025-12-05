package com.astercasc.squid.thebookofgrudges.ui

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.input.rememberTextFieldState
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.sharp.MenuBook
import androidx.compose.material.icons.filled.Edit
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import cafe.adriel.voyager.core.screen.Screen
import cafe.adriel.voyager.core.screen.ScreenKey
import cafe.adriel.voyager.core.screen.uniqueScreenKey
import com.astercasc.squid.thebookofgrudges.constant.enums.ViewEnum
import com.astercasc.squid.thebookofgrudges.ui.components.*

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

    // sheet
    var showNewGrudgeSheet by rememberSaveable { mutableStateOf(false) }
    var showReadGrudgeSheet by rememberSaveable { mutableStateOf(false) }
    // new tag & obj 这里对话框展示状态不用在重组之后保留
    var openNewObjDialog by remember { mutableStateOf(false) }
    var newObjectName by rememberSaveable { mutableStateOf("") }
    var openNewTagDialog by remember { mutableStateOf(false) }
    var newTagName by rememberSaveable { mutableStateOf("") }


    Scaffold(
        topBar = {
        MainAppBar("todo title")
    }, bottomBar = {}, floatingActionButton = {}, floatingActionButtonPosition = FabPosition.Start
    ) { padding ->


        Box(modifier = Modifier.fillMaxSize().padding(padding)) {
            // 主内容

            LazyColumn(
                modifier = Modifier.fillMaxSize()
            ) {

                items(20) { index ->
                    ListItem(
                        headlineContent = { Text("todo $index") })
                }

                item {
                    Spacer(Modifier.height(75.dp))
                }

            }

            SmallFloatingActionButton(
                onClick = { showNewGrudgeSheet = true },
                shape = RoundedCornerShape(6.dp),
                modifier = Modifier.align(Alignment.BottomStart).padding(start = 16.dp, bottom = 16.dp)
            ) {
                Row(
                    modifier = Modifier.padding(vertical = 12.dp, horizontal = 12.dp),
                    verticalAlignment = Alignment.CenterVertically,
                    horizontalArrangement = Arrangement.spacedBy(8.dp)
                ) {
                    Icon(
                        modifier = Modifier.size(18.dp),
                        imageVector = Icons.Filled.Edit,
                        contentDescription = "todo something"
                    )
                    Text("todo something")
                }

            }


            SmallFloatingActionButton(
                onClick = { showReadGrudgeSheet = true },
                shape = CircleShape,
                modifier = Modifier.align(Alignment.CenterEnd).padding(end = 16.dp)
            ) {
                Icon(
                    modifier = Modifier.padding(12.dp).size(25.dp),
                    imageVector = Icons.AutoMirrored.Sharp.MenuBook,
                    contentDescription = "todo something"
                )

            }

            // showNewGrudgeSheet
            val newGTitleState = rememberTextFieldState("")
            val newGDescState = rememberTextFieldState("")
            var newGSliderPosition by rememberSaveable {
                mutableFloatStateOf(1f)
            }

            // newGrudge
            if (showNewGrudgeSheet) {
                NewGrudgeSheet(
                    newGTitleState = newGTitleState,
                    newGDescState = newGDescState,
                    newGSliderPosition = newGSliderPosition,
                    closeSheet = { showNewGrudgeSheet = false },
                    updateSliderPosition = { newGSliderPosition = it },
                    openNewObjDialog = { openNewObjDialog = true },
                    openNewTagDialog = { openNewTagDialog = true }
                )
            }


            // readSheet
            if (showReadGrudgeSheet) {
                ReadGrudgeSheet { showReadGrudgeSheet = false }
            }

            // newObj
            if (openNewObjDialog) {
                NewGrudgeObject(
                    onDismissRequest = { openNewObjDialog = false },
                )
            }

            // newTag
            if (openNewTagDialog) {
                NewGrudgeTag(
                    onDismissRequest = { openNewTagDialog = false },
                )
            }


        }
    }


}

