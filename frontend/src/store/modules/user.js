import { login, logout, getInfo } from '@/api/user'
import { getToken, setToken, removeToken } from '@/utils/auth'
import { resetRouter } from '@/router'

const getDefaultState = () => {
    return {
        token: getToken(),
        name: '',
        avatar: '',
        roles: '',
        mail: '',
        auth: '',
        level: '',
    }
}

const state = getDefaultState()

const mutations = {
    RESET_STATE: (state) => {
        Object.assign(state, getDefaultState())
    },
    SET_TOKEN: (state, token) => {
        state.token = token
    },
    SET_NAME: (state, name) => {
        state.name = name
    },
    SET_AVATAR: (state, avatar) => {
        state.avatar = avatar
    },
    SET_ROLES: (state, roles) => {
        state.roles = roles
    },
    SET_MAIL: (state, mail) => {
        state.mail = mail
    },
    SET_AUTH: (state, auth) => {
        state.auth = auth
    },
    SET_LEVEL: (state, level) => {
        state.level = level
    },
}

const actions = {
    // user login
    login({ commit }, userInfo) {
        const { username, password } = userInfo
        return new Promise((resolve, reject) => {
            login({ username: username.trim(), password: password }).then(response => {
                if ( response.code === 20000){
                    const { data } = response
                    commit('SET_TOKEN', data.token)
                    commit('SET_AUTH', data.auth)
                    setToken(data.token)
                    resolve()
                }
            }).catch(error => {
                reject(error)
            })
        })
    },

    // get user info
    getInfo({ commit, state }) {
        return new Promise((resolve, reject) => {
            getInfo(state.token).then(response => {
                const { data } = response
                    
                if (!data) {
                    reject('Verification failed, please Login again.')
                }
                const { name, avatar, roles, mail } = data
                let role = []
                if (roles) { role.push(roles) }
                commit('SET_NAME', name)
                commit('SET_AVATAR', avatar)
                commit('SET_ROLES', role)
                commit('SET_MAIL', mail)
                commit('SET_LEVEL', data.level)
                resolve(data)
            }).catch(error => {
                reject(error)
            })
        })
    },

    // user logout
    logout({ commit, state }) {
        return new Promise((resolve, reject) => {
            logout(state.token).then(() => {
                removeToken() // must remove  token  first
                resetRouter()
                commit('RESET_STATE')
                resolve()
            }).catch(error => {
                reject(error)
            })
        })
    },

    // remove token
    resetToken({ commit }) {
        return new Promise(resolve => {
            removeToken() // must remove  token  first
            commit('RESET_STATE')
            resolve()
        })
    }
}

export default {
    namespaced: true,
    state,
    mutations,
    actions
}