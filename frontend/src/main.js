import { createApp } from 'vue'
import './style.css'
import 'animate.css'
import App from './App.vue'

console.log('API URL from build:', __API_URL__);

createApp(App).mount('#app')
