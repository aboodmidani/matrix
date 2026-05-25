<template>
  <div class="min-h-screen bg-black relative overflow-x-hidden" style="font-family: 'Share Tech Mono', monospace;">
    <MatrixBackground />

    <div class="relative z-10 min-h-screen flex flex-col">

      <!-- Top bar -->
      <header class="border-b" style="border-color: rgba(0,255,65,0.1); background: rgba(0,0,0,0.7); backdrop-filter: blur(8px);">
        <div class="max-w-6xl mx-auto px-6 py-3 flex items-center justify-between">
          <div class="flex items-center gap-3">
            <div class="w-2 h-2 rounded-full" style="background: #00ff41; box-shadow: 0 0 8px #00ff41;"></div>
            <span class="text-xs tracking-[0.3em] uppercase" style="font-family: 'Orbitron', monospace; color: rgba(0,255,65,0.6);">
              MatrixScanner
            </span>
          </div>
          <div class="flex items-center gap-4">
            <span class="text-xs hidden sm:inline" style="color: rgba(0,255,65,0.7);">Web Security Audit Platform</span>
            <span class="text-xs" style="color: rgba(0,255,65,0.7);">v2.0.0</span>
          </div>
        </div>
      </header>

      <!-- Main content -->
      <main class="flex-1 max-w-6xl w-full mx-auto px-4 sm:px-6 py-8">

        <!-- Hero -->
        <section class="text-center mb-6">
          <p class="entrance-subtitle text-xs tracking-[0.5em] uppercase mb-3" style="color: rgba(0,255,65,0.35);">
            Web Security Assessment &amp; Vulnerability Scanner
          </p>
          <h1
            ref="heroTitleRef"
            class="entrance-hero text-5xl sm:text-6xl font-black mb-1 typing-text"
            style="font-family: 'Orbitron', monospace; color: #00ff41; text-shadow: var(--glow-green); letter-spacing: 0.12em; line-height: 1;"
          >
            MATRIX SCANNER
          </h1>
          <p class="entrance-tagline text-xs sm:text-sm mb-4 tracking-wider max-w-xl mx-auto" style="color: rgba(0,255,65,0.45); line-height: 1.6;">
            Online DNS lookup, port scanner, SSL checker, WAF detector, security headers analysis, technology fingerprinting, web crawler &amp; subdomain discovery — all in one free security audit tool.
          </p>
          <div class="entrance-metrics flex items-center justify-center gap-6 mb-2">
            <div class="flex items-center gap-2 text-xs" style="color: rgba(0,255,65,0.5);">
              <span class="text-lg font-black count-up" ref="counterRef" style="color: #00ff41; font-family: 'Orbitron', monospace;">0</span>
              <span>scans completed</span>
            </div>
            <div class="flex items-center gap-2 text-xs" style="color: rgba(0,255,65,0.5);">
              <span class="text-lg font-black" style="color: #00ff41; font-family: 'Orbitron', monospace;">11</span>
              <span>security checks</span>
            </div>
            <div class="flex items-center gap-2 text-xs" style="color: rgba(0,255,65,0.5);">
              <span class="text-lg font-black" style="color: #00ff41; font-family: 'Orbitron', monospace;">Free</span>
            </div>
          </div>
          <div class="entrance-divider flex items-center justify-center gap-4">
            <div class="h-px flex-1 max-w-32" style="background: linear-gradient(90deg, transparent, rgba(0,255,65,0.3));"></div>
            <div class="flex gap-1.5">
              <span class="w-1 h-1 rounded-full" style="background: rgba(0,255,65,0.4);"></span>
              <span class="w-1 h-1 rounded-full" style="background: rgba(0,255,65,0.6);"></span>
              <span class="w-1 h-1 rounded-full" style="background: rgba(0,255,65,0.4);"></span>
            </div>
            <div class="h-px flex-1 max-w-32" style="background: linear-gradient(90deg, rgba(0,255,65,0.3), transparent);"></div>
          </div>
        </section>

        <!-- Disclaimer -->
        <div class="entrance-disclaimer">
          <DisclaimerCard v-if="!accepted" @accepted="accept" />
        </div>

        <!-- Scanner section -->
        <Transition name="fade">
          <section v-if="accepted">

            <!-- Input card -->
            <div class="entrance-input-card matrix-card bracket-corners mb-4">
              <div class="px-6 pt-5 pb-3 border-b" style="border-color: rgba(0,255,65,0.08);">
                <div class="flex items-center gap-2">
                  <span class="w-1.5 h-1.5 rounded-full" style="background: #00ff41;"></span>
                  <span class="text-xs tracking-[0.25em] uppercase" style="color: rgba(0,255,65,0.4);">Target</span>
                </div>
              </div>
              <div class="px-6 py-5">
                <div class="flex flex-col sm:flex-row gap-3">
                  <div class="flex-1 relative">
                    <span
                      class="absolute left-4 top-1/2 -translate-y-1/2 text-base select-none pointer-events-none"
                      style="color: rgba(0,255,65,0.4);"
                    >&#8250;</span>
                    <input
                      ref="urlInputRef"
                      v-model="targetUrl"
                      type="text"
                      placeholder="https://target.com"
                      aria-label="Target URL to scan"
                      aria-describedby="url-history-desc"
                      autocomplete="off"
                      class="matrix-input w-full pl-9 pr-4 py-3 text-sm"
                      style="
                        background: rgba(0,8,2,0.9);
                        border: 1px solid rgba(0,255,65,0.7);
                        color: #00ff41;
                        font-family: 'Share Tech Mono', monospace;
                        border-radius: 2px;
                      "
                      :style="urlError ? { borderColor: 'var(--matrix-red)' } : {}"
                      :disabled="scanState.isScanning"
                      @focus="showHistory = true"
                      @blur="onBlurInput"
                      @keyup.enter="start"
                      @paste="onPaste"
                    />
                    <UrlHistory
                      v-if="showHistory && urlHistory.length"
                      :history="urlHistory"
                      @select="selectHistory"
                      @remove="removeHistory"
                    />
                    <span id="url-history-desc" class="sr-only">Type or paste a URL. Recent URLs will appear below.</span>
                  </div>
                  <div class="flex gap-2">
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
                          background: rgba(255,0,60,0.08);
                          border: 1px solid rgba(255,0,60,0.45);
                          color: #ff003c;
                          font-family: 'Orbitron', monospace;
                          border-radius: 2px;
                        "
                        title="Stop all scans"
                      >
                        <svg class="w-3.5 h-3.5 flex-shrink-0" fill="currentColor" viewBox="0 0 24 24"><rect x="6" y="6" width="12" height="12" rx="1"/></svg>
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
                    class="entrance-quick-item text-xs transition-colors duration-150"
                    :style="targetUrl === t
                      ? 'color: #00ff41; text-decoration: underline;'
                      : 'color: rgba(0,255,65,0.4);'"
                    :disabled="scanState.isScanning"
                  >
                    {{ displayUrl(t) }}
                  </button>
                </div>
                <p v-if="urlError" class="text-xs mt-2" style="color: var(--matrix-red);">
                  {{ urlError }}
                </p>
              </div>
            </div>

            <!-- Progress panel -->
            <Transition name="slide-down">
              <div v-if="scanState.isScanning || (scanState.done && scanState.isStopped)" class="matrix-card mb-4 overflow-hidden">
                <div class="px-6 pt-4 pb-3 border-b flex items-center justify-between" style="border-color: rgba(0,255,65,0.08);">
                  <div class="flex items-center gap-2">
                    <span
                      class="w-1.5 h-1.5 rounded-full"
                      :style="scanState.isScanning
                        ? 'background: #ffd700; box-shadow: 0 0 6px #ffd700; animation: pulse 1s ease-in-out infinite;'
                        : 'background: #ff003c;'"
                    ></span>
                    <span class="text-xs tracking-[0.25em] uppercase" style="color: rgba(0,255,65,0.4);">
                      {{ scanState.isScanning ? 'Scanning' : 'Stopped' }}
                    </span>
                  </div>
                  <span class="text-xs font-bold" style="font-family: 'Orbitron', monospace; color: #00ff41;">
                    {{ scanState.completed }}/{{ scanState.total }}
                  </span>
                </div>
                <div class="px-6 pt-4 pb-2">
                  <div class="flex items-center justify-between mb-1.5">
                    <span class="text-xs truncate max-w-xs" style="color: rgba(0,255,65,0.55);">
                      {{ scanState.currentScan || (scanState.isStopped ? 'Scan stopped' : '') }}
                    </span>
                    <span class="text-xs ml-2 flex-shrink-0" style="color: rgba(0,255,65,0.4);">{{ scanState.progress }}%</span>
                  </div>
                  <div class="h-1.5 overflow-hidden flex gap-px" style="background: rgba(0,255,65,0.03); border-radius: 2px; padding: 1px;">
                    <div
                      v-for="(cfg, key) in SCAN_CONFIGS"
                      :key="key"
                      class="progress-segment flex-1 rounded-sm"
                      :class="scans[key].status"
                      :title="cfg.label + ': ' + scans[key].status"
                    ></div>
                  </div>
                </div>
                <div class="px-6 pb-5 pt-3 grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-2">
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
                          scans[key].status === 'error'    ? '#ff003c' :
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
                          scans[key].status === 'error'    ? 'rgba(255,0,60,0.7)' :
                          scans[key].status === 'scanning' ? '#ffd700' :
                          'rgba(0,255,65,0.7)',
                      }"
                    >{{ cfg.label }}</span>
                    <span v-if="scans[key].status === 'done'"  class="text-xs flex-shrink-0" style="color: #00ff41;">&#10003;</span>
                    <span v-if="scans[key].status === 'error'" class="text-xs flex-shrink-0" style="color: #ff003c;">&#10007;</span>
                  </div>
                </div>
              </div>
            </Transition>

            <!-- Skeleton placeholders during scan -->
            <div v-if="scanState.isScanning" class="space-y-3 fade-in-up-stagger">
              <SkeletonCard v-for="n in 4" :key="'skel-' + n" />
            </div>

            <!-- Scan complete banner -->
            <Transition name="fade">
              <div v-if="scanState.done && !scanState.isStopped" class="scan-banner matrix-card px-6 py-4 mb-4 text-center" style="border-color: rgba(0,255,65,0.7); box-shadow: 0 0 24px rgba(0,255,65,0.15), inset 0 0 24px rgba(0,255,65,0.05);">
                <div class="text-xs tracking-[0.3em] mb-1" style="color: rgba(0,255,65,0.35); font-family: 'Orbitron', monospace;">╔══════════════════════════════════╗</div>
                <div class="text-sm font-bold tracking-[0.3em] mb-1" style="color: #00ff41; font-family: 'Orbitron', monospace;">║ SCAN COMPLETE ║</div>
                <div class="text-xs tracking-[0.2em] mb-1" style="color: rgba(0,255,65,0.55); font-family: 'Orbitron', monospace;">
                  ║ {{ Object.values(scans).filter(s => s.status === 'done').length }}/{{ Object.keys(SCAN_CONFIGS).length }} checks finished ║
                </div>
                <div class="text-xs tracking-[0.3em]" style="color: rgba(0,255,65,0.35); font-family: 'Orbitron', monospace;">╚══════════════════════════════════╝</div>
              </div>
            </Transition>

            <!-- Results -->
            <Transition name="fade">
              <section v-if="scanState.done" class="space-y-3">

                <!-- Stats bar -->
                <StatsBar :stats="scanStats" />

                <!-- Results toolbar -->
                <div class="matrix-card px-6 py-3 flex items-center justify-between gap-4">
                  <div class="flex items-center gap-3 min-w-0">
                    <div
                      class="w-2 h-2 rounded-full flex-shrink-0"
                      :style="scanState.isStopped
                        ? 'background: #ff003c; box-shadow: 0 0 6px #ff003c;'
                        : 'background: #00ff41; box-shadow: 0 0 8px #00ff41;'"
                    ></div>
                    <span
                      class="text-sm font-bold tracking-[0.2em] uppercase flex-shrink-0"
                      style="font-family: 'Orbitron', monospace;"
                      :style="scanState.isStopped ? 'color: #ff003c;' : 'color: #00ff41;'"
                    >
                      {{ scanState.isStopped ? 'Scan Stopped' : 'Scan Complete' }}
                    </span>
                    <span class="text-xs hidden md:inline truncate" style="color: rgba(0,255,65,0.3);">{{ targetUrl }}</span>
                  </div>
                  <div class="flex items-center gap-2 flex-shrink-0">
                    <ShareButton :url="targetUrl" :title="'Security scan results for ' + targetUrl" label="all results" />
                    <button @click="exportTxt(targetUrl, scans, SCAN_CONFIGS)" class="btn-matrix flex items-center gap-2 px-4 py-2 text-xs tracking-[0.15em] uppercase" style="background: rgba(0,255,65,0.06); border: 1px solid rgba(0,255,65,0.3); color: #00ff41; font-family: 'Orbitron', monospace; border-radius: 2px;" title="Download .txt report">
                      <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"/></svg>
                      <span class="hidden sm:inline">TXT</span>
                    </button>
                    <button @click="exportJson(targetUrl, scans, SCAN_CONFIGS)" class="btn-matrix flex items-center gap-2 px-4 py-2 text-xs tracking-[0.15em] uppercase" style="background: rgba(0,255,65,0.06); border: 1px solid rgba(0,255,65,0.3); color: #00ff41; font-family: 'Orbitron', monospace; border-radius: 2px;" title="Download .json report">
                      <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"/></svg>
                      <span class="hidden sm:inline">JSON</span>
                    </button>
                    <button @click="reset" class="btn-matrix px-4 py-2 text-xs tracking-[0.15em] uppercase" style="border: 1px solid rgba(0,255,65,0.7); color: rgba(0,255,65,0.55); font-family: 'Orbitron', monospace; border-radius: 2px;">
                      NEW SCAN
                    </button>
                  </div>
                </div>

                <!-- DNS -->
                <ScanCard :config="SCAN_CONFIGS.dns" :scan="scans.dns" :targetUrl="targetUrl" @rerun="rerunScan('dns')">
                  <template #results="{ data }">
                    <div v-if="hasAnyRecord(data.records)" class="space-y-2">
                      <RecordGroup label="A Records (IPv4)"    :items="data.records?.A"    />
                      <RecordGroup label="AAAA Records (IPv6)" :items="data.records?.AAAA" />
                      <RecordGroup label="MX Records"          :items="data.records?.MX"   />
                      <RecordGroup label="NS Records"          :items="data.records?.NS"   />
                      <RecordGroup label="TXT Records"         :items="data.records?.TXT"  />
                      <RecordGroup label="SOA Records"         :items="data.records?.SOA"  />
                      <RecordGroup label="SRV Records"         :items="data.records?.SRV"  />
                      <RecordGroup label="CNAME Records"       :items="data.records?.CNAME" />
                    </div>
                    <p v-else class="text-xs py-2" style="color: rgba(0,255,65,0.3);">No DNS records found.</p>
                  </template>
                </ScanCard>

                <!-- Ports -->
                <ScanCard :config="SCAN_CONFIGS.ports" :scan="scans.ports" :targetUrl="targetUrl" @rerun="rerunScan('ports')">
                  <template #results="{ data }">
                    <div v-if="data.ports && data.ports.length">
                      <p class="text-xs mb-3 tracking-widest uppercase" style="color: rgba(255,215,0,0.5);">
                        {{ data.ports.length }} open port{{ data.ports.length !== 1 ? 's' : '' }} detected
                      </p>
                      <table class="w-full matrix-table">
                        <thead><tr>
                          <th class="text-left">Port</th><th class="text-left">Protocol</th><th class="text-left">Service</th><th class="text-left hidden sm:table-cell">Version</th>
                        </tr></thead>
                        <tbody>
                          <tr v-for="p in data.ports" :key="p.port">
                            <td><span class="font-bold" style="color: #ffd700;">{{ p.port }}</span></td>
                            <td style="color: rgba(0,255,65,0.55);">{{ p.protocol }}</td>
                            <td style="color: #00ff41;">{{ p.service }}</td>
                            <td class="hidden sm:table-cell" style="color: rgba(0,255,65,0.35); font-size: 0.75rem;">{{ p.version || '&mdash;' }}</td>
                          </tr>
                        </tbody>
                      </table>
                    </div>
                    <p v-else class="text-xs py-2" style="color: rgba(0,255,65,0.3);">No open ports found on scanned range.</p>
                  </template>
                </ScanCard>

                <!-- Firewall -->
                <ScanCard :config="SCAN_CONFIGS.firewall" :scan="scans.firewall" :targetUrl="targetUrl" @rerun="rerunScan('firewall')">
                  <template #results="{ data }">
                    <div class="flex flex-wrap items-center gap-4">
                      <div class="flex items-center gap-2.5 px-4 py-2.5" style="border-radius: 2px;"
                        :style="data.firewall?.detected
                          ? 'background: rgba(255,0,60,0.08); border: 1px solid rgba(255,0,60,0.35); color: #ff003c;'
                          : 'background: rgba(0,255,65,0.05); border: 1px solid rgba(0,255,65,0.7); color: #00ff41;'"
                      >
                        <span class="text-base" aria-hidden="true">&#9679;</span>
                        <span class="font-bold text-sm tracking-wider" style="font-family: 'Orbitron', monospace;"
                          :style="data.firewall?.detected ? 'color: #ff003c;' : 'color: #00ff41;'"
                        >
                          {{ data.firewall?.detected ? 'WAF DETECTED' : 'NO WAF' }}
                        </span>
                      </div>
                      <div class="flex flex-wrap gap-x-6 gap-y-1 text-sm">
                        <div>
                          <span style="color: rgba(0,255,65,0.35);">NAME </span>
                          <span style="color: #00ff41;">{{ data.firewall?.waf_name || '&mdash;' }}</span>
                        </div>
                        <div v-if="data.firewall?.manufacturer && data.firewall.manufacturer !== data.firewall.waf_name">
                          <span style="color: rgba(0,255,65,0.35);">VENDOR </span>
                          <span style="color: #00ff41;">{{ data.firewall.manufacturer }}</span>
                        </div>
                        <div>
                          <span style="color: rgba(0,255,65,0.35);">CONFIDENCE </span>
                          <span style="color: #ffd700;">{{ data.firewall?.confidence || '&mdash;' }}</span>
                        </div>
                      </div>
                    </div>
                  </template>
                </ScanCard>

                <!-- Technology -->
                <ScanCard :config="SCAN_CONFIGS.technology" :scan="scans.technology" :targetUrl="targetUrl" @rerun="rerunScan('technology')">
                  <template #results="{ data }">
                    <div v-if="data.technologies && Object.keys(data.technologies).length">
                      <p class="text-xs mb-3 tracking-widest uppercase" style="color: rgba(191,0,255,0.5);">
                        {{ Object.keys(data.technologies).length }} technologies identified
                      </p>
                      <div class="flex flex-wrap gap-2">
                        <div v-for="(info, name) in data.technologies" :key="name"
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

                <!-- Subdomains -->
                <ScanCard :config="SCAN_CONFIGS.subdomains" :scan="scans.subdomains" :targetUrl="targetUrl" @rerun="rerunScan('subdomains')">
                  <template #results="{ data }">
                    <div v-if="data.subdomains && data.subdomains.length">
                      <p class="text-xs mb-3 tracking-widest uppercase" style="color: rgba(0,255,65,0.45);">
                        {{ data.subdomains.length }} subdomain{{ data.subdomains.length !== 1 ? 's' : '' }} discovered
                      </p>
                      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-1.5">
                        <div v-for="s in data.subdomains" :key="s.subdomain"
                          class="flex items-center gap-2 px-3 py-1.5 text-xs truncate"
                          style="background: rgba(0,255,65,0.03); border: 1px solid rgba(0,255,65,0.1); border-radius: 2px; color: #00ff41;"
                        >
                          <span style="color: rgba(0,255,65,0.3);">&#8250;</span>
                          <span class="truncate">{{ s.subdomain }}</span>
                        </div>
                      </div>
                    </div>
                    <p v-else class="text-xs py-2" style="color: rgba(0,255,65,0.3);">No subdomains discovered.</p>
                  </template>
                </ScanCard>

                <!-- Live Status -->
                <ScanCard :config="SCAN_CONFIGS.live" :scan="scans.live" :targetUrl="targetUrl" @rerun="rerunScan('live')">
                  <template #results="{ data }">
                    <div class="flex flex-wrap items-center gap-4">
                      <div class="flex items-center gap-2.5 px-4 py-2.5" style="border-radius: 2px;"
                        :style="data.live?.alive
                          ? 'background: rgba(0,255,65,0.05); border: 1px solid rgba(0,255,65,0.7); color: #00ff41;'
                          : 'background: rgba(255,0,60,0.08); border: 1px solid rgba(255,0,60,0.35); color: #ff003c;'"
                      >
                        <span class="w-2 h-2 rounded-full" :style="data.live?.alive
                          ? 'background: #00ff41; box-shadow: 0 0 6px #00ff41;'
                          : 'background: #ff003c; box-shadow: 0 0 6px #ff003c;'"></span>
                        <span class="font-bold text-sm tracking-wider" style="font-family: 'Orbitron', monospace;">
                          {{ data.live?.alive ? 'ONLINE' : 'OFFLINE / UNREACHABLE' }}
                        </span>
                      </div>
                      <div class="flex flex-wrap gap-x-6 gap-y-1 text-sm">
                        <div>
                          <span style="color: rgba(0,255,65,0.35);">PING </span>
                          <span style="color: #00ff41;">{{ data.live?.ping_time_ms != null ? data.live.ping_time_ms + ' ms' : '&mdash;' }}</span>
                        </div>
                        <div>
                          <span style="color: rgba(0,255,65,0.35);">HTTP </span>
                          <span :style="data.live?.http_status && data.live.http_status < 400
                            ? 'color: #00ff41;'
                            : data.live?.http_status && data.live.http_status < 500
                              ? 'color: #ffd700;'
                              : 'color: #ff003c;'">
                            {{ data.live?.http_status || '&mdash;' }}
                          </span>
                        </div>
                      </div>
                    </div>
                  </template>
                </ScanCard>

                <!-- SSL -->
                <ScanCard :config="SCAN_CONFIGS.ssl" :scan="scans.ssl" :targetUrl="targetUrl" @rerun="rerunScan('ssl')">
                  <template #results="{ data }">
                    <div v-if="data.ssl && data.ssl.certificate && data.ssl.certificate.subject">
                      <div class="flex flex-wrap items-center gap-3 mb-4">
                        <div class="flex items-center gap-2 px-4 py-2" style="border-radius: 2px;"
                          :style="data.ssl.certificate.expired
                            ? 'background: rgba(255,0,60,0.08); border: 1px solid rgba(255,0,60,0.35);'
                            : data.ssl.certificate.days_remaining < 30
                              ? 'background: rgba(255,215,0,0.08); border: 1px solid rgba(255,215,0,0.35);'
                              : 'background: rgba(0,255,65,0.05); border: 1px solid rgba(0,255,65,0.7);'"
                        >
                          <span class="font-bold text-sm tracking-wider" style="font-family: 'Orbitron', monospace;"
                            :style="data.ssl.certificate.expired
                              ? 'color: #ff003c;'
                              : data.ssl.certificate.days_remaining < 30
                                ? 'color: #ffd700;'
                                : 'color: #00ff41;'"
                          >
                            {{ data.ssl.certificate.expired ? 'EXPIRED' : data.ssl.certificate.days_remaining + ' days' }}
                          </span>
                        </div>
                      </div>
                      <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 text-sm">
                        <div><span style="color: rgba(0,255,65,0.35);">SUBJECT</span><br><span style="color: #00ff41;">{{ data.ssl.certificate.subject }}</span></div>
                        <div><span style="color: rgba(0,255,65,0.35);">ISSUER</span><br><span style="color: #00ff41;">{{ data.ssl.certificate.issuer }}</span></div>
                        <div><span style="color: rgba(0,255,65,0.35);">SERIAL</span><br><span style="color: rgba(0,255,65,0.7); font-size: 0.7rem;">{{ data.ssl.certificate.serial }}</span></div>
                        <div><span style="color: rgba(0,255,65,0.35);">EXPIRES</span><br><span style="color: rgba(0,255,65,0.7);">{{ data.ssl.certificate.not_after }}</span></div>
                        <div class="sm:col-span-2" v-if="data.ssl.certificate.san && data.ssl.certificate.san.length">
                          <span style="color: rgba(0,255,65,0.35);">SAN ({{ data.ssl.certificate.san.length }})</span><br>
                          <div class="flex flex-wrap gap-1 mt-1">
                            <span v-for="s in data.ssl.certificate.san" :key="s" class="chip" style="color: rgba(0,255,65,0.6); background: rgba(0,255,65,0.04); border-color: rgba(0,255,65,0.12); font-size: 0.7rem;">{{ s }}</span>
                          </div>
                        </div>
                      </div>
                    </div>
                    <div v-else-if="data.ssl && data.ssl.error" class="flex items-start gap-2 py-2">
                      <span class="text-red-400 text-lg leading-none">&#9888;</span>
                      <p class="text-red-400 text-xs">{{ data.ssl.error }}</p>
                    </div>
                    <p v-else class="text-xs py-2" style="color: rgba(0,255,65,0.3);">No SSL certificate data available.</p>
                  </template>
                </ScanCard>

                <!-- Security Headers -->
                <ScanCard :config="SCAN_CONFIGS.headers" :scan="scans.headers" :targetUrl="targetUrl" @rerun="rerunScan('headers')">
                  <template #results="{ data }">
                    <div v-if="data.headers">
                      <div class="flex items-center gap-4 mb-4 text-sm">
                        <span style="color: rgba(0,255,65,0.5);">
                          Security headers:
                          <span style="color: #00ff41;">{{ data.headers.security_headers_found }}</span>
                          /
                          <span style="color: rgba(0,255,65,0.5);">{{ data.headers.security_headers_total }}</span>
                        </span>
                        <span v-if="data.headers.missing_security_headers && data.headers.missing_security_headers.length" class="text-xs" style="color: #ff003c;">
                          {{ data.headers.missing_security_headers.length }} missing
                        </span>
                      </div>
                      <div class="space-y-1.5 max-h-64 overflow-y-auto" style="scrollbar-width: thin;">
                        <div v-for="(report, hdr) in data.headers.security_report" :key="hdr"
                          class="flex items-start gap-2 px-3 py-2 text-xs"
                          :style="report.present
                            ? 'background: rgba(0,255,65,0.03); border-left: 2px solid rgba(0,255,65,0.4);'
                            : 'background: rgba(255,0,60,0.03); border-left: 2px solid rgba(255,0,60,0.4);'"
                        >
                          <span :style="report.present ? 'color: #00ff41;' : 'color: #ff003c;'">
                            {{ report.present ? '&#10003;' : '&#10007;' }}
                          </span>
                          <div>
                            <span style="color: #ffd700;">{{ hdr }}</span>
                            <p v-if="report.value" style="color: rgba(0,255,65,0.5); word-break: break-all;">{{ report.value }}</p>
                            <p v-else style="color: rgba(255,0,60,0.5);">MISSING</p>
                          </div>
                        </div>
                      </div>
                    </div>
                    <p v-else class="text-xs py-2" style="color: rgba(0,255,65,0.3);">No header data available.</p>
                  </template>
                </ScanCard>

                <!-- Crawl -->
                <ScanCard :config="SCAN_CONFIGS.crawl" :scan="scans.crawl" :targetUrl="targetUrl" @rerun="rerunScan('crawl')">
                  <template #results="{ data }">
                    <div v-if="data.crawl">
                      <div class="flex flex-wrap gap-4 mb-4">
                        <span class="text-xs px-3 py-1.5" style="background: rgba(0,255,65,0.04); border: 1px solid rgba(0,255,65,0.12); border-radius: 2px; color: rgba(0,255,65,0.7);">URLs: <span style="color: #00ff41;">{{ (data.crawl.urls || []).length }}</span></span>
                        <span class="text-xs px-3 py-1.5" style="background: rgba(0,255,65,0.04); border: 1px solid rgba(0,255,65,0.12); border-radius: 2px; color: rgba(0,255,65,0.7);">Links: <span style="color: #00ff41;">{{ (data.crawl.links || []).length }}</span></span>
                        <span class="text-xs px-3 py-1.5" style="background: rgba(191,0,255,0.04); border: 1px solid rgba(191,0,255,0.12); border-radius: 2px; color: rgba(191,0,255,0.7);">JS: <span style="color: #bf00ff;">{{ (data.crawl.js_files || []).length }}</span></span>
                        <span class="text-xs px-3 py-1.5" style="background: rgba(255,215,0,0.04); border: 1px solid rgba(255,215,0,0.12); border-radius: 2px; color: rgba(255,215,0,0.7);">Forms: <span style="color: #ffd700;">{{ (data.crawl.forms || []).length }}</span></span>
                        <span class="text-xs px-3 py-1.5" style="background: rgba(0,191,255,0.04); border: 1px solid rgba(0,191,255,0.12); border-radius: 2px; color: rgba(0,191,255,0.7);">Emails: <span style="color: #00bfff;">{{ (data.crawl.emails || []).length }}</span></span>
                        <span class="text-xs px-3 py-1.5" style="background: rgba(0,255,65,0.04); border: 1px solid rgba(0,255,65,0.12); border-radius: 2px; color: rgba(0,255,65,0.7);">Comments: <span style="color: #00ff41;">{{ (data.crawl.comments || []).length }}</span></span>
                      </div>
                      <div v-if="data.crawl.links && data.crawl.links.length" class="max-h-48 overflow-y-auto space-y-1">
                        <div v-for="link in data.crawl.links.slice(0, 30)" :key="link" class="text-xs truncate" style="color: rgba(0,255,65,0.5);">
                          <span style="color: rgba(0,255,65,0.3);">&#8250;</span> {{ link }}
                        </div>
                        <p v-if="data.crawl.links.length > 30" class="text-xs mt-1" style="color: rgba(0,255,65,0.3);">... and {{ data.crawl.links.length - 30 }} more</p>
                      </div>
                    </div>
                    <p v-else class="text-xs py-2" style="color: rgba(0,255,65,0.3);">No crawl data available.</p>
                  </template>
                </ScanCard>

                <!-- Directories -->
                <ScanCard :config="SCAN_CONFIGS.directories" :scan="scans.directories" :targetUrl="targetUrl" @rerun="rerunScan('directories')">
                  <template #results="{ data }">
                    <div v-if="data.directories">
                      <p class="text-xs mb-3" style="color: rgba(0,255,65,0.45);">
                        Scanned {{ data.directories.total_scanned }} paths
                        <span v-if="data.directories.found && data.directories.found.length">
                          &mdash; <span style="color: #ffd700;">{{ data.directories.found.length }} found</span>
                        </span>
                      </p>
                      <div v-if="data.directories.found && data.directories.found.length" class="space-y-1">
                        <div v-for="d in data.directories.found" :key="d.path"
                          class="flex items-center gap-2 px-3 py-1.5 text-xs"
                          style="background: rgba(0,255,65,0.03); border: 1px solid rgba(0,255,65,0.07); border-radius: 2px;"
                        >
                          <span :style="{
                            color: d.status < 300 ? '#00ff41' : d.status < 400 ? '#ffd700' : d.status < 500 ? '#ff003c' : 'rgba(0,255,65,0.5)',
                          }">{{ d.path }}</span>
                          <span class="ml-auto" style="color: rgba(0,255,65,0.35);">{{ d.status }}</span>
                        </div>
                      </div>
                      <p v-else class="text-xs py-2" style="color: rgba(0,255,65,0.3);">No interesting paths found.</p>
                    </div>
                    <p v-else class="text-xs py-2" style="color: rgba(0,255,65,0.3);">No directory scan data available.</p>
                  </template>
                </ScanCard>

                <!-- DNS Extended -->
                <ScanCard :config="SCAN_CONFIGS.dnsExtended" :scan="scans.dnsExtended" :targetUrl="targetUrl" @rerun="rerunScan('dnsExtended')">
                  <template #results="{ data }">
                    <div v-if="data.dns_extended">
                      <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                        <div class="px-3 py-2" style="background: rgba(0,255,65,0.03); border: 1px solid rgba(0,255,65,0.07); border-radius: 2px;">
                          <span style="color: rgba(0,255,65,0.35);">CAA Records</span><br>
                          <span v-if="data.dns_extended.caa_records && data.dns_extended.caa_records.length" style="color: #00ff41;">
                            {{ data.dns_extended.caa_records.join(', ') }}
                          </span>
                          <span v-else style="color: rgba(0,255,65,0.3);">None found</span>
                        </div>
                        <div class="px-3 py-2" style="background: rgba(0,255,65,0.03); border: 1px solid rgba(0,255,65,0.07); border-radius: 2px;">
                          <span style="color: rgba(0,255,65,0.35);">DNSSEC</span><br>
                          <span :style="data.dns_extended.dnssec ? 'color: #00ff41;' : 'color: rgba(0,255,65,0.3);'">
                            {{ data.dns_extended.dnssec ? 'Enabled' : 'Not detected' }}
                          </span>
                        </div>
                        <div class="px-3 py-2" style="background: rgba(0,255,65,0.03); border: 1px solid rgba(0,255,65,0.07); border-radius: 2px;">
                          <span style="color: rgba(0,255,65,0.35);">Zone Transfer</span><br>
                          <span :style="{
                            color: data.dns_extended.zone_transfer === 'vulnerable' ? '#ff003c' :
                                   data.dns_extended.zone_transfer === 'secure' ? '#00ff41' : 'rgba(0,255,65,0.3)',
                          }">
                            {{ data.dns_extended.zone_transfer === 'vulnerable' ? 'VULNERABLE' :
                               data.dns_extended.zone_transfer === 'secure' ? 'Secure' :
                               data.dns_extended.zone_transfer || 'Unknown' }}
                          </span>
                        </div>
                      </div>
                    </div>
                    <p v-else class="text-xs py-2" style="color: rgba(0,255,65,0.3);">No extended DNS data available.</p>
                  </template>
                </ScanCard>

              </section>
            </Transition>

          </section>
        </Transition>

      </main>

      <!-- Footer -->
      <footer class="border-t py-6" style="border-color: rgba(0,255,65,0.08); background: rgba(0,0,0,0.5);">
        <div class="max-w-6xl mx-auto px-6">
          <div class="flex flex-col sm:flex-row items-center justify-between gap-4 mb-4">
            <p class="text-xs" style="color: rgba(0,255,65,0.7);">
              MatrixScanner &mdash; Free web security audit &amp; online vulnerability scanner
            </p>
            <div class="flex flex-wrap items-center gap-x-4 gap-y-1 text-xs" style="color: rgba(0,255,65,0.5);">
              <span>DNS &middot; Ports &middot; WAF &middot; Tech &middot; Subdomains</span>
              <span class="hidden sm:inline">&middot;</span>
              <span>SSL &middot; Headers &middot; Crawl &middot; Dirs &middot; DNS-X</span>
            </div>
          </div>
          <div class="h-px mb-4" style="background: rgba(0,255,65,0.06);"></div>
          <div class="flex flex-col sm:flex-row items-center justify-between gap-3">
            <p class="text-xs" style="color: rgba(0,255,65,0.35);">
              Built with security tools from
              <a href="https://nmap.org/" target="_blank" rel="noopener" style="color: rgba(0,255,65,0.6);">Nmap</a>,
              <a href="https://wafw00f.readthedocs.io/" target="_blank" rel="noopener" style="color: rgba(0,255,65,0.6);">wafw00f</a>,
              <a href="https://www.dnsrecon.org/" target="_blank" rel="noopener" style="color: rgba(0,255,65,0.6);">dnsrecon</a>,
              <a href="https://github.com/projectdiscovery/subfinder" target="_blank" rel="noopener" style="color: rgba(0,255,65,0.6);">Subfinder</a>,
              <a href="https://github.com/OJ/gobuster" target="_blank" rel="noopener" style="color: rgba(0,255,65,0.6);">Gobuster</a>,
              <a href="https://github.com/jaeles-project/gospider" target="_blank" rel="noopener" style="color: rgba(0,255,65,0.6);">Gospider</a>,
              and <a href="https://www.cloudflare.com/" target="_blank" rel="noopener" style="color: rgba(0,255,65,0.6);">Cloudflare</a>.
            </p>
            <div class="flex items-center gap-4">
              <a href="https://github.com/aboodmidani/matrix" target="_blank" rel="noopener" class="flex items-center gap-1.5 text-xs transition-colors" style="color: rgba(0,255,65,0.5);" :title="'Star on GitHub'">
                <svg class="w-3.5 h-3.5" fill="currentColor" viewBox="0 0 24 24"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg>
                Star on GitHub
              </a>
              <a href="https://github.com/aboodmidani/matrix/issues" target="_blank" rel="noopener" class="text-xs transition-colors" style="color: rgba(0,255,65,0.5);">
                Report Issue
              </a>
              <a href="https://owasp.org/www-project-web-security-testing-guide/" target="_blank" rel="noopener" class="text-xs transition-colors" style="color: rgba(0,255,65,0.5);">
                OWASP Guide
              </a>
            </div>
          </div>
          <p class="text-xs mt-4 text-center" style="color: rgba(0,255,65,0.2);">
            For authorized security testing only. &copy; MatrixScanner
          </p>
        </div>
      </footer>

    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'
import MatrixBackground   from '../components/MatrixBackground.vue'
import DisclaimerCard     from '../components/DisclaimerCard.vue'
import ScanCard           from '../components/ScanCard.vue'
import RecordGroup        from '../components/RecordGroup.vue'
import StatsBar           from '../components/StatsBar.vue'
import ShareButton        from '../components/ShareButton.vue'
import SkeletonCard       from '../components/SkeletonCard.vue'
import UrlHistory from '../components/UrlHistory.vue'
import { getUrlHistory, addUrlHistory } from '../utils/storage.js'
import { scanState, scans, SCAN_CONFIGS, runAllScans, runSingleScan, stopScans, resetScans, getSavedState, restoreSavedScans } from '../composables/useScanner.js'
import { exportTxt, exportJson }      from '../utils/exportReport.js'
import { useScanResultMeta }          from '../composables/usePageMeta.js'

const targetUrl    = ref('')
const urlError     = ref('')
const quickTargets = ['https://example.com', 'https://google.com', 'https://github.com', 'https://stackoverflow.com']
const urlHistory   = ref([])
const showHistory  = ref(false)

const accepted = ref(false)
function accept() { accepted.value = true }

let elapsedTimer = null
onUnmounted(() => { if (elapsedTimer) clearInterval(elapsedTimer) })

const urlInputRef   = ref(null)
const heroTitleRef  = ref(null)
const counterRef    = ref(null)

const savedState = getSavedState()
if (savedState) {
  accepted.value = true
  targetUrl.value = savedState.url || ''
  restoreSavedScans(savedState)
}

// Load URL history
onMounted(() => {
  urlHistory.value = getUrlHistory()
  // Typing animation for hero title (using clip-path reveal)
  if (heroTitleRef.value) {
    const el = heroTitleRef.value
    const text = el.textContent
    el.style.clipPath = 'inset(0 100% 0 0)'
    el.style.visibility = 'visible'
    const totalLen = text.length
    let i = 0
    function typeChar() {
      if (i <= totalLen) {
        const pct = ((totalLen - i) / totalLen) * 100
        el.style.clipPath = `inset(0 ${pct}% 0 0)`
        i++
        setTimeout(typeChar, 70 + Math.random() * 30)
      } else {
        el.classList.add('typing-done')
        startCounter()
      }
    }
    setTimeout(typeChar, 800)
  } else {
    startCounter()
  }
})

function startCounter() {
  const el = counterRef.value
  if (!el) return
  const target = 10000
  let current = 0
  const step = Math.ceil(target / 60)
  const interval = setInterval(() => {
    current += step
    if (current >= target) {
      current = target
      clearInterval(interval)
    }
    el.textContent = current.toLocaleString() + '+'
  }, 30)
}

function validateUrl(url) {
  if (!url.trim()) return 'URL is required'
  const cleaned = url.trim()
  try {
    const withProto = cleaned.startsWith('http') ? cleaned : `https://${cleaned}`
    const parsed = new URL(withProto)
    if (!parsed.hostname || !parsed.hostname.includes('.')) return 'Invalid domain'
    const privatePatterns = [/^127\./, /^10\./, /^172\.(1[6-9]|2\d|3[01])\./, /^192\.168\./, /^localhost$/i, /^0\.0\.0\.0$/]
    if (privatePatterns.some(p => p.test(parsed.hostname))) return 'Private/internal addresses are not allowed'
    return ''
  } catch {
    return 'Invalid URL format'
  }
}

function selectHistory(url) {
  targetUrl.value = url
  showHistory.value = false
  start()
}

function onBlurInput() {
  setTimeout(() => { showHistory.value = false }, 200)
}

function removeHistory(index) {
  const history = getUrlHistory()
  history.splice(index, 1)
  localStorage.setItem('ms-url-history', JSON.stringify(history))
  urlHistory.value = getUrlHistory()
}

function onPaste(e) {
  setTimeout(() => {
    const val = targetUrl.value.trim()
    if (val && !val.match(/^https?:\/\//)) {
      targetUrl.value = 'https://' + val.replace(/^(?:https?:\/\/)?/, '')
    }
  }, 0)
}

async function start() {
  if (scanState.isScanning) return
  urlError.value = validateUrl(targetUrl.value)
  if (urlError.value) return
  const cleaned = targetUrl.value.trim()
  addUrlHistory(cleaned)
  urlHistory.value = getUrlHistory()
  if (typeof window.gtag !== 'undefined') {
    window.gtag('event', 'scan_started', { target_url: cleaned })
  }
  if (elapsedTimer) clearInterval(elapsedTimer)
  elapsedTimer = setInterval(() => {
    if (scanState.startTime) {
      const secs = Math.floor((Date.now() - scanState.startTime) / 1000)
      scanState.elapsed = secs >= 60 ? `${Math.floor(secs / 60)}m ${secs % 60}s` : `${secs}s`
    }
  }, 1000)
  await runAllScans(cleaned)
  if (elapsedTimer) clearInterval(elapsedTimer)
  if (scanState.startTime) {
    const secs = Math.floor((Date.now() - scanState.startTime) / 1000)
    scanState.elapsed = secs >= 60 ? `${Math.floor(secs / 60)}m ${secs % 60}s` : `${secs}s`
  }
}

function stop()  { stopScans() }
function reset() {
  if (elapsedTimer) clearInterval(elapsedTimer)
  elapsedTimer = null
  scanState.startTime = null
  scanState.elapsed = ''
  resetScans()
}

function rerunScan(key) {
  if (scanState.isScanning) return
  runSingleScan(key, targetUrl.value.trim())
}

function displayUrl(url) {
  return url.replace(/^https?:\/\//, '')
}

function hasAnyRecord(records) {
  if (!records) return false
  return Object.values(records).some(arr => Array.isArray(arr) && arr.length > 0)
}

// Dynamic page meta per scan results
useScanResultMeta(targetUrl, scans)

// Stats computation for StatsBar
const scanStats = computed(() => {
  const pass = Object.values(scans).filter(s => s.status === 'done').length
  const error = Object.values(scans).filter(s => s.status === 'error').length
  const scanning = Object.values(scans).filter(s => s.status === 'scanning').length
  const total = Object.keys(SCAN_CONFIGS).length
  let duration = ''
  if (scanState.elapsed) {
    duration = scanState.elapsed
  } else if (scanState.isScanning) {
    duration = 'Scanning...'
  } else if (scanState.startTime) {
    const secs = Math.floor((Date.now() - scanState.startTime) / 1000)
    duration = secs >= 60 ? `${Math.floor(secs / 60)}m ${secs % 60}s` : `${secs}s`
  }
  return {
    pass,
    warn: scanning,
    fail: error,
    total,
    duration,
  }
})

watch(() => scanState.isScanning, (scanning) => {
  if (!scanning && scanState.done && typeof window.gtag !== 'undefined') {
    const completed = Object.values(scans).filter(s => s.status === 'done').length
    const errors = Object.values(scans).filter(s => s.status === 'error').length
    window.gtag('event', 'scan_completed', {
      target_url: targetUrl.value,
      checks_completed: completed,
      checks_failed: errors,
    })
  }
})
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
