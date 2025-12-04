package com.astercasc.squid.thebookofgrudges.ui.components

import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.ModalBottomSheet
import androidx.compose.material3.Text
import androidx.compose.material3.rememberModalBottomSheetState
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp

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