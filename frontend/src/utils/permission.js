import store from '@/store'
import permData from './botton-perm-config.json'

export function permDataFactory(perm_table, permData) {
    if (permData.length <= 0) { return [] }
    let edit_prem = [],
        add_prem = [],
        del_prem = [],
        view_prem = [],
        export_prem = []
    perm_table.forEach(item => {
        if (item.Edit === "Yes") { edit_prem.push(item.Grade) }
        if (item.Add === "Yes") { add_prem.push(item.Grade) }
        if (item.Delete === "Yes") { del_prem.push(item.Grade) }
        if (item.View === "Yes") { view_prem.push(item.Grade) }
        if (item.Export === "Yes") { export_prem.push(item.Grade) }
    })

    if (edit_prem.length === perm_table.length) { edit_prem = [] } else if (edit_prem.length === 0) { edit_prem = ["noAccess"] }
    if (add_prem.length === perm_table.length) { add_prem = [] } else if (add_prem.length === 0) { add_prem = ["noAccess"] }
    if (del_prem.length === perm_table.length) { del_prem = [] } else if (del_prem.length === 0) { del_prem = ["noAccess"] }
    if (view_prem.length === perm_table.length) { view_prem = [] } else if (view_prem.length === 0) { view_prem = ["noAccess"] }

    let permDataKey = Object.keys(permData)
    permDataKey.forEach(key => {
        if (typeof(permData[key]["edit"])) {
            permData[key]["edit"] = edit_prem
        }
        if (typeof(permData[key]["add"])) {
            permData[key]["add"] = add_prem
        }
        if (typeof(permData[key]["del"])) {
            permData[key]["del"] = del_prem
        }
        if (typeof(permData[key]["view"])) {
            permData[key]["view"] = view_prem
        }
        if (typeof(permData[key]["export"])) {
            permData[key]["export"] = export_prem
        }
    })
    return permData
}

/**
 * @param {Array} value
 * @returns {Boolean}
 * @example see @/views/permission/directive.vue
 */
export default function checkPermission(permissionGroupName, option) {
    // user`s level is '1'
    let level = store.getters.level
    if (level && level === "1") {
        return false
    }
    let permData = store.getters.perm_data
    // user have access
    let passRoles = []
    if (permData[permissionGroupName] && permData[permissionGroupName][option]) {
        passRoles = permData[permissionGroupName][option]
    } else {
        return false
    }

    if (passRoles instanceof Array && passRoles.length === 0) {
        return true
    } else if (passRoles && passRoles instanceof Array && passRoles.length > 0) {
        let roles = store.getters.roles

        if (roles.some(role => ["Administrator"].includes(role))) { return true }

        const permissionRoles = passRoles
        const hasPermission = roles.some(role => {
            return permissionRoles.includes(role)
        })
        return hasPermission
    } else {
        console.error(`need roles! Like v-permission="['admin','editor']"`)
        return false
    }
}