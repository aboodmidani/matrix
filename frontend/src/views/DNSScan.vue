<template>
  <div class="bg-black border-2 border-green-500 rounded-lg p-6 shadow-2xl">
    <div class="flex items-center mb-4 text-green-400 text-sm font-mono">
      <span class="animate-pulse">●</span>
      <span class="ml-2">DNS RECONNAISSANCE</span>
      <span class="ml-auto">SESSION: {{ sessionId }}</span>
    </div>

    <!-- Input Section -->
    <div class="border border-green-600 rounded p-4 md:p-6 bg-gray-900 mb-6">
      <div class="text-green-400 font-mono text-sm mb-3">
        <span class="text-green-300">></span> Enter target URL:
      </div>
      <div class="flex flex-col sm:flex-row gap-3">
        <input v-model="targetUrl" type="text" placeholder="https://target-system.com" class="flex-1 bg-black border border-green-500 rounded px-3 py-3 md:py-2 text-green-400 font-mono text-sm md:text-base focus:outline-none focus:border-green-400 transition-colors" />
        <button @click="startScan" :disabled="loading || !targetUrl.trim()" class="px-6 py-3 md:py-2 bg-green-600 hover:bg-green-500 disabled:bg-gray-600 text-black font-mono font-bold rounded border border-green-400 hover:border-green-300 transition-all duration-300 disabled:cursor-not-allowed min-h-[44px] touch-manipulation">
          <span v-if="loading" class="flex items-center">
            <span class="animate-spin mr-2">⟳</span>
            <span class="hidden sm:inline">SCANNING...</span>
            <span class="sm:hidden">SCANNING</span>
          </span>
          <span v-else>
            <span class="hidden sm:inline">START DNS SCAN</span>
            <span class="sm:hidden">SCAN</span>
          </span>
        </button>
      </div>
    </div>

    <!-- Progress Bar -->
    <div v-if="loading" class="mt-8 bg-black border-2 border-green-500 rounded-lg p-6">
      <div class="text-green-400 font-mono text-lg font-bold tracking-wider mb-4">
        <span class="text-green-300">[DNS SCAN IN PROGRESS]</span>
      </div>
      <div class="border border-green-600 rounded p-4 bg-gray-900">
        <div class="text-green-400 font-mono text-xs mb-2">
          <span class="text-green-300">root@matrix</span>:<span class="text-blue-400">~</span>$ dnsrecon -d {{ getDomain() }}
        </div>
        <div class="w-full bg-gray-700 h-2 rounded">
          <div class="bg-green-500 h-2 rounded animate-pulse" style="width: 100%"></div>
        </div>
        <div class="text-center text-green-300 font-mono text-xs mt-2">
          EXECUTING DNS RECONNAISSANCE
        </div>
      </div>
    </div>

    <!-- Error Notification -->
    <div v-if="error" class="mt-8 bg-black border-2 border-red-500 rounded-lg p-6">
      <div class="text-red-400 font-mono text-sm mb-4">
        <span class="text-red-300">[ERROR]</span> DNS scan failed
      </div>
      <div class="border border-red-600 rounded p-4 bg-gray-900">
        <div class="text-red-400 font-mono text-xs mb-2">
          <span class="text-red-300">root@matrix</span>:<span class="text-blue-400">~</span>$ dnsrecon -d {{ getDomain() }}
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
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2H5a2 2 0 00-2-2z"></path>
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 5a2 2 0 012-2h4a2 2 0 012 2v2H8V5z"></path>
          </svg>
          DNS Scan Results
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
          <pre class="mt-2 p-2 bg-black border border-green-600 rounded text-xs overflow-auto max-h-96">{{ results.output }}</pre>
        </div>
        <div v-else class="text-red-400 font-mono text-sm">
          <div class="text-red-400 font-bold">[FAILED]</div>
          <div class="mt-2 p-2 bg-black border border-red-600 rounded text-xs">{{ results.error }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import { apiService } from '../utils/api'

// XSS Protection: Sanitize URL input
const sanitizeUrl = (url) => {
  if (!url) return ''
  
  // Remove any HTML/script tags
  let sanitized = url.replace(/<[^>]*>/g, '')
  
  // Remove javascript: protocol and other dangerous protocols
  sanitized = sanitized.replace(/^(javascript|data|vbscript|file):/i, '')
  
  // Remove any whitespace that could be used for bypass
  sanitized = sanitized.trim()
  
  // Only allow http:// and https:// protocols, or no protocol (will add https://)
  const urlPattern = /^(https?:\/\/)?[a-zA-Z0-9]([a-zA-Z0-9-]*[a-zA-Z0-9])?(\.[a-zA-Z0-9]([a-zA-Z0-9-]*[a-zA-Z0-9])?)*(:[0-9]{1,5})?(\/[^\s]*)?$/
  if (!urlPattern.test(sanitized)) {
    return ''
  }
  
  return sanitized
}

// Escape HTML entities for safe display
const escapeHtml = (text) => {
  if (!text) return ''
  const map = {
    '&': '&',
    '<': '<',
    '>': '>',
    '"': '"',
    "'": '&#039;'
  }
  return String(text).replace(/[&<>"']/g, m => map[m])
}

export default {
  name: 'DNSScan',
  setup() {
    const targetUrl = ref('')
    const loading = ref(false)
    const results = ref(null)
    const error = ref(null)
    const sessionId = Math.random().toString(36).substring(2, 8).toUpperCase()

    const getDomain = () => {
      if (!targetUrl.value) return ''
      try {
        const url = new URL(targetUrl.value)
        return url.hostname
      } catch {
        return targetUrl.value
      }
    }

    const startScan = async () => {
      // XSS Protection: Sanitize the URL before processing
      const sanitizedUrl = sanitizeUrl(targetUrl.value)
      
      if (!sanitizedUrl) {
        error.value = 'Please enter a valid URL (e.g., https://example.com)'
        return
      }

      loading.value = true
      error.value = null
      results.value = null

      try {
        // Use apiService which respects environment variables
        const formData = new URLSearchParams()
        formData.append('url', sanitizedUrl)
        
        const response = await fetch(`${apiService.baseURL}/scan/dns`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
          },
          body: formData
        })

        if (response.ok) {
          const data = await response.json()
          // XSS Protection: Sanitize response data before storing
          if (data.output) {
            data.output = escapeHtml(data.output)
          }
          results.value = data
        } else {
          const errorData = await response.json().catch(() => ({}))
          throw new Error(errorData.detail || 'DNS scan failed')
        }
      } catch (err) {
        error.value = err.message || 'DNS scan failed'
      } finally {
        loading.value = false
      }
    }

    const downloadReport = async () => {
      if (!results.value) return

      try {
        // Use apiService which respects environment variables
        await apiService.downloadReport(results.value, 'dns')
      } catch (error) {
        console.error('Download error:', error)
        alert('Failed to download report')
      }
    }

    return {
      targetUrl,
      loading,
      results,
      error,
      sessionId,
      startScan,
      downloadReport,
      getDomain
    }
  }
}
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