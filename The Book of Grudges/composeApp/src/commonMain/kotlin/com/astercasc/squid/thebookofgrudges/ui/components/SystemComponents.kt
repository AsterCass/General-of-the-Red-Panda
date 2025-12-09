package com.astercasc.squid.thebookofgrudges.ui.components

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import androidx.compose.ui.window.Dialog


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

@Composable
fun SystemConfirm(
    title: String,
    onConfirmRequest: () -> Unit,
    onDismissRequest: () -> Unit
) {

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
                        text = title,
                        style = MaterialTheme.typography.bodyLarge
                    )
                }

                Row(
                    modifier = Modifier.fillMaxWidth().padding(top = 8.dp),
                    horizontalArrangement = Arrangement.spacedBy(8.dp)
                ) {

                    Button(
                        modifier = Modifier.weight(1f),
                        onClick = {
                            onConfirmRequest()
                            onDismissRequest()
                        },
                        shape = RoundedCornerShape(6.dp),

                        ) {
                        Text("确认")
                    }

                    OutlinedButton(
                        modifier = Modifier.weight(1f),
                        onClick = onDismissRequest,
                        shape = RoundedCornerShape(6.dp),
                    ) {
                        Text("取消")
                    }
                }
            }
        }
    }

}