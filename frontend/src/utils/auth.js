import Cookies from 'js-cookie'
import store from '@/store'

const TokenKey = 'vue_admin_template_token'
const UserName = 'username'
const EncodedAuth = 'encodedAuth'

export function getToken() {
    return Cookies.get(TokenKey)
}

export function setToken(token) {
    var millisecond = new Date().getTime()
    var expiresTime = new Date(millisecond + 60 * 1000 * 60 * 5)

    return Cookies.set(TokenKey, token, {
        expires: expiresTime,
    })

    // return Cookies.set(TokenKey, token)
}

export function removeToken() {
    return Cookies.remove(TokenKey)
}

export function getUserName() {
    return store.getters.name
}

export function getEncodedAuth() {
    let cookie_name = Cookies.get(EncodedAuth)
    if (cookie_name == null || cookie_name == 'none') {
        cookie_name = ""
    }
    return cookie_name
}