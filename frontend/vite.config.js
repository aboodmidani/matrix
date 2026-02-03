import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  define: {
    'import.meta.env.CORS_ORIGINS': JSON.stringify(process.env.CORS_ORIGINS)
  }
})
