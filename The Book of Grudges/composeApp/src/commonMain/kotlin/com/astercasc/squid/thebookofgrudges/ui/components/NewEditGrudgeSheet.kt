package com.astercasc.squid.thebookofgrudges.ui.components

import androidx.compose.foundation.*
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.input.TextFieldLineLimits
import androidx.compose.foundation.text.input.TextFieldState
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.AddCircle
import androidx.compose.material.icons.filled.Done
import androidx.compose.material.icons.filled.Edit
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.alpha
import androidx.compose.ui.draw.clip
import androidx.compose.ui.geometry.CornerRadius
import androidx.compose.ui.geometry.Size
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.unit.dp
import cafe.adriel.voyager.navigator.LocalNavigator
import cafe.adriel.voyager.navigator.currentOrThrow
import com.astercasc.squid.thebookofgrudges.constant.GRUDGE_LEVEL_MAX
import com.astercasc.squid.thebookofgrudges.constant.GRUDGE_LEVEL_MAX_COLOR
import com.astercasc.squid.thebookofgrudges.constant.GRUDGE_LEVEL_MIN
import com.astercasc.squid.thebookofgrudges.constant.GRUDGE_LEVEL_MIN_COLOR
import com.astercasc.squid.thebookofgrudges.constant.enums.GrudgeLevelEnum
import com.astercasc.squid.thebookofgrudges.data.model.GlobalDataModel
import com.astercasc.squid.thebookofgrudges.ui.EditGrudgeObjectObj
import com.astercasc.squid.thebookofgrudges.ui.EditGrudgeTagObj
import com.astercasc.squid.thebookofgrudges.utils.getStringByName
import com.astercasc.squid.thebookofgrudges.utils.interColorRange
import kotlinx.coroutines.launch
import org.jetbrains.compose.resources.vectorResource
import org.koin.compose.koinInject
import thebookofgrudges.composeapp.generated.resources.Res
import thebookofgrudges.composeapp.generated.resources.devil

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun NewEditGrudgeSheet(
    newGTitleState: TextFieldState,
    newGDescState: TextFieldState,
    newGSliderPosition: Float,
    closeSheet: () -> Unit,
    newGruSheetState: SheetState,
    updateSliderPosition: (Float) -> Unit,
    openNewObjDialog: () -> Unit,
    openNewTagDialog: () -> Unit,
    operation: @Composable () -> Unit,
) {

    val globalDataModel: GlobalDataModel = koinInject()
    val navigator = LocalNavigator.currentOrThrow
    val scope = rememberCoroutineScope()


    ModalBottomSheet(
        shape = RoundedCornerShape(6.dp, 6.dp, 0.dp, 0.dp),
        onDismissRequest = closeSheet,
        sheetState = newGruSheetState,

    ) {
        // todo 这里可能触发 ModalBottomSheet 的滚动，也可能触发 Column 的，所以最好是再做一个页面
        Column(
            modifier = Modifier.fillMaxWidth().padding(horizontal = 10.dp).verticalScroll(rememberScrollState()),
            verticalArrangement = Arrangement.spacedBy(18.dp)
        ) {

            // important 这里 OutlinedTextField 默认的样式太大了，使用 MaterialTheme 修改降级
            MaterialTheme(
                typography = MaterialTheme.typography.copy(
                    bodyLarge = MaterialTheme.typography.bodyMedium
                )
            ) {
                Column(
                    modifier = Modifier.fillMaxWidth(),
                    verticalArrangement = Arrangement.spacedBy(4.dp)
                ) {
                    OutlinedTextField(
                        modifier = Modifier.fillMaxWidth().height(58.dp),
                        state = newGTitleState,
                        lineLimits = TextFieldLineLimits.SingleLine,
                        label = { Text("todo 记仇标题") },
                        placeholder = { Text("todo 标题占位符") },
                        shape = RoundedCornerShape(6.dp),
                    )

                    OutlinedTextField(
                        modifier = Modifier.fillMaxWidth().height(100.dp),
                        state = newGDescState,
                        lineLimits = TextFieldLineLimits.MultiLine(1, 3),
                        label = { Text("todo 记仇描述") },
                        placeholder = { Text("todo 描述占位符") },
                        shape = RoundedCornerShape(6.dp),
                    )
                }

            }

            Column(
                modifier = Modifier.fillMaxWidth(),
                verticalArrangement = Arrangement.spacedBy(6.dp)
            ) {

                Row(
                    modifier = Modifier.fillMaxWidth(),
                    verticalAlignment = Alignment.CenterVertically,
                ) {
                    Text("TODO 记仇对象：", style = MaterialTheme.typography.bodyLarge)

                    Box(
                        modifier = Modifier.size(22.dp)
                            .clip(RoundedCornerShape(6.dp))
                            .alpha(0.72f)
                            .clickable(onClick = {
                                scope
                                    .launch {
                                        newGruSheetState.hide()
                                    }
                                    .invokeOnCompletion {
                                        navigator.push(EditGrudgeObjectObj)
                                        // 这里不改变状态，用户回退时候自动再次拉起 sheet
//                                        if (!sheetState.isVisible) {
//                                            closeSheet()
//                                        }
                                    }
                            }),
                        contentAlignment = Alignment.Center

                    ) {
                        Icon(
                            modifier = Modifier.size(16.dp),
                            imageVector = Icons.Filled.Edit,
                            contentDescription = "todo something"
                        )
                    }
                }


                FlowRow(
                    horizontalArrangement = Arrangement.spacedBy(6.dp),
                    verticalArrangement = Arrangement.spacedBy(6.dp)
                ) {

                    val objList = globalDataModel.objList.collectAsState().value
                    val objListSelected = globalDataModel.objListSelected.collectAsState().value

                    for (obj in objList) {
                        FilterChip(
                            modifier = Modifier.height(28.dp),
                            selected = objListSelected.contains(obj),
                            leadingIcon = if (objListSelected.contains(obj)) {
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
                                globalDataModel.toggleObjSelected(obj)
                            },
                            label = {
                                Text(obj.name, modifier = Modifier.padding(vertical = 0.dp))
                            },
                            shape = RoundedCornerShape(6.dp),

                            )
                    }

                    Box(
                        modifier = Modifier.size(28.dp)
                            .clip(RoundedCornerShape(6.dp))
                            .alpha(0.72f)
                            .clickable(onClick = openNewObjDialog),
                        contentAlignment = Alignment.Center

                    ) {
                        Icon(
                            modifier = Modifier.size(22.dp),
                            imageVector = Icons.Filled.AddCircle,
                            contentDescription = "todo something"
                        )
                    }


                }
            }

            Column(
                modifier = Modifier.fillMaxWidth(),
                verticalArrangement = Arrangement.spacedBy(6.dp)
            ) {

                Row(
                    modifier = Modifier.fillMaxWidth(),
                    verticalAlignment = Alignment.CenterVertically,
                ) {
                    Text("TODO 记仇标签：", style = MaterialTheme.typography.bodyLarge)

                    Box(
                        modifier = Modifier.size(22.dp)
                            .clip(RoundedCornerShape(6.dp))
                            .alpha(0.72f)
                            .clickable(onClick = {
                                scope
                                    .launch {
                                        newGruSheetState.hide()
                                    }
                                    .invokeOnCompletion {
                                        navigator.push(EditGrudgeTagObj)
                                        // 这里不改变状态，用户回退时候自动再次拉起 sheet
//                                        if (!sheetState.isVisible) {
//                                            closeSheet()
//                                        }
                                    }

                            }),
                        contentAlignment = Alignment.Center

                    ) {
                        Icon(
                            modifier = Modifier.size(16.dp),
                            imageVector = Icons.Filled.Edit,
                            contentDescription = "todo something"
                        )
                    }
                }


                FlowRow(
                    horizontalArrangement = Arrangement.spacedBy(6.dp),
                    verticalArrangement = Arrangement.spacedBy(6.dp)
                ) {

                    val tagList = globalDataModel.tagList.collectAsState().value
                    val tagListSelected = globalDataModel.tagListSelected.collectAsState().value

                    for (tag in tagList) {
                        FilterChip(
                            modifier = Modifier.height(28.dp),
                            selected = tagListSelected.contains(tag),
                            leadingIcon = if (tagListSelected.contains(tag)) {
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
                                globalDataModel.toggleTagSelected(tag)
                            },
                            label = {
                                Text(tag.name, modifier = Modifier.padding(vertical = 0.dp))
                            },
                            shape = RoundedCornerShape(6.dp),

                        )
                    }



                    Box(
                        modifier = Modifier.size(28.dp)
                            .clip(RoundedCornerShape(6.dp))
                            .alpha(0.72f)
                            .clickable(onClick = openNewTagDialog),
                        contentAlignment = Alignment.Center

                    ) {
                        Icon(
                            modifier = Modifier.size(22.dp),
                            imageVector = Icons.Filled.AddCircle,
                            contentDescription = "todo something"
                        )
                    }


                }
            }

            Column(modifier = Modifier.fillMaxWidth()) {


                Row {
                    Text("TODO 记仇等级：", style = MaterialTheme.typography.bodyLarge)
                    Text(
                        "${newGSliderPosition.toInt()}  ${
                            getStringByName(
                                GrudgeLevelEnum.getEnumByCode(newGSliderPosition.toInt()).title
                            )
                        }",
                        style = MaterialTheme.typography.bodyLarge, color = interColorRange(
                            GRUDGE_LEVEL_MIN_COLOR,
                            GRUDGE_LEVEL_MAX_COLOR,
                            newGSliderPosition,
                            GRUDGE_LEVEL_MIN,
                            GRUDGE_LEVEL_MAX,

                            )
                    )
                }

                Slider(
                    modifier = Modifier.height(22.dp).background(Color.Transparent),
                    value = newGSliderPosition,
                    onValueChange = updateSliderPosition, valueRange = GRUDGE_LEVEL_MIN..GRUDGE_LEVEL_MAX,
                    track = {
                        Canvas(
                            modifier = Modifier
                                .fillMaxWidth()
                                .height(15.dp)
                        ) {
                            val radius = 6.dp.toPx()
                            val gradient = Brush.horizontalGradient(
                                colors = listOf(GRUDGE_LEVEL_MIN_COLOR, GRUDGE_LEVEL_MAX_COLOR)
                            )
                            drawRoundRect(
                                brush = gradient,
                                cornerRadius = CornerRadius(radius, radius),
                                size = Size(size.width, size.height),
                            )
                        }
                    },
                    thumb = {
                        Icon(
                            imageVector = vectorResource(Res.drawable.devil),
                            contentDescription = null,
                            modifier = Modifier.size(24.dp),
                            tint = Color.Unspecified
                        )
                    }
                )

                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.Center
                ) {
                    Text(
                        getStringByName(
                            GrudgeLevelEnum.getEnumByCode(newGSliderPosition.toInt()).desc
                        ),
                        modifier = Modifier.alpha(0.5f),
                        style = MaterialTheme.typography.labelMedium
                    )
                }

            }

            operation()

        }
    }
}