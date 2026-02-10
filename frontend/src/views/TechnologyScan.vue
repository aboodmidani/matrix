<template>
  <div class="bg-black border-2 border-purple-500 rounded-lg p-6 shadow-2xl">
    <div class="flex items-center mb-4 text-purple-400 text-sm font-mono">
      <span class="animate-pulse">●</span>
      <span class="ml-2">{{ scanTitle }}</span>
      <span class="ml-auto">{{ sessionLabel }}: {{ sessionId }}</span>
    </div>

    <!-- Input Section -->
    <div class="border border-purple-600 rounded p-4 md:p-6 bg-gray-900 mb-6">
      <div class="text-purple-400 font-mono text-sm mb-3">
        <span class="text-purple-300">></span> {{ enterTargetLabel }}
      </div>
      <div class="flex flex-col sm:flex-row gap-3">
        <input v-model="targetUrl" type="text" :placeholder="placeholderText" class="flex-1 bg-black border border-purple-500 rounded px-3 py-3 md:py-2 text-purple-400 font-mono text-sm md:text-base focus:outline-none focus:border-purple-400 transition-all duration-300" />
        <button @click="startScan" :disabled="loading || !targetUrl.trim()" class="px-6 py-3 md:py-2 bg-purple-600 hover:bg-purple-500 disabled:bg-gray-600 text-black font-mono font-bold rounded border border-purple-400 hover:border-purple-300 transition-all duration-300 disabled:cursor-not-allowed min-h-[44px] touch-manipulation relative overflow-hidden">
          <span v-if="loading" class="flex items-center justify-center">
            <svg class="animate-spin mr-2 h-5 w-5" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" fill="none"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            <span>{{ scanningLabel }}</span>
          </span>
          <span v-else class="flex items-center">
            <span class="hidden sm:inline">{{ startScanLabel }}</span>
            <span class="sm:hidden">{{ scanLabel }}</span>
          </span>
        </button>
      </div>
    </div>

    <!-- Progress Animation -->
    <transition name="fade">
      <div v-if="loading" class="mt-8 bg-black border-2 border-purple-500 rounded-lg p-6">
        <div class="flex items-center justify-between mb-4">
          <span class="text-purple-400 font-mono text-lg font-bold tracking-wider">
            {{ processingMessage }}
          </span>
          <div class="flex space-x-1">
            <div class="w-2 h-2 bg-purple-500 rounded-full animate-bounce" style="animation-delay: 0s"></div>
            <div class="w-2 h-2 bg-purple-500 rounded-full animate-bounce" style="animation-delay: 0.1s"></div>
            <div class="w-2 h-2 bg-purple-500 rounded-full animate-bounce" style="animation-delay: 0.2s"></div>
          </div>
        </div>
        <div class="border border-purple-600 rounded p-4 bg-gray-900">
          <div class="text-purple-400 font-mono text-xs mb-3">
            <span class="text-purple-300">root@matrix</span>:<span class="text-blue-400">~</span>$ {{ commandDisplay }}
          </div>
          <div class="relative h-8 bg-gray-800 rounded border border-purple-700 overflow-hidden">
            <div class="absolute inset-0 flex items-center justify-center">
              <div class="flex space-x-1">
                <template v-for="i in 20" :key="i">
                  <div 
                    class="w-1 h-4 bg-purple-500 rounded-sm transition-all duration-300"
                    :class="{ 'h-6 bg-purple-400': loading, 'h-2 bg-purple-700': !loading }"
                    :style="{ 'animation-delay': `${(i * 0.05)}s` }"
                  ></div>
                </template>
              </div>
            </div>
          </div>
          <div class="text-center text-purple-400 font-mono text-xs mt-2">
            {{ executingLabel }}
          </div>
        </div>
      </div>
    </transition>

    <!-- Error Notification -->
    <transition name="slide-fade">
      <div v-if="error" class="mt-8 bg-black border-2 border-red-500 rounded-lg p-6">
        <div class="flex items-center mb-4">
          <svg class="w-6 h-6 text-red-500 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z"></path>
          </svg>
          <span class="text-red-400 font-mono text-sm font-bold">{{ errorTitle }}</span>
        </div>
        <div class="border border-red-600 rounded p-4 bg-gray-900">
          <div class="text-red-400 font-mono text-xs mb-2">
            <span class="text-red-300">root@matrix</span>:<span class="text-blue-400">~</span>$ {{ commandDisplay }}
          </div>
          <div class="text-red-400 font-mono text-sm bg-red-900/20 border border-red-700 rounded p-3">
            <span class="text-red-500 font-bold">[ERROR]</span> {{ error }}
          </div>
        </div>
      </div>
    </transition>

    <!-- Results -->
    <transition name="slide-up">
      <div v-if="results" class="mt-8 bg-black bg-opacity-90 border border-purple-500 rounded-lg p-6">
        <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center mb-4 gap-2">
          <h3 class="text-xl font-bold text-purple-400 flex items-center">
            <svg class="w-6 h-6 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"></path>
            </svg>
            {{ resultsTitle }}
          </h3>
          <button @click="downloadReport" class="px-4 py-2 bg-purple-600 hover:bg-purple-500 text-black font-mono text-sm font-bold rounded border border-purple-400 transition-all duration-300 hover:shadow-lg hover:shadow-purple-500/20 flex items-center">
            <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"></path>
            </svg>
            {{ downloadLabel }}
          </button>
        </div>
        
        <div class="border border-purple-600 rounded p-4 bg-gray-900">
          <div class="grid grid-cols-1 sm:grid-cols-3 gap-3 mb-4 pb-4 border-b border-purple-700">
            <div class="text-purple-400 font-mono text-sm">
              <span class="text-purple-500">{{ targetLabel }}</span>
              <div class="text-purple-200 break-all">{{ results.url }}</div>
            </div>
            <div class="text-purple-400 font-mono text-sm">
              <span class="text-purple-500">{{ toolLabel }}</span>
              <div class="text-purple-200">{{ results.tool_name }}</div>
            </div>
            <div class="text-purple-400 font-mono text-sm">
              <span class="text-purple-500">{{ detectedLabel }}</span>
              <div class="text-purple-200">{{ technologiesCount }} {{ techLabel }}</div>
            </div>
          </div>
          
          <div class="mb-4">
            <div class="text-purple-500 font-mono text-xs mb-1">{{ commandLabel }}</div>
            <div class="text-purple-300 font-mono text-sm bg-black rounded p-2 border border-purple-700">
              {{ results.command }}
            </div>
          </div>

          <div v-if="results.technologies && Object.keys(results.technologies).length > 0" class="space-y-2">
            <div class="text-purple-500 font-mono text-xs mb-1 uppercase">{{ technologiesLabel }}</div>
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-2">
              <div v-for="(tech, name) in results.technologies" :key="name" class="bg-purple-900/20 border border-purple-500/30 rounded-md p-3">
                <div class="text-purple-300 font-mono font-bold">{{ name }}</div>
                <div class="text-purple-400 font-mono text-xs" v-if="tech.version">Version: {{ tech.version }}</div>
                <div class="text-purple-400 font-mono text-xs" v-if="tech.confidence">Confidence: {{ tech.confidence }}%</div>
              </div>
            </div>
          </div>
          
          <div v-if="results.success" class="mt-4 pt-4 border-t border-purple-700">
            <div class="flex items-center text-purple-400">
              <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
              </svg>
              <span class="font-mono font-bold">{{ successMessage }}</span>
            </div>
          </div>
        </div>
      </div>
    </transition>
  </div>
</template>

<script>
import { ref, computed } from 'vue'
import { apiService } from '../utils/api'

export default {
  name: 'TechnologyScan',
  setup() {
    const targetUrl = ref('')
    const loading = ref(false)
    const results = ref(null)
    const error = ref(null)
    const sessionId = ref(Math.random().toString(36).substring(2, 8).toUpperCase())
    
    const labels = ref({
      scanTitle: 'TECHNOLOGY DETECTION',
      sessionLabel: 'SESSION',
      enterTargetLabel: 'Enter target URL:',
      placeholderText: 'https://target-system.com',
      startScanLabel: 'START TECHNOLOGY SCAN',
      scanLabel: 'SCAN',
      scanningLabel: 'SCANNING...',
      processingMessage: 'ANALYZING TARGET TECHNOLOGIES',
      executingLabel: 'EXECUTING TECHNOLOGY DETECTION',
      errorTitle: 'TECHNOLOGY SCAN FAILED',
      resultsTitle: 'TECHNOLOGY SCAN RESULTS',
      downloadLabel: '[DOWNLOAD]',
      targetLabel: 'Target:',
      toolLabel: 'Tool:',
      commandLabel: 'Command:',
      detectedLabel: 'Detected:',
      technologiesLabel: 'IDENTIFIED TECHNOLOGIES',
      techLabel: 'technologies',
      successMessage: 'TECHNOLOGY SCAN COMPLETED'
    })

    const technologiesCount = computed(() => {
      if (results.value && results.value.technologies) {
        return Object.keys(results.value.technologies).length
      }
      return 0
    })

    const commandDisplay = computed(() => {
      if (results.value) {
        return results.value.command
      }
      return `wappalyzer ${targetUrl.value || '<target>'}`
    })

    const startScan = async () => {
      if (!targetUrl.value.trim()) {
        error.value = 'Please enter a valid URL'
        return
      }

      loading.value = true
      error.value = null
      results.value = null

      try {
        const formData = new URLSearchParams()
        formData.append('url', targetUrl.value.trim())
        
        const response = await fetch(`${apiService.baseURL}/scan/technologies`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
          },
          body: formData
        })

        if (response.ok) {
          const data = await response.json()
          results.value = data
          
          if (data.message) {
            labels.value = { ...labels.value, ...data.message }
          }
        } else {
          const errorData = await response.json().catch(() => ({}))
          throw new Error(errorData.detail || 'Technology scan failed')
        }
      } catch (err) {
        error.value = err.message || 'Technology scan failed'
      } finally {
        loading.value = false
      }
    }

    const downloadReport = async () => {
      if (!results.value) return
      try {
        await apiService.downloadReport(results.value, 'technologies')
      } catch (err) {
        console.error('Download error:', err)
        alert('Failed to download report')
      }
    }

    return {
      targetUrl, loading, results, error, sessionId, labels, technologiesCount,
      commandDisplay, startScan, downloadReport,
      scanTitle: computed(() => labels.value.scanTitle),
      sessionLabel: computed(() => labels.value.sessionLabel),
      enterTargetLabel: computed(() => labels.value.enterTargetLabel),
      placeholderText: computed(() => labels.value.placeholderText),
      startScanLabel: computed(() => labels.value.startScanLabel),
      scanLabel: computed(() => labels.value.scanLabel),
      scanningLabel: computed(() => labels.value.scanningLabel),
      processingMessage: computed(() => labels.value.processingMessage),
      executingLabel: computed(() => labels.value.executingLabel),
      errorTitle: computed(() => labels.value.errorTitle),
      resultsTitle: computed(() => labels.value.resultsTitle),
      downloadLabel: computed(() => labels.value.downloadLabel),
      targetLabel: computed(() => labels.value.targetLabel),
      toolLabel: computed(() => labels.value.toolLabel),
      commandLabel: computed(() => labels.value.commandLabel),
      detectedLabel: computed(() => labels.value.detectedLabel),
      technologiesLabel: computed(() => labels.value.technologiesLabel),
      techLabel: computed(() => labels.value.techLabel),
      successMessage: computed(() => labels.value.successMessage)
    }
  }
}
</script>

<style scoped>
.fade-enter-active, .fade-leave-active { transition: opacity 0.3s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; }
.slide-fade-enter-active { transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1); }
.slide-fade-leave-active { transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1); }
.slide-fade-enter-from, .slide-fade-leave-to { transform: translateY(-10px); opacity: 0; }
.slide-up-enter-active { transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1); }
.slide-up-leave-active { transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1); }
.slide-up-enter-from { transform: translateY(20px); opacity: 0; }
.slide-up-leave-to { transform: translateY(0); opacity: 0; }
::-webkit-scrollbar { width: 8px; }
::-webkit-scrollbar-track { background: #000; }
::-webkit-scrollbar-thumb { background: #9333ea; border-radius: 4px; }
::-webkit-scrollbar-thumb:hover { background: #7e22ce; }
button:hover { transform: translateY(-2px); box-shadow: 0 4px 20px rgba(147, 51, 234, 0.3); }
input:focus { box-shadow: 0 0 0 3px rgba(147, 51, 234, 0.2); }
@media (max-width: 768px) { .hidden-sm { display: none; } }
</style>
