package com.astercasc.squid.thebookofgrudges.ui.components

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.input.TextFieldLineLimits
import androidx.compose.foundation.text.input.rememberTextFieldState
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import androidx.compose.ui.window.Dialog
import com.astercasc.squid.thebookofgrudges.data.DataStorageManager
import com.astercasc.squid.thebookofgrudges.data.addNewObj
import com.astercasc.squid.thebookofgrudges.data.model.GlobalDataModel
import org.jetbrains.compose.resources.stringResource
import org.koin.compose.koinInject
import thebookofgrudges.composeapp.generated.resources.Res
import thebookofgrudges.composeapp.generated.resources.add_obj_name
import thebookofgrudges.composeapp.generated.resources.add_obj_title
import thebookofgrudges.composeapp.generated.resources.add_obj_title_cancel
import thebookofgrudges.composeapp.generated.resources.add_obj_title_confirm
import thebookofgrudges.composeapp.generated.resources.error_name_empty

@Composable
fun NewGrudgeObject(
    onDismissRequest: () -> Unit
) {
    val newObjectName = rememberTextFieldState("")
    val dataStorageManager: DataStorageManager = koinInject()
    val globalDataModel: GlobalDataModel = koinInject()

    var emptyName by remember { mutableStateOf(false) }

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
                        text = stringResource(Res.string.add_obj_title),
                        style = MaterialTheme.typography.bodyLarge
                    )
                }


                MaterialTheme(
                    typography = MaterialTheme.typography.copy(
                        bodyLarge = MaterialTheme.typography.bodyMedium
                    )
                ) {
                    OutlinedTextField(
                        modifier = Modifier.fillMaxWidth().height(76.dp),
                        state = newObjectName,
                        lineLimits = TextFieldLineLimits.SingleLine,
                        label = { Text(stringResource(Res.string.add_obj_name)) },
                        shape = RoundedCornerShape(6.dp),
                        isError = emptyName,
                        supportingText = {
                            if (emptyName)
                                Text(stringResource(Res.string.error_name_empty))
                        },
                    )
                }


                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.spacedBy(8.dp)
                ) {

                    Button(
                        modifier = Modifier.weight(1f),
                        onClick = {
                            if (newObjectName.text.isEmpty()) {
                                emptyName = true
                                return@Button
                            }
                            emptyName = false
                            addNewObj(globalDataModel, dataStorageManager, newObjectName.text.toString())
                            onDismissRequest()
                        },
                        shape = RoundedCornerShape(6.dp),

                        ) {
                        Text(stringResource(Res.string.add_obj_title_confirm))
                    }

                    OutlinedButton(
                        modifier = Modifier.weight(1f),
                        onClick = onDismissRequest,
                        shape = RoundedCornerShape(6.dp),
                    ) {
                        Text(stringResource(Res.string.add_obj_title_cancel))
                    }
                }
            }
        }
    }

}