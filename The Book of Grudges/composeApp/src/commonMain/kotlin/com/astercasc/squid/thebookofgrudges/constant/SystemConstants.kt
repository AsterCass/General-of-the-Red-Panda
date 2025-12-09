package com.astercasc.squid.thebookofgrudges.constant

import com.astercasc.squid.thebookofgrudges.data.GrudgeTag

const val TAG_PREFIX: String = "GT"

val EXAMPLE_TAG_1: GrudgeTag = GrudgeTag(
    id = "${TAG_PREFIX}0",
    name = "下次一定",
)

val EXAMPLE_TAG_2: GrudgeTag = GrudgeTag(
    id = "${TAG_PREFIX}1",
    name = "背后原因让人暖心",
)