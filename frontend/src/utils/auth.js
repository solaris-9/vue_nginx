import Cookies from 'js-cookie'

const TokenKey = 'devicedp_token'
const InfoKey = 'user_info'

export function getToken() {
  return Cookies.get(TokenKey)
}

export function setToken(token) {
  return Cookies.set(TokenKey, token)
}

export function removeToken() {
  return Cookies.remove(TokenKey)
}

export function getUserCookie() {
  return Cookies.get(InfoKey)
}

export function setUserCookie(info) {
  return Cookies.set(InfoKey, info)
}

export function removeUserCookie() {
  return Cookies.remove(InfoKey)
}
