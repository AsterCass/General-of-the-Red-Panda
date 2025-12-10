package com.astercasc.squid.thebookofgrudges.data.model

import com.astercasc.squid.thebookofgrudges.data.*
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update

class GlobalDataModel(
    dataStorageManager: DataStorageManager
) {

    // tag
    private val _tagList = MutableStateFlow(initTagList(dataStorageManager))
    val tagList = _tagList.asStateFlow()
    fun addTag(tag: GrudgeTag) {
        _tagList.update { list ->
            list.plus(tag)
        }
    }
    fun removeTag(tagId: String) {
        _tagListSelected.update { list ->
            list.filterNot { it.id == tagId }
        }
        _tagList.update { list ->
            list.filterNot { it.id == tagId }
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

    fun clearTagSelected() {
        _tagListSelected.value = emptyList()
    }


    // obj
    private val _objList = MutableStateFlow(initObjList(dataStorageManager))
    val objList = _objList.asStateFlow()
    fun addObj(obj: GrudgeObj) {
        _objList.update { list ->
            list.plus(obj)
        }
    }

    fun removeObj(objId: String) {
        _objListSelected.update { list ->
            list.filterNot { it.id == objId }
        }
        _objList.update { list ->
            list.filterNot { it.id == objId }
        }
    }

    private val _objListSelected = MutableStateFlow<List<GrudgeObj>>(emptyList())
    val objListSelected = _objListSelected.asStateFlow()
    fun toggleObjSelected(obj: GrudgeObj) {
        _objListSelected.update { list ->
            if (list.any { it.id == obj.id }) {
                list.filterNot { it.id == obj.id }
            } else {
                list.plus(obj)
            }
        }
    }
    fun clearObjSelected() {
        _objListSelected.value = emptyList()
    }
    
    // grudge
    private val _gruList = MutableStateFlow(initGrudgeList(dataStorageManager))
    val gruList = _gruList.asStateFlow()
    fun addGru(gru: GrudgeCell) {
        _gruList.update { list ->
            list.plus(gru)
        }
    }

    private val _gruListSelected = MutableStateFlow<List<GrudgeCell>>(emptyList())
    val gruListSelected = _gruListSelected.asStateFlow()

    private val _currentGru = MutableStateFlow(GrudgeCell())
    val currentGru = _currentGru.asStateFlow()






}