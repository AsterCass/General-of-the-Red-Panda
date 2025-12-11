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
        _tagListSelectedNew.update { list ->
            list.filterNot { it.id == tagId }
        }
        _tagListSelectedEdit.update { list ->
            list.filterNot { it.id == tagId }
        }
        _tagList.update { list ->
            list.filterNot { it.id == tagId }
        }
    }

    private val _tagListSelectedNew = MutableStateFlow<List<GrudgeTag>>(emptyList())
    val tagListSelectedNew = _tagListSelectedNew.asStateFlow()
    fun toggleTagSelectedNew(tag: GrudgeTag) {
        _tagListSelectedNew.update { list ->
            if (list.any { it.id == tag.id }) {
                list.filterNot { it.id == tag.id }
            } else {
                list.plus(tag)
            }
        }
    }

    fun clearTagSelectedNew() {
        _tagListSelectedNew.value = emptyList()
    }

    private val _tagListSelectedEdit = MutableStateFlow<List<GrudgeTag>>(emptyList())
    val tagListSelectedEdit = _tagListSelectedEdit.asStateFlow()
    fun toggleTagSelectedEdit(tag: GrudgeTag) {
        _tagListSelectedEdit.update { list ->
            if (list.any { it.id == tag.id }) {
                list.filterNot { it.id == tag.id }
            } else {
                list.plus(tag)
            }
        }
    }

    fun resetTagSelectedEdit(list: List<GrudgeTag>) {
        _tagListSelectedEdit.value = list
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
        _objListSelectedNew.update { list ->
            list.filterNot { it.id == objId }
        }
        _objListSelectedEdit.update { list ->
            list.filterNot { it.id == objId }
        }
        _objList.update { list ->
            list.filterNot { it.id == objId }
        }
    }

    private val _objListSelectedNew = MutableStateFlow<List<GrudgeObj>>(emptyList())
    val objListSelectedNew = _objListSelectedNew.asStateFlow()
    fun toggleObjSelectedNew(obj: GrudgeObj) {
        _objListSelectedNew.update { list ->
            if (list.any { it.id == obj.id }) {
                list.filterNot { it.id == obj.id }
            } else {
                list.plus(obj)
            }
        }
    }

    fun clearObjSelectedNew() {
        _objListSelectedNew.value = emptyList()
    }

    private val _objListSelectedEdit = MutableStateFlow<List<GrudgeObj>>(emptyList())
    val objListSelectedEdit = _objListSelectedEdit.asStateFlow()
    fun toggleObjSelectedEdit(obj: GrudgeObj) {
        _objListSelectedEdit.update { list ->
            if (list.any { it.id == obj.id }) {
                list.filterNot { it.id == obj.id }
            } else {
                list.plus(obj)
            }
        }
    }

    fun resetObjSelectedEdit(list: List<GrudgeObj>) {
        _objListSelectedEdit.value = list
    }
    
    // grudge
    private val _gruList = MutableStateFlow(initGrudgeList(dataStorageManager))
    val gruList = _gruList.asStateFlow()
    fun addGru(gru: GrudgeCell) {
        _gruList.update { list ->
            list.plus(gru)
        }
    }

    fun editGru(gru: GrudgeCell) {
        _gruList.update { list ->
            list.map { obj ->
                if (obj.id == gru.id) gru else obj
            }
        }
    }

    fun removeGru(gruId: String) {
        _gruIdListSelected.update { list ->
            list.filterNot { it == gruId }
        }
        _gruList.update { list ->
            list.filterNot { it.id == gruId }
        }
    }

    fun addGruRef(gruId: String) {
        _gruList.update { list ->
            list.map { obj ->
                if (obj.id == gruId) {
                    obj.copy(
                        referCount = obj.referCount + 1,
                    )
                } else obj
            }
        }
    }


    private val _gruIdListSelected = MutableStateFlow<List<String>>(emptyList())
    val gruIdListSelected = _gruIdListSelected.asStateFlow()


    // search 
    private val _objListSearch = MutableStateFlow<List<String>>(emptyList())
    val objListSearch = _objListSearch.asStateFlow()
    fun toggleObjSearch(objId: String) {
        _objListSearch.update { list ->
            if (list.any { it == objId }) {
                list.filterNot { it == objId }
            } else {
                list.plus(objId)
            }
        }
    }

    private val _tagListSearch = MutableStateFlow<List<String>>(emptyList())
    val tagListSearch = _tagListSearch.asStateFlow()
    fun toggleTagSearch(tagId: String) {
        _tagListSearch.update { list ->
            if (list.any { it == tagId }) {
                list.filterNot { it == tagId }
            } else {
                list.plus(tagId)
            }
        }
    }

}