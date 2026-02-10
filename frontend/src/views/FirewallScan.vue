<template>
  <div class="bg-black border-2 border-red-500 rounded-lg p-6 shadow-2xl">
    <div class="flex items-center mb-4 text-red-400 text-sm font-mono">
      <span class="animate-pulse">●</span>
      <span class="ml-2">{{ scanTitle }}</span>
      <span class="ml-auto">{{ sessionLabel }}: {{ sessionId }}</span>
    </div>
    <div class="border border-red-600 rounded p-4 md:p-6 bg-gray-900 mb-6">
      <div class="text-red-400 font-mono text-sm mb-3">
        <span class="text-red-300">></span> {{ enterTargetLabel }}
      </div>
      <div class="flex flex-col sm:flex-row gap-3">
        <input v-model="targetUrl" type="text" :placeholder="placeholderText" class="flex-1 bg-black border border-red-500 rounded px-3 py-3 md:py-2 text-red-400 font-mono text-sm md:text-base focus:outline-none focus:border-red-400 transition-all duration-300" />
        <button @click="startScan" :disabled="loading || !targetUrl.trim()" class="px-6 py-3 md:py-2 bg-red-600 hover:bg-red-500 disabled:bg-gray-600 text-white font-mono font-bold rounded border border-red-400 hover:border-red-300 transition-all duration-300 disabled:cursor-not-allowed min-h-[44px]">
          <span v-if="loading">{{ scanningLabel }}</span>
          <span v-else>{{ startScanLabel }}</span>
        </button>
      </div>
    </div>
    <transition name="fade">
      <div v-if="loading" class="mt-8 bg-black border-2 border-red-500 rounded-lg p-6">
        <div class="flex items-center justify-between mb-4">
          <span class="text-red-400 font-mono text-lg font-bold tracking-wider">{{ processingMessage }}</span>
          <div class="flex space-x-1">
            <div class="w-2 h-2 bg-red-500 rounded-full animate-bounce" style="animation-delay: 0s"></div>
            <div class="w-2 h-2 bg-red-500 rounded-full animate-bounce" style="animation-delay: 0.1s"></div>
            <div class="w-2 h-2 bg-red-500 rounded-full animate-bounce" style="animation-delay: 0.2s"></div>
          </div>
        </div>
        <div class="border border-red-600 rounded p-4 bg-gray-900">
          <div class="text-red-400 font-mono text-xs mb-2">
            <span class="text-red-300">root@matrix</span>:<span class="text-blue-400">~</span>$ {{ commandDisplay }}
          </div>
          <div class="text-center text-red-400 font-mono text-xs mt-2">{{ executingLabel }}</div>
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
      <div v-if="results" class="mt-8 bg-black bg-opacity-90 border border-red-500 rounded-lg p-6">
        <div class="flex justify-between items-center mb-4">
          <h3 class="text-xl font-bold text-red-400 flex items-center">
            <svg class="w-6 h-6 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"></path>
            </svg>
            {{ resultsTitle }}
          </h3>
          <button @click="downloadReport" class="px-4 py-2 bg-red-600 hover:bg-red-500 text-white font-mono text-sm font-bold rounded border border-red-400">{{ downloadLabel }}</button>
        </div>
        <div class="border border-red-600 rounded p-4 bg-gray-900">
          <div class="text-red-400 font-mono text-sm mb-2">
            <span class="text-red-500">{{ targetLabel }}</span> {{ results.url }}
          </div>
          <div class="text-red-400 font-mono text-sm mb-2">
            <span class="text-red-500">{{ toolLabel }}</span> {{ results.tool_name }}
          </div>
          <div class="text-red-400 font-mono text-sm mb-2">
            <span class="text-red-500">{{ commandLabel }}</span> {{ results.command }}
          </div>
          <div v-if="results.waf_detection" class="mt-4">
            <div v-if="results.waf_detection.detected" class="text-red-400 font-mono">
              <span class="font-bold">{{ wafDetectedLabel }}</span> {{ results.waf_detection.waf_name }}
            </div>
            <div v-else class="text-green-400 font-mono">{{ noWafLabel }}</div>
          </div>
          <div v-if="results.success" class="mt-4 pt-4 border-t border-red-700">
            <div class="flex items-center text-red-400">
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
  name: 'FirewallScan',
  setup() {
    const targetUrl = ref('')
    const loading = ref(false)
    const results = ref(null)
    const error = ref(null)
    const sessionId = ref(Math.random().toString(36).substring(2, 8).toUpperCase())
    
    const labels = ref({
      scanTitle: 'WAF DETECTION',
      sessionLabel: 'SESSION',
      enterTargetLabel: 'Enter target URL:',
      placeholderText: 'https://target-system.com',
      startScanLabel: 'START WAF DETECTION',
      scanningLabel: 'SCANNING...',
      processingMessage: 'ANALYZING WEB APPLICATION FIREWALL',
      executingLabel: 'EXECUTING WAF DETECTION',
      errorTitle: 'WAF DETECTION FAILED',
      resultsTitle: 'WAF DETECTION RESULTS',
      downloadLabel: '[DOWNLOAD]',
      targetLabel: 'Target:',
      toolLabel: 'Tool:',
      commandLabel: 'Command:',
      wafDetectedLabel: 'WAF DETECTED:',
      noWafLabel: 'NO WAF DETECTED',
      successMessage: 'WAF DETECTION COMPLETED'
    })

    const commandDisplay = computed(() => {
      if (results.value) return results.value.command
      return `wafw00f ${targetUrl.value || '<target>'}`
    })

    const startScan = async () => {
      if (!targetUrl.value.trim()) { error.value = 'Please enter a valid URL'; return }
      loading.value = true; error.value = null; results.value = null
      try {
        const formData = new URLSearchParams()
        formData.append('url', targetUrl.value.trim())
        const response = await fetch(`${apiService.baseURL}/scan/firewall`, {
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
          throw new Error(errorData.detail || 'Firewall scan failed')
        }
      } catch (err) { error.value = err.message || 'Firewall scan failed' }
      finally { loading.value = false }
    }

    const downloadReport = async () => {
      if (!results.value) return
      try { await apiService.downloadReport(results.value, 'firewall') }
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
      wafDetectedLabel: computed(() => labels.value.wafDetectedLabel),
      noWafLabel: computed(() => labels.value.noWafLabel),
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
::-webkit-scrollbar-thumb { background: #ef4444; border-radius: 4px; }
::-webkit-scrollbar-thumb:hover { background: #dc2626; }
button:hover { transform: translateY(-2px); box-shadow: 0 4px 20px rgba(239, 68, 68, 0.3); }
input:focus { box-shadow: 0 0 0 3px rgba(239, 68, 68, 0.2); }
</style>
