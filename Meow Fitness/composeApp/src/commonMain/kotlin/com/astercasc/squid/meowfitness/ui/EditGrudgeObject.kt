package com.astercasc.squid.meowfitness.ui

import androidx.compose.foundation.background
import androidx.compose.foundation.isSystemInDarkTheme
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Add
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.alpha
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.unit.dp
import cafe.adriel.voyager.core.screen.Screen
import cafe.adriel.voyager.core.screen.ScreenKey
import cafe.adriel.voyager.core.screen.uniqueScreenKey
import com.astercasc.squid.meowfitness.constant.enums.ViewEnum
import com.astercasc.squid.meowfitness.data.DataStorageManager
import com.astercasc.squid.meowfitness.data.GrudgeObj
import com.astercasc.squid.meowfitness.data.deleteObj
import com.astercasc.squid.meowfitness.data.model.GlobalDataModel
import com.astercasc.squid.meowfitness.ui.components.MainAppBar
import com.astercasc.squid.meowfitness.ui.components.NewGrudgeObject
import com.astercasc.squid.meowfitness.ui.components.SystemConfirm
import com.astercasc.squid.meowfitness.utils.LocalBgBrush
import com.astercasc.squid.meowfitness.utils.formatTimestamp
import org.jetbrains.compose.resources.stringResource
import org.koin.compose.koinInject
import meowfitness.composeapp.generated.resources.*

object EditGrudgeObjectObj : Screen {

    override val key: ScreenKey = "${ViewEnum.EDIT_GRU_OBJ.code}$uniqueScreenKey"

    @Composable
    override fun Content() {
        EditGrudgeObject()
    }

}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun EditGrudgeObject() {

    Scaffold(
        topBar = {
            MainAppBar(stringResource(Res.string.edit_obj_title))
        }, bottomBar = {}, floatingActionButton = {}, floatingActionButtonPosition = FabPosition.Start
    ) { padding ->


        // inject
        val globalDataModel: GlobalDataModel = koinInject()
        val dataStorageManager: DataStorageManager = koinInject()
        val isDark = isSystemInDarkTheme()
        // new tag & obj 这里对话框展示状态不用在重组之后保留
        var openNewObjDialog by remember { mutableStateOf(false) }
        var deleteObjDialog by remember { mutableStateOf(false) }
        // obj data
        val objList = globalDataModel.objList.collectAsState().value
        var currentSelectObj by remember { mutableStateOf(GrudgeObj()) }

        Box(
            modifier = Modifier.fillMaxSize().padding(padding)
                .then(if (isDark) Modifier else Modifier.background(brush = LocalBgBrush.current))
        ) {


            LazyColumn(
                modifier = Modifier.padding(horizontal = 12.dp).fillMaxSize().background(Color.Transparent),
                verticalArrangement = Arrangement.spacedBy(8.dp)
            ) {

                item {
                    Spacer(Modifier.height(18.dp))
                }

                for (obj in objList) {
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
                            Row(
                                modifier = Modifier.fillMaxWidth().background(Color.Transparent).padding(12.dp),
                                horizontalArrangement = Arrangement.SpaceBetween,
                                verticalAlignment = Alignment.CenterVertically
                            ) {
                                Column(
                                    verticalArrangement = Arrangement.spacedBy(8.dp)
                                ) {
                                    Text(
                                        text = obj.name,
                                        style = MaterialTheme.typography.bodyMedium
                                    )
                                    Text(
                                        modifier = Modifier.alpha(0.35f),
                                        text = stringResource(Res.string.create_time) + " ${formatTimestamp(obj.createTime)}",
                                        style = MaterialTheme.typography.labelSmall
                                    )
                                }

                                Button(
                                    modifier = Modifier.height(24.dp),
                                    contentPadding = PaddingValues(0.dp),
                                    onClick = {
                                        currentSelectObj = obj
                                        deleteObjDialog = true
                                    },
                                    colors = ButtonDefaults.buttonColors().copy(
                                        containerColor = MaterialTheme.colorScheme.error,
                                        contentColor = MaterialTheme.colorScheme.onError,
                                    ),
                                    shape = RoundedCornerShape(6.dp),
                                ) {
                                    Text(
                                        text = stringResource(Res.string.system_delete),
                                        style = MaterialTheme.typography.labelSmall
                                    )
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
                onClick = { openNewObjDialog = true },
                shape = CircleShape,
                modifier = Modifier.align(Alignment.BottomEnd).padding(bottom = 16.dp, end = 16.dp)
            ) {
                Icon(
                    modifier = Modifier.padding(12.dp).size(25.dp),
                    imageVector = Icons.Filled.Add,
                    contentDescription = "Add Grudge Object",
                )

            }

            // newObj
            if (openNewObjDialog) {
                NewGrudgeObject(
                    onDismissRequest = { openNewObjDialog = false },
                )
            }

            // delete
            if (deleteObjDialog) {
                SystemConfirm(
                    title = stringResource(Res.string.delete_obj_title) + "【${currentSelectObj.name}】",
                    onConfirmRequest = {
                        deleteObj(globalDataModel, dataStorageManager, currentSelectObj.id)
                    },
                    onDismissRequest = { deleteObjDialog = false },
                )
            }

        }
    }


}

