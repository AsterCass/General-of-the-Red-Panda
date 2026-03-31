package com.astercasc.squid.meowfitness.data

import kotlinx.serialization.Serializable
import kotlinx.serialization.json.Json


val commonJson = Json { ignoreUnknownKeys = true }

@Serializable
data class FitnessCell(
    var id: String = "",
    var title: String = "",

    )

