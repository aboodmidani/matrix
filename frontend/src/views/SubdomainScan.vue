<template>
  <div class="bg-black border-2 border-green-500 rounded-lg p-6 shadow-2xl">
    <div class="flex items-center mb-4 text-green-400 text-sm font-mono">
      <span class="animate-pulse">●</span>
      <span class="ml-2">SUBDOMAIN DISCOVERY</span>
      <span class="ml-auto">SESSION: {{ sessionId }}</span>
    </div>

    <!-- Input Section -->
    <div class="border border-green-600 rounded p-4 md:p-6 bg-gray-900 mb-6">
      <div class="text-green-400 font-mono text-sm mb-3">
        <span class="text-green-300">></span> Enter target domain:
      </div>
      <div class="flex flex-col sm:flex-row gap-3">
        <input v-model="targetUrl" type="text" placeholder="example.com" class="flex-1 bg-black border border-green-500 rounded px-3 py-3 md:py-2 text-green-400 font-mono text-sm md:text-base focus:outline-none focus:border-green-400 transition-colors" />
        <button @click="startScan" :disabled="loading || !targetUrl.trim()" class="px-6 py-3 md:py-2 bg-green-600 hover:bg-green-500 disabled:bg-gray-600 text-black font-mono font-bold rounded border border-green-400 hover:border-green-300 transition-all duration-300 disabled:cursor-not-allowed min-h-[44px] touch-manipulation">
          <span v-if="loading" class="flex items-center">
            <span class="animate-spin mr-2">⟳</span>
            <span class="hidden sm:inline">SCANNING...</span>
            <span class="sm:hidden">SCANNING</span>
          </span>
          <span v-else>
            <span class="hidden sm:inline">START SUBDOMAIN SCAN</span>
            <span class="sm:hidden">SCAN</span>
          </span>
        </button>
      </div>
    </div>

    <!-- Progress Bar -->
    <div v-if="loading" class="mt-8 bg-black border-2 border-green-500 rounded-lg p-6">
      <div class="text-green-400 font-mono text-lg font-bold tracking-wider mb-4">
        <span class="text-green-300">[SUBDOMAIN SCAN IN PROGRESS]</span>
      </div>
      <div class="border border-green-600 rounded p-4 bg-gray-900">
        <div class="text-green-400 font-mono text-xs mb-2">
          <span class="text-green-300">root@matrix</span>:<span class="text-blue-400">~</span>$ subfinder -d {{ getDomain() }}
        </div>
        <div class="w-full bg-gray-700 h-2 rounded">
          <div class="bg-green-500 h-2 rounded animate-pulse" style="width: 100%"></div>
        </div>
        <div class="text-center text-green-300 font-mono text-xs mt-2">
          DISCOVERING SUBDOMAINS
        </div>
      </div>
    </div>

    <!-- Error Notification -->
    <div v-if="error" class="mt-8 bg-black border-2 border-red-500 rounded-lg p-6">
      <div class="text-red-400 font-mono text-sm mb-4">
        <span class="text-red-300">[ERROR]</span> Subdomain scan failed
      </div>
      <div class="border border-red-600 rounded p-4 bg-gray-900">
        <div class="text-red-400 font-mono text-xs mb-2">
          <span class="text-red-300">root@matrix</span>:<span class="text-blue-400">~</span>$ subfinder -d {{ getDomain() }}
        </div>
        <div class="text-red-300 font-mono text-xs">
          <span class="text-red-400">[ERROR]</span> {{ error }}
        </div>
      </div>
    </div>

    <!-- Results -->
    <div v-if="results" class="mt-8 bg-black bg-opacity-80 border border-green-500 rounded-lg p-6">
      <div class="flex justify-between items-center mb-4">
        <h3 class="text-xl font-bold text-green-400 flex items-center">
          <svg class="w-6 h-6 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 01-9 9m9-9a9 9 0 00-9-9m9 9H3m9 9v-9m0-9v9m0 9c-5 0-9-4-9-9s4-9 9-9"></path>
          </svg>
          Subdomain Discovery Results
        </h3>
        <div class="flex space-x-2">
          <button @click="downloadReport()" class="px-4 py-2 bg-blue-600 hover:bg-blue-500 text-black font-mono text-sm font-bold rounded border border-blue-400 transition-all duration-300">[DOWNLOAD]</button>
        </div>
      </div>
      <div class="border border-green-600 rounded p-4 bg-gray-900">
        <div class="text-green-400 font-mono text-sm mb-2">
          <span class="text-green-300">Target:</span> {{ results.url }}
        </div>
        <div class="text-green-400 font-mono text-sm mb-2">
          <span class="text-green-300">Domain:</span> {{ getDomain() }}
        </div>
        <div class="text-green-400 font-mono text-sm mb-2">
          <span class="text-green-300">Command:</span> {{ results.command }}
        </div>
        <div v-if="results.success" class="text-green-300 font-mono text-sm">
          <div class="text-green-400 font-bold">[SUCCESS]</div>
          <div class="mt-2">
            <div class="text-green-400 font-mono text-sm mb-2">DISCOVERED SUBDOMAINS ({{ results.subdomains ? results.subdomains.length : 0 }}):</div>
            <div v-if="results.subdomains && results.subdomains.length > 0" class="space-y-2">
              <div v-for="(subdomain, index) in results.subdomains" :key="index" class="bg-green-900/20 border border-green-500/30 rounded-md p-2">
                <div class="flex items-center justify-between">
                  <div>
                    <span class="text-green-300 font-mono text-xs">Subdomain:</span>
                    <p class="text-green-100 font-mono font-bold">{{ subdomain.subdomain }}</p>
                  </div>
                  <div class="text-green-400 font-mono text-xs">
                    {{ subdomain.source }}
                  </div>
                </div>
              </div>
            </div>
            <div v-else class="text-center py-4 text-green-400 font-mono">
              No subdomains discovered
            </div>
          </div>
        </div>
        <div v-else class="text-red-400 font-mono text-sm">
          <div class="text-red-400 font-bold">[FAILED]</div>
          <div class="mt-2 p-2 bg-black border border-red-600 rounded text-xs">{{ results.error }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { apiService, useApi } from '../utils/api'

const targetUrl = ref('')
const loading = ref(false)
const results = ref(null)
const error = ref(null)
const sessionId = Math.random().toString(36).substring(2, 8).toUpperCase()

const { executeRequest, clearError } = useApi()

const getDomain = () => {
  if (!targetUrl.value) return ''
  try {
    const url = new URL(targetUrl.value.startsWith('http') ? targetUrl.value : `https://${targetUrl.value}`)
    return url.hostname
  } catch {
    return targetUrl.value
  }
}

const startScan = async () => {
  if (!targetUrl.value.trim()) {
    error.value = 'Please enter a valid domain name (e.g., example.com)'
    return
  }

  loading.value = true
  error.value = null
  results.value = null

  try {
    const result = await executeRequest(() => 
      apiService.postForm('/scan/subdomains', new URLSearchParams({
        url: targetUrl.value.trim()
      }))
    )
    
    results.value = result
  } catch (err) {
    error.value = err.message || 'Subdomain scan failed'
  } finally {
    loading.value = false
  }
}

const downloadReport = async () => {
  if (!results.value) return
  
  try {
    await apiService.downloadReport(results.value, 'subdomains')
  } catch (error) {
    console.error('Download error:', error)
    alert('Failed to download report')
  }
}

// Initialize
onMounted(() => {
  // Clear any previous errors
  clearError()
})
</script>

<style scoped>
/* Enhanced animations */
.animate-pulse {
  animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

.animate-spin {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

/* Custom scrollbar */
::-webkit-scrollbar {
  width: 8px;
}

::-webkit-scrollbar-track {
  background: #000;
}

::-webkit-scrollbar-thumb {
  background: #00ff41;
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: #00cc33;
}

/* Enhanced hover effects */
button:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 20px rgba(0, 255, 65, 0.3);
}

input:focus {
  box-shadow: 0 0 0 3px rgba(0, 255, 65, 0.2);
}

/* Responsive design improvements */
@media (max-width: 768px) {
  .hidden-sm {
    display: none;
  }
}
</style>