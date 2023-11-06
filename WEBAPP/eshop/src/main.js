import './assets/main.css'

import { createApp, watch } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
// Vuetify
import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'

const vuetify = createVuetify({
  components,
  directives
})
const pinia = createPinia()

pinia.use((context) => {
  const storeId = context.store.$id

  const serializer = {
    serialize: JSON.stringify,
    deserialize: JSON.parse
  }

  const fromStorage = serializer.deserialize(window.localStorage.getItem(storeId))

  if (fromStorage) {
    context.store.$patch(fromStorage)
  }
  context.store.$subscribe((mutation, state) => {
    window.localStorage.setItem(storeId, serializer.serialize(state))
  })
})
const app = createApp(App)

app.use(createPinia())
app.use(router)
app.use(vuetify)
app.use(pinia)
app.mount('#app')
