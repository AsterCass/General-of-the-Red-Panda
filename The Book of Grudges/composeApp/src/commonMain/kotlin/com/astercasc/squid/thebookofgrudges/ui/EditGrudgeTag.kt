package com.astercasc.squid.thebookofgrudges.ui

import androidx.compose.foundation.background
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
import androidx.compose.ui.draw.paint
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.ColorFilter
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.unit.dp
import cafe.adriel.voyager.core.screen.Screen
import cafe.adriel.voyager.core.screen.ScreenKey
import cafe.adriel.voyager.core.screen.uniqueScreenKey
import com.astercasc.squid.thebookofgrudges.constant.enums.ViewEnum
import com.astercasc.squid.thebookofgrudges.data.DataStorageManager
import com.astercasc.squid.thebookofgrudges.data.GrudgeTag
import com.astercasc.squid.thebookofgrudges.data.deleteTag
import com.astercasc.squid.thebookofgrudges.data.model.GlobalDataModel
import com.astercasc.squid.thebookofgrudges.ui.components.MainAppBar
import com.astercasc.squid.thebookofgrudges.ui.components.NewGrudgeTag
import com.astercasc.squid.thebookofgrudges.ui.components.SystemConfirm
import com.astercasc.squid.thebookofgrudges.utils.LocalBgBrush
import com.astercasc.squid.thebookofgrudges.utils.formatTimestamp
import org.jetbrains.compose.resources.painterResource
import org.koin.compose.koinInject
import thebookofgrudges.composeapp.generated.resources.Res
import thebookofgrudges.composeapp.generated.resources.bg2

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
            MainAppBar("标签管理")
        }, bottomBar = {}, floatingActionButton = {}, floatingActionButtonPosition = FabPosition.Start
    ) { padding ->

        // inject
        val globalDataModel: GlobalDataModel = koinInject()
        val dataStorageManager: DataStorageManager = koinInject()
        // new tag & obj 这里对话框展示状态不用在重组之后保留
        var openNewTagDialog by remember { mutableStateOf(false) }
        var deleteTagDialog by remember { mutableStateOf(false) }
        // tag data
        val tagList = globalDataModel.tagList.collectAsState().value
        var currentSelectTag by remember { mutableStateOf(GrudgeTag()) }

        Box(
            modifier = Modifier.fillMaxSize().padding(padding)
                .background(
                    brush = LocalBgBrush.current
                )
                .paint(
                    painter = painterResource(Res.drawable.bg2),
                    contentScale = ContentScale.Crop,
                    colorFilter = ColorFilter.tint(MaterialTheme.colorScheme.primaryContainer),
                )
        ) {


            LazyColumn(
                modifier = Modifier
                    .padding(horizontal = 12.dp).fillMaxSize().background(Color.Transparent),
                verticalArrangement = Arrangement.spacedBy(8.dp)
            ) {
                item {
                    Spacer(Modifier.height(18.dp))
                }

                for (tag in tagList) {
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
                                modifier = Modifier.fillMaxWidth()
                                    .background(Color.Transparent).padding(12.dp),
                                horizontalArrangement = Arrangement.SpaceBetween,
                                verticalAlignment = Alignment.CenterVertically
                            ) {
                                Column(
                                    verticalArrangement = Arrangement.spacedBy(8.dp)
                                ) {
                                    Text(
                                        text = tag.name,
                                        style = MaterialTheme.typography.bodyMedium
                                    )
                                    Text(
                                        modifier = Modifier.alpha(0.35f),
                                        text = "创建时间 ${formatTimestamp(tag.createTime)}",
                                        style = MaterialTheme.typography.labelSmall
                                    )
                                }

                                Button(
                                    modifier = Modifier.height(24.dp),
                                    contentPadding = PaddingValues(0.dp),
                                    onClick = {
                                        currentSelectTag = tag
                                        deleteTagDialog = true
                                    },
                                    colors = ButtonDefaults.buttonColors().copy(
                                        containerColor = MaterialTheme.colorScheme.error,
                                        contentColor = MaterialTheme.colorScheme.onError,
                                    ),
                                    shape = RoundedCornerShape(6.dp),
                                ) {
                                    Text(
                                        text = "Delete",
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
                onClick = { openNewTagDialog = true },
                shape = CircleShape,
                modifier = Modifier.align(Alignment.BottomEnd).padding(bottom = 16.dp, end = 16.dp)
            ) {
                Icon(
                    modifier = Modifier.padding(12.dp).size(25.dp),
                    imageVector = Icons.Filled.Add,
                    contentDescription = "todo something"
                )

            }

            // newTag
            if (openNewTagDialog) {
                NewGrudgeTag(
                    onDismissRequest = { openNewTagDialog = false },
                )
            }

            // delete
            if (deleteTagDialog) {
                SystemConfirm(
                    title = "是否删除【${currentSelectTag.name}】标签",
                    onConfirmRequest = {
                        deleteTag(globalDataModel, dataStorageManager, currentSelectTag.id)
                    },
                    onDismissRequest = { deleteTagDialog = false },
                )
            }

        }
    }


}

