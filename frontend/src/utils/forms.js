import axios from "axios"
import { MessageBox, ElMessage, ElNotification } from 'element-plus'

export function getFormItemTitle(type) {
    let base_title = { "display": "inline-block", "width": "350px", "br": false }
    let extend_title = {}
    let item_title = {}
    switch (type) {
        case "hide":
            base_title.display = "none"
            extend_title = { "type": "input", "placeholder": "", "readonly": true }
            break
        case "input":
            extend_title = { "type": "input", "placeholder": "", "readonly": false }
            break
        case "input-change":
            extend_title = { "type": "input-change", "placeholder": "", "readonly": false }
            break
        case "radio":
            extend_title = { "type": "radio", "readonly": false, "choiceList": [] }
            break
        case "checkbox":
            extend_title = { "type": "checkbox", "readonly": false, "choiceList": [] }
            break
        case "select":
            extend_title = { "type": "select", "readonly": false, "multiple": false, "choiceList": [] }
            break
        case "select-change":
            extend_title = { "type": "select-change", "readonly": false, "multiple": false, "choiceList": [] }
            break
        case "textarea":
            base_title.display = "block", base_title.width = "1050px"
            extend_title = { "type": "textarea", "readonly": false, "maxRows": 10 }
            break
    }
    item_title = Object.assign(base_title, extend_title)
    return item_title
}

//fromrules,from表单rule规则填写
export function formSettingRule(rowData, FromRequired) {
    let rules = {}
    console.log("rules", rules)
    Object.keys(rowData).forEach(key => {
        if ((FromRequired.some(item => item === key))) {
            let rule = [{ required: true, message: "\"" + key + "\"" + " is required", trigger: ["blur", "change"] }]
            rules[key] = rule
        }
    })
    console.log("rules", rules)
    return rules
}

// Await get table info API
export async function requestInfoAPI(url, update_params = {}, timeout=60) {
    let infoData = []

    await axios.get(url, { params: update_params, timeout: timeout*1000 }).then(response => {
        if (response.data && response.data.data) {
            infoData = response.data.data || response.data
        }
    }).catch(error => {
        ElMessage({
            type: "error",
            message: error,
            duration: 2 * 1000
        })
    })
    return infoData
}

//Based on URL and update_params Request Interface
export async function requestAPI(url, update_params, options, popup = false) {
    let repsonse_status = ""
    await axios.get(url, { params: update_params }).then(response => {
        if (response.data && response.data.data && response.data.data.status) {
            repsonse_status = response.data.data.status
        } else {
            repsonse_status = "nodata"
        }
        if (repsonse_status === "successful") {

        }
    }).catch(error => {
        repsonse_status = "error"
        console.error("error updateTable", error)
    })

    let title = "Successful",
        msg = options + " successful",
        type = "success"

    switch (repsonse_status) {
        case "successful":
            break;
        case "nodata":
        case "error":
            title = "Error", msg = "An error occurred while " + options, type = "error"
            break;
        default:
            title = "Failed", msg = options + " failed, " + repsonse_status, type = "warning"
            break;
    }
    if (popup) {
        ElNotification({
            title: title,
            type: type,
            message: msg,
            duration: 2 * 1000
        })
    }

    return { "title": title, "msg": msg, "type": type }
}

export function changeAgGridColumn(columnDefs, changeColumnName = null, changeData = null, options = "add") {
    if (options === "add") {
        for (let [index, item] of columnDefs.entries()) {
            if (item.field === changeColumnName) {
                Object.assign(columnDefs[index], changeData)
            }
        }

    }
    return columnDefs
}

/**
 * @description: data conversion
 * @param {*} data
 * @param {*} conversion_type 
 * @param {*} forward_conversion 
 * @returns
 */
export function dataConversion(data, conversion_type = "stringToArray", forward_conversion = true) {
    switch (conversion_type) {
        case "stringToArray":
            return stringToArray(data, forward_conversion)
            break

    }
}

/**
 * @description: dataConversion sub function, implement data conversion function
 * @param {*} data 
 * @param {*} forward_conversion 
 * @returns 
 */
function stringToArray(data, forward_conversion) {
    let conversion_data = null
    if (forward_conversion) {
        if (data instanceof String) {
            conversion_data = data.splice(",")
        } else {
            conversion_data = []
        }
    } else {
        if (data instanceof Array) {
            conversion_data = data.join(",")
        } else {
            conversion_data = ""
        }
    }
    return conversion_data
}