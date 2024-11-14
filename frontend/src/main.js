import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import axios from 'axios'
import 'normalize.css/normalize.css'
import '@/styles/index.scss'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css' 
//import InstallIcons from '@/icons'
/* import { library } from '@fortawesome/fontawesome-svg-core'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { faUser } from '@fortawesome/free-solid-svg-icons'
import { faLock } from '@fortawesome/free-solid-svg-icons' */

/* add icons to the library */
/* library.add(faUser)
library.add(faLock) */


const app = createApp(App)

import '@/icons'
import '@/permission' // permission control
import SvgIcon from '@/components/SvgIcon'

app.use(ElementPlus)
app.component('svg-icon', SvgIcon)
//app.component("font-awesome-icon", FontAwesomeIcon);
//InstallIcons(app)

axios.defaults.baseURL = 'http://0.0.0.0:8880'

app.use(store).use(router, axios).mount('#app')
