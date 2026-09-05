import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'
import { installI18n } from './i18n'

const app = createApp(App)

app.use(createPinia())
installI18n(app)
app.use(router)

app.mount('#app')
