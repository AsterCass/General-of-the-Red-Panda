package com.astercasc.squid.thebookofgrudges.ui.components

import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.unit.dp
import androidx.compose.ui.window.Dialog
import cafe.adriel.voyager.core.annotation.InternalVoyagerApi
import cafe.adriel.voyager.navigator.LocalNavigator
import cafe.adriel.voyager.navigator.currentOrThrow
import org.jetbrains.compose.resources.stringResource
import thebookofgrudges.composeapp.generated.resources.Res
import thebookofgrudges.composeapp.generated.resources.system_confirm_cancel
import thebookofgrudges.composeapp.generated.resources.system_confirm_ok


@OptIn(ExperimentalMaterial3Api::class, InternalVoyagerApi::class)
@Composable
fun MainAppBar(
    title: String,
) {

    val navigator = LocalNavigator.currentOrThrow

    Surface(
        color = MaterialTheme.colorScheme.primaryContainer,
        contentColor = MaterialTheme.colorScheme.onPrimaryContainer,
    ) {


        Box(
            modifier = Modifier.windowInsetsPadding(TopAppBarDefaults.windowInsets).fillMaxWidth()
                .padding(horizontal = 3.dp, vertical = 6.dp),
        ) {

            if (navigator.canPop) {
                Box(
                    modifier = Modifier.align(Alignment.CenterStart).padding(start = 12.dp)
                        .clip(RoundedCornerShape(6.dp))
                        .clickable(onClick = { navigator.pop() }),
                ) {
                    Icon(
                        modifier = Modifier.padding(3.dp).size(24.dp),
                        imageVector = Icons.AutoMirrored.Filled.ArrowBack,
                        contentDescription = "Back",
                    )
                }
            }

            Box(
                modifier = Modifier.align(Alignment.Center),
            ) {
                Text(
                    text = title, style = MaterialTheme.typography.headlineSmall
                )
            }
        }

    }
}

@Composable
fun SystemConfirm(
    title: String,
    onConfirmRequest: () -> Unit = {},
    onDismissRequest: () -> Unit = {},
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
                        Text(stringResource(Res.string.system_confirm_ok))
                    }

                    OutlinedButton(
                        modifier = Modifier.weight(1f),
                        onClick = onDismissRequest,
                        shape = RoundedCornerShape(6.dp),
                    ) {
                        Text(stringResource(Res.string.system_confirm_cancel))
                    }
                }
            }
        }
    }

}