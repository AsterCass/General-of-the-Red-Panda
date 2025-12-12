package com.astercasc.squid.thebookofgrudges.ui.components

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
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.unit.dp
import com.astercasc.squid.thebookofgrudges.data.model.GlobalDataModel
import kotlinx.coroutines.launch
import org.koin.compose.koinInject

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
    val scope = rememberCoroutineScope()

    ModalBottomSheet(
        shape = RoundedCornerShape(6.dp, 6.dp, 0.dp, 0.dp),
        onDismissRequest = closeSheet, sheetState = searchSheetState
    ) {
        Column(
            modifier = Modifier.fillMaxWidth().padding(start = 10.dp, end = 10.dp, bottom = 10.dp)
                .verticalScroll(rememberScrollState()),
            verticalArrangement = Arrangement.spacedBy(16.dp),
        ) {
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.Center,
            ) {
                Text(
                    modifier = Modifier.alpha(0.7f),
                    text = "记仇条目检索",
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
                        label = { Text("关键词") },
                        placeholder = { Text("标题/描述") },
                        shape = RoundedCornerShape(6.dp),
                    )
                }
            }

            Column(
                modifier = Modifier.fillMaxWidth(), verticalArrangement = Arrangement.spacedBy(6.dp)
            ) {
                Text("记仇对象筛选：", style = MaterialTheme.typography.bodyLarge)

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
                                        contentDescription = "Done icon",
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
                Text("记仇标签筛选：", style = MaterialTheme.typography.bodyLarge)

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
                                        contentDescription = "Done icon",
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
                Text("记仇等级检索区间：", style = MaterialTheme.typography.bodyLarge)

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
                            label = { Text("最小值") },
                            placeholder = { Text("检索记仇等级最小值") },
                            shape = RoundedCornerShape(6.dp),
                        )

                        OutlinedTextField(
                            modifier = Modifier.fillMaxWidth().height(58.dp).weight(1f),
                            state = searchLevelMax,
                            keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Number),
                            inputTransformation = numericInputTransformation().then(InputTransformation.maxLength(2)),
                            lineLimits = TextFieldLineLimits.SingleLine,
                            label = { Text("最大值") },
                            placeholder = { Text("检索记仇等级最大值") },
                            shape = RoundedCornerShape(6.dp),
                        )
                    }
                }

            }




            Column(
                modifier = Modifier.fillMaxWidth(),
            ) {
                Text("提及次数检索区间：", style = MaterialTheme.typography.bodyLarge)

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
                            label = { Text("最小值") },
                            placeholder = { Text("提及次数最小值") },
                            shape = RoundedCornerShape(6.dp),
                        )

                        OutlinedTextField(
                            modifier = Modifier.fillMaxWidth().height(58.dp).weight(1f),
                            state = searchReferMax,
                            keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Number),
                            inputTransformation = numericInputTransformation().then(InputTransformation.maxLength(4)),
                            lineLimits = TextFieldLineLimits.SingleLine,
                            label = { Text("最大值") },
                            placeholder = { Text("提及次数最大值") },
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
                    Text("列表展示")
                }


                Button(
                    modifier = Modifier.weight(1f),
                    onClick = {
                        scope.launch {
                            // operation
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
                    Text("升堂细数")
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
                    Text("先放一马")
                }
            }





        }
    }
}

fun numericInputTransformation() = InputTransformation {
    val filtered = this.asCharSequence().filter { ch -> ch.isDigit() }
    replace(0, length, filtered)
}