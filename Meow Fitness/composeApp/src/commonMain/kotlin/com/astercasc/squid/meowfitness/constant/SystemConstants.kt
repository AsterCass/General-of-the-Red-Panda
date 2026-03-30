package com.astercasc.squid.meowfitness.constant

import androidx.compose.ui.graphics.Color
import com.astercasc.squid.meowfitness.data.GrudgeObj
import com.astercasc.squid.meowfitness.data.GrudgeTag

const val TAG_PREFIX: String = "GT"

const val OBJ_PREFIX: String = "GO"

const val GRU_PREFIX: String = "GG"

val GRUDGE_LEVEL_MIN_COLOR = Color(0xFF2196F3)
val GRUDGE_LEVEL_MAX_COLOR = Color(0xFFF44336)
const val GRUDGE_LEVEL_MIN = 1f;
const val GRUDGE_LEVEL_MAX = 10f;

val EXAMPLE_TAG_1: GrudgeTag = GrudgeTag(
    id = "${TAG_PREFIX}0",
    name = "下次一定",
)

val EXAMPLE_TAG_2: GrudgeTag = GrudgeTag(
    id = "${TAG_PREFIX}1",
    name = "背后原因让人暖心",
)

val EXAMPLE_OBJ_1: GrudgeObj = GrudgeObj(
    id = "${OBJ_PREFIX}0",
    name = "错的不是我，是这个世界",
)