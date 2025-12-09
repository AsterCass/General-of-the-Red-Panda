package com.astercasc.squid.thebookofgrudges.data.model

import com.astercasc.squid.thebookofgrudges.data.DataStorageManager
import com.astercasc.squid.thebookofgrudges.data.GrudgeTag
import com.astercasc.squid.thebookofgrudges.data.initTagList
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update

class GlobalDataModel(
    dataStorageManager: DataStorageManager
) {

    private val _tagList = MutableStateFlow(initTagList(dataStorageManager))
    val tagList = _tagList.asStateFlow()
    fun addTag(tag: GrudgeTag) {
        _tagList.update { list ->
            list.plus(tag)
        }
    }

    private val _tagListSelected = MutableStateFlow<List<GrudgeTag>>(emptyList())
    val tagListSelected = _tagListSelected.asStateFlow()
    fun toggleTagSelected(tag: GrudgeTag) {
        _tagListSelected.update { list ->
            if (list.any { it.id == tag.id }) {
                list.filterNot { it.id == tag.id }
            } else {
                list.plus(tag)
            }
        }
    }



}