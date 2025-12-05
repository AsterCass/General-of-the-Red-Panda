package com.astercasc.squid.thebookofgrudges.ui.components

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.input.TextFieldLineLimits
import androidx.compose.foundation.text.input.rememberTextFieldState
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import androidx.compose.ui.window.Dialog

@Composable
fun NewGrudgeObject(
    onDismissRequest: () -> Unit
) {
    val newObjectName = rememberTextFieldState("")

    Dialog(onDismissRequest = { onDismissRequest() }) {
        Card(
            modifier = Modifier
                .fillMaxWidth(),
            shape = RoundedCornerShape(6.dp),
        ) {
            Column(
                Modifier.padding(16.dp),
                verticalArrangement = Arrangement.spacedBy(8.dp)
            ) {
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.Center,
                ) {
                    Text(
                        text = "进入《死亡笔记》待审人员名单",
                        style = MaterialTheme.typography.bodyLarge
                    )
                }


                MaterialTheme(
                    typography = MaterialTheme.typography.copy(
                        bodyLarge = MaterialTheme.typography.bodyMedium
                    )
                ) {
                    OutlinedTextField(
                        modifier = Modifier.fillMaxWidth().height(58.dp),
                        state = newObjectName,
                        lineLimits = TextFieldLineLimits.SingleLine,
                        label = { Text("todo 新建记仇对象") },
                        placeholder = { Text("todo 记仇对象占位符") },
                        shape = RoundedCornerShape(6.dp),
                    )
                }


                Row(
                    modifier = Modifier.fillMaxWidth().padding(top = 8.dp),
                    horizontalArrangement = Arrangement.spacedBy(8.dp)
                ) {

                    Button(
                        modifier = Modifier.weight(1f),
                        onClick = {

                            onDismissRequest()
                        },
                        shape = RoundedCornerShape(6.dp),

                        ) {
                        Text("记仇标记！")
                    }

                    OutlinedButton(
                        modifier = Modifier.weight(1f),
                        onClick = onDismissRequest,
                        shape = RoundedCornerShape(6.dp),
                    ) {
                        Text("再观察观察")
                    }
                }
            }
        }
    }

}