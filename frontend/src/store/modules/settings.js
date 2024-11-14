import { custometList, getProductList, getReleaseList } from "@/api/table"
import defaultSettings from '@/settings'

const { showSettings, fixedHeader, sidebarLogo, tagsView } = defaultSettings
const state = {
    showSettings: showSettings,
    tagsView: tagsView,
    fixedHeader: fixedHeader,
    sidebarLogo: sidebarLogo,
    customerList: [],
    productList: [],
    releaseList: [],
}


const mutations = {
    CHANGE_SETTING: (state, { key, value }) => {
        // eslint-disable-next-line no-prototype-builtins
        if (state.hasOwnProperty(key)) {
            state[key] = value
        }
    },
    CUSTOMER_LIST: (state, customerList) => {
        state.customerList = customerList
    },
    PRODUCT_LIST: (state, productList) => {
        state.productList = productList
    },
    RELEASE_LIST: (state, releaseList) => {
        state.releaseList = releaseList
    },
}

const actions = {
    changeSetting({ commit }, data) {
        commit('CHANGE_SETTING', data)
    },
    getCustometList({ commit }) {
        return new Promise((resolve, reject) => {
            custometList({ type: "0" }).then(response => {
                let customerList = response.data.items.map(item => item.Customer).sort()
                commit('CUSTOMER_LIST', customerList)
                resolve()
            }).catch(error => {
                reject(error)
            })
        })
    },
    ProductList({ commit }) {
        return new Promise((resolve, reject) => {
            getProductList({ product: "all" }).then(response => {
                let productList = response.data.items.map(item => item.Product).sort()
                commit('PRODUCT_LIST', productList)
                resolve()
            }).catch(error => {
                reject(error)
            })
        })
    },
    ReleaseList({ commit }) {
        return new Promise((resolve, reject) => {
            getReleaseList({ type: "0" }).then(response => {
                let releaseList = response.data.items.map(item => item.Release).sort()
                commit('RELEASE_LIST', releaseList)
                resolve()
            }).catch(error => {
                reject(error)
            })
        })
    }
}

export default {
    namespaced: true,
    state,
    mutations,
    actions
}