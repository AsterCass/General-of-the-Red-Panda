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
import kotlinx.coroutines.launch


@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun MainAppBar(
    title: String,
) {
    Surface(
        color = MaterialTheme.colorScheme.primaryContainer,
        contentColor = MaterialTheme.colorScheme.onPrimaryContainer,
    ) {
        Row(
            modifier = Modifier.windowInsetsPadding(TopAppBarDefaults.windowInsets).fillMaxWidth()
                .padding(horizontal = 3.dp, vertical = 6.dp),
            horizontalArrangement = Arrangement.Center,
            verticalAlignment = Alignment.CenterVertically,
        ) {

            Text(
                text = title, style = MaterialTheme.typography.headlineSmall
            )

        }
    }
}

fun getCurrentColor(value: Float): Color {
    val normalizedValue = (value - 1f) / 9f // 归一化到 0-1
    val blue = Color(0xFF2196F3)
    val red = Color(0xFFF44336)

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
) {

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
            verticalArrangement = Arrangement.spacedBy(12.dp)
        ) {

            // important 这里 OutlinedTextField 默认的样式太大了，使用 MaterialTheme 修改降级
            MaterialTheme(
                typography = MaterialTheme.typography.copy(
                    bodyLarge = MaterialTheme.typography.bodyMedium
                )
            ) {
                OutlinedTextField(
                    modifier = Modifier.fillMaxWidth(),
                    state = newGTitleState,
                    lineLimits = TextFieldLineLimits.SingleLine,
                    label = { Text("todo 仇恨标题") },
                    placeholder = { Text("todo 标题占位符") },
                    shape = RoundedCornerShape(6.dp),
                )

                OutlinedTextField(
                    modifier = Modifier.fillMaxWidth(),
                    state = newGDescState,
                    lineLimits = TextFieldLineLimits.MultiLine(1, 3),
                    label = { Text("todo 仇恨描述") },
                    placeholder = { Text("todo 描述占位符") },
                    shape = RoundedCornerShape(6.dp),
                )
            }

            Column(
                modifier = Modifier.fillMaxWidth(),
                verticalArrangement = Arrangement.spacedBy(6.dp)
            ) {

                Row(
                    modifier = Modifier.fillMaxWidth(),
                    verticalAlignment = Alignment.CenterVertically,
                ) {
                    Text("TODO 仇恨对象：", style = MaterialTheme.typography.bodyLarge)

                    Box(
                        modifier = Modifier.size(22.dp)
                            .clip(RoundedCornerShape(6.dp))
                            .alpha(0.72f)
                            .clickable(onClick = {
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
                            .clickable(onClick = {
                            }),
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
                    Text("TODO 仇恨标签：", style = MaterialTheme.typography.bodyLarge)

                    Box(
                        modifier = Modifier.size(22.dp)
                            .clip(RoundedCornerShape(6.dp))
                            .alpha(0.72f)
                            .clickable(onClick = {
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
                            .clickable(onClick = {
                            }),
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

                Text("TODO 仇恨等级：", style = MaterialTheme.typography.bodyLarge)

                Slider(
                    value = newGSliderPosition,
                    onValueChange = updateSliderPosition,
                    steps = 8,
                    valueRange = 1f..10f,
                    track = {
                        Canvas(
                            modifier = Modifier
                                .fillMaxWidth()
                                .height(15.dp)
                        ) {
                            val radius = 6.dp.toPx()
                            val gradient = Brush.horizontalGradient(
                                colors = listOf(Color(0xFF2196F3), Color(0xFFF44336))
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
                            modifier = Modifier.size(18.dp).background(Color.LightGray),
                            imageVector = Icons.Filled.Edit,
                            contentDescription = "todo something"
                        )
                    }
                )

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

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun ReadGrudgeSheet(
    closeSheet: () -> Unit,
) {

    val sheetState = rememberModalBottomSheetState()

    ModalBottomSheet(
        shape = RoundedCornerShape(6.dp, 6.dp, 0.dp, 0.dp),
        onDismissRequest = closeSheet,
        sheetState = sheetState
    ) {
        Column(modifier = Modifier.fillMaxWidth().height(150.dp)) {
            Text("ReadGrudgeSheet")
        }
    }
}