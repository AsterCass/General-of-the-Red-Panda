package com.astercasc.squid.thebookofgrudges.ui

import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.isSystemInDarkTheme
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
import com.astercasc.squid.thebookofgrudges.data.*
import com.astercasc.squid.thebookofgrudges.data.model.GlobalDataModel
import com.astercasc.squid.thebookofgrudges.ui.components.*
import com.astercasc.squid.thebookofgrudges.utils.LocalBgBrush
import com.astercasc.squid.thebookofgrudges.utils.formatTimestamp
import com.astercasc.squid.thebookofgrudges.utils.interColorRange
import kotlinx.coroutines.launch
import org.jetbrains.compose.resources.stringResource
import org.jetbrains.compose.resources.vectorResource
import org.koin.compose.koinInject
import thebookofgrudges.composeapp.generated.resources.*

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
    val scope = rememberCoroutineScope()
    val isDark = isSystemInDarkTheme()
    // read sheet
    var showReadGrudgeSheet by rememberSaveable { mutableStateOf(false) }
    val searchSheetState = rememberModalBottomSheetState(
        skipPartiallyExpanded = true
    )
    val searchKeyState = rememberTextFieldState("")
    val searchLevelMin = rememberTextFieldState("")
    val searchLevelMax = rememberTextFieldState("")
    val searchReferMin = rememberTextFieldState("")
    val searchReferMax = rememberTextFieldState("")
    val gruIdListSelected = globalDataModel.gruIdListSelected.collectAsState().value
    val gruSearch = globalDataModel.gruSearch.collectAsState().value
    // new sheet
    var newGruSheetShow by rememberSaveable { mutableStateOf(false) }
    val newGruSheetState = rememberModalBottomSheetState(
        skipPartiallyExpanded = true
    )
    val newGTitleState = rememberTextFieldState("")
    val newGDescState = rememberTextFieldState("")
    var newGSliderPosition by rememberSaveable {
        mutableFloatStateOf(1f)
    }
    // edit sheet
    var editGru by remember { mutableStateOf(GrudgeCell()) }
    var editGruSheetShow by rememberSaveable { mutableStateOf(false) }
    val editGruSheetState = rememberModalBottomSheetState(
        skipPartiallyExpanded = true
    )
    val editGTitleState = rememberTextFieldState("")
    val editGDescState = rememberTextFieldState("")
    var editGSliderPosition by rememberSaveable {
        mutableFloatStateOf(1f)
    }
    // new tag & obj 这里对话框展示状态不用在重组之后保留
    var openNewObjDialog by remember { mutableStateOf(false) }
    var openNewTagDialog by remember { mutableStateOf(false) }
    var deleteGruDialog by remember { mutableStateOf(false) }
    var errorDialogText by remember { mutableStateOf("") }
    // gru data
    val gruList = globalDataModel.gruList.collectAsState().value
    var currentDeleteGru by remember { mutableStateOf(GrudgeCell()) }
    //text
    val errorDialogTextRes = stringResource(Res.string.error_gru_title_empty)

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

                for (gru in gruList) {

                    if (gruSearch && !gruIdListSelected.contains(gru.id)) {
                        continue
                    }

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
                            colors = CardDefaults.outlinedCardColors().copy(
                                containerColor = CardDefaults.outlinedCardColors().containerColor.copy(alpha = 0.92f),
                            ),
                        ) {


                            Column(
                                modifier = Modifier.fillMaxWidth().background(Color.Transparent)
                                    .padding(12.dp),
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
                                                    .padding(vertical = 3.dp, horizontal = 6.dp),
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
                                                    .padding(vertical = 3.dp, horizontal = 6.dp),
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
                                                editGru = gru
                                                editGTitleState.edit {
                                                    replace(0, length, editGru.title)
                                                }
                                                editGDescState.edit {
                                                    replace(0, length, editGru.description)
                                                }
                                                editGSliderPosition = editGru.level.toFloat()
                                                globalDataModel.resetTagSelectedEdit(editGru.tags)
                                                globalDataModel.resetObjSelectedEdit(editGru.objs)
                                                editGruSheetShow = true
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
                onClick = { newGruSheetShow = true },
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
                        contentDescription = stringResource(Res.string.add_gru)
                    )
                    Text(stringResource(Res.string.add_gru))
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
                    contentDescription = stringResource(Res.string.read_gru_title),
                )

            }



            // newGrudge
            if (newGruSheetShow) {
                NewEditGrudgeSheet(
                    isNew = true,
                    gruTitleState = newGTitleState,
                    gruDescState = newGDescState,
                    gruSliderPosition = newGSliderPosition,
                    closeSheet = { newGruSheetShow = false },
                    gruSheetState = newGruSheetState,
                    updateSliderPosition = { newGSliderPosition = it },
                    openNewObjDialog = { openNewObjDialog = true },
                    openNewTagDialog = { openNewTagDialog = true },
                ) {
                    Row(
                        modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(8.dp)
                    ) {

                        Button(
                            modifier = Modifier.weight(1f),
                            onClick = {
                                if (newGTitleState.text.isEmpty()) {
                                    errorDialogText = errorDialogTextRes
                                    return@Button
                                }
                                scope.launch {
                                    //new
                                    addNewGru(
                                        globalDataModel = globalDataModel,
                                        dataStorageManager = dataStorageManager,
                                        title = newGTitleState.text.toString(),
                                        description = newGDescState.text.toString(),
                                        level = newGSliderPosition.toInt(),
                                    )
                                    //clear status
                                    newGTitleState.clearText()
                                    newGDescState.clearText()
                                    newGSliderPosition = 1f
                                    globalDataModel.clearObjSelectedNew()
                                    globalDataModel.clearTagSelectedNew()
                                    // hide
                                    newGruSheetState.hide()
                                }.invokeOnCompletion {
                                    if (!newGruSheetState.isVisible) {
                                        newGruSheetShow = false
                                    }
                                }
                            },
                            shape = RoundedCornerShape(6.dp),
                        ) {
                            Text("开始卧薪尝胆")
                        }

                        OutlinedButton(
                            modifier = Modifier.weight(1f),
                            onClick = {
                                scope.launch { newGruSheetState.hide() }.invokeOnCompletion {
                                    if (!newGruSheetState.isVisible) {
                                        newGruSheetShow = false
                                    }
                                }
                            },
                            shape = RoundedCornerShape(6.dp),
                        ) {
                            Text("算了，先放Ta一马")
                        }
                    }
                }
            }


            // editGrudge
            if (editGruSheetShow) {
                NewEditGrudgeSheet(
                    isNew = false,
                    gruTitleState = editGTitleState,
                    gruDescState = editGDescState,
                    gruSliderPosition = editGSliderPosition,
                    closeSheet = { editGruSheetShow = false },
                    gruSheetState = editGruSheetState,
                    updateSliderPosition = { editGSliderPosition = it },
                    openNewObjDialog = { openNewObjDialog = true },
                    openNewTagDialog = { openNewTagDialog = true },
                ) {
                    Row(
                        modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(8.dp)
                    ) {

                        Button(
                            modifier = Modifier.weight(1f),
                            onClick = {
                                if (editGTitleState.text.isEmpty()) {
                                    errorDialogText = errorDialogTextRes
                                    return@Button
                                }
                                scope.launch {
                                    //edit
                                    editGru(
                                        globalDataModel = globalDataModel,
                                        dataStorageManager = dataStorageManager,
                                        title = editGTitleState.text.toString(),
                                        description = editGDescState.text.toString(),
                                        level = editGSliderPosition.toInt(),
                                        editGru = editGru,
                                    )
                                    // hide
                                    editGruSheetState.hide()
                                }.invokeOnCompletion {
                                    if (!editGruSheetState.isVisible) {
                                        editGruSheetShow = false
                                    }
                                }
                            },
                            shape = RoundedCornerShape(6.dp),
                        ) {
                            Text("确定保存")
                        }

                        OutlinedButton(
                            modifier = Modifier.weight(1f),
                            onClick = {
                                scope.launch { editGruSheetState.hide() }.invokeOnCompletion {
                                    if (!editGruSheetState.isVisible) {
                                        editGruSheetShow = false
                                    }
                                }
                            },
                            shape = RoundedCornerShape(6.dp),
                        ) {
                            Text("放弃")
                        }
                    }
                }
            }


            // readSheet
            if (showReadGrudgeSheet) {
                ReadGrudgeSheet(
                    searchSheetState = searchSheetState,
                    searchKeyState = searchKeyState,
                    searchLevelMin = searchLevelMin,
                    searchLevelMax = searchLevelMax,
                    searchReferMin = searchReferMin,
                    searchReferMax = searchReferMax,
                    closeSheet = { showReadGrudgeSheet = false },
                )
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

            // error
            if (!errorDialogText.isEmpty()) {
                SystemConfirm(
                    title = errorDialogText,
                    onDismissRequest = { errorDialogText = "" },
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