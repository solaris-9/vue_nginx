import request from '@/utils/request'

export function loginApi(data) {
  return request({
    url: '/login/login',
    method: 'post',
    data
  })
}

export function userInfoApi(token) {

  return request({
    url: '/login/info',
    method: 'get',
    params: { token }
  })
}

export function logoutApi(data) {
  return request({
    url: '/login/logout',
    method: 'post',
    data
  })
}


