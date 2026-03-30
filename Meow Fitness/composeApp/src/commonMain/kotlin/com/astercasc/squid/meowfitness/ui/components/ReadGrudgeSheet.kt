package com.astercasc.squid.meowfitness.ui.components

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.foundation.text.input.*
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Done
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.alpha
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.unit.dp
import cafe.adriel.voyager.navigator.LocalNavigator
import cafe.adriel.voyager.navigator.currentOrThrow
import com.astercasc.squid.meowfitness.data.model.GlobalDataModel
import com.astercasc.squid.meowfitness.ui.ReadGrudgeObj
import kotlinx.coroutines.launch
import org.jetbrains.compose.resources.stringResource
import org.koin.compose.koinInject
import meowfitness.composeapp.generated.resources.*

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun ReadGrudgeSheet(
    searchSheetState: SheetState,
    searchKeyState: TextFieldState,
    searchLevelMin: TextFieldState,
    searchLevelMax: TextFieldState,
    searchReferMin: TextFieldState,
    searchReferMax: TextFieldState,
    closeSheet: () -> Unit,
) {
    //todo 升堂 ~~~~~ 清汤大老爷 质询模式开启！

    // inject
    val globalDataModel: GlobalDataModel = koinInject()
    val navigator = LocalNavigator.currentOrThrow
    val scope = rememberCoroutineScope()

    ModalBottomSheet(
        shape = RoundedCornerShape(6.dp, 6.dp, 0.dp, 0.dp),
        onDismissRequest = closeSheet, sheetState = searchSheetState,
        containerColor = BottomSheetDefaults.ContainerColor.copy(
            alpha = 0.92f,
        ),
    ) {
        // todo 这里可能触发 ModalBottomSheet 的滚动，也可能触发 Column 的，所以最好是再做一个页面
        Column(
            modifier = Modifier.fillMaxWidth().padding(start = 10.dp, end = 10.dp, bottom = 10.dp)
                .verticalScroll(rememberScrollState()).background(Color.Transparent),
            verticalArrangement = Arrangement.spacedBy(16.dp),
        ) {
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.Center,
            ) {
                Text(
                    modifier = Modifier.alpha(0.7f),
                    text = stringResource(Res.string.search_gru_title),
                    style = MaterialTheme.typography.titleLarge,
                )
            }


            // important 这里 OutlinedTextField 默认的样式太大了，使用 MaterialTheme 修改降级
            MaterialTheme(
                typography = MaterialTheme.typography.copy(
                    bodyLarge = MaterialTheme.typography.bodyMedium
                )
            ) {
                Column(
                    modifier = Modifier.fillMaxWidth(), verticalArrangement = Arrangement.spacedBy(4.dp)
                ) {
                    OutlinedTextField(
                        modifier = Modifier.fillMaxWidth().height(58.dp),
                        state = searchKeyState,
                        lineLimits = TextFieldLineLimits.SingleLine,
                        label = { Text(stringResource(Res.string.search_gru_keyword)) },
                        placeholder = {
                            Text(
                                modifier = Modifier.alpha(0.35f),
                                text = stringResource(Res.string.search_gru_keyword_placeholder)
                            )
                        },
                        shape = RoundedCornerShape(6.dp),
                    )
                }
            }

            Column(
                modifier = Modifier.fillMaxWidth(), verticalArrangement = Arrangement.spacedBy(6.dp)
            ) {
                Text(
                    stringResource(Res.string.search_gru_objects),
                    style = MaterialTheme.typography.bodyLarge
                )

                FlowRow(
                    horizontalArrangement = Arrangement.spacedBy(6.dp), verticalArrangement = Arrangement.spacedBy(6.dp)
                ) {

                    val objList = globalDataModel.objList.collectAsState().value
                    val objSearchList = globalDataModel.objListSearch.collectAsState().value

                    for (obj in objList) {
                        FilterChip(
                            modifier = Modifier.height(28.dp),
                            selected = objSearchList.contains(obj.id),
                            leadingIcon = if (objSearchList.contains(obj.id)) {
                                {
                                    Icon(
                                        imageVector = Icons.Filled.Done,
                                        contentDescription = "Selected",
                                        modifier = Modifier.size(FilterChipDefaults.IconSize)
                                    )
                                }
                            } else {
                                null
                            },
                            onClick = {
                                globalDataModel.toggleObjSearch(obj.id)
                            },
                            label = {
                                Text(obj.name, modifier = Modifier.padding(vertical = 0.dp))
                            },
                            shape = RoundedCornerShape(6.dp),
                        )
                    }

                }
            }


            Column(
                modifier = Modifier.fillMaxWidth(), verticalArrangement = Arrangement.spacedBy(6.dp)
            ) {
                Text(
                    stringResource(Res.string.search_gru_tags),
                    style = MaterialTheme.typography.bodyLarge
                )

                FlowRow(
                    horizontalArrangement = Arrangement.spacedBy(6.dp), verticalArrangement = Arrangement.spacedBy(6.dp)
                ) {

                    val tagList = globalDataModel.tagList.collectAsState().value
                    val tagSearchList = globalDataModel.tagListSearch.collectAsState().value

                    for (tag in tagList) {
                        FilterChip(
                            modifier = Modifier.height(28.dp),
                            selected = tagSearchList.contains(tag.id),
                            leadingIcon = if (tagSearchList.contains(tag.id)) {
                                {
                                    Icon(
                                        imageVector = Icons.Filled.Done,
                                        contentDescription = "Selected",
                                        modifier = Modifier.size(FilterChipDefaults.IconSize)
                                    )
                                }
                            } else {
                                null
                            },
                            onClick = {
                                globalDataModel.toggleTagSearch(tag.id)
                            },
                            label = {
                                Text(tag.name, modifier = Modifier.padding(vertical = 0.dp))
                            },
                            shape = RoundedCornerShape(6.dp),
                        )
                    }

                }
            }


            Column(
                modifier = Modifier.fillMaxWidth(),
            ) {
                Text(stringResource(Res.string.search_gru_level), style = MaterialTheme.typography.bodyLarge)

                MaterialTheme(
                    typography = MaterialTheme.typography.copy(
                        bodyLarge = MaterialTheme.typography.bodyMedium
                    )
                ) {
                    Row(
                        horizontalArrangement = Arrangement.spacedBy(12.dp),
                    ) {
                        OutlinedTextField(
                            modifier = Modifier.fillMaxWidth().height(58.dp).weight(1f),
                            state = searchLevelMin,
                            keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Number),
                            inputTransformation = numericInputTransformation().then(InputTransformation.maxLength(2)),
                            lineLimits = TextFieldLineLimits.SingleLine,
                            label = { Text(stringResource(Res.string.search_gru_level_min)) },
                            shape = RoundedCornerShape(6.dp),
                        )

                        OutlinedTextField(
                            modifier = Modifier.fillMaxWidth().height(58.dp).weight(1f),
                            state = searchLevelMax,
                            keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Number),
                            inputTransformation = numericInputTransformation().then(InputTransformation.maxLength(2)),
                            lineLimits = TextFieldLineLimits.SingleLine,
                            label = { Text(stringResource(Res.string.search_gru_level_max)) },
                            shape = RoundedCornerShape(6.dp),
                        )
                    }
                }

            }




            Column(
                modifier = Modifier.fillMaxWidth(),
            ) {
                Text(
                    stringResource(Res.string.search_gru_refer_count),
                    style = MaterialTheme.typography.bodyLarge
                )

                MaterialTheme(
                    typography = MaterialTheme.typography.copy(
                        bodyLarge = MaterialTheme.typography.bodyMedium
                    )
                ) {
                    Row(
                        horizontalArrangement = Arrangement.spacedBy(12.dp),
                    ) {
                        OutlinedTextField(
                            modifier = Modifier.fillMaxWidth().height(58.dp).weight(1f),
                            state = searchReferMin,
                            keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Number),
                            inputTransformation = numericInputTransformation().then(InputTransformation.maxLength(4)),
                            lineLimits = TextFieldLineLimits.SingleLine,
                            label = { Text(stringResource(Res.string.search_gru_refer_count_min)) },
                            shape = RoundedCornerShape(6.dp),
                        )

                        OutlinedTextField(
                            modifier = Modifier.fillMaxWidth().height(58.dp).weight(1f),
                            state = searchReferMax,
                            keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Number),
                            inputTransformation = numericInputTransformation().then(InputTransformation.maxLength(4)),
                            lineLimits = TextFieldLineLimits.SingleLine,
                            label = { Text(stringResource(Res.string.search_gru_refer_count_max)) },
                            shape = RoundedCornerShape(6.dp),
                        )
                    }
                }

            }




            Row(
                modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(8.dp)
            ) {

                Button(
                    modifier = Modifier.weight(1f),
                    onClick = {
                        scope.launch {
                            // operation
                            globalDataModel.updateParams(
                                keyword = searchKeyState.text.toString(),
                                minLevel = searchLevelMin.text.toString(),
                                maxLevel = searchLevelMax.text.toString(),
                                minRefer = searchReferMin.text.toString(),
                                maxRefer = searchReferMax.text.toString(),
                            )
                            globalDataModel.startSearch()
                            // hide
                            searchSheetState.hide()
                        }.invokeOnCompletion {
                            if (!searchSheetState.isVisible) {
                                closeSheet()
                            }
                        }
                    },
                    shape = RoundedCornerShape(6.dp),
                ) {
                    Text(stringResource(Res.string.search_gru_for_list))
                }


                Button(
                    modifier = Modifier.weight(1f),
                    onClick = {
                        scope.launch {
                            // operation
                            globalDataModel.updateParams(
                                keyword = searchKeyState.text.toString(),
                                minLevel = searchLevelMin.text.toString(),
                                maxLevel = searchLevelMax.text.toString(),
                                minRefer = searchReferMin.text.toString(),
                                maxRefer = searchReferMax.text.toString(),
                            )
                            // hide
                            searchSheetState.hide()
                        }.invokeOnCompletion {
                            if (!searchSheetState.isVisible) {
                                closeSheet()
                            }
                            globalDataModel.resetSingleViewForGrudge(false)
                            navigator.push(ReadGrudgeObj)
                        }
                    },
                    shape = RoundedCornerShape(6.dp),
                ) {
                    Text(stringResource(Res.string.search_gru_for_alone))
                }

                OutlinedButton(
                    modifier = Modifier.weight(1f),
                    onClick = {
                        scope.launch {
                            //operation
                            searchKeyState.clearText()
                            searchLevelMin.clearText()
                            searchLevelMax.clearText()
                            searchReferMin.clearText()
                            searchReferMax.clearText()
                            globalDataModel.clearObjSearch()
                            globalDataModel.clearTagSearch()
                            globalDataModel.stopSearch()
                            //hide
                            searchSheetState.hide()
                        }.invokeOnCompletion {
                            if (!searchSheetState.isVisible) {
                                closeSheet()
                            }
                        }
                    },
                    shape = RoundedCornerShape(6.dp),
                ) {
                    Text(stringResource(Res.string.search_gru_for_cancel))
                }
            }





        }
    }
}

fun numericInputTransformation() = InputTransformation {
    val filtered = this.asCharSequence().filter { ch -> ch.isDigit() }
    replace(0, length, filtered)
}