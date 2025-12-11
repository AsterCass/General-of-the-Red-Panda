package com.astercasc.squid.thebookofgrudges.ui

import androidx.compose.foundation.border
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.input.clearText
import androidx.compose.foundation.text.input.rememberTextFieldState
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.sharp.MenuBook
import androidx.compose.material.icons.filled.Edit
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.alpha
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.unit.dp
import cafe.adriel.voyager.core.screen.Screen
import cafe.adriel.voyager.core.screen.ScreenKey
import cafe.adriel.voyager.core.screen.uniqueScreenKey
import com.astercasc.squid.thebookofgrudges.constant.GRUDGE_LEVEL_MAX
import com.astercasc.squid.thebookofgrudges.constant.GRUDGE_LEVEL_MAX_COLOR
import com.astercasc.squid.thebookofgrudges.constant.GRUDGE_LEVEL_MIN
import com.astercasc.squid.thebookofgrudges.constant.GRUDGE_LEVEL_MIN_COLOR
import com.astercasc.squid.thebookofgrudges.constant.enums.ViewEnum
import com.astercasc.squid.thebookofgrudges.data.DataStorageManager
import com.astercasc.squid.thebookofgrudges.data.GrudgeCell
import com.astercasc.squid.thebookofgrudges.data.addGruRef
import com.astercasc.squid.thebookofgrudges.data.deleteGru
import com.astercasc.squid.thebookofgrudges.data.model.GlobalDataModel
import com.astercasc.squid.thebookofgrudges.ui.components.*
import com.astercasc.squid.thebookofgrudges.utils.formatTimestamp
import com.astercasc.squid.thebookofgrudges.utils.interColorRange
import org.jetbrains.compose.resources.vectorResource
import org.koin.compose.koinInject
import thebookofgrudges.composeapp.generated.resources.Res
import thebookofgrudges.composeapp.generated.resources.trident

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
    // sheet
    var showNewGrudgeSheet by rememberSaveable { mutableStateOf(false) }
    var showReadGrudgeSheet by rememberSaveable { mutableStateOf(false) }
    // new tag & obj 这里对话框展示状态不用在重组之后保留
    var openNewObjDialog by remember { mutableStateOf(false) }
    var openNewTagDialog by remember { mutableStateOf(false) }
    var deleteGruDialog by remember { mutableStateOf(false) }
    // gru data
    val gruList = globalDataModel.gruList.collectAsState().value
    var currentDeleteGru by remember { mutableStateOf(GrudgeCell()) }

    Scaffold(
        topBar = {
        MainAppBar("todo title")
    }, bottomBar = {}, floatingActionButton = {}, floatingActionButtonPosition = FabPosition.Start
    ) { padding ->


        Box(modifier = Modifier.fillMaxSize().padding(padding)) {
            // 主内容

            LazyColumn(
                modifier = Modifier
                    .padding(start = 12.dp, end = 12.dp, top = 18.dp, bottom = 12.dp).fillMaxSize(),
                verticalArrangement = Arrangement.spacedBy(8.dp)
            ) {
                for (gru in gruList) {

                    val mainColor = interColorRange(
                        GRUDGE_LEVEL_MIN_COLOR,
                        GRUDGE_LEVEL_MAX_COLOR,
                        gru.level.toFloat(),
                        GRUDGE_LEVEL_MIN,
                        GRUDGE_LEVEL_MAX,

                        )

                    val isEmptyTagObj = gru.tags.isEmpty() && gru.objs.isEmpty()

                    item {
                        OutlinedCard(
                            modifier = Modifier.fillMaxWidth(),
                            shape = RoundedCornerShape(6.dp),
                            elevation = CardDefaults.cardElevation(
                                defaultElevation = 3.dp
                            ),
                        ) {
                            Column(
                                modifier = Modifier.fillMaxWidth().padding(12.dp),
                                verticalArrangement = Arrangement.spacedBy(8.dp),
                            ) {
                                Row(
                                    modifier = Modifier.fillMaxWidth(),
                                    horizontalArrangement = Arrangement.SpaceBetween,
                                    verticalAlignment = Alignment.Top
                                ) {

                                    Text(
                                        modifier = Modifier.weight(1f).padding(end = 8.dp).alpha(0.7f),
                                        text = gru.title,
                                        style = MaterialTheme.typography.titleMedium
                                    )

                                    Text(
                                        modifier = Modifier.wrapContentWidth().alpha(0.35f),
                                        text = "提及次数: ${gru.referCount}",
                                        style = MaterialTheme.typography.labelSmall
                                    )

                                }


                                Row(
                                    modifier = Modifier.fillMaxWidth(),
                                    horizontalArrangement = Arrangement.SpaceBetween,
                                    verticalAlignment = Alignment.Top
                                ) {

                                    FlowRow(
                                        modifier = Modifier.weight(1f).padding(end = 8.dp),
                                        horizontalArrangement = Arrangement.spacedBy(6.dp),
                                        verticalArrangement = Arrangement.spacedBy(6.dp),
                                    ) {
                                        for (obj in gru.objs) {
                                            Box(
                                                modifier = Modifier
                                                    .border(
                                                        width = 1.dp,
                                                        color = MaterialTheme.colorScheme.primaryContainer,
                                                        shape = RoundedCornerShape(6.dp)
                                                    )
                                                    .padding(vertical = 3.dp, horizontal = 5.dp),
                                            ) {
                                                Text(
                                                    text = obj.name,
                                                    color = MaterialTheme.colorScheme.onPrimaryContainer,
                                                    style = MaterialTheme.typography.labelSmall
                                                )
                                            }
                                        }

                                        for (tag in gru.tags) {
                                            Box(
                                                modifier = Modifier
                                                    .border(
                                                        width = 1.dp,
                                                        color = MaterialTheme.colorScheme.primaryContainer,
                                                        shape = RoundedCornerShape(6.dp)
                                                    )
                                                    .padding(vertical = 3.dp, horizontal = 5.dp),
                                            ) {
                                                Text(
                                                    text = tag.name,
                                                    color = MaterialTheme.colorScheme.onPrimaryContainer,
                                                    style = MaterialTheme.typography.labelSmall
                                                )
                                            }
                                        }
                                    }

                                    if (!isEmptyTagObj) {
                                        CardIcons(mainColor, gru.level)
                                    }
                                }

                                Row(
                                    modifier = Modifier.fillMaxWidth(),
                                    horizontalArrangement = Arrangement.SpaceBetween,
                                    verticalAlignment = Alignment.Top
                                ) {

                                    Text(
                                        modifier = Modifier.wrapContentWidth().alpha(0.35f),
                                        text = gru.description,
                                        style = MaterialTheme.typography.labelSmall
                                    )

                                    if (isEmptyTagObj) {
                                        CardIcons(mainColor, gru.level)
                                    }
                                }


                                Row(
                                    modifier = Modifier.fillMaxWidth(),
                                    horizontalArrangement = Arrangement.SpaceBetween,
                                    verticalAlignment = Alignment.CenterVertically,
                                ) {

                                    Text(
                                        modifier = Modifier.wrapContentWidth().alpha(0.35f),
                                        text = formatTimestamp(gru.createTime),
                                        style = MaterialTheme.typography.labelSmall
                                    )

                                    Row(
                                        horizontalArrangement = Arrangement.End,
                                        verticalAlignment = Alignment.CenterVertically,
                                    ) {

                                        Button(
                                            modifier = Modifier.height(24.dp),
                                            contentPadding = PaddingValues(0.dp),
                                            onClick = {
                                            },
                                            colors = ButtonDefaults.buttonColors().copy(
                                                containerColor = MaterialTheme.colorScheme.secondaryContainer,
                                                contentColor = MaterialTheme.colorScheme.onSecondaryContainer,
                                            ),
                                            shape = RoundedCornerShape(6.dp),
                                        ) {
                                            Text(
                                                text = "编辑",
                                                style = MaterialTheme.typography.labelSmall
                                            )
                                        }


                                        Button(
                                            modifier = Modifier.padding(horizontal = 6.dp).height(24.dp),
                                            contentPadding = PaddingValues(0.dp),
                                            onClick = {
                                                addGruRef(
                                                    globalDataModel = globalDataModel,
                                                    dataStorageManager = dataStorageManager,
                                                    id = gru.id,
                                                )
                                            },
                                            colors = ButtonDefaults.buttonColors().copy(
                                                containerColor = MaterialTheme.colorScheme.tertiaryContainer,
                                                contentColor = MaterialTheme.colorScheme.onTertiaryContainer,
                                            ),
                                            shape = RoundedCornerShape(6.dp),
                                        ) {
                                            Text(
                                                text = "再次提及",
                                                style = MaterialTheme.typography.labelSmall
                                            )
                                        }


                                        Button(
                                            modifier = Modifier.height(24.dp),
                                            contentPadding = PaddingValues(0.dp),
                                            onClick = {
                                                currentDeleteGru = gru
                                                deleteGruDialog = true
                                            },
                                            colors = ButtonDefaults.buttonColors().copy(
                                                containerColor = MaterialTheme.colorScheme.errorContainer,
                                                contentColor = MaterialTheme.colorScheme.onErrorContainer,
                                            ),
                                            shape = RoundedCornerShape(6.dp),
                                        ) {
                                            Text(
                                                text = "已报仇",
                                                style = MaterialTheme.typography.labelSmall
                                            )
                                        }
                                    }

                                }

                            }


                        }
                    }
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
                modifier = Modifier.align(Alignment.BottomEnd).padding(end = 16.dp, bottom = 16.dp)
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
                    openNewTagDialog = { openNewTagDialog = true },
                    clearStatus = {
                        newGTitleState.clearText()
                        newGDescState.clearText()
                        newGSliderPosition = 1f
                        globalDataModel.clearObjSelected()
                        globalDataModel.clearTagSelected()
                    }
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

            // delete
            if (deleteGruDialog) {
                SystemConfirm(
                    title = "是否不再对【${currentDeleteGru.title}】记仇",
                    onConfirmRequest = {
                        deleteGru(
                            globalDataModel = globalDataModel,
                            dataStorageManager = dataStorageManager,
                            id = currentDeleteGru.id,
                        )
                    },
                    onDismissRequest = { deleteGruDialog = false },
                )
            }


        }
    }


}


@Composable
fun CardIcons(
    color: Color,
    level: Int
) {
    Row(
        modifier = Modifier.wrapContentWidth(),
        verticalAlignment = Alignment.CenterVertically,
    ) {
        Icon(
            imageVector = vectorResource(Res.drawable.trident),
            contentDescription = null,
            modifier = Modifier.size(24.dp),
            tint = color,
        )
        Text(
            text = "X $level",
            color = color,
            style = MaterialTheme.typography.bodySmall
        )
    }
}