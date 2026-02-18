<template>
  <div class="min-h-screen bg-black text-green-400 font-mono relative overflow-hidden">
    <MatrixBackground />

    <main class="relative z-10 max-w-5xl mx-auto px-4 py-8">

      <!-- Header -->
      <div class="text-center mb-8">
        <h1 class="text-4xl font-bold text-green-400 mb-1 tracking-widest">MATRIX SCANNER</h1>
        <p class="text-green-600 text-sm">Web Security Assessment Platform</p>
      </div>

      <!-- Disclaimer -->
      <div v-if="!accepted" class="bg-black/90 border border-yellow-500/50 rounded-lg p-6 mb-8 max-w-xl mx-auto text-center">
        <h2 class="text-xl font-bold text-yellow-400 mb-2">[LEGAL DISCLAIMER]</h2>
        <p class="text-green-400 text-sm mb-4">
          This tool is for educational and authorized security testing only.<br>
          Only scan targets you own or have explicit permission to test.
        </p>
        <button
          @click="accept"
          class="px-6 py-2 bg-green-600 hover:bg-green-500 text-black font-bold rounded border border-green-400 transition-all"
        >
          [ACCEPT &amp; CONTINUE]
        </button>
      </div>

      <!-- Input -->
      <div v-if="accepted" class="mb-6">
        <div class="bg-black/90 border border-green-500/50 rounded-lg p-5">
          <div class="flex flex-col md:flex-row gap-3">
            <div class="flex-1 relative">
              <span class="absolute left-3 top-1/2 -translate-y-1/2 text-green-500 select-none">›</span>
              <input
                v-model="targetUrl"
                type="text"
                placeholder="https://example.com"
                class="w-full bg-gray-900/60 border border-green-500/40 rounded-lg pl-8 pr-4 py-3 text-green-300 placeholder-green-700 focus:outline-none focus:border-green-400 transition-all"
                @keyup.enter="start"
              />
            </div>
            <button
              @click="start"
              :disabled="!targetUrl.trim() || scanState.isScanning"
              class="px-8 py-3 bg-green-600 hover:bg-green-500 disabled:bg-gray-700 disabled:cursor-not-allowed text-black font-bold rounded border border-green-400 transition-all"
            >
              {{ scanState.isScanning ? 'SCANNING…' : 'START SCAN' }}
            </button>
          </div>

          <!-- Quick targets -->
          <div class="flex gap-3 mt-3">
            <button @click="targetUrl = 'https://example.com'" class="text-xs text-green-600 hover:text-green-400">[example.com]</button>
            <button @click="targetUrl = 'https://codiay.com'"  class="text-xs text-green-600 hover:text-green-400">[codiay.com]</button>
          </div>
        </div>

        <!-- Progress bar -->
        <div v-if="scanState.isScanning" class="mt-3 bg-black/90 border border-green-500/30 rounded-lg p-4">
          <div class="flex justify-between mb-1 text-sm">
            <span class="text-green-400 animate-pulse">{{ scanState.currentScan }}</span>
            <span class="text-green-600">{{ scanState.progress }}%</span>
          </div>
          <div class="h-1.5 bg-gray-800 rounded-full overflow-hidden">
            <div
              class="h-full bg-gradient-to-r from-green-700 to-green-400 transition-all duration-300"
              :style="{ width: `${scanState.progress}%` }"
            ></div>
          </div>
        </div>
      </div>

      <!-- Results -->
      <div v-if="scanState.done" class="space-y-4">

        <!-- Results header -->
        <div class="flex items-center justify-between bg-black/90 border border-green-500/40 rounded-lg px-5 py-3">
          <div>
            <span class="font-bold text-green-400">SCAN RESULTS</span>
            <span class="ml-3 text-xs text-green-700">{{ targetUrl }}</span>
          </div>
          <button
            @click="reset"
            class="px-4 py-1.5 bg-gray-800 hover:bg-gray-700 text-green-400 text-sm rounded border border-gray-600 transition-all"
          >
            NEW SCAN
          </button>
        </div>

        <!-- DNS -->
        <ScanCard :config="SCAN_CONFIGS.dns" :scan="scans.dns">
          <template #results="{ data }">
            <div class="space-y-3">
              <RecordGroup label="A Records (IPv4)"    :items="data.records?.A"    />
              <RecordGroup label="AAAA Records (IPv6)" :items="data.records?.AAAA" />
              <RecordGroup label="MX Records"          :items="data.records?.MX"   />
              <RecordGroup label="NS Records"          :items="data.records?.NS"   />
              <RecordGroup label="TXT Records"         :items="data.records?.TXT"  />
            </div>
          </template>
        </ScanCard>

        <!-- Ports -->
        <ScanCard :config="SCAN_CONFIGS.ports" :scan="scans.ports">
          <template #results="{ data }">
            <div v-if="data.ports && data.ports.length">
              <table class="w-full text-sm">
                <thead>
                  <tr class="text-green-600 border-b border-green-900">
                    <th class="text-left py-1 pr-4">Port</th>
                    <th class="text-left py-1 pr-4">Protocol</th>
                    <th class="text-left py-1 pr-4">Service</th>
                    <th class="text-left py-1">Version</th>
                  </tr>
                </thead>
                <tbody>
                  <tr
                    v-for="p in data.ports"
                    :key="p.port"
                    class="border-b border-green-900/30 hover:bg-green-900/10"
                  >
                    <td class="py-1 pr-4 text-yellow-400 font-bold">{{ p.port }}</td>
                    <td class="py-1 pr-4 text-green-500">{{ p.protocol }}</td>
                    <td class="py-1 pr-4 text-green-300">{{ p.service }}</td>
                    <td class="py-1 text-green-600 text-xs">{{ p.version || '—' }}</td>
                  </tr>
                </tbody>
              </table>
            </div>
            <p v-else class="text-green-700 text-sm">No open ports found on scanned range.</p>
          </template>
        </ScanCard>

        <!-- Firewall -->
        <ScanCard :config="SCAN_CONFIGS.firewall" :scan="scans.firewall">
          <template #results="{ data }">
            <div class="flex flex-wrap items-center gap-4">
              <span
                class="px-3 py-1 rounded-full text-sm font-bold"
                :class="data.firewall?.detected
                  ? 'bg-red-900/50 text-red-400 border border-red-500/50'
                  : 'bg-green-900/30 text-green-400 border border-green-500/30'"
              >
                {{ data.firewall?.detected ? '⚠ WAF DETECTED' : '✓ NO WAF' }}
              </span>
              <div class="text-sm space-x-4">
                <span>
                  <span class="text-green-600">Name: </span>
                  <span class="text-green-300">{{ data.firewall?.waf_name || '—' }}</span>
                </span>
                <span v-if="data.firewall?.manufacturer">
                  <span class="text-green-600">Manufacturer: </span>
                  <span class="text-green-300">{{ data.firewall.manufacturer }}</span>
                </span>
                <span>
                  <span class="text-green-600">Confidence: </span>
                  <span class="text-green-300">{{ data.firewall?.confidence || '—' }}</span>
                </span>
              </div>
            </div>
          </template>
        </ScanCard>

        <!-- Technologies -->
        <ScanCard :config="SCAN_CONFIGS.technology" :scan="scans.technology">
          <template #results="{ data }">
            <div v-if="data.technologies && Object.keys(data.technologies).length">
              <div class="flex flex-wrap gap-2">
                <span
                  v-for="(info, name) in data.technologies"
                  :key="name"
                  class="px-3 py-1 bg-purple-900/30 border border-purple-500/30 rounded-full text-sm text-purple-300"
                >
                  {{ name }}
                  <span v-if="info.version" class="text-purple-500 text-xs ml-1">{{ info.version }}</span>
                  <span v-if="info.confidence" class="text-purple-600 text-xs ml-1">({{ info.confidence }}%)</span>
                </span>
              </div>
            </div>
            <p v-else class="text-green-700 text-sm">No technologies detected.</p>
          </template>
        </ScanCard>

        <!-- Subdomains -->
        <ScanCard :config="SCAN_CONFIGS.subdomains" :scan="scans.subdomains">
          <template #results="{ data }">
            <div v-if="data.subdomains && data.subdomains.length">
              <p class="text-green-600 text-xs mb-2">{{ data.subdomains.length }} subdomain(s) found</p>
              <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-1">
                <span
                  v-for="s in data.subdomains"
                  :key="s.subdomain"
                  class="text-sm text-green-300 bg-green-900/20 border border-green-800/40 rounded px-2 py-1 truncate"
                >
                  {{ s.subdomain }}
                </span>
              </div>
            </div>
            <p v-else class="text-green-700 text-sm">No subdomains discovered.</p>
          </template>
        </ScanCard>

      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import MatrixBackground from '../components/MatrixBackground.vue'
import ScanCard from '../components/ScanCard.vue'
import RecordGroup from '../components/RecordGroup.vue'
import { scanState, scans, SCAN_CONFIGS, runAllScans, resetScans } from '../composables/useScanner.js'

// ── Disclaimer ────────────────────────────────────────────────────────────────
const accepted = ref(false)
function accept() {
  accepted.value = true
  localStorage.setItem('disclaimerAccepted', 'true')
}
onMounted(() => {
  accepted.value = localStorage.getItem('disclaimerAccepted') === 'true'
})

// ── Scan ──────────────────────────────────────────────────────────────────────
const targetUrl = ref('')

async function start() {
  if (!targetUrl.value.trim() || scanState.isScanning) return
  await runAllScans(targetUrl.value.trim())
}

function reset() {
  resetScans()
}
</script>
