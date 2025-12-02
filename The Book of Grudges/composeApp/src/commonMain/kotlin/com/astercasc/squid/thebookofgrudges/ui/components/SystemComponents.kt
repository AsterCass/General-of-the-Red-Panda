package com.astercasc.squid.thebookofgrudges.ui.components

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.input.TextFieldLineLimits
import androidx.compose.foundation.text.input.rememberTextFieldState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp


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

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun NewGrudgeSheet(
    closeSheet: () -> Unit,
) {

    val sheetState = rememberModalBottomSheetState(
        skipPartiallyExpanded = true
    )

    ModalBottomSheet(
        shape = RoundedCornerShape(6.dp),
        onDismissRequest = closeSheet,
        sheetState = sheetState,
    ) {
        // todo 这里可能触发 ModalBottomSheet 的滚动，也可能触发 Column 的，所以最好是再做一个页面
        Column(
            modifier = Modifier.fillMaxWidth().verticalScroll(rememberScrollState()),
        ) {
            TextField(
                state = rememberTextFieldState(),
                lineLimits = TextFieldLineLimits.SingleLine,
                label = { Text("Label") },
            )

            Text("12342432")


            OutlinedButton(
                onClick = {},
            ) {
                Text("todo create")
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
        shape = RoundedCornerShape(6.dp),
        onDismissRequest = closeSheet,
        sheetState = sheetState
    ) {
        Column(modifier = Modifier.fillMaxWidth().height(150.dp)) {
            Text("ReadGrudgeSheet")
        }
    }
}