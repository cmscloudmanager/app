import './assets/main.scss'

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import { createVuetify } from 'vuetify';
import router from './router'

const app = createApp(App)
const vuetify = createVuetify()

app.use(createPinia())
app.use(router)
app.use(vuetify)

app.mount('#app')
