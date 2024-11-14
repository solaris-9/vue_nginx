import { createRouter, createWebHistory } from 'vue-router'

import login from '@/views/login/'
import home from '@/views/home'


const routes = [
  {
    path: '/',
    name: 'Home',
    component: home
  }, 
  {
    path: '/login',
    name: 'login',
    component: login
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

/* router.beforeEach((to, from, next) => {
  if (to.matched.some(record => record.meta.requireLogin) && !store.state.isAuthenticated) {
    next({ name: 'login', query: { to: to.path } });
  } else {
    next()
  }
}) */

export default router