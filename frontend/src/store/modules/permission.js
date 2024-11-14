import { asyncRoutes, constantRoutes } from '@/router'
import { adminGradeManagement } from '@/api/table'
import { permDataFactory } from '@/utils/permission'
import permData from '@/utils/botton-perm-config.json'
import store from '@/store'

/**
 * @description: Use meta.role to determine if the current user has permission
 * @param roles
 * @param route
 */
function hasPermission(roles, route) {
    if (route.meta && route.meta.accesspass) {
        return true
    } else if (!store.getters.level || store.getters.level === '1' || store.getters.level === '') {
        return false
    } else if (roles.includes('Administrator')) {
        return true
    } else if (route.meta && route.meta.roles) {
        return roles.some(role => route.meta.roles.includes(role)) || route.meta.roles.length <= 0
    } else {
        return false
    }
}

/**
 * @description: Remove the left silder meun where the childen of the router is empty
 * @param {Array} filterRoutes 
 * @returns 
 */
export function filterHasChildRoutes(filterRoutes) {
    const res = []
    filterRoutes.forEach(route => {
        if (!(route.children && (route.children instanceof Array) && route.children.length <= 0)) {
            res.push(route)
        }

    })
    return res
}

/**
 * Filter asynchronous routing tables by recursion
 * @param routes asyncRoutes
 * @param roles
 */
export function filterAsyncRoutes(routes, roles) {
    const res = []
    routes.forEach(route => {
        const tmp = {...route }
        if (hasPermission(roles, tmp)) {
            if (tmp.children) {
                tmp.children = filterAsyncRoutes(tmp.children, roles)
            }
            res.push(tmp)
        }
    })

    return res
}

/**
 * @description: 处理asyncRoutes数据为后端获取的权限数据
 * @param {*} asyncRoutes 
 */
function handleAsyncRoutes(asyncRoutes, permData) {
    asyncRoutes.forEach(router => {
        if (router.children) {
            router.children.forEach(r => {
                if (permData[r.name]) {
                    r.meta.roles = permData[r.name]['view']
                } else {
                    if (r.meta.roles.length > 0) {
                        let mapNames = {
                            'Index': 'MyView',
                            'Report': 'CustomerReport',
                            'MyFavorite': 'CustomerReport',
                            'ProductNWCCSaaS': 'NWCCSaaS',
                            'PreconfigureManagement': 'PreConfig',
                            'Home': 'home'
                        }
                        r.meta.roles = permData[mapNames[r.name]]['view']
                    }
                }
            })
        }
    })
    return asyncRoutes
}

const state = {
    routes: [],
    addRoutes: [],
    permData: [],
}

const mutations = {
    SET_ROUTES: (state, routes) => {
        state.addRoutes = routes
        state.routes = constantRoutes.concat(routes)
    },
    SET_PERM_DATA: (state, permData) => {
        state.permData = permData
    },
}

const actions = {
    // access filter
    generateRoutes({ commit, state }, roles) {
        return new Promise(resolve => {
            let handleRoutes = handleAsyncRoutes(asyncRoutes, state.permData)
            let accessedRoutes = filterAsyncRoutes(handleRoutes, roles)
            accessedRoutes = filterHasChildRoutes(accessedRoutes)
            commit('SET_ROUTES', accessedRoutes)
            resolve(accessedRoutes)
        })
    },
    // get grade access table data
    getPermTable({ commit }) {
        return new Promise((resolve, reject) => {
            adminGradeManagement({ Grade: "all" }).then(response => {
                let perm_data = permDataFactory(response.data.items, permData)
                commit('SET_PERM_DATA', perm_data)
                resolve()
            }).catch(error => {
                reject(error)
            })
        })
    },
}

export default {
    namespaced: true,
    state,
    mutations,
    actions
}