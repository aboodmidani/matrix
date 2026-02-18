<template>
  <div class="min-h-screen bg-black text-green-400 relative overflow-hidden" style="font-family: 'Share Tech Mono', monospace;">
    <MatrixBackground />

    <main class="relative z-10 max-w-4xl mx-auto px-4 py-10">

      <!-- ── Header ─────────────────────────────────────────────────────── -->
      <header class="text-center mb-10 fade-in-up">
        <div class="inline-block mb-3">
          <p class="text-xs tracking-[0.4em] uppercase mb-1" style="color: rgba(0,255,65,0.4);">[ SECURITY ASSESSMENT PLATFORM ]</p>
          <h1
            class="text-5xl md:text-6xl font-black tracking-[0.15em] glow-green"
            style="font-family: 'Orbitron', monospace; color: #00ff41; letter-spacing: 0.15em;"
          >
            MATRIX
          </h1>
          <h2
            class="text-xl md:text-2xl font-bold tracking-[0.5em] mt-1"
            style="font-family: 'Orbitron', monospace; color: rgba(0,255,65,0.6);"
          >
            SCANNER
          </h2>
        </div>
        <div class="flex items-center justify-center gap-3 mt-2">
          <div class="h-px flex-1 max-w-24" style="background: linear-gradient(90deg, transparent, rgba(0,255,65,0.4));"></div>
          <span class="text-xs tracking-widest" style="color: rgba(0,255,65,0.35);">v1.0.0</span>
          <div class="h-px flex-1 max-w-24" style="background: linear-gradient(90deg, rgba(0,255,65,0.4), transparent);"></div>
        </div>
      </header>

      <!-- ── Disclaimer ─────────────────────────────────────────────────── -->
      <Transition name="fade">
        <div v-if="!accepted" class="mb-10 fade-in-up">
          <div class="matrix-card bracket-corners max-w-lg mx-auto p-8 text-center scanline">
            <div class="mb-4">
              <span class="text-xs tracking-[0.3em] uppercase" style="color: rgba(255,215,0,0.5);">⚠ WARNING ⚠</span>
              <h2 class="text-xl font-bold mt-2 mb-1" style="font-family: 'Orbitron', monospace; color: #ffd700;">
                LEGAL DISCLAIMER
              </h2>
              <div class="h-px my-3" style="background: linear-gradient(90deg, transparent, rgba(255,215,0,0.3), transparent);"></div>
            </div>
            <p class="text-sm leading-relaxed mb-6" style="color: rgba(0,255,65,0.7);">
              This tool is intended for <span style="color: #00ff41;">educational purposes</span> and
              <span style="color: #00ff41;">authorized security testing only</span>.<br><br>
              Only scan systems you own or have explicit written permission to test.
              Unauthorized scanning may be illegal.
            </p>
            <button
              @click="accept"
              class="btn-matrix px-8 py-3 font-bold tracking-widest text-sm uppercase"
              style="
                background: rgba(0,255,65,0.1);
                border: 1px solid rgba(0,255,65,0.5);
                color: #00ff41;
                font-family: 'Orbitron', monospace;
              "
            >
              [ ACCEPT &amp; CONTINUE ]
            </button>
          </div>
        </div>
      </Transition>

      <!-- ── Input panel ────────────────────────────────────────────────── -->
      <Transition name="fade">
        <div v-if="accepted" class="mb-8 fade-in-up">
          <div class="matrix-card bracket-corners p-6">
            <!-- Terminal prompt line -->
            <div class="flex items-center gap-2 mb-4">
              <span class="text-xs tracking-widest" style="color: rgba(0,255,65,0.4);">root@matrix:~$</span>
              <span class="text-xs cursor-blink" style="color: rgba(0,255,65,0.3);">scan --target</span>
            </div>

            <div class="flex flex-col sm:flex-row gap-3">
              <!-- URL input -->
              <div class="flex-1 relative">
                <span class="absolute left-4 top-1/2 -translate-y-1/2 text-sm select-none" style="color: rgba(0,255,65,0.5);">›</span>
                <input
                  v-model="targetUrl"
                  type="text"
                  placeholder="https://target.com"
                  class="matrix-input w-full pl-9 pr-4 py-3 text-sm rounded-none"
                  style="
                    background: rgba(0,10,2,0.8);
                    border: 1px solid rgba(0,255,65,0.25);
                    color: #00ff41;
                    font-family: 'Share Tech Mono', monospace;
                  "
                  @keyup.enter="start"
                />
              </div>

              <!-- Scan button -->
              <button
                @click="start"
                :disabled="!targetUrl.trim() || scanState.isScanning"
                class="btn-matrix px-8 py-3 font-bold tracking-widest text-sm uppercase rounded-none"
                :class="scanState.isScanning ? 'pulse-glow' : ''"
                style="
                  background: rgba(0,255,65,0.12);
                  border: 1px solid rgba(0,255,65,0.5);
                  color: #00ff41;
                  font-family: 'Orbitron', monospace;
                  min-width: 160px;
                "
                :style="(!targetUrl.trim() || scanState.isScanning) ? { opacity: 0.4, cursor: 'not-allowed' } : {}"
              >
                <span v-if="scanState.isScanning" class="flex items-center justify-center gap-2">
                  <span class="inline-block w-2 h-2 rounded-full bg-green-400 animate-ping"></span>
                  SCANNING
                </span>
                <span v-else>[ SCAN ]</span>
              </button>
            </div>

            <!-- Quick targets -->
            <div class="flex flex-wrap gap-3 mt-4">
              <span class="text-xs" style="color: rgba(0,255,65,0.3);">QUICK:</span>
              <button
                v-for="t in quickTargets"
                :key="t"
                @click="targetUrl = t"
                class="text-xs transition-all duration-200 hover:underline"
                style="color: rgba(0,255,65,0.45);"
                :style="targetUrl === t ? { color: '#00ff41' } : {}"
              >
                {{ t.replace('https://', '') }}
              </button>
            </div>
          </div>

          <!-- ── Progress ──────────────────────────────────────────────── -->
          <Transition name="fade">
            <div v-if="scanState.isScanning" class="mt-3 matrix-card p-4">
              <div class="flex justify-between items-center mb-2">
                <div class="flex items-center gap-2">
                  <span class="inline-block w-1.5 h-1.5 rounded-full bg-green-400 animate-ping"></span>
                  <span class="text-xs tracking-wider" style="color: rgba(0,255,65,0.7);">{{ scanState.currentScan }}</span>
                </div>
                <span class="text-xs font-bold" style="color: #00ff41; font-family: 'Orbitron', monospace;">
                  {{ scanState.progress }}%
                </span>
              </div>
              <div class="h-1 rounded-none overflow-hidden" style="background: rgba(0,255,65,0.08);">
                <div
                  class="h-full progress-shimmer transition-all duration-500"
                  :style="{ width: `${scanState.progress}%` }"
                ></div>
              </div>
              <!-- Per-scan status row -->
              <div class="flex flex-wrap gap-3 mt-3">
                <div v-for="(cfg, key) in SCAN_CONFIGS" :key="key" class="flex items-center gap-1.5">
                  <span
                    class="w-1.5 h-1.5 rounded-full"
                    :style="{
                      background: scans[key].status === 'done'     ? '#00ff41'
                               : scans[key].status === 'error'    ? '#ff3c5a'
                               : scans[key].status === 'scanning' ? '#ffd700'
                               : 'rgba(0,255,65,0.2)',
                      boxShadow: scans[key].status === 'scanning' ? '0 0 6px #ffd700' : 'none',
                    }"
                  ></span>
                  <span class="text-xs" style="color: rgba(0,255,65,0.4);">{{ cfg.label }}</span>
                </div>
              </div>
            </div>
          </Transition>
        </div>
      </Transition>

      <!-- ── Results ────────────────────────────────────────────────────── -->
      <Transition name="fade">
        <div v-if="scanState.done" class="space-y-3 fade-in-up">

          <!-- Results header bar -->
          <div class="matrix-card px-5 py-3 flex items-center justify-between">
            <div class="flex items-center gap-3">
              <div class="w-2 h-2 rounded-full" style="background: #00ff41; box-shadow: 0 0 8px #00ff41;"></div>
              <span class="text-sm font-bold tracking-widest" style="font-family: 'Orbitron', monospace; color: #00ff41;">
                SCAN COMPLETE
              </span>
              <span class="text-xs hidden sm:inline" style="color: rgba(0,255,65,0.35);">{{ targetUrl }}</span>
            </div>
            <button
              @click="reset"
              class="btn-matrix text-xs px-4 py-2 tracking-widest uppercase"
              style="
                border: 1px solid rgba(0,255,65,0.25);
                color: rgba(0,255,65,0.6);
                font-family: 'Orbitron', monospace;
              "
            >
              [ NEW SCAN ]
            </button>
          </div>

          <!-- ── DNS ──────────────────────────────────────────────────── -->
          <ScanCard :config="SCAN_CONFIGS.dns" :scan="scans.dns">
            <template #results="{ data }">
              <div v-if="hasAnyRecord(data.records)" class="space-y-1">
                <RecordGroup label="A Records (IPv4)"    :items="data.records?.A"    />
                <RecordGroup label="AAAA Records (IPv6)" :items="data.records?.AAAA" />
                <RecordGroup label="MX Records"          :items="data.records?.MX"   />
                <RecordGroup label="NS Records"          :items="data.records?.NS"   />
                <RecordGroup label="TXT Records"         :items="data.records?.TXT"  />
              </div>
              <p v-else class="text-xs py-2" style="color: rgba(0,255,65,0.3);">No DNS records found.</p>
            </template>
          </ScanCard>

          <!-- ── Ports ─────────────────────────────────────────────────── -->
          <ScanCard :config="SCAN_CONFIGS.ports" :scan="scans.ports">
            <template #results="{ data }">
              <div v-if="data.ports && data.ports.length">
                <div class="flex items-center gap-2 mb-3">
                  <span class="text-xs tracking-widest uppercase" style="color: rgba(255,215,0,0.5);">
                    {{ data.ports.length }} open port{{ data.ports.length !== 1 ? 's' : '' }} detected
                  </span>
                </div>
                <table class="w-full matrix-table">
                  <thead>
                    <tr>
                      <th class="text-left">Port</th>
                      <th class="text-left">Protocol</th>
                      <th class="text-left">Service</th>
                      <th class="text-left hidden sm:table-cell">Version</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="p in data.ports" :key="p.port">
                      <td>
                        <span class="font-bold" style="color: #ffd700;">{{ p.port }}</span>
                      </td>
                      <td style="color: rgba(0,255,65,0.6);">{{ p.protocol }}</td>
                      <td style="color: #00ff41;">{{ p.service }}</td>
                      <td class="hidden sm:table-cell" style="color: rgba(0,255,65,0.4); font-size: 0.75rem;">
                        {{ p.version || '—' }}
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
              <p v-else class="text-xs py-2" style="color: rgba(0,255,65,0.3);">No open ports found on scanned range.</p>
            </template>
          </ScanCard>

          <!-- ── Firewall ───────────────────────────────────────────────── -->
          <ScanCard :config="SCAN_CONFIGS.firewall" :scan="scans.firewall">
            <template #results="{ data }">
              <div class="flex flex-wrap items-start gap-4">
                <!-- Detection badge -->
                <div
                  class="flex items-center gap-2 px-4 py-2 rounded-none"
                  :style="data.firewall?.detected
                    ? 'background: rgba(255,60,90,0.1); border: 1px solid rgba(255,60,90,0.4);'
                    : 'background: rgba(0,255,65,0.06); border: 1px solid rgba(0,255,65,0.25);'"
                >
                  <span class="text-lg">{{ data.firewall?.detected ? '🔴' : '🟢' }}</span>
                  <span
                    class="font-bold text-sm tracking-wider"
                    :style="data.firewall?.detected ? 'color: #ff3c5a;' : 'color: #00ff41;'"
                    style="font-family: 'Orbitron', monospace;"
                  >
                    {{ data.firewall?.detected ? 'WAF DETECTED' : 'NO WAF' }}
                  </span>
                </div>

                <!-- Details -->
                <div class="flex flex-wrap gap-x-6 gap-y-1 text-sm">
                  <div>
                    <span style="color: rgba(0,255,65,0.4);">NAME </span>
                    <span style="color: #00ff41;">{{ data.firewall?.waf_name || '—' }}</span>
                  </div>
                  <div v-if="data.firewall?.manufacturer && data.firewall.manufacturer !== data.firewall.waf_name">
                    <span style="color: rgba(0,255,65,0.4);">VENDOR </span>
                    <span style="color: #00ff41;">{{ data.firewall.manufacturer }}</span>
                  </div>
                  <div>
                    <span style="color: rgba(0,255,65,0.4);">CONFIDENCE </span>
                    <span style="color: #ffd700;">{{ data.firewall?.confidence || '—' }}</span>
                  </div>
                </div>
              </div>
            </template>
          </ScanCard>

          <!-- ── Technologies ───────────────────────────────────────────── -->
          <ScanCard :config="SCAN_CONFIGS.technology" :scan="scans.technology">
            <template #results="{ data }">
              <div v-if="data.technologies && Object.keys(data.technologies).length">
                <p class="text-xs tracking-widest uppercase mb-3" style="color: rgba(191,0,255,0.5);">
                  {{ Object.keys(data.technologies).length }} technologies identified
                </p>
                <div class="flex flex-wrap gap-2">
                  <div
                    v-for="(info, name) in data.technologies"
                    :key="name"
                    class="chip"
                    style="color: #bf00ff; background: rgba(191,0,255,0.07); border-color: rgba(191,0,255,0.25);"
                  >
                    <span>{{ name }}</span>
                    <span v-if="info.version" style="color: rgba(191,0,255,0.5); font-size: 0.7rem;">{{ info.version }}</span>
                    <span v-if="info.confidence" style="color: rgba(191,0,255,0.35); font-size: 0.65rem;">({{ info.confidence }}%)</span>
                  </div>
                </div>
              </div>
              <p v-else class="text-xs py-2" style="color: rgba(0,255,65,0.3);">No technologies detected.</p>
            </template>
          </ScanCard>

          <!-- ── Subdomains ─────────────────────────────────────────────── -->
          <ScanCard :config="SCAN_CONFIGS.subdomains" :scan="scans.subdomains">
            <template #results="{ data }">
              <div v-if="data.subdomains && data.subdomains.length">
                <p class="text-xs tracking-widest uppercase mb-3" style="color: rgba(0,255,65,0.5);">
                  {{ data.subdomains.length }} subdomain{{ data.subdomains.length !== 1 ? 's' : '' }} discovered
                </p>
                <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-1.5">
                  <div
                    v-for="s in data.subdomains"
                    :key="s.subdomain"
                    class="flex items-center gap-2 px-3 py-1.5 text-xs truncate"
                    style="background: rgba(0,255,65,0.04); border: 1px solid rgba(0,255,65,0.12); color: #00ff41;"
                  >
                    <span style="color: rgba(0,255,65,0.3);">›</span>
                    <span class="truncate">{{ s.subdomain }}</span>
                  </div>
                </div>
              </div>
              <p v-else class="text-xs py-2" style="color: rgba(0,255,65,0.3);">No subdomains discovered.</p>
            </template>
          </ScanCard>

          <!-- Footer -->
          <div class="text-center pt-4 pb-2">
            <p class="text-xs tracking-widest" style="color: rgba(0,255,65,0.2);">
              — MATRIX SCANNER · FOR AUTHORIZED USE ONLY —
            </p>
          </div>

        </div>
      </Transition>

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
const quickTargets = ['https://example.com', 'https://codiay.com']

async function start() {
  if (!targetUrl.value.trim() || scanState.isScanning) return
  await runAllScans(targetUrl.value.trim())
}

function reset() {
  resetScans()
}

// ── Helpers ───────────────────────────────────────────────────────────────────
function hasAnyRecord(records) {
  if (!records) return false
  return Object.values(records).some(arr => Array.isArray(arr) && arr.length > 0)
}
</script>

<style scoped>
.fade-enter-active, .fade-leave-active { transition: opacity 0.3s ease; }
.fade-enter-from, .fade-leave-to       { opacity: 0; }
</style>
