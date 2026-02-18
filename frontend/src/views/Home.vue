<template>
  <div class="min-h-screen bg-black relative overflow-x-hidden" style="font-family: 'Share Tech Mono', monospace;">
    <MatrixBackground />

    <!-- ── Page wrapper ──────────────────────────────────────────────────── -->
    <div class="relative z-10 min-h-screen flex flex-col">

      <!-- ── Top bar ───────────────────────────────────────────────────── -->
      <header class="border-b" style="border-color: rgba(0,255,65,0.1); background: rgba(0,0,0,0.7); backdrop-filter: blur(8px);">
        <div class="max-w-5xl mx-auto px-6 py-3 flex items-center justify-between">
          <div class="flex items-center gap-3">
            <div class="w-2 h-2 rounded-full" style="background: #00ff41; box-shadow: 0 0 8px #00ff41;"></div>
            <span class="text-xs tracking-[0.3em] uppercase" style="font-family: 'Orbitron', monospace; color: rgba(0,255,65,0.6);">
              Matrix Scanner
            </span>
          </div>
          <span class="text-xs" style="color: rgba(0,255,65,0.7);">v1.0.0</span>
        </div>
      </header>

      <!-- ── Main content ──────────────────────────────────────────────── -->
      <main class="flex-1 max-w-5xl w-full mx-auto px-4 sm:px-6 py-12">

        <!-- ── Hero ────────────────────────────────────────────────────── -->
        <section class="text-center mb-12 fade-in-up">
          <p class="text-xs tracking-[0.5em] uppercase mb-4" style="color: rgba(0,255,65,0.35);">
            Web Security Assessment Platform
          </p>
          <h1
            class="text-6xl sm:text-7xl font-black mb-2 glow-green"
            style="font-family: 'Orbitron', monospace; color: #00ff41; letter-spacing: 0.12em; line-height: 1;"
          >
            MATRIX
          </h1>
          <h2
            class="text-lg sm:text-xl font-bold tracking-[0.6em] mb-6"
            style="font-family: 'Orbitron', monospace; color: rgba(0,255,65,0.4);"
          >
            SCANNER
          </h2>
          <!-- Divider -->
          <div class="flex items-center justify-center gap-4">
            <div class="h-px flex-1 max-w-32" style="background: linear-gradient(90deg, transparent, rgba(0,255,65,0.3));"></div>
            <div class="flex gap-1.5">
              <span class="w-1 h-1 rounded-full" style="background: rgba(0,255,65,0.4);"></span>
              <span class="w-1 h-1 rounded-full" style="background: rgba(0,255,65,0.6);"></span>
              <span class="w-1 h-1 rounded-full" style="background: rgba(0,255,65,0.4);"></span>
            </div>
            <div class="h-px flex-1 max-w-32" style="background: linear-gradient(90deg, rgba(0,255,65,0.3), transparent);"></div>
          </div>
        </section>

        <!-- ── Disclaimer overlay ───────────────────────────────────────── -->
        <DisclaimerCard v-if="!accepted" @accepted="accept" />

        <!-- ── Scanner section ──────────────────────────────────────────── -->
        <Transition name="fade">
          <section v-if="accepted">

            <!-- Input card -->
            <div class="matrix-card bracket-corners mb-4">
              <!-- Card header -->
              <div class="px-6 pt-5 pb-3 border-b" style="border-color: rgba(0,255,65,0.08);">
                <div class="flex items-center gap-2">
                  <span class="w-1.5 h-1.5 rounded-full" style="background: #00ff41;"></span>
                  <span class="text-xs tracking-[0.25em] uppercase" style="color: rgba(0,255,65,0.4);">Target</span>
                </div>
              </div>

              <!-- Input row -->
              <div class="px-6 py-5">
                <div class="flex flex-col sm:flex-row gap-3">
                  <!-- URL field -->
                  <div class="flex-1 relative">
                    <span
                      class="absolute left-4 top-1/2 -translate-y-1/2 text-base select-none pointer-events-none"
                      style="color: rgba(0,255,65,0.4);"
                    >›</span>
                    <input
                      v-model="targetUrl"
                      type="text"
                      placeholder="https://target.com"
                      class="matrix-input w-full pl-9 pr-4 py-3 text-sm"
                      style="
                        background: rgba(0,8,2,0.9);
                        border: 1px solid rgba(0,255,65,0.7);
                        color: #00ff41;
                        font-family: 'Share Tech Mono', monospace;
                        border-radius: 2px;
                      "
                      :disabled="scanState.isScanning"
                      @keyup.enter="start"
                    />
                  </div>

                  <!-- Action buttons -->
                  <div class="flex gap-2">
                    <!-- SCAN / SCANNING -->
                    <button
                      v-if="!scanState.isScanning"
                      @click="start"
                      :disabled="!targetUrl.trim()"
                      class="btn-matrix flex-1 sm:flex-none px-8 py-3 font-bold tracking-[0.2em] text-sm uppercase"
                      style="
                        background: rgba(0,255,65,0.1);
                        border: 1px solid rgba(0,255,65,0.5);
                        color: #00ff41;
                        font-family: 'Orbitron', monospace;
                        min-width: 140px;
                        border-radius: 2px;
                      "
                      :style="!targetUrl.trim() ? { opacity: 0.35, cursor: 'not-allowed' } : {}"
                    >
                      [ SCAN ]
                    </button>

                    <!-- STOP button — shown while scanning -->
                    <template v-if="scanState.isScanning">
                      <button
                        disabled
                        class="flex-1 sm:flex-none px-6 py-3 font-bold tracking-[0.2em] text-sm uppercase flex items-center justify-center gap-2"
                        style="
                          background: rgba(0,255,65,0.06);
                          border: 1px solid rgba(0,255,65,0.7);
                          color: rgba(0,255,65,0.5);
                          font-family: 'Orbitron', monospace;
                          min-width: 140px;
                          border-radius: 2px;
                          cursor: default;
                        "
                      >
                        <span class="inline-block w-2 h-2 rounded-full bg-green-400 animate-ping"></span>
                        SCANNING
                      </button>
                      <button
                        @click="stop"
                        class="btn-matrix px-5 py-3 font-bold tracking-[0.15em] text-sm uppercase flex items-center gap-2"
                        style="
                          background: rgba(255,60,90,0.08);
                          border: 1px solid rgba(255,60,90,0.45);
                          color: #ff3c5a;
                          font-family: 'Orbitron', monospace;
                          border-radius: 2px;
                        "
                        title="Stop all scans"
                      >
                        <svg class="w-3.5 h-3.5 flex-shrink-0" fill="currentColor" viewBox="0 0 24 24">
                          <rect x="6" y="6" width="12" height="12" rx="1"/>
                        </svg>
                        <span class="hidden sm:inline">STOP</span>
                      </button>
                    </template>
                  </div>
                </div>

                <!-- Quick targets -->
                <div class="flex flex-wrap items-center gap-x-4 gap-y-1 mt-4">
                  <span class="text-xs" style="color: rgba(0,255,65,0.7);">QUICK SELECT:</span>
                  <button
                    v-for="t in quickTargets"
                    :key="t"
                    @click="targetUrl = t"
                    class="text-xs transition-colors duration-150"
                    :style="targetUrl === t
                      ? 'color: #00ff41; text-decoration: underline;'
                      : 'color: rgba(0,255,65,0.4);'"
                    :disabled="scanState.isScanning"
                  >
                    {{ t.replace('https://', '') }}
                  </button>
                </div>
              </div>
            </div>

            <!-- ── Progress panel ──────────────────────────────────────── -->
            <Transition name="slide-down">
              <div v-if="scanState.isScanning || (scanState.done && scanState.isStopped)" class="matrix-card mb-4 overflow-hidden">
                <!-- Header -->
                <div class="px-6 pt-4 pb-3 border-b flex items-center justify-between" style="border-color: rgba(0,255,65,0.08);">
                  <div class="flex items-center gap-2">
                    <span
                      class="w-1.5 h-1.5 rounded-full"
                      :style="scanState.isScanning
                        ? 'background: #ffd700; box-shadow: 0 0 6px #ffd700; animation: pulse 1s ease-in-out infinite;'
                        : 'background: #ff3c5a;'"
                    ></span>
                    <span class="text-xs tracking-[0.25em] uppercase" style="color: rgba(0,255,65,0.4);">
                      {{ scanState.isScanning ? 'Scanning' : 'Stopped' }}
                    </span>
                  </div>
                  <span class="text-xs font-bold" style="font-family: 'Orbitron', monospace; color: #00ff41;">
                    {{ scanState.completed }}/{{ scanState.total }}
                  </span>
                </div>

                <!-- Progress bar -->
                <div class="px-6 pt-4 pb-2">
                  <div class="flex items-center justify-between mb-1.5">
                    <span class="text-xs truncate max-w-xs" style="color: rgba(0,255,65,0.55);">
                      {{ scanState.currentScan || (scanState.isStopped ? 'Scan stopped' : '') }}
                    </span>
                    <span class="text-xs ml-2 flex-shrink-0" style="color: rgba(0,255,65,0.4);">{{ scanState.progress }}%</span>
                  </div>
                  <div class="h-1 overflow-hidden" style="background: rgba(0,255,65,0.07); border-radius: 1px;">
                    <div
                      class="h-full transition-all duration-700"
                      :class="scanState.isScanning ? 'progress-shimmer' : ''"
                      :style="{
                        width: `${scanState.progress}%`,
                        background: scanState.isScanning ? '' : 'rgba(255,60,90,0.5)',
                      }"
                    ></div>
                  </div>
                </div>

                <!-- Per-scan status grid -->
                <div class="px-6 pb-5 pt-3 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-2">
                  <div
                    v-for="(cfg, key) in SCAN_CONFIGS"
                    :key="key"
                    class="flex items-center gap-2 px-3 py-2"
                    style="background: rgba(0,255,65,0.03); border: 1px solid rgba(0,255,65,0.07); border-radius: 2px;"
                  >
                    <span
                      class="w-2 h-2 rounded-full flex-shrink-0"
                      :style="{
                        background:
                          scans[key].status === 'done'     ? '#00ff41' :
                          scans[key].status === 'error'    ? '#ff3c5a' :
                          scans[key].status === 'scanning' ? '#ffd700' :
                          'rgba(0,255,65,0.12)',
                        boxShadow:
                          scans[key].status === 'scanning' ? '0 0 6px #ffd700' :
                          scans[key].status === 'done'     ? '0 0 5px rgba(0,255,65,0.5)' : 'none',
                      }"
                    ></span>
                    <span class="text-xs flex-1 truncate"
                      :style="{
                        color:
                          scans[key].status === 'done'     ? 'rgba(0,255,65,0.7)' :
                          scans[key].status === 'error'    ? 'rgba(255,60,90,0.7)' :
                          scans[key].status === 'scanning' ? '#ffd700' :
                          'rgba(0,255,65,0.7)',
                      }"
                    >{{ cfg.label }}</span>
                    <span v-if="scans[key].status === 'done'"  class="text-xs flex-shrink-0" style="color: #00ff41;">✓</span>
                    <span v-if="scans[key].status === 'error'" class="text-xs flex-shrink-0" style="color: #ff3c5a;">✗</span>
                  </div>
                </div>
              </div>
            </Transition>

            <!-- ── Results ─────────────────────────────────────────────── -->
            <Transition name="fade">
              <section v-if="scanState.done" class="space-y-3 fade-in-up">

                <!-- Results toolbar -->
                <div class="matrix-card px-6 py-3 flex items-center justify-between gap-4">
                  <div class="flex items-center gap-3 min-w-0">
                    <div
                      class="w-2 h-2 rounded-full flex-shrink-0"
                      :style="scanState.isStopped
                        ? 'background: #ff3c5a; box-shadow: 0 0 6px #ff3c5a;'
                        : 'background: #00ff41; box-shadow: 0 0 8px #00ff41;'"
                    ></div>
                    <span
                      class="text-sm font-bold tracking-[0.2em] uppercase flex-shrink-0"
                      style="font-family: 'Orbitron', monospace;"
                      :style="scanState.isStopped ? 'color: #ff3c5a;' : 'color: #00ff41;'"
                    >
                      {{ scanState.isStopped ? 'Scan Stopped' : 'Scan Complete' }}
                    </span>
                    <span class="text-xs hidden md:inline truncate" style="color: rgba(0,255,65,0.3);">{{ targetUrl }}</span>
                  </div>
                  <div class="flex items-center gap-2 flex-shrink-0">
                    <!-- Export -->
                    <button
                      @click="exportTxt(targetUrl, scans, SCAN_CONFIGS)"
                      class="btn-matrix flex items-center gap-2 px-4 py-2 text-xs tracking-[0.15em] uppercase"
                      style="
                        background: rgba(0,255,65,0.06);
                        border: 1px solid rgba(0,255,65,0.3);
                        color: #00ff41;
                        font-family: 'Orbitron', monospace;
                        border-radius: 2px;
                      "
                      title="Download .txt report"
                    >
                      <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                          d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"/>
                      </svg>
                      <span class="hidden sm:inline">EXPORT</span>
                    </button>
                    <!-- New scan -->
                    <button
                      @click="reset"
                      class="btn-matrix px-4 py-2 text-xs tracking-[0.15em] uppercase"
                      style="
                        border: 1px solid rgba(0,255,65,0.7);
                        color: rgba(0,255,65,0.55);
                        font-family: 'Orbitron', monospace;
                        border-radius: 2px;
                      "
                    >
                      NEW SCAN
                    </button>
                  </div>
                </div>

                <!-- ── DNS ──────────────────────────────────────────────── -->
                <ScanCard :config="SCAN_CONFIGS.dns" :scan="scans.dns">
                  <template #results="{ data }">
                    <div v-if="hasAnyRecord(data.records)" class="space-y-2">
                      <RecordGroup label="A Records (IPv4)"    :items="data.records?.A"    />
                      <RecordGroup label="AAAA Records (IPv6)" :items="data.records?.AAAA" />
                      <RecordGroup label="MX Records"          :items="data.records?.MX"   />
                      <RecordGroup label="NS Records"          :items="data.records?.NS"   />
                      <RecordGroup label="TXT Records"         :items="data.records?.TXT"  />
                    </div>
                    <p v-else class="text-xs py-2" style="color: rgba(0,255,65,0.3);">No DNS records found.</p>
                  </template>
                </ScanCard>

                <!-- ── Ports ────────────────────────────────────────────── -->
                <ScanCard :config="SCAN_CONFIGS.ports" :scan="scans.ports">
                  <template #results="{ data }">
                    <div v-if="data.ports && data.ports.length">
                      <p class="text-xs mb-3 tracking-widest uppercase" style="color: rgba(255,215,0,0.5);">
                        {{ data.ports.length }} open port{{ data.ports.length !== 1 ? 's' : '' }} detected
                      </p>
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
                            <td><span class="font-bold" style="color: #ffd700;">{{ p.port }}</span></td>
                            <td style="color: rgba(0,255,65,0.55);">{{ p.protocol }}</td>
                            <td style="color: #00ff41;">{{ p.service }}</td>
                            <td class="hidden sm:table-cell" style="color: rgba(0,255,65,0.35); font-size: 0.75rem;">{{ p.version || '—' }}</td>
                          </tr>
                        </tbody>
                      </table>
                    </div>
                    <p v-else class="text-xs py-2" style="color: rgba(0,255,65,0.3);">No open ports found on scanned range.</p>
                  </template>
                </ScanCard>

                <!-- ── Firewall ──────────────────────────────────────────── -->
                <ScanCard :config="SCAN_CONFIGS.firewall" :scan="scans.firewall">
                  <template #results="{ data }">
                    <div class="flex flex-wrap items-center gap-4">
                      <div
                        class="flex items-center gap-2.5 px-4 py-2.5"
                        style="border-radius: 2px;"
                        :style="data.firewall?.detected
                          ? 'background: rgba(255,60,90,0.08); border: 1px solid rgba(255,60,90,0.35);'
                          : 'background: rgba(0,255,65,0.05); border: 1px solid rgba(0,255,65,0.7);'"
                      >
                        <span class="text-base">{{ data.firewall?.detected ? '🔴' : '🟢' }}</span>
                        <span
                          class="font-bold text-sm tracking-wider"
                          style="font-family: 'Orbitron', monospace;"
                          :style="data.firewall?.detected ? 'color: #ff3c5a;' : 'color: #00ff41;'"
                        >
                          {{ data.firewall?.detected ? 'WAF DETECTED' : 'NO WAF' }}
                        </span>
                      </div>
                      <div class="flex flex-wrap gap-x-6 gap-y-1 text-sm">
                        <div>
                          <span style="color: rgba(0,255,65,0.35);">NAME </span>
                          <span style="color: #00ff41;">{{ data.firewall?.waf_name || '—' }}</span>
                        </div>
                        <div v-if="data.firewall?.manufacturer && data.firewall.manufacturer !== data.firewall.waf_name">
                          <span style="color: rgba(0,255,65,0.35);">VENDOR </span>
                          <span style="color: #00ff41;">{{ data.firewall.manufacturer }}</span>
                        </div>
                        <div>
                          <span style="color: rgba(0,255,65,0.35);">CONFIDENCE </span>
                          <span style="color: #ffd700;">{{ data.firewall?.confidence || '—' }}</span>
                        </div>
                      </div>
                    </div>
                  </template>
                </ScanCard>

                <!-- ── Technologies ──────────────────────────────────────── -->
                <ScanCard :config="SCAN_CONFIGS.technology" :scan="scans.technology">
                  <template #results="{ data }">
                    <div v-if="data.technologies && Object.keys(data.technologies).length">
                      <p class="text-xs mb-3 tracking-widest uppercase" style="color: rgba(191,0,255,0.5);">
                        {{ Object.keys(data.technologies).length }} technologies identified
                      </p>
                      <div class="flex flex-wrap gap-2">
                        <div
                          v-for="(info, name) in data.technologies"
                          :key="name"
                          class="chip"
                          style="color: #bf00ff; background: rgba(191,0,255,0.06); border-color: rgba(191,0,255,0.22);"
                        >
                          <span>{{ name }}</span>
                          <span v-if="info.version" style="color: rgba(191,0,255,0.45); font-size: 0.7rem;">{{ info.version }}</span>
                          <span v-if="info.confidence" style="color: rgba(191,0,255,0.3); font-size: 0.65rem;">({{ info.confidence }}%)</span>
                        </div>
                      </div>
                    </div>
                    <p v-else class="text-xs py-2" style="color: rgba(0,255,65,0.3);">No technologies detected.</p>
                  </template>
                </ScanCard>

                <!-- ── Subdomains ────────────────────────────────────────── -->
                <ScanCard :config="SCAN_CONFIGS.subdomains" :scan="scans.subdomains">
                  <template #results="{ data }">
                    <div v-if="data.subdomains && data.subdomains.length">
                      <p class="text-xs mb-3 tracking-widest uppercase" style="color: rgba(0,255,65,0.45);">
                        {{ data.subdomains.length }} subdomain{{ data.subdomains.length !== 1 ? 's' : '' }} discovered
                      </p>
                      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-1.5">
                        <div
                          v-for="s in data.subdomains"
                          :key="s.subdomain"
                          class="flex items-center gap-2 px-3 py-1.5 text-xs truncate"
                          style="background: rgba(0,255,65,0.03); border: 1px solid rgba(0,255,65,0.1); border-radius: 2px; color: #00ff41;"
                        >
                          <span style="color: rgba(0,255,65,0.3);">›</span>
                          <span class="truncate">{{ s.subdomain }}</span>
                        </div>
                      </div>
                    </div>
                    <p v-else class="text-xs py-2" style="color: rgba(0,255,65,0.3);">No subdomains discovered.</p>
                  </template>
                </ScanCard>

              </section>
            </Transition>

          </section>
        </Transition>

      </main>

      <!-- ── Footer ────────────────────────────────────────────────────── -->
      <footer class="border-t py-4" style="border-color: rgba(0,255,65,0.08); background: rgba(0,0,0,0.5);">
        <div class="max-w-5xl mx-auto px-6 flex flex-col sm:flex-row items-center justify-between gap-2">
          <p class="text-xs" style="color: rgba(0,255,65,0.7);">
            Matrix Scanner — For authorized use only
          </p>
          <p class="text-xs" style="color: rgba(0,255,65,0.7);">
            DNS · Ports · Firewall · Technologies · Subdomains
          </p>
        </div>
      </footer>

    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import MatrixBackground   from '../components/MatrixBackground.vue'
import DisclaimerCard     from '../components/DisclaimerCard.vue'
import ScanCard           from '../components/ScanCard.vue'
import RecordGroup        from '../components/RecordGroup.vue'
import { scanState, scans, SCAN_CONFIGS, runAllScans, stopScans, resetScans } from '../composables/useScanner.js'
import { exportTxt }      from '../utils/exportReport.js'

// ── Disclaimer ────────────────────────────────────────────────────────────────
const accepted = ref(false)
function accept() { accepted.value = true }

// ── Scan ──────────────────────────────────────────────────────────────────────
const targetUrl    = ref('')
const quickTargets = ['https://example.com', 'https://google.com']

async function start() {
  if (!targetUrl.value.trim() || scanState.isScanning) return
  await runAllScans(targetUrl.value.trim())
}

function stop()  { stopScans() }
function reset() { resetScans() }

// ── Helpers ───────────────────────────────────────────────────────────────────
function hasAnyRecord(records) {
  if (!records) return false
  return Object.values(records).some(arr => Array.isArray(arr) && arr.length > 0)
}
</script>

<style scoped>
.fade-enter-active,  .fade-leave-active  { transition: opacity 0.3s ease; }
.fade-enter-from,    .fade-leave-to      { opacity: 0; }

.slide-down-enter-active, .slide-down-leave-active {
  transition: all 0.3s ease;
  overflow: hidden;
}
.slide-down-enter-from, .slide-down-leave-to {
  opacity: 0;
  max-height: 0;
}
.slide-down-enter-to, .slide-down-leave-from {
  opacity: 1;
  max-height: 600px;
}
</style>
