<template>
  <div class="min-h-screen bg-black text-green-400 font-mono overflow-hidden relative">
    <!-- Matrix Background Animation -->
    <canvas id="matrix-canvas" class="fixed inset-0 z-0 opacity-20"></canvas>

    <!-- Legal Disclaimer Modal -->
    <div v-if="showDisclaimer" class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-80 backdrop-blur-sm animate__animated animate__fadeIn p-4">
      <div class="bg-gray-900 border-2 border-green-500 rounded-lg p-4 md:p-8 max-w-sm sm:max-w-2xl mx-4 w-full shadow-2xl animate__animated animate__zoomIn">
        <div class="text-center mb-8">
          <div class="w-16 h-16 mx-auto mb-4 border-2 border-amber-500 rounded-full flex items-center justify-center bg-gray-800 animate-pulse">
            <svg class="w-8 h-8 text-amber-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z"></path>
            </svg>
          </div>
          <h2 class="text-2xl font-bold text-green-400 mb-2 font-mono tracking-wider">[LEGAL DISCLAIMER]</h2>
          <p class="text-green-300 font-mono">Please read carefully before accessing this system</p>
        </div>

        <div class="bg-gray-800 border border-green-600 rounded p-6 mb-8">
          <div class="text-green-300 text-sm font-mono space-y-3">
            <p><span class="text-red-400">[WARNING]</span> This tool is for educational and authorized security testing purposes only.</p>
            <p><span class="text-green-400">></span> Only scan systems you own or have explicit permission to test</p>
            <p><span class="text-green-400">></span> Unauthorized scanning may violate laws and terms of service</p>
            <p><span class="text-green-400">></span> The developers are not responsible for misuse of this tool</p>
            <p><span class="text-green-400">></span> Results may contain false positives or miss vulnerabilities</p>
            <p><span class="text-green-400">></span> Use at your own risk and responsibility</p>
          </div>
        </div>

        <div class="grid grid-cols-2 gap-4">
          <button @click="acceptDisclaimer" class="bg-green-600 hover:bg-green-500 text-black font-bold py-4 px-6 rounded border-2 border-green-400 hover:border-green-300 transition-all duration-300 transform hover:scale-105 font-mono tracking-wide">[ACCEPT & CONTINUE]</button>
          <button @click="declineDisclaimer" class="bg-red-600 hover:bg-red-500 text-white font-bold py-4 px-6 rounded border-2 border-red-400 hover:border-red-300 transition-all duration-300 font-mono tracking-wide">[EXIT SYSTEM]</button>
        </div>
      </div>
    </div>

    <!-- Header -->
    <header class="sticky top-0 z-40 bg-black border-b border-green-500 shadow-lg">
      <div class="max-w-7xl mx-auto px-4 py-4">
        <div class="flex items-center justify-between">
          <div class="flex items-center space-x-4">
            <div class="w-10 h-10 border border-green-500 flex items-center justify-center animate-pulse">
              <svg class="w-6 h-6 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"></path>
              </svg>
            </div>
            <div>
              <h1 class="text-xl font-bold text-green-400 font-mono tracking-wider">WEB SECURITY MATRIX</h1>
              <p class="text-xs text-green-300 font-mono">v3.0 - ADVANCED PENETRATION FRAMEWORK</p>
            </div>
          </div>
          <div class="flex items-center space-x-4 text-xs text-green-400 font-mono">
            <span>{{ currentTime.toLocaleTimeString() }}</span>
            <span>|</span>
            <span>SESSION: {{ sessionId }}</span>
          </div>
        </div>
      </div>
    </header>

    <!-- Main Content -->
    <main class="relative z-10 px-4 py-8 max-w-7xl mx-auto">
      <!-- Command Terminal Interface -->
      <div class="bg-black border-2 border-green-500 rounded-lg p-6 mb-8 shadow-2xl">
        <div class="flex items-center mb-4 text-green-400 text-sm font-mono">
          <span class="animate-pulse">●</span>
          <span class="ml-2">TERMINAL ACCESS GRANTED</span>
          <span class="ml-auto">SESSION: {{ sessionId }}</span>
        </div>

        <!-- Terminal Header -->
        <div class="border border-green-600 rounded p-4 mb-6 bg-gray-900">
          <div class="text-green-400 font-mono text-sm mb-2">
            <span class="text-green-300">root@matrix</span>:<span class="text-blue-400">~</span>$ security-audit --target [INPUT_REQUIRED]
          </div>
          <div class="text-green-400 font-mono text-xs opacity-75">Advanced Penetration Testing Suite with Modular Scanning</div>
        </div>

        <!-- Input Section -->
        <div class="grid grid-cols-1 xl:grid-cols-3 gap-4 md:gap-6">
          <!-- Left Panel - Target Input -->
          <div class="xl:col-span-2">
            <div class="border border-green-600 rounded p-4 md:p-6 bg-gray-900">
              <div class="text-green-400 font-mono text-sm mb-3">
                <span class="text-green-300">></span> Enter target coordinates:
              </div>
              <div class="flex flex-col sm:flex-row gap-3">
                <input v-model="targetUrl" type="text" placeholder="https://target-system.com" class="flex-1 bg-black border border-green-500 rounded px-3 py-3 md:py-2 text-green-400 font-mono text-sm md:text-base focus:outline-none focus:border-green-400 transition-colors" :class="{ 'animate__animated animate__pulse': loading }" />
                <button @click="startAudit" :disabled="loading || !targetUrl.trim()" class="px-6 py-3 md:py-2 bg-green-600 hover:bg-green-500 disabled:bg-gray-600 text-black font-mono font-bold rounded border border-green-400 hover:border-green-300 transition-all duration-300 disabled:cursor-not-allowed min-h-[44px] touch-manipulation" :class="{ 'animate__animated animate__bounce': loading }">
                  <span v-if="loading" class="flex items-center">
                    <span class="animate-spin mr-2">⟳</span>
                    <span class="hidden sm:inline">EXECUTING...</span>
                    <span class="sm:hidden">SCANNING</span>
                  </span>
                  <span v-else>
                    <span class="hidden sm:inline">INITIATE SCAN</span>
                    <span class="sm:hidden">SCAN</span>
                  </span>
                </button>
              </div>
            </div>
          </div>

          <!-- Right Panel - Scan Options -->
          <div class="space-y-4">
            <div class="border border-green-600 rounded p-4 md:p-6 bg-gray-900">
              <div class="text-green-400 font-mono text-sm mb-3">
                <span class="text-green-300">></span> Scan modules:
              </div>
              <div class="space-y-3">
                <label class="flex items-center text-green-300 font-mono text-xs md:text-sm">
                  <input v-model="scanOptions.enable_dns" type="checkbox" class="mr-2 accent-green-500 w-4 h-4" />
                  <span class="hidden sm:inline">[DNS] Domain enumeration</span>
                  <span class="sm:hidden">[DNS]</span>
                </label>
                <label class="flex items-center text-green-300 font-mono text-xs md:text-sm">
                  <input v-model="scanOptions.enable_ports" type="checkbox" class="mr-2 accent-green-500 w-4 h-4" />
                  <span class="hidden sm:inline">[NET] Port reconnaissance</span>
                  <span class="sm:hidden">[NET]</span>
                </label>
                <label class="flex items-center text-green-300 font-mono text-xs md:text-sm">
                  <input v-model="scanOptions.enable_vulns" type="checkbox" class="mr-2 accent-green-500 w-4 h-4" />
                  <span class="hidden sm:inline">[VULN] Vulnerability assessment</span>
                  <span class="sm:hidden">[VULN]</span>
                </label>
                <label class="flex items-center text-green-300 font-mono text-xs md:text-sm">
                  <input v-model="scanOptions.enable_directories" type="checkbox" class="mr-2 accent-green-500 w-4 h-4" />
                  <span class="hidden sm:inline">[DIR] Directory traversal</span>
                  <span class="sm:hidden">[DIR]</span>
                </label>
              </div>
            </div>

            <!-- Wordlist Selection -->
            <div class="border border-green-600 rounded p-4 md:p-6 bg-gray-900">
              <div class="text-green-400 font-mono text-sm mb-3">
                <span class="text-green-300">></span> Directory scan wordlist:
              </div>
              <select v-model="scanOptions.wordlist" class="w-full bg-black border border-green-500 rounded px-3 py-2 text-green-400 font-mono text-sm focus:outline-none focus:border-green-400 transition-colors">
                <option value="common">Common (Fast)</option>
                <option value="fast">Fast (Small)</option>
                <option value="big">Big (Comprehensive)</option>
                <option value="all">All (Extended)</option>
              </select>
            </div>
          </div>
        </div>
      </div>

      <!-- Progress Bar -->
      <div v-if="loading" class="bg-black border-2 border-green-500 rounded-lg p-6 mb-8 shadow-2xl">
        <div class="flex justify-between items-center mb-6">
          <div class="text-green-400 font-mono text-lg font-bold tracking-wider">
            <span class="text-green-300">[SYSTEM SCAN IN PROGRESS]</span>
          </div>
          <button @click="stopScan" class="px-6 py-3 bg-red-600 hover:bg-red-700 text-white font-mono text-sm font-bold rounded border-2 border-red-500 hover:border-red-400 transition-all duration-300 shadow-lg hover:shadow-red-500/25">[TERMINATE SCAN]</button>
        </div>
        <div class="border border-green-600 rounded p-4 bg-gray-900">
          <div class="text-green-400 font-mono text-xs mb-2">
            <span class="text-green-300">root@matrix</span>:<span class="text-blue-400">~</span>$ ./security-audit --verbose
          </div>
          <div class="space-y-1">
            <div class="flex items-center text-green-300 font-mono text-xs">
              <span class="animate-pulse mr-2">></span>
              <span>Initializing scan engines...</span>
              <span class="ml-auto text-green-400">[OK]</span>
            </div>
            <div class="flex items-center text-green-300 font-mono text-xs">
              <span class="animate-pulse mr-2">></span>
              <span>Connecting to target...</span>
              <span class="ml-auto text-green-400">[OK]</span>
            </div>
            <div v-if="scanOptions.enable_dns" class="flex items-center text-green-300 font-mono text-xs">
              <span class="mr-2" :class="scanProgress.dns === 'DONE' ? 'text-green-400' : 'animate-spin'">{{ scanProgress.dns === "DONE" ? "✓" : "⟳" }}</span>
              <span>DNS enumeration & reconnaissance...</span>
              <span class="ml-auto" :class="scanProgress.dns === 'DONE' ? 'text-green-400' : 'text-yellow-400'">[{{ scanProgress.dns }}]</span>
            </div>
            <div v-if="scanOptions.enable_ports" class="flex items-center text-green-300 font-mono text-xs">
              <span class="mr-2" :class="scanProgress.ports === 'DONE' ? 'text-green-400' : scanProgress.ports === 'IN PROGRESS' ? 'animate-spin' : ''">{{ scanProgress.ports === "DONE" ? "✓" : scanProgress.ports === "IN PROGRESS" ? "⟳" : ">" }}</span>
              <span>Port scanning & service detection...</span>
              <span class="ml-auto" :class="scanProgress.ports === 'DONE' ? 'text-green-400' : scanProgress.ports === 'IN PROGRESS' ? 'text-yellow-400' : 'text-gray-500'">[{{ scanProgress.ports }}]</span>
            </div>
            <div v-if="scanOptions.enable_vulns" class="flex items-center text-green-300 font-mono text-xs">
              <span class="mr-2" :class="scanProgress.vulnerabilities === 'DONE' ? 'text-green-400' : scanProgress.vulnerabilities === 'IN PROGRESS' ? 'animate-spin' : ''">{{ scanProgress.vulnerabilities === "DONE" ? "✓" : scanProgress.vulnerabilities === "IN PROGRESS" ? "⟳" : ">" }}</span>
              <span>Vulnerability assessment...</span>
              <span class="ml-auto" :class="scanProgress.vulnerabilities === 'DONE' ? 'text-green-400' : scanProgress.vulnerabilities === 'IN PROGRESS' ? 'text-yellow-400' : 'text-gray-500'">[{{ scanProgress.vulnerabilities }}]</span>
            </div>
            <div v-if="scanOptions.enable_directories" class="flex items-center text-green-300 font-mono text-xs">
              <span class="mr-2" :class="scanProgress.directories === 'DONE' ? 'text-green-400' : scanProgress.directories === 'IN PROGRESS' ? 'animate-spin' : ''">{{ scanProgress.directories === "DONE" ? "✓" : scanProgress.directories === "IN PROGRESS" ? "⟳" : ">" }}</span>
              <span>Directory traversal & exposure check...</span>
              <span class="ml-auto" :class="scanProgress.directories === 'DONE' ? 'text-green-400' : scanProgress.directories === 'IN PROGRESS' ? 'text-yellow-400' : 'text-gray-500'">[{{ scanProgress.directories }}]</span>
            </div>
          </div>
          <div class="mt-4">
            <div class="w-full bg-gray-700 h-2 rounded">
              <div class="bg-green-500 h-2 rounded animate-pulse" style="width: 100%"></div>
            </div>
            <div class="text-center text-green-300 font-mono text-xs mt-2">
              <span class="animate-pulse">█</span><span class="animate-pulse ml-1">█</span><span class="animate-pulse ml-1">█</span>
              EXECUTING ACTIVE SCAN MODULES
              <span class="animate-pulse ml-1">█</span><span class="animate-pulse ml-1">█</span><span class="animate-pulse ml-1">█</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Error Notification -->
      <div v-if="error" class="bg-black border-2 border-red-500 rounded-lg p-6 mb-8 shadow-2xl">
        <div class="text-red-400 font-mono text-sm mb-4">
          <span class="text-red-300">[ERROR]</span> Scan execution failed
        </div>
        <div class="border border-red-600 rounded p-4 bg-gray-900">
          <div class="text-red-400 font-mono text-xs mb-2">
            <span class="text-red-300">root@matrix</span>:<span class="text-blue-400">~</span>$ ./security-audit --target {{ targetUrl }}
          </div>
          <div class="text-red-300 font-mono text-xs">
            <span class="text-red-400">[ERROR]</span> {{ error }}
          </div>
          <div class="mt-2 text-red-400 font-mono text-xs">
            <span class="text-red-300">></span> Check target URL and try again
          </div>
        </div>
      </div>

      <!-- Results Dashboard -->
      <div v-if="results" class="space-y-6">
        <!-- System Information -->
        <div class="bg-black bg-opacity-80 border border-green-500 rounded-lg p-6">
          <div class="flex justify-between items-center mb-4">
            <h3 class="text-xl font-bold text-green-400 flex items-center">
              <svg class="w-6 h-6 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
              </svg>
              System Information
            </h3>
            <div class="flex space-x-2">
              <button @click="downloadReport('all')" class="px-4 py-2 bg-blue-600 hover:bg-blue-500 text-black font-mono text-sm font-bold rounded border border-blue-400 transition-all duration-300">[DOWNLOAD ALL]</button>
            </div>
          </div>
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            <div class="bg-gray-900 p-4 rounded border border-green-600">
              <span class="text-green-300 text-sm">Target:</span>
              <span class="text-green-400 font-mono block mt-1">{{ results.domain }}</span>
            </div>
            <div class="bg-gray-900 p-4 rounded border border-green-600">
              <span class="text-green-300 text-sm">URL:</span>
              <span class="text-green-400 font-mono text-sm block mt-1">{{ results.url }}</span>
            </div>
            <div v-if="results.dns && results.dns.records" class="bg-gray-900 p-4 rounded border border-green-600">
              <span class="text-green-300 text-sm">DNS Records:</span>
              <span class="text-green-400 font-mono text-sm block mt-1">{{ results.dns.records.A_records.length }} A records</span>
            </div>
            <div v-if="results.ports && results.ports.length > 0" class="bg-gray-900 p-4 rounded border border-green-600">
              <span class="text-green-300 text-sm">Open Ports:</span>
              <span class="text-green-400 font-mono text-sm block mt-1">{{ results.ports.length }} found</span>
            </div>
          </div>
        </div>

        <!-- DNS Results -->
        <div v-if="results.dns" class="bg-black bg-opacity-80 border border-green-500 rounded-lg p-6">
          <div class="flex justify-between items-center mb-4">
            <h3 class="text-xl font-bold text-green-400 flex items-center">
              <svg class="w-6 h-6 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 01-9 9m9-9a9 9 0 00-9-9m9 9H3m9 9v-9m0-9v9m0 9c-5 0-9-4-9-9s4-9 9-9"></path>
              </svg>
              DNS Information
            </h3>
            <div class="flex space-x-2">
              <button @click="downloadReport('dns')" class="px-4 py-2 bg-blue-600 hover:bg-blue-500 text-black font-mono text-sm font-bold rounded border border-blue-400 transition-all duration-300">[DOWNLOAD]</button>
            </div>
          </div>
              <div v-if="results.dns.records" class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div class="bg-gray-900 p-4 rounded border border-green-600">
                  <h4 class="text-green-400 font-bold mb-2">A Records (IPv4)</h4>
                  <div v-if="results.dns.records.A_records.length > 0" class="space-y-1">
                    <div v-for="ip in results.dns.records.A_records" :key="ip" class="text-green-400 font-mono text-sm break-all">{{ ip }}</div>
                  </div>
                  <div v-else class="text-green-300">No A records found</div>
                </div>
                <div class="bg-gray-900 p-4 rounded border border-green-600">
                  <h4 class="text-green-400 font-bold mb-2">MX Records</h4>
                  <div v-if="results.dns.records.MX_records.length > 0" class="space-y-1">
                    <div v-for="mx in results.dns.records.MX_records" :key="mx" class="text-green-400 font-mono text-sm break-all">{{ mx }}</div>
                  </div>
                  <div v-else class="text-green-300">No MX records found</div>
                </div>
                <div class="bg-gray-900 p-4 rounded border border-green-600">
                  <h4 class="text-green-400 font-bold mb-2">NS Records</h4>
                  <div v-if="results.dns.records.NS_records.length > 0" class="space-y-1">
                    <div v-for="ns in results.dns.records.NS_records" :key="ns" class="text-green-400 font-mono text-sm break-all">{{ ns }}</div>
                  </div>
                  <div v-else class="text-green-300">No NS records found</div>
                </div>
                <div class="bg-gray-900 p-4 rounded border border-green-600">
                  <h4 class="text-green-400 font-bold mb-2">TXT Records</h4>
                  <div v-if="results.dns.records.TXT_records.length > 0" class="space-y-1">
                    <div v-for="txt in results.dns.records.TXT_records" :key="txt" class="text-green-400 font-mono text-sm break-all">{{ txt }}</div>
                  </div>
                  <div v-else class="text-green-300">No TXT records found</div>
                </div>
              </div>
          <div v-else-if="results.dns.error" class="text-red-400">{{ results.dns.error }}</div>
        </div>

        <!-- Port Scan Results -->
        <div v-if="results.ports" class="bg-black bg-opacity-80 border border-green-500 rounded-lg p-6">
          <div class="flex justify-between items-center mb-4">
            <h3 class="text-xl font-bold text-green-400 flex items-center">
              <svg class="w-6 h-6 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path>
              </svg>
              Network Intelligence
            </h3>
            <div class="flex space-x-2">
              <button @click="downloadReport('ports')" class="px-4 py-2 bg-blue-600 hover:bg-blue-500 text-black font-mono text-sm font-bold rounded border border-blue-400 transition-all duration-300">[DOWNLOAD]</button>
            </div>
          </div>
          <div v-if="results.ports.length > 0 && !results.ports[0].error" class="overflow-x-auto">
            <table class="w-full text-sm">
              <thead>
                <tr class="border-b border-green-600">
                  <th class="text-left text-green-400 font-mono py-2">Port</th>
                  <th class="text-left text-green-400 font-mono py-2">Protocol</th>
                  <th class="text-left text-green-400 font-mono py-2">Service</th>
                  <th class="text-left text-green-400 font-mono py-2">Status</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="port in results.ports" :key="port.port" class="border-b border-gray-700 hover:bg-gray-800">
                  <td class="text-green-400 font-mono py-2 break-all">{{ port.port }}</td>
                  <td class="text-green-400 font-mono py-2 break-all">{{ port.protocol }}</td>
                  <td class="text-green-400 font-mono py-2 break-all">{{ port.service }}</td>
                  <td class="py-2">
                    <span class="px-2 py-1 bg-green-600 text-black text-xs rounded font-mono">OPEN</span>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
          <div v-else-if="results.ports[0] && results.ports[0].error" class="text-red-400">{{ results.ports[0].error }}</div>
          <div v-else class="text-green-300">No open ports detected</div>
        </div>

        <!-- Directory Scan Results -->
        <div v-if="results.directories" class="bg-black bg-opacity-80 border border-green-500 rounded-lg p-6">
          <div class="flex justify-between items-center mb-4">
            <h3 class="text-xl font-bold text-green-400 flex items-center">
              <svg class="w-6 h-6 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2H5a2 2 0 00-2-2z"></path>
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 5a2 2 0 012-2h4a2 2 0 012 2v2H8V5z"></path>
              </svg>
              Directory Scan Results
            </h3>
            <div class="flex space-x-2">
              <button @click="downloadReport('directories')" class="px-4 py-2 bg-blue-600 hover:bg-blue-500 text-black font-mono text-sm font-bold rounded border border-blue-400 transition-all duration-300">[DOWNLOAD]</button>
            </div>
          </div>
          <div v-if="results.directories.length > 0 && !results.directories[0].error" class="overflow-x-auto">
            <table class="w-full text-sm">
              <thead>
                <tr class="border-b border-green-600">
                  <th class="text-left text-green-400 font-mono py-2">Status</th>
                  <th class="text-left text-green-400 font-mono py-2">URL</th>
                  <th class="text-left text-green-400 font-mono py-2">Status Code</th>
                  <th class="text-left text-green-400 font-mono py-2">Size</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="result in results.directories" :key="result.url" class="border-b border-gray-700 hover:bg-gray-800">
                  <td class="py-2">
                    <span class="px-2 py-1 rounded text-xs font-bold" :class="result.found ? 'bg-orange-600' : 'bg-blue-600'">
                      {{ result.found ? "EXPOSED" : "SECURE" }}
                    </span>
                  </td>
                  <td class="text-green-400 font-mono text-sm py-2 break-all">{{ result.url }}</td>
                  <td class="text-green-400 font-mono py-2 break-all">{{ result.status_code }}</td>
                  <td class="text-green-400 font-mono py-2 break-all">{{ result.size || 'N/A' }}</td>
                </tr>
              </tbody>
            </table>
          </div>
          <div v-else-if="results.directories[0] && results.directories[0].error" class="text-red-400">{{ results.directories[0].error }}</div>
          <div v-else class="text-green-300">No directories found</div>
        </div>

        <!-- Vulnerability Scan Results -->
        <div v-if="results.vulnerabilities" class="bg-black bg-opacity-80 border border-green-500 rounded-lg p-6">
          <div class="flex justify-between items-center mb-4">
            <h3 class="text-xl font-bold text-green-400 flex items-center">
              <svg class="w-6 h-6 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z"></path>
              </svg>
              Security Vulnerabilities
            </h3>
            <div class="flex space-x-2">
              <button @click="downloadReport('vulnerabilities')" class="px-4 py-2 bg-blue-600 hover:bg-blue-500 text-black font-mono text-sm font-bold rounded border border-blue-400 transition-all duration-300">[DOWNLOAD]</button>
            </div>
          </div>
          <div v-if="results.vulnerabilities.length > 0 && !results.vulnerabilities[0].error" class="space-y-4">
            <div v-for="vuln in results.vulnerabilities" :key="vuln.description" class="p-4 bg-gray-900 rounded border-l-4" :class="vuln.severity === 'High' ? 'border-red-500' : vuln.severity === 'Medium' ? 'border-yellow-500' : 'border-blue-500'">
              <div class="flex justify-between items-start">
                <div>
                  <span class="text-green-400 font-bold break-all">{{ vuln.type }}</span>
                  <p class="text-green-300 text-sm mt-1 break-all">{{ vuln.description }}</p>
                </div>
                <span class="px-2 py-1 rounded text-xs font-bold" :class="vuln.severity === 'High' ? 'bg-red-600' : vuln.severity === 'Medium' ? 'bg-yellow-600' : 'bg-blue-600'">{{ vuln.severity }}</span>
              </div>
            </div>
          </div>
          <div v-else-if="results.vulnerabilities[0] && results.vulnerabilities[0].error" class="text-red-400">{{ results.vulnerabilities[0].error }}</div>
          <div v-else class="text-green-300">No vulnerabilities detected</div>
        </div>
      </div>
    </main>
  </div>
</template>

<script>
export default {
  name: 'App',
  data() {
    return {
      showDisclaimer: true,
      targetUrl: '',
      loading: false,
      results: null,
      error: null,
      currentTime: new Date(),
      scanProgress: {
        dns: 'PENDING',
        ports: 'PENDING',
        vulnerabilities: 'PENDING',
        directories: 'PENDING',
      },
      scanOptions: {
        enable_dns: true,
        enable_ports: true,
        enable_vulns: true,
        enable_directories: true,
        wordlist: 'common',
      },
    };
  },
  computed: {
    sessionId() {
      return Math.random().toString(36).substring(2, 8).toUpperCase();
    },
  },
  mounted() {
    this.initMatrixRain();
    this.startLiveClock();
  },
  beforeUnmount() {
    if (this.matrixCleanup) {
      this.matrixCleanup();
    }
  },
  methods: {
    async startAudit() {
      if (!this.targetUrl.trim()) {
        this.error = 'Please enter a valid URL';
        return;
      }

      this.loading = true;
      this.error = null;
      this.results = null;

      // Initialize progress states
      this.resetScanProgress();

      try {
        const formData = new FormData();
        formData.append('url', this.targetUrl);
        formData.append('enable_dns', this.scanOptions.enable_dns ? 'true' : 'false');
        formData.append('enable_ports', this.scanOptions.enable_ports ? 'true' : 'false');
        formData.append('enable_vulns', this.scanOptions.enable_vulns ? 'true' : 'false');
        formData.append('enable_directories', this.scanOptions.enable_directories ? 'true' : 'false');
        formData.append('wordlist', this.scanOptions.wordlist);

        // Start dynamic progress simulation
        this.simulateScanProgress();

        const response = await fetch('http://localhost:8000/audit', {
          method: 'POST',
          body: formData,
        });

        if (!response.ok) {
          throw new Error('Audit failed');
        }

        this.results = await response.json();
        this.completeAllProgress();
      } catch (err) {
        this.error = err.message;
        this.resetScanProgress();
      } finally {
        this.loading = false;
      }
    },

    resetScanProgress() {
      this.scanProgress = {
        dns: this.scanOptions.enable_dns ? 'PENDING' : 'DISABLED',
        ports: this.scanOptions.enable_ports ? 'PENDING' : 'DISABLED',
        vulnerabilities: this.scanOptions.enable_vulns ? 'PENDING' : 'DISABLED',
        directories: this.scanOptions.enable_directories ? 'PENDING' : 'DISABLED',
      };
    },

    simulateScanProgress() {
      if (this.scanOptions.enable_dns) this.scanProgress.dns = 'IN PROGRESS';
      
      setTimeout(() => {
        if (this.scanOptions.enable_ports) this.scanProgress.ports = 'IN PROGRESS';
      }, 1000);

      setTimeout(() => {
        if (this.scanOptions.enable_vulns) this.scanProgress.vulnerabilities = 'IN PROGRESS';
      }, 2000);

      setTimeout(() => {
        if (this.scanOptions.enable_directories) this.scanProgress.directories = 'IN PROGRESS';
      }, 3000);
    },

    completeAllProgress() {
      if (this.scanOptions.enable_dns) this.scanProgress.dns = 'DONE';
      if (this.scanOptions.enable_ports) this.scanProgress.ports = 'DONE';
      if (this.scanOptions.enable_vulns) this.scanProgress.vulnerabilities = 'DONE';
      if (this.scanOptions.enable_directories) this.scanProgress.directories = 'DONE';
    },

    acceptDisclaimer() {
      this.showDisclaimer = false;
    },

    declineDisclaimer() {
      window.close();
    },

    stopScan() {
      this.loading = false;
      this.error = 'Scan stopped by user';
    },

    async downloadReport(scanType) {
      if (!this.results) return;

      try {
        const response = await fetch('http://localhost:8000/download-results', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            results: this.results,
            scan_type: scanType
          })
        });

        if (response.ok) {
          const blob = await response.blob();
          const url = window.URL.createObjectURL(blob);
          const a = document.createElement('a');
          a.href = url;
          a.download = `scan_results_${scanType}_${Date.now()}.txt`;
          document.body.appendChild(a);
          a.click();
          window.URL.revokeObjectURL(url);
          document.body.removeChild(a);
        } else {
          alert('Failed to download report');
        }
      } catch (error) {
        console.error('Download error:', error);
        alert('Failed to download report');
      }
    },

    startLiveClock() {
      setInterval(() => {
        this.currentTime = new Date();
      }, 1000);
    },

    initMatrixRain() {
      const canvas = document.getElementById('matrix-canvas');
      if (!canvas) return;

      const ctx = canvas.getContext('2d');
      let animationId;
      let lastTime = 0;

      const resizeCanvas = () => {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
      };

      resizeCanvas();

      const matrix = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ123456789@#$%^&*()*&^%+-/~{[|`]}';
      const matrixArray = matrix.split('');
      const fontSize = 14;
      const columns = Math.floor(canvas.width / fontSize);
      const drops = new Array(columns).fill(1);

      const draw = (currentTime) => {
        if (currentTime - lastTime < 33) {
          animationId = requestAnimationFrame(draw);
          return;
        }
        lastTime = currentTime;

        ctx.fillStyle = 'rgba(0, 0, 0, 0.04)';
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        ctx.fillStyle = '#00ff41';
        ctx.font = `${fontSize}px 'Courier New', monospace`;

        for (let i = 0; i < drops.length; i++) {
          const text = matrixArray[Math.floor(Math.random() * matrixArray.length)];
          ctx.fillText(text, i * fontSize, drops[i] * fontSize);

          if (drops[i] * fontSize > canvas.height && Math.random() > 0.98) {
            drops[i] = 0;
          }
          drops[i]++;
        }

        animationId = requestAnimationFrame(draw);
      };

      const startAnimation = () => {
        if (animationId) cancelAnimationFrame(animationId);
        lastTime = 0;
        animationId = requestAnimationFrame(draw);
      };

      window.addEventListener('resize', resizeCanvas);
      startAnimation();

      this.matrixCleanup = () => {
        if (animationId) cancelAnimationFrame(animationId);
        window.removeEventListener('resize', resizeCanvas);
      };
    },
  },
};
</script>

<style scoped>
.matrix-bg {
  background: linear-gradient(45deg, #000000, #001100, #000000);
  background-size: 400% 400%;
  animation: matrixShift 10s ease-in-out infinite;
}

@keyframes matrixShift {
  0%, 100% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
}

.animate-pulse {
  animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

.animate-bounce {
  animation: bounce 1s infinite;
}

@keyframes bounce {
  0%, 20%, 53%, 80%, 100% {
    animation-timing-function: cubic-bezier(0.215, 0.61, 0.355, 1);
    transform: translate3d(0, 0, 0);
  }
  40%, 43% {
    animation-timing-function: cubic-bezier(0.755, 0.05, 0.855, 0.06);
    transform: translate3d(0, -30px, 0);
  }
  70% {
    animation-timing-function: cubic-bezier(0.755, 0.05, 0.855, 0.06);
    transform: translate3d(0, -15px, 0);
  }
  90% {
    transform: translate3d(0, -4px, 0);
  }
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

/* Enhanced animations */
.animate-glow {
  animation: glow 2s ease-in-out infinite alternate;
}

@keyframes glow {
  from {
    text-shadow:
      0 0 5px rgba(0, 255, 65, 0.5),
      0 0 10px rgba(0, 255, 65, 0.3),
      0 0 15px rgba(0, 255, 65, 0.2);
  }
  to {
    text-shadow:
      0 0 10px rgba(0, 255, 65, 0.8),
      0 0 20px rgba(0, 255, 65, 0.6),
      0 0 30px rgba(0, 255, 65, 0.4);
  }
}

.animate-fade-in {
  animation: fadeIn 1.5s ease-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.animate-modal-appear {
  animation: modalAppear 0.3s ease-out;
}

@keyframes modalAppear {
  from {
    opacity: 0;
    transform: scale(0.9) translateY(-20px);
  }
  to {
    opacity: 1;
    transform: scale(1) translateY(0);
  }
}

/* Smooth transitions for all elements */
* {
  transition: all 0.3s ease;
}

/* Enhanced hover effects */
button:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 20px rgba(0, 255, 65, 0.3);
}

input:focus {
  box-shadow: 0 0 0 3px rgba(0, 255, 65, 0.2);
}

.checkbox:hover {
  transform: scale(1.05);
}

/* Professional loading animation */
@keyframes professionalPulse {
  0%, 100% {
    opacity: 0.6;
    transform: scale(1);
  }
  50% {
    opacity: 1;
    transform: scale(1.02);
  }
}

.animate-professional-pulse {
  animation: professionalPulse 2s ease-in-out infinite;
}

/* Enhanced card hover effects */
.bg-black {
  transition: all 0.3s ease;
}

.bg-black:hover {
  box-shadow: 0 0 30px rgba(0, 255, 65, 0.2);
}

/* Smooth text animations */
.text-green-400 {
  transition: color 0.3s ease;
}

.text-green-400:hover {
  color: #00ff88;
}

/* Professional gradient backgrounds */
.matrix-bg {
  background: linear-gradient(
    135deg,
    #000000 0%,
    #001100 25%,
    #000000 50%,
    #000011 75%,
    #000000 100%
  );
  background-size: 400% 400%;
  animation: matrixShift 15s ease-in-out infinite;
}

/* Enhanced scrollbar */
::-webkit-scrollbar {
  width: 10px;
}

::-webkit-scrollbar-track {
  background: rgba(0, 0, 0, 0.3);
  border-radius: 5px;
}

::-webkit-scrollbar-thumb {
  background: linear-gradient(180deg, #00ff41, #00cc33);
  border-radius: 5px;
  border: 1px solid rgba(0, 0, 0, 0.5);
}

::-webkit-scrollbar-thumb:hover {
  background: linear-gradient(180deg, #00ff88, #00ff41);
}

/* Professional glow effects */
.glow {
  box-shadow:
    0 0 30px rgba(0, 255, 65, 0.4),
    0 0 60px rgba(0, 255, 65, 0.2),
    0 0 90px rgba(0, 255, 65, 0.1);
}

.text-shadow {
  text-shadow:
    0 0 10px rgba(0, 255, 65, 0.8),
    0 0 20px rgba(0, 255, 65, 0.4),
    0 0 30px rgba(0, 255, 65, 0.2);
}

/* Smooth focus transitions */
input:focus,
select:focus,
button:focus {
  outline: none;
  box-shadow:
    0 0 0 2px rgba(0, 255, 65, 0.5),
    0 0 0 4px rgba(0, 255, 65, 0.2);
}

/* Professional button states */
button:active {
  transform: translateY(0);
  box-shadow: 0 2px 10px rgba(0, 255, 65, 0.2);
}

/* Enhanced checkbox styling */
input[type="checkbox"] {
  accent-color: #00ff41;
  transform: scale(1.1);
}

/* Professional form styling */
input,
select {
  transition: all 0.3s ease;
  border: 2px solid transparent;
}

input:hover,
select:hover {
  border-color: rgba(0, 255, 65, 0.3);
}

/* Table styling */
table {
  border-collapse: collapse;
}

th, td {
  border-bottom: 1px solid #333;
  padding: 8px;
}

/* Responsive design improvements */
@media (max-width: 768px) {
  .grid-cols-4 {
    grid-template-columns: 1fr;
  }
  
  .hidden-sm {
    display: none;
  }
}
</style>