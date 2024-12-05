import request from '@/utils/request'

export function loginApi(data) {
  return request({
    url: '/user/login',
    method: 'post',
    data
  })
}

export function userInfoApi(token) {

  return request({
    url: '/user/info',
    method: 'get',
    params: { token }
  })
}

export function logoutApi(data) {
  return request({
    url: '/user/logout',
    method: 'post',
    data
  })
}


