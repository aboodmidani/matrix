<template>
  <div class="min-h-screen bg-black text-green-400 font-mono overflow-hidden relative">
    <!-- Matrix Background Animation -->
    <canvas id="matrix-canvas" class="fixed inset-0 z-0 opacity-20"></canvas>

    <!-- Navigation -->
    <nav class="sticky top-0 z-50 bg-black border-b border-green-500 shadow-lg">
      <div class="max-w-7xl mx-auto px-6">
        <div class="flex items-center justify-between h-16">
          <div class="flex items-center space-x-4">
            <div class="w-10 h-10 bg-gradient-to-br from-green-400 to-green-600 border border-green-500 flex items-center justify-center animate-pulse">
              <svg class="w-6 h-6 text-black font-bold" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"></path>
              </svg>
            </div>
            <div class="flex flex-col">
              <h1 class="text-lg font-bold bg-gradient-to-r from-green-400 to-green-300 bg-clip-text text-transparent font-mono tracking-wider">WEB SECURITY MATRIX</h1>
              <p class="text-xs text-green-600 font-mono tracking-wider">v3.0</p>
            </div>
          </div>
          
          <!-- Desktop Navigation -->
          <div class="hidden lg:flex items-center space-x-4">
            <div class="flex space-x-2">
              <router-link 
                v-for="route in routes" 
                :key="route.path"
                :to="route.path" 
                class="nav-link group"
              >
                <span class="relative">
                  {{ route.name }}
                  <span class="absolute -bottom-1 left-0 w-0 h-0.5 bg-gradient-to-r from-green-400 to-transparent transition-all duration-300 group-hover:w-full"></span>
                </span>
              </router-link>
            </div>
            <span class="text-xs text-green-600 font-mono">{{ currentTime.toLocaleTimeString() }}</span>
          </div>

          <!-- Mobile menu button -->
          <div class="lg:hidden flex items-center space-x-4">
            <!-- API Status Indicator -->
            <div class="flex items-center space-x-2">
              <div class="w-2 h-2 rounded-full" :class="apiStatus ? 'bg-green-400 animate-pulse' : 'bg-red-400'"></div>
              <span class="text-xs text-green-600 font-mono">{{ apiStatus ? 'ONLINE' : 'OFFLINE' }}</span>
            </div>
            
            <button 
              @click="toggleMobileMenu"
              class="text-green-400 hover:text-green-300 focus:outline-none transition-all duration-300 hover:scale-110"
              :class="{ 'text-green-300 scale-110': mobileMenuOpen }"
            >
              <div class="w-8 h-8 flex flex-col justify-center items-center">
                <span 
                  class="block w-6 h-0.5 bg-green-400 mb-1 transition-all duration-300"
                  :class="{ 'rotate-45 translate-y-1': mobileMenuOpen }"
                ></span>
                <span 
                  class="block w-6 h-0.5 bg-green-400 mb-1 transition-all duration-300"
                  :class="{ 'opacity-0 w-0': mobileMenuOpen }"
                ></span>
                <span 
                  class="block w-6 h-0.5 bg-green-400 transition-all duration-300"
                  :class="{ '-rotate-45 -translate-y-1': mobileMenuOpen }"
                ></span>
              </div>
            </button>
          </div>
        </div>
      </div>

      <!-- Mobile Navigation Drawer -->
      <transition
        enter-active-class="transition-all duration-300 ease-in-out"
        leave-active-class="transition-all duration-300 ease-in-out"
        enter-from-class="opacity-0 translate-x-full"
        enter-to-class="opacity-100 translate-x-0"
        leave-from-class="opacity-100 translate-x-0"
        leave-to-class="opacity-0 translate-x-full"
      >
        <div v-if="mobileMenuOpen" class="lg:hidden fixed inset-0 bg-black z-50">
          <!-- Close button -->
          <div class="flex justify-end p-6">
            <button 
              @click="toggleMobileMenu"
              class="text-green-400 hover:text-green-300 transition-all duration-300 text-3xl"
            >
              ✕
            </button>
          </div>

          <!-- Mobile Menu Content -->
          <div class="px-8 py-4">
            <div class="space-y-8">
              <div class="border-t border-green-500/30 pt-6">
                <h2 class="text-green-400 text-sm font-bold uppercase tracking-wider mb-4">Navigation</h2>
                <div class="space-y-2">
                  <router-link 
                    v-for="route in routes" 
                    :key="route.path"
                    :to="route.path" 
                    @click="toggleMobileMenu"
                    class="block text-green-400 hover:text-green-300 transition-all duration-300 font-bold text-lg border-l-4 border-transparent hover:border-green-400 pl-4 py-3 transform hover:translate-x-2"
                  >
                    {{ route.name }}
                  </router-link>
                </div>
              </div>

              <!-- Quick Actions -->
              <div class="border-t border-green-500/30 pt-6">
                <h2 class="text-green-400 text-sm font-bold uppercase tracking-wider mb-4">Quick Actions</h2>
                <div class="grid grid-cols-2 gap-3">
                  <button 
                    @click="toggleMobileMenu; $router.push('/')"
                    class="bg-green-500/10 hover:bg-green-500/20 border border-green-500/50 text-green-400 font-bold py-3 px-4 rounded transition-all duration-300 hover:scale-105"
                  >
                    Home
                  </button>
                  <button 
                    @click="toggleMobileMenu; $router.push('/dns-scan')"
                    class="bg-green-500/10 hover:bg-green-500/20 border border-green-500/50 text-green-400 font-bold py-3 px-4 rounded transition-all duration-300 hover:scale-105"
                  >
                    Quick Scan
                  </button>
                </div>
              </div>

              <!-- Footer Info -->
              <div class="border-t border-green-500/30 pt-6">
                <p class="text-green-600 text-xs text-center">
                  Web Security Matrix v3.0<br>
                  For educational and authorized security testing only.
                </p>
              </div>
            </div>
          </div>
        </div>
      </transition>
    </nav>

    <!-- Main Content -->
    <main class="relative z-10 px-4 py-8 max-w-7xl mx-auto">
      <router-view />
    </main>
  </div>
</template>

<script>
export default {
  name: 'App',
  data() {
    return {
      currentTime: new Date(),
      mobileMenuOpen: false,
      apiStatus: true
    }
  },
  computed: {
    routes() {
      return [
        { path: '/', name: 'HOME' },
        { path: '/subdomain-scan', name: 'SUBDOMAIN' },
        { path: '/dns-scan', name: 'DNS SCAN' },
        { path: '/port-scan', name: 'PORT SCAN' },
        // { path: '/directory-scan', name: 'DIRECTORY' },
        // { path: '/vulnerability-scan', name: 'VULNERABILITY' },
        { path: '/technology-scan', name: 'TECHNOLOGY' },
        { path: '/firewall-scan', name: 'FIREWALL' }
      ]
    }
  },
  mounted() {
    this.initMatrixRain()
    this.startLiveClock()
    this.checkAPIStatus()
  },
  beforeUnmount() {
    if (this.matrixCleanup) {
      this.matrixCleanup()
    }
  },
  methods: {
    toggleMobileMenu() {
      this.mobileMenuOpen = !this.mobileMenuOpen
    },
    startLiveClock() {
      setInterval(() => {
        this.currentTime = new Date()
      }, 1000)
    },
    async checkAPIStatus() {
      try {
        const response = await fetch('http://localhost:8000/health')
        this.apiStatus = response.ok
      } catch (error) {
        this.apiStatus = false
      }
    },
    initMatrixRain() {
      const canvas = document.getElementById('matrix-canvas')
      if (!canvas) return

      const ctx = canvas.getContext('2d')
      let animationId
      let lastTime = 0

      const resizeCanvas = () => {
        canvas.width = window.innerWidth
        canvas.height = window.innerHeight
      }

      resizeCanvas()

      const matrix = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ123456789@#$%^&*()*&^%+-/~{[|`]}'
      const matrixArray = matrix.split('')
      const fontSize = 14
      const columns = Math.floor(canvas.width / fontSize)
      const drops = new Array(columns).fill(1)

      const draw = (currentTime) => {
        if (currentTime - lastTime < 33) {
          animationId = requestAnimationFrame(draw)
          return
        }
        lastTime = currentTime

        ctx.fillStyle = 'rgba(0, 0, 0, 0.04)'
        ctx.fillRect(0, 0, canvas.width, canvas.height)

        ctx.fillStyle = '#00ff41'
        ctx.font = `${fontSize}px 'Courier New', monospace`

        for (let i = 0; i < drops.length; i++) {
          const text = matrixArray[Math.floor(Math.random() * matrixArray.length)]
          ctx.fillText(text, i * fontSize, drops[i] * fontSize)

          if (drops[i] * fontSize > canvas.height && Math.random() > 0.98) {
            drops[i] = 0
          }
          drops[i]++
        }

        animationId = requestAnimationFrame(draw)
      }

      const startAnimation = () => {
        if (animationId) cancelAnimationFrame(animationId)
        lastTime = 0
        animationId = requestAnimationFrame(draw)
      }

      window.addEventListener('resize', resizeCanvas)
      startAnimation()

      this.matrixCleanup = () => {
        if (animationId) cancelAnimationFrame(animationId)
        window.removeEventListener('resize', resizeCanvas)
      }
    }
  }
}
</script>

<style>
/* Navigation Link Styles */
.nav-link {
  @apply px-3 py-2 text-green-400 font-mono text-sm border border-green-500/30 rounded hover:bg-green-600/20 hover:text-green-300 transition-all duration-300 hover:scale-105;
}

/* Mobile-specific responsive styles */
@media (max-width: 640px) {
  /* Reduce matrix rain intensity on mobile for performance */
  #matrix-canvas {
    opacity: 0.1 !important
  }

  /* Touch-friendly button sizes */
  .touch-button {
    min-height: 44px
  }

  /* Better spacing for mobile cards */
  .mobile-card {
    padding: 1rem
  }

  /* Responsive text scaling */
  .responsive-text {
    font-size: clamp(0.875rem, 2.5vw, 1rem)
  }

  /* Improved touch targets */
  button {
    min-height: 44px
  }

    /* Better form inputs on mobile */
    input[type="text"], input[type="url"] {
      font-size: 16px;
      padding: 12px 16px;
    }

  /* Improved checkbox and radio button sizes */
  input[type="checkbox"], input[type="radio"] {
    width: 20px;
    height: 20px;
    margin-right: 8px;
  }
}

/* Performance optimizations for mobile */
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.05ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.05ms !important;
  }
}

/* High contrast mode support */
@media (prefers-contrast: high) {
  .matrix-bg {
    background: #000;
    opacity: 0.9;
  }

  #matrix-canvas {
    opacity: 0.05 !important;
  }
}

/* Print styles */
@media print {
  #matrix-canvas {
    display: none !important
  }

  .no-print {
    display: none !important
  }
}
</style>
