import { createApp } from 'vue'
import { createHead } from '@unhead/vue'
import { createGtag } from 'vue-gtag'
import './style.css'
import App from './App.vue'

const app = createApp(App)

const head = createHead()
app.use(head)

const gaId = import.meta.env.VITE_GA_ID
if (gaId) {
  const gtagPlugin = createGtag({
    config: { id: gaId, params: { send_page_view: true } },
  })
  app.use(gtagPlugin)
}

app.mount('#app')
