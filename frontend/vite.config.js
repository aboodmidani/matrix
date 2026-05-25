import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import Sitemap from 'vite-plugin-sitemap'

export default defineConfig({
  plugins: [
    vue(),
    Sitemap({
      hostname: process.env.VITE_SITE_URL || 'https://matrixscanner.app/',
      dynamicRoutes: ['/', '/privacy', '/terms'],
      exclude: ['/admin'],
      changefreq: 'weekly',
      priority: 1.0,
    }),
  ],
})
