import Cookies from 'js-cookie'

const TokenKey = 'devicedp_token'
const InfoKey = 'user_info'
//const csrfKey = "csrf_token"

export function getToken() {
  return Cookies.get(TokenKey)
}

export function setToken(token) {
  var millisecond = new Date().getTime()
  var expiresTime = new Date(millisecond + 60 * 1000 * 60 * 5)
  return Cookies.set(TokenKey, token, {
    expires: expiresTime
  })
}

export function removeToken() {
  return Cookies.remove(TokenKey)
}

export function getUserCookie() {
  const cookies = Cookies.get();
  const info = Cookies.get(InfoKey);
  return info ? JSON.parse(info) : null;
}

export function setUserCookie(info) {
  var millisecond = new Date().getTime()
  var expiresTime = new Date(millisecond + 60 * 1000 * 60 * 5)
  return Cookies.set(InfoKey, JSON.stringify(info), {
    expires: expiresTime
  })
}

export function removeUserCookie() {
  return Cookies.remove(InfoKey)
}

// export function setCsrfToken(token) {
//   return Cookies.set(csrfKey, token)
// }