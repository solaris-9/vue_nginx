import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import axios from 'axios'
import 'normalize.css/normalize.css'
import '@/styles/index.scss'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css' 


const app = createApp(App)

import '@/icons'
import '@/permission' // permission control
import SvgIcon from '@/components/SvgIcon'

app.use(ElementPlus)
app.component('svg-icon', SvgIcon)


axios.defaults.baseURL = 'http://0.0.0.0:8880'

app.use(store).use(router, axios).mount('#app')
