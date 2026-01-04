package com.astercasc.squid.thebookofgrudges.ui

import androidx.compose.foundation.background
import androidx.compose.foundation.isSystemInDarkTheme
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.pager.HorizontalPager
import androidx.compose.foundation.pager.rememberPagerState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.alpha
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.unit.dp
import cafe.adriel.voyager.core.screen.Screen
import cafe.adriel.voyager.core.screen.ScreenKey
import cafe.adriel.voyager.core.screen.uniqueScreenKey
import cafe.adriel.voyager.navigator.LocalNavigator
import cafe.adriel.voyager.navigator.currentOrThrow
import com.astercasc.squid.thebookofgrudges.constant.GRUDGE_LEVEL_MAX
import com.astercasc.squid.thebookofgrudges.constant.GRUDGE_LEVEL_MAX_COLOR
import com.astercasc.squid.thebookofgrudges.constant.GRUDGE_LEVEL_MIN
import com.astercasc.squid.thebookofgrudges.constant.GRUDGE_LEVEL_MIN_COLOR
import com.astercasc.squid.thebookofgrudges.constant.enums.ViewEnum
import com.astercasc.squid.thebookofgrudges.data.DataStorageManager
import com.astercasc.squid.thebookofgrudges.data.addGruRef
import com.astercasc.squid.thebookofgrudges.data.deleteGru
import com.astercasc.squid.thebookofgrudges.data.model.GlobalDataModel
import com.astercasc.squid.thebookofgrudges.ui.components.MainAppBar
import com.astercasc.squid.thebookofgrudges.ui.components.SystemConfirm
import com.astercasc.squid.thebookofgrudges.utils.LocalBgBrush
import com.astercasc.squid.thebookofgrudges.utils.formatTimestamp
import com.astercasc.squid.thebookofgrudges.utils.interColorRange
import kotlinx.coroutines.launch
import org.jetbrains.compose.resources.stringResource
import org.jetbrains.compose.resources.vectorResource
import org.koin.compose.koinInject
import thebookofgrudges.composeapp.generated.resources.*

object ReadGrudgeObj : Screen {

    override val key: ScreenKey = "${ViewEnum.READ_GRU.code}$uniqueScreenKey"

    @Composable
    override fun Content() {
        ReadGrudge()
    }

}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun ReadGrudge() {

    // inject
    val globalDataModel: GlobalDataModel = koinInject()
    val dataStorageManager: DataStorageManager = koinInject()
    val scope = rememberCoroutineScope()
    val isDark = isSystemInDarkTheme()
    val navigator = LocalNavigator.currentOrThrow
    // is single view for read grudge
    val singleViewForGrudge = globalDataModel.singleViewForGrudge.collectAsState().value
    // search data
    val gruIdListSelected = globalDataModel.gruIdListSelected.collectAsState().value
    // gru data
    val gruList = globalDataModel.gruList.collectAsState().value
    val gruIdMap = gruList.associateBy { it.id }
    val pagerState = rememberPagerState(pageCount = {
        gruIdListSelected.size
    })
    var deleteGruDialog by remember { mutableStateOf(false) }
    Scaffold(
        topBar = {
            MainAppBar(stringResource(Res.string.read_gru_title))
        }, bottomBar = {}, floatingActionButton = {}, floatingActionButtonPosition = FabPosition.Start
    ) { padding ->


        Box(
            modifier = Modifier.fillMaxSize().padding(padding)
                .then(if (isDark) Modifier else Modifier.background(brush = LocalBgBrush.current))
        ) {


            HorizontalPager(
                state = pagerState, verticalAlignment = Alignment.Top
            ) { page ->

                // grudge
                val gru = gruIdMap[gruIdListSelected[page]] ?: return@HorizontalPager

                // color
                val mainColor = interColorRange(
                    GRUDGE_LEVEL_MIN_COLOR,
                    GRUDGE_LEVEL_MAX_COLOR,
                    gru.level.toFloat(),
                    GRUDGE_LEVEL_MIN,
                    GRUDGE_LEVEL_MAX,
                )

                Column(
                    modifier = Modifier.padding(start = 12.dp, end = 12.dp, top = 18.dp, bottom = 12.dp).fillMaxWidth()
                ) {

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
                            modifier = Modifier.fillMaxWidth()
                                .background(Color.Transparent).padding(12.dp),
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
                                    style = MaterialTheme.typography.titleLarge
                                )

                                Text(
                                    modifier = Modifier.wrapContentWidth().alpha(0.35f),
                                    text = stringResource(Res.string.gru_refer_count) + " ${gru.referCount}",
                                    style = MaterialTheme.typography.labelMedium
                                )

                            }


                            FlowRow(
                                horizontalArrangement = Arrangement.spacedBy(6.dp),
                                verticalArrangement = Arrangement.spacedBy(6.dp),
                            ) {
                                for (obj in gru.objs) {
                                    Box(
                                        modifier = Modifier.clip(RoundedCornerShape(6.dp))
                                            .background(MaterialTheme.colorScheme.tertiaryContainer)
                                            .padding(vertical = 3.dp, horizontal = 6.dp),
                                    ) {
                                        Text(
                                            text = obj.name,
                                            color = MaterialTheme.colorScheme.onTertiaryContainer,
                                            style = MaterialTheme.typography.labelMedium
                                        )
                                    }
                                }

                                for (tag in gru.tags) {
                                    Box(
                                        modifier = Modifier.clip(RoundedCornerShape(6.dp))
                                            .background(MaterialTheme.colorScheme.secondaryContainer)
                                            .padding(vertical = 3.dp, horizontal = 6.dp),
                                    ) {
                                        Text(
                                            text = tag.name,
                                            color = MaterialTheme.colorScheme.onSecondaryContainer,
                                            style = MaterialTheme.typography.labelMedium
                                        )
                                    }
                                }

                            }


                            Text(
                                modifier = Modifier.alpha(0.35f),
                                text = gru.description,
                                style = MaterialTheme.typography.labelMedium
                            )

                            Row(
                                modifier = Modifier.fillMaxWidth(),
                                verticalAlignment = Alignment.CenterVertically,
                            ) {

                                Text(
                                    modifier = Modifier.alpha(0.35f),
                                    text = stringResource(Res.string.gru_level),
                                    style = MaterialTheme.typography.labelMedium
                                )

                                repeat(gru.level) { index ->
                                    Icon(
                                        imageVector = vectorResource(Res.drawable.trident),
                                        contentDescription = "Grudge level",
                                        modifier = Modifier.size(24.dp).offset(x = (index * -4).dp),
                                        tint = mainColor,
                                    )
                                }

                            }

                            HorizontalDivider(
                                modifier = Modifier.padding(vertical = 6.dp),
                            )


                            Row(
                                modifier = Modifier.fillMaxWidth(),
                                horizontalArrangement = Arrangement.SpaceBetween,
                                verticalAlignment = Alignment.CenterVertically,
                            ) {

                                Text(
                                    modifier = Modifier.alpha(0.35f),
                                    text = stringResource(Res.string.create_time) +
                                            ": ${formatTimestamp(gru.createTime)}",
                                    style = MaterialTheme.typography.labelSmall
                                )

                                Text(
                                    modifier = Modifier.alpha(0.35f),
                                    text = stringResource(Res.string.update_time) +
                                            ": ${formatTimestamp(gru.updateTime)}",
                                    style = MaterialTheme.typography.labelSmall
                                )

                            }


                        }


                    }

                    Spacer(Modifier.height(150.dp))

                }


            }


            val gru = gruIdMap[gruIdListSelected.getOrNull(pagerState.currentPage)] ?: return@Box

            if(!singleViewForGrudge) {
                SmallFloatingActionButton(
                    onClick = {
                        scope.launch {
                            pagerState.animateScrollToPage(pagerState.currentPage - 1)
                        }
                    },
                    shape = RoundedCornerShape(6.dp),
                    elevation = FloatingActionButtonDefaults.elevation(2.dp),
                    modifier = Modifier.align(Alignment.BottomStart).padding(start = 16.dp, bottom = 16.dp)
                ) {
                    Row(
                        modifier = Modifier.padding(vertical = 12.dp, horizontal = 12.dp),
                        verticalAlignment = Alignment.CenterVertically,
                        horizontalArrangement = Arrangement.spacedBy(8.dp)
                    ) {
                        Text(stringResource(Res.string.search_gru_pre))
                    }

                }
            }


            SmallFloatingActionButton(
                onClick = {
                    deleteGruDialog = true
                },
                shape = RoundedCornerShape(6.dp),
                elevation = FloatingActionButtonDefaults.elevation(2.dp),
                modifier = Modifier.align(Alignment.BottomEnd).padding(end = 16.dp,
                    bottom = if(singleViewForGrudge) 76.dp else 136.dp),
                containerColor = MaterialTheme.colorScheme.errorContainer,
                contentColor = MaterialTheme.colorScheme.onErrorContainer,
            ) {
                Row(
                    modifier = Modifier.padding(vertical = 12.dp, horizontal = 12.dp),
                    verticalAlignment = Alignment.CenterVertically,
                    horizontalArrangement = Arrangement.spacedBy(8.dp)
                ) {
                    Text(stringResource(Res.string.gru_done))
                }

            }

            SmallFloatingActionButton(
                onClick = {
                    addGruRef(
                        globalDataModel = globalDataModel,
                        dataStorageManager = dataStorageManager,
                        id = gru.id,
                    )
                },
                shape = RoundedCornerShape(6.dp),
                elevation = FloatingActionButtonDefaults.elevation(2.dp),
                modifier = Modifier.align(Alignment.BottomEnd).padding(end = 16.dp,
                    bottom = if(singleViewForGrudge) 16.dp else 76.dp)
            ) {
                Row(
                    modifier = Modifier.padding(vertical = 12.dp, horizontal = 12.dp),
                    verticalAlignment = Alignment.CenterVertically,
                    horizontalArrangement = Arrangement.spacedBy(8.dp)
                ) {
                    Text(stringResource(Res.string.search_gru_refer_count_plus))
                }

            }

            if(!singleViewForGrudge) {
                SmallFloatingActionButton(
                    onClick = {
                        scope.launch {
                            pagerState.animateScrollToPage(pagerState.currentPage + 1)
                        }
                    },
                    shape = RoundedCornerShape(6.dp),
                    elevation = FloatingActionButtonDefaults.elevation(2.dp),
                    modifier = Modifier.align(Alignment.BottomEnd).padding(end = 16.dp, bottom = 16.dp),
                ) {
                    Text(
                        modifier = Modifier.padding(vertical = 12.dp, horizontal = 12.dp),
                        text = stringResource(Res.string.search_gru_next)
                    )
                }
            }


            // delete
            if (deleteGruDialog) {
                SystemConfirm(
                    title = stringResource(Res.string.delete_gru_confirm) + "【${gru.title}】",
                    onConfirmRequest = {
                        deleteGru(
                            globalDataModel = globalDataModel,
                            dataStorageManager = dataStorageManager,
                            id = gru.id,
                        )
                        // 要么为空，要么就剩下马上要删除那一个id了，此时数据可能还没有刷新
                        if ((gruIdMap.isEmpty() || (gruIdMap.size == 1 && gruIdMap.containsKey(gru.id))) && navigator.canPop) {
                            navigator.pop()
                        }
                    },
                    onDismissRequest = { deleteGruDialog = false },
                )
            }




        }
    }


}

