<template>
  <div class="min-h-screen bg-black text-green-400 font-mono relative overflow-hidden">
    <MatrixBackground />
    <main class="relative z-10 max-w-5xl mx-auto px-4 py-8">
      <div class="text-center mb-8" data-aos="fade-in">
        <h1 class="text-4xl font-bold text-green-400 mb-2">MATRIX SCANNER</h1>
        <p class="text-green-600">Web Security Assessment Platform</p>
      </div>
      <div v-if="!acceptedDisclaimer" class="bg-black/90 border border-yellow-500/50 rounded-lg p-6 mb-8 max-w-xl mx-auto" data-aos="fade-in">
        <div class="text-center">
          <h2 class="text-xl font-bold text-yellow-400 mb-2">[LEGAL DISCLAIMER]</h2>
          <p class="text-green-400 text-sm mb-4">This tool is for educational and authorized security testing only.</p>
          <button @click="acceptDisclaimer" class="px-6 py-2 bg-green-600 hover:bg-green-500 text-black font-bold rounded border border-green-400 transition-all" data-aos="fade-up">[ACCEPT & CONTINUE]</button>
        </div>
      </div>
      <div v-show="acceptedDisclaimer" class="mb-8" data-aos="fade-down">
        <div class="bg-black/90 border border-green-500/50 rounded-lg p-6">
          <div class="flex flex-col md:flex-row gap-4">
            <div class="flex-1 relative">
              <span class="absolute left-4 top-1/2 -translate-y-1/2 text-green-500">></span>
              <input v-model="targetUrl" type="text" placeholder="Enter target URL (e.g., https://example.com)" class="w-full bg-gray-900/50 border border-green-500/50 rounded-lg pl-10 pr-4 py-3 text-green-400 placeholder-green-600/50 focus:outline-none focus:border-green-400 transition-all" @keyup.enter="startScan" />
            </div>
            <button @click="startScan" :disabled="!targetUrl || scanState.isScanning" class="px-8 py-3 bg-green-600 hover:bg-green-500 disabled:bg-gray-600 text-black font-bold rounded border border-green-400 transition-all disabled:cursor-not-allowed">
              {{ scanState.isScanning ? 'SCANNING...' : 'START SCAN' }}
            </button>
          </div>
          <div class="flex gap-2 mt-4">
            <button @click="targetUrl = 'https://codiay.com'" class="text-xs text-green-500 hover:text-green-400">[codiay.com]</button>
            <button @click="targetUrl = 'https://example.com'" class="text-xs text-green-500 hover:text-green-400">[example.com]</button>
          </div>
        </div>
        <div v-if="scanState.isScanning" class="mt-4 bg-black/90 border border-green-500/30 rounded-lg p-4" data-aos="fade-in">
          <div class="flex justify-between mb-2">
            <span class="text-sm text-green-400">{{ scanState.currentScan }}</span>
            <span class="text-sm text-green-500">{{ scanState.progress }}%</span>
          </div>
          <div class="h-2 bg-gray-800 rounded-full overflow-hidden">
            <div class="h-full bg-gradient-to-r from-green-600 to-green-400 transition-all" :style="{ width: `${scanState.progress}%` }"></div>
          </div>
        </div>
      </div>
      <div v-if="scanState.results" class="space-y-4">
        <div class="flex justify-between bg-black/90 border border-green-500/50 rounded-lg p-4" data-aos="fade-in">
          <div>
            <h2 class="text-lg font-bold text-green-400">SCAN RESULTS</h2>
            <p class="text-xs text-green-600">{{ targetUrl }}</p>
          </div>
          <button @click="resetScans" class="px-4 py-2 bg-gray-700 hover:bg-gray-600 text-white text-sm rounded border border-gray-500">NEW SCAN</button>
        </div>
        <div v-for="(config, key) in scanConfigs" :key="key" v-show="scans[key].status !== 'idle'" class="bg-black/90 border rounded-lg overflow-hidden" :class="`border-${config.color}-500/50`" data-aos="fade-up">
          <button @click="toggleSection(key)" class="w-full px-6 py-4 flex items-center justify-between hover:bg-opacity-10 transition-colors" :class="`hover:bg-${config.color}-500/10`">
            <div class="flex items-center space-x-3">
              <span class="text-xl">{{ config.icon }}</span>
              <span class="font-bold" :class="`text-${config.color}-400`">{{ config.name }}</span>
              <span v-if="scans[key].status === 'scanning'" class="text-sm text-yellow-400 animate-pulse">[SCANNING...]</span>
              <span v-else-if="scans[key].status === 'complete'" class="text-sm text-green-400">[COMPLETE]</span>
              <span v-else class="text-sm text-red-400">[ERROR]</span>
            </div>
            <svg class="w-5 h-5 transition-transform" :class="`text-${config.color}-400 ${sections[key] ? 'rotate-180' : ''}`" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path>
            </svg>
          </button>
          <div v-if="sections[key]" class="px-6 pb-4 border-t" :class="`border-${config.color}-30`">
            <div v-if="scans[key].data && scans[key].status === 'complete'" class="mt-4">
              <p class="text-green-500 text-sm">Results available</p>
            </div>
            <p v-else-if="scans[key].error" class="text-red-400 text-sm mt-4">{{ scans[key].error }}</p>
            <p v-else class="text-green-500 text-sm mt-4">No results found</p>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script>
import { ref, reactive, onMounted } from 'vue'
import AOS from 'aos'
import 'aos/dist/aos.css'
import MatrixBackground from '../components/MatrixBackground.vue'
import { useScanner } from '../composables/useScanner'

export default {
  name: 'Home',
  components: { MatrixBackground },
  setup() {
    const { scanState, scans, scanConfigs, runAllScans, resetScans } = useScanner()
    const targetUrl = ref('')
    const acceptedDisclaimer = ref(false)
    const sections = reactive({ dns: true, ports: true, technology: true, firewall: true, subdomain: true })

    const toggleSection = (key) => { sections[key] = !sections[key] }
    const acceptDisclaimer = () => { acceptedDisclaimer.value = true; localStorage.setItem('disclaimerAccepted', 'true') }
    const startScan = async () => { if (targetUrl.value) { Object.keys(sections).forEach(k => sections[k] = true); await runAllScans(targetUrl.value) } }

    onMounted(() => {
      AOS.init({ duration: 500, once: true })
      acceptedDisclaimer.value = localStorage.getItem('disclaimerAccepted') === 'true'
    })

    return { targetUrl, scanState, scans, scanConfigs, sections, acceptedDisclaimer, toggleSection, acceptDisclaimer, startScan, resetScans }
  }
}
</script>
