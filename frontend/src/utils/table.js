import axios from 'axios'
import store from '@/store'

/**
 * @description: According to the table data, the header required for producing ag-grid-vue
 * @param {arry} rowData ag-grid-vue table data
 * @returns {arry} [columnDefs, rowData]
 */
export function getGridData(rowData) {
    let table_head = rowData[0]
    let columnDefs = []
    for (let k in table_head) {
        let item = { field: k, headerName: k, headerTooltip: k, filterParams: { applyMiniFilterWhileTyping: true }, autoHeight: true, wrapText: true }
        if (k.toUpperCase() === "ID") { item.hide = true }
        columnDefs.push(item)
    }
    return [columnDefs, rowData]
}

/**
 * @description: According to the table head list, the columnDefs required for producing ag-grid-vue
 * @param {arry} column ag-grid-vue table head
 * @returns {arry} columnDefs
 */
export function getGridColumn(column, hide_column = ["ID"]) {
    if (!(column instanceof Array)) { return [] }
    let columnDefs = []
    column.forEach(k => {
        let item = { field: k, headerName: k, headerTooltip: k, filterParams: { applyMiniFilterWhileTyping: true }, autoHeight: true, wrapText: true }
        if (hide_column.some(hide_item => hide_item === k)) { item.hide = true }
        columnDefs.push(item)
    })
    return columnDefs
}

/**
 * @description: 
 * @param {arry} allTableData All data obtained from the original table
 * @param {Object} filterOptions Filter Parameter Template
 * @returns {arry} filter table
 */
export function tableFilter(allTableData, filterOptions) {
    let filter_condition = "true"
    if(filterOptions.select){
        Object.keys(filterOptions.select).forEach(key => {
            if (filterOptions.select[key].value.length > 0) {
                filter_condition += "&&(filterOptions.select['" + key + "'].value.length<=0||filterOptions.select['" + key + "'].value.includes(item['" + key + "']))"
            }
        })
    }
    console.log('filterOptions.str',filterOptions.str)
    if(filterOptions.str){    
        Object.keys(filterOptions.str).forEach(key => {
            let _search = filterOptions.str[key].value.toLowerCase()
            if (_search) {
                filter_condition += "&&(!'" + _search + "'||('" + _search + "'&&(item['" + key + "'].toLowerCase().indexOf('" + _search + "')!==-1)))"
            }
        })
    }
    
    let rowData = allTableData.filter((item) => {
        if (filter_condition != "true") {
            console.log(filter_condition)
            return eval(filter_condition)
        } else {
            return true
        }
    })
    return rowData
}

export async function network_options(url, options_params) { //同步方法
    var res = null
    await axios.get(url, { params: options_params }).then(response => {
        res = response.data
    }).catch(error => {
        res = { "error": error }
    })
    return res
}

/**
 * @description 全局ag-grid上下文菜单配置
 * @returns 
 */
export default function getContextMenuItems() {
    let result = [
            // 'cut',
            'copy',
            // 'paste',
            // 'separator',
            // 'chartRange',
        ]
        // if (true) {
        //     result.splice(3, 0, 'export')
        // }
    return result
}

export async function getCustomer() {
    let customerList = store.getters.customer_list
    if (!(customerList && customerList.length && customerList.length > 0)) {
        await store.dispatch('settings/getCustometList')
        customerList = store.getters.customer_list
    }
    return customerList
}

export async function getProduct() {
    let productList = store.getters.product_list
    if (!(productList && productList.length && productList.length > 0)) {
        await store.dispatch('settings/ProductList')
        productList = store.getters.product_list
    }
    return productList
}

export async function getRelease() {
    let releaseList = store.getters.release_list
    if (!(releaseList && releaseList.length && releaseList.length > 0)) {
        await store.dispatch('settings/ReleaseList')
        releaseList = store.getters.release_list
    }
    return releaseList
}

export async function getCertificates() {
    let certificatesList = JSON.parse(localStorage.getItem("certificatesList"))

    if (!certificatesList || certificatesList.length === 0) {
        await axios.get("/api/dbquery/certificates", { params: { type: "0", certificates: "all" } }).then(response => {
            certificatesList = response.data.data.items.map(item => (item.Certificates))
        }).catch(error => {
            certificatesList = []
        })
        localStorage.setItem("certificatesList", JSON.stringify(certificatesList))

    }

    return certificatesList
}

/**
 * @description: List data is grouped by a certain column name
 * @param {String} arr 
 * @param {Array} property 
 * @returns 
 */
export function groupBy(arr, property){
    if (!Array.isArray(arr)) return []
    return arr.reduce((pre, obj) => {
        var newObj = {
            [property]: obj[property],
            data: [obj],
        }

        if (!pre.length) {
            return [newObj]
        }

        for (let i = 0; i < pre.length; i++) {
            let item = pre[i]
            if(item[property] === obj[property]) {
            item.data = [...item.data, obj]
            return pre
            }
        }
        return [...pre, newObj]
    }, [])
}

/**
 * @description: 根据分组，统计每组数量
 */
export function totalGroupBy(arr, property){
    let groupByData = groupBy(arr, property)
    if(groupByData && groupByData.length>0){
        let propertyTotal = groupByData.map(item=>{
            let dict = {}
            dict['name'] = item[property]
            dict['value'] = item.data.length
            return dict
        })
        return propertyTotal
    }else{
        return []
    }
}

/**
 * @description: 列表去重
 */
export function arrayDeduplication(arr){
    return Array.from(new Set(arr))
}

/**
 * @description 将数据转化为ag-grid筛选数据格式
 */
export function convertToFilterData(filterData, tableHead){
    let filterDataKeys = Object.keys(filterData)
    let hardcodedFilter = {}
    let obj = {
        filterType: 'text',
        type: 'set',
        values: []
    }
    let tableHeadKeys = tableHead.map(item=>item.field) // 表头所有key
    filterDataKeys.forEach(key=>{
        if(tableHeadKeys.includes(key)){
            let obj2 = JSON.parse(JSON.stringify(obj))
            obj2.values.push(filterData[key])
            hardcodedFilter[key] = obj2
        }
    })
    return hardcodedFilter
}

/**
 * @description 对象型列表排序
 */
export function sortArrayObject(arrObj, sortObjKey, reverse=false){
    arrObj.sort((a, b) => {
        const nameA = a[sortObjKey]
        const nameB = b[sortObjKey]
        if(nameA instanceof String ){nameA=nameA.toUpperCase();}// 忽略大小写
        if(nameB instanceof String ){nameB=nameB.toUpperCase();}// 忽略大小写

        if (nameA < nameB) {
          return -1;
        }
        if (nameA > nameB) {
          return 1;
        }

        // name 必须相等
        return 0;
    })

    // 倒序
    if(reverse){
        arrObj.reverse()
    }
}

/**
 * @description 判断是不是管理员
 */
export function isAdmin(roles){
    return roles.includes("Administrator")
}