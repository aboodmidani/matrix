<template>
  <div class="bg-black border-2 border-blue-500 rounded-lg p-6 shadow-2xl">
    <div class="flex items-center mb-4 text-blue-400 text-sm font-mono">
      <span class="animate-pulse">●</span>
      <span class="ml-2">{{ scanTitle }}</span>
      <span class="ml-auto">{{ sessionLabel }}: {{ sessionId }}</span>
    </div>
    <div class="border border-blue-600 rounded p-4 md:p-6 bg-gray-900 mb-6">
      <div class="text-blue-400 font-mono text-sm mb-3">
        <span class="text-blue-300">></span> {{ enterTargetLabel }}
      </div>
      <div class="flex flex-col sm:flex-row gap-3">
        <input v-model="targetUrl" type="text" :placeholder="placeholderText" class="flex-1 bg-black border border-blue-500 rounded px-3 py-3 md:py-2 text-blue-400 font-mono text-sm md:text-base focus:outline-none focus:border-blue-400 transition-all duration-300" />
        <button @click="startScan" :disabled="loading || !targetUrl.trim()" class="px-6 py-3 md:py-2 bg-blue-600 hover:bg-blue-500 disabled:bg-gray-600 text-black font-mono font-bold rounded border border-blue-400 hover:border-blue-300 transition-all duration-300 disabled:cursor-not-allowed min-h-[44px]">
          <span v-if="loading">{{ scanningLabel }}</span>
          <span v-else>{{ startScanLabel }}</span>
        </button>
      </div>
    </div>
    <transition name="fade">
      <div v-if="loading" class="mt-8 bg-black border-2 border-blue-500 rounded-lg p-6">
        <div class="flex items-center justify-between mb-4">
          <span class="text-blue-400 font-mono text-lg font-bold tracking-wider">{{ processingMessage }}</span>
          <div class="flex space-x-1">
            <div class="w-2 h-2 bg-blue-500 rounded-full animate-bounce" style="animation-delay: 0s"></div>
            <div class="w-2 h-2 bg-blue-500 rounded-full animate-bounce" style="animation-delay: 0.1s"></div>
            <div class="w-2 h-2 bg-blue-500 rounded-full animate-bounce" style="animation-delay: 0.2s"></div>
          </div>
        </div>
        <div class="border border-blue-600 rounded p-4 bg-gray-900">
          <div class="text-blue-400 font-mono text-xs mb-2">
            <span class="text-blue-300">root@matrix</span>:<span class="text-blue-400">~</span>$ {{ commandDisplay }}
          </div>
          <div class="text-center text-blue-400 font-mono text-xs mt-2">{{ executingLabel }}</div>
        </div>
      </div>
    </transition>
    <transition name="slide-fade">
      <div v-if="error" class="mt-8 bg-black border-2 border-red-500 rounded-lg p-6">
        <div class="flex items-center mb-4">
          <span class="text-red-400 font-mono text-sm font-bold">{{ errorTitle }}</span>
        </div>
        <div class="border border-red-600 rounded p-4 bg-gray-900">
          <div class="text-red-400 font-mono text-xs mb-2">
            <span class="text-red-300">root@matrix</span>:<span class="text-blue-400">~</span>$ {{ commandDisplay }}
          </div>
          <div class="text-red-400 font-mono text-sm">{{ error }}</div>
        </div>
      </div>
    </transition>
    <transition name="slide-up">
      <div v-if="results" class="mt-8 bg-black bg-opacity-90 border border-blue-500 rounded-lg p-6">
        <div class="flex justify-between items-center mb-4">
          <h3 class="text-xl font-bold text-blue-400 flex items-center">
            <svg class="w-6 h-6 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2H5a2 2 0 00-2 2z"></path>
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 5a2 2 0 012-2h4a2 2 0 012 2v2H8V5z"></path>
            </svg>
            {{ resultsTitle }}
          </h3>
          <button @click="downloadReport" class="px-4 py-2 bg-blue-600 hover:bg-blue-500 text-black font-mono text-sm font-bold rounded border border-blue-400">{{ downloadLabel }}</button>
        </div>
        <div class="border border-blue-600 rounded p-4 bg-gray-900">
          <div class="text-blue-400 font-mono text-sm mb-2">
            <span class="text-blue-500">{{ targetLabel }}</span> {{ results.url }}
          </div>
          <div class="text-blue-400 font-mono text-sm mb-2">
            <span class="text-blue-500">{{ toolLabel }}</span> {{ results.tool_name }}
          </div>
          <div class="text-blue-400 font-mono text-sm mb-2">
            <span class="text-blue-500">{{ commandLabel }}</span> {{ results.command }}
          </div>
          <div v-if="results.directories && results.directories.length > 0" class="mt-4">
            <div class="text-blue-500 font-mono text-sm mb-2">{{ foundLabel }} ({{ results.directories.length }})</div>
            <div class="space-y-1 max-h-64 overflow-y-auto">
              <div v-for="(dir, idx) in results.directories" :key="idx" class="bg-blue-900/20 border border-blue-500/30 rounded-md p-2">
                <div class="text-blue-300 font-mono text-sm">{{ dir.url }}</div>
                <div class="text-blue-400 font-mono text-xs">Status: {{ dir.status_code }}</div>
              </div>
            </div>
          </div>
          <div v-else class="mt-4 text-center text-blue-400 font-mono">
            {{ noDirsLabel }}
          </div>
          <div v-if="results.success" class="mt-4 pt-4 border-t border-blue-700">
            <div class="flex items-center text-blue-400">
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
  name: 'DirectoryScan',
  setup() {
    const targetUrl = ref('')
    const loading = ref(false)
    const results = ref(null)
    const error = ref(null)
    const sessionId = ref(Math.random().toString(36).substring(2, 8).toUpperCase())
    
    const labels = ref({
      scanTitle: 'DIRECTORY ENUMERATION',
      sessionLabel: 'SESSION',
      enterTargetLabel: 'Enter target URL:',
      placeholderText: 'https://target-system.com',
      startScanLabel: 'START DIRECTORY SCAN',
      scanningLabel: 'SCANNING...',
      processingMessage: 'SCANNING FOR HIDDEN DIRECTORIES',
      executingLabel: 'EXECUTING DIRECTORY ENUMERATION',
      errorTitle: 'DIRECTORY SCAN FAILED',
      resultsTitle: 'DIRECTORY SCAN RESULTS',
      downloadLabel: '[DOWNLOAD]',
      targetLabel: 'Target:',
      toolLabel: 'Tool:',
      commandLabel: 'Command:',
      foundLabel: 'FOUND DIRECTORIES',
      noDirsLabel: 'No directories found',
      successMessage: 'DIRECTORY SCAN COMPLETED'
    })

    const commandDisplay = computed(() => {
      if (results.value) return results.value.command
      return `dirsearch -u ${targetUrl.value || '<target>'} -w common.txt`
    })

    const startScan = async () => {
      if (!targetUrl.value.trim()) { error.value = 'Please enter a valid URL'; return }
      loading.value = true; error.value = null; results.value = null
      try {
        const formData = new URLSearchParams()
        formData.append('url', targetUrl.value.trim())
        const response = await fetch(`${apiService.baseURL}/scan/directories`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
          body: formData
        })
        if (response.ok) {
          const data = await response.json()
          results.value = data
          if (data.message) labels.value = { ...labels.value, ...data.message }
        } else {
          const errorData = await response.json().catch(() => ({}))
          throw new Error(errorData.detail || 'Directory scan failed')
        }
      } catch (err) { error.value = err.message || 'Directory scan failed' }
      finally { loading.value = false }
    }

    const downloadReport = async () => {
      if (!results.value) return
      try { await apiService.downloadReport(results.value, 'directories') }
      catch (err) { console.error('Download error:', err) }
    }

    return {
      targetUrl, loading, results, error, sessionId, labels, commandDisplay,
      startScan, downloadReport,
      scanTitle: computed(() => labels.value.scanTitle),
      sessionLabel: computed(() => labels.value.sessionLabel),
      enterTargetLabel: computed(() => labels.value.enterTargetLabel),
      placeholderText: computed(() => labels.value.placeholderText),
      startScanLabel: computed(() => labels.value.startScanLabel),
      scanningLabel: computed(() => labels.value.scanningLabel),
      processingMessage: computed(() => labels.value.processingMessage),
      executingLabel: computed(() => labels.value.executingLabel),
      errorTitle: computed(() => labels.value.errorTitle),
      resultsTitle: computed(() => labels.value.resultsTitle),
      downloadLabel: computed(() => labels.value.downloadLabel),
      targetLabel: computed(() => labels.value.targetLabel),
      toolLabel: computed(() => labels.value.toolLabel),
      commandLabel: computed(() => labels.value.commandLabel),
      foundLabel: computed(() => labels.value.foundLabel),
      noDirsLabel: computed(() => labels.value.noDirsLabel),
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
::-webkit-scrollbar-thumb { background: #0041ff; border-radius: 4px; }
::-webkit-scrollbar-thumb:hover { background: #0033cc; }
button:hover { transform: translateY(-2px); box-shadow: 0 4px 20px rgba(0, 65, 255, 0.3); }
input:focus { box-shadow: 0 0 0 3px rgba(0, 65, 255, 0.2); }
</style>
