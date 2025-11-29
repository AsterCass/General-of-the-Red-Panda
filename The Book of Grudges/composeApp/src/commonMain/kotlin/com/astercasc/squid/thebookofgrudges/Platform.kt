package com.astercasc.squid.thebookofgrudges

interface Platform {
    val name: String
}

expect fun getPlatform(): Platform