package com.astercasc.squid.thebookofgrudges.ui.components

import androidx.compose.foundation.*
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.input.TextFieldLineLimits
import androidx.compose.foundation.text.input.TextFieldState
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.AddCircle
import androidx.compose.material.icons.filled.Edit
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
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
import com.astercasc.squid.thebookofgrudges.constant.enums.GrudgeLevelEnum
import com.astercasc.squid.thebookofgrudges.ui.EditGrudgeObjectObj
import com.astercasc.squid.thebookofgrudges.ui.EditGrudgeTagObj
import com.astercasc.squid.thebookofgrudges.utils.getStringByName
import kotlinx.coroutines.launch
import org.jetbrains.compose.resources.vectorResource
import thebookofgrudges.composeapp.generated.resources.Res
import thebookofgrudges.composeapp.generated.resources.devil

val GrudgeLevelMinColor = Color(0xFF2196F3)
val GrudgeLevelMaxColor = Color(0xFFF44336)

fun getCurrentColor(value: Float): Color {
    val normalizedValue = (value - 1f) / 9f // 归一化到 0-1
    val blue = GrudgeLevelMinColor
    val red = GrudgeLevelMaxColor

    return Color(
        red = blue.red + (red.red - blue.red) * normalizedValue,
        green = blue.green + (red.green - blue.green) * normalizedValue,
        blue = blue.blue + (red.blue - blue.blue) * normalizedValue
    )
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun NewGrudgeSheet(
    newGTitleState: TextFieldState,
    newGDescState: TextFieldState,
    newGSliderPosition: Float,
    closeSheet: () -> Unit,
    updateSliderPosition: (Float) -> Unit,
    openNewObjDialog: () -> Unit,
    openNewTagDialog: () -> Unit,
) {

    val navigator = LocalNavigator.currentOrThrow
    val scope = rememberCoroutineScope()
    val sheetState = rememberModalBottomSheetState(

        skipPartiallyExpanded = true
    )

    ModalBottomSheet(
        shape = RoundedCornerShape(6.dp, 6.dp, 0.dp, 0.dp),
        onDismissRequest = closeSheet,
        sheetState = sheetState,

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
                                        sheetState.hide()
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

                    FilterChip(
                        modifier = Modifier.height(28.dp),
                        selected = false,
                        onClick = {},
                        label = {
                            Text("错的不是我，是这个世界", modifier = Modifier.padding(vertical = 0.dp))
                        },
                        shape = RoundedCornerShape(6.dp),

                        )

                    repeat(5) {
//                        FilterChip(
//                            modifier = Modifier.height(28.dp),
//                            selected = false,
//                            onClick = {},
//                            label = {
//                                Text("Tag $it" , modifier = Modifier.padding(vertical = 0.dp))
//                            },
//                            shape = RoundedCornerShape(6.dp),
//
//                        )
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
                                        sheetState.hide()
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

                    FilterChip(
                        modifier = Modifier.height(28.dp),
                        selected = false,
                        onClick = {},
                        label = {
                            Text("家里", modifier = Modifier.padding(vertical = 0.dp))
                        },
                        shape = RoundedCornerShape(6.dp),

                        )

                    FilterChip(
                        modifier = Modifier.height(28.dp),
                        selected = false,
                        onClick = {},
                        label = {
                            Text("酒桌", modifier = Modifier.padding(vertical = 0.dp))
                        },
                        shape = RoundedCornerShape(6.dp),

                        )



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
                        style = MaterialTheme.typography.bodyLarge,
                        color = getCurrentColor(newGSliderPosition)
                    )
                }

                Slider(
                    modifier = Modifier.height(22.dp).background(Color.Transparent),
                    value = newGSliderPosition,
                    onValueChange = updateSliderPosition,
                    valueRange = 1f..10f,
                    track = {
                        Canvas(
                            modifier = Modifier
                                .fillMaxWidth()
                                .height(15.dp)
                        ) {
                            val radius = 6.dp.toPx()
                            val gradient = Brush.horizontalGradient(
                                colors = listOf(GrudgeLevelMinColor, GrudgeLevelMaxColor)
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



            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.spacedBy(8.dp)
            ) {

                Button(
                    modifier = Modifier.weight(1f),
                    onClick = {},
                    shape = RoundedCornerShape(6.dp),

                    ) {
                    Text("开始卧薪尝胆")
                }

                OutlinedButton(
                    modifier = Modifier.weight(1f),
                    onClick = {
                        scope
                            .launch { sheetState.hide() }
                            .invokeOnCompletion {
                                if (!sheetState.isVisible) {
                                    closeSheet()
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
}