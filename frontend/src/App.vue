<template>
  <div
    class="min-h-screen bg-black text-green-400 font-mono overflow-hidden relative"
  >
    <!-- Matrix Background Animation -->
    <canvas id="matrix-canvas" class="fixed inset-0 z-0 opacity-20"></canvas>

    <!-- Legal Disclaimer Modal -->
    <div
      v-if="showDisclaimer"
      class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-80 backdrop-blur-sm animate__animated animate__fadeIn p-4"
    >
      <div
        class="bg-gray-900 border-2 border-green-500 rounded-lg p-4 md:p-8 max-w-sm sm:max-w-2xl mx-4 w-full shadow-2xl animate__animated animate__zoomIn"
      >
        <div class="text-center mb-8">
          <div
            class="w-16 h-16 mx-auto mb-4 border-2 border-amber-500 rounded-full flex items-center justify-center bg-gray-800 animate-pulse"
          >
            <svg
              class="w-8 h-8 text-amber-400"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z"
              ></path>
            </svg>
          </div>
          <h2
            class="text-2xl font-bold text-green-400 mb-2 font-mono tracking-wider"
          >
            [LEGAL DISCLAIMER]
          </h2>
          <p class="text-green-300 font-mono">
            Please read carefully before accessing this system
          </p>
        </div>

        <div class="bg-gray-800 border border-green-600 rounded p-6 mb-8">
          <div class="text-green-300 text-sm font-mono space-y-3">
            <p>
              <span class="text-red-400">[WARNING]</span> This tool is for
              educational and authorized security testing purposes only.
            </p>
            <p>
              <span class="text-green-400">></span> Only scan systems you own or
              have explicit permission to test
            </p>
            <p>
              <span class="text-green-400">></span> Unauthorized scanning may
              violate laws and terms of service
            </p>
            <p>
              <span class="text-green-400">></span> The developers are not
              responsible for misuse of this tool
            </p>
            <p>
              <span class="text-green-400">></span> Results may contain false
              positives or miss vulnerabilities
            </p>
            <p>
              <span class="text-green-400">></span> Use at your own risk and
              responsibility
            </p>
          </div>
        </div>

        <div class="grid grid-cols-2 gap-4">
          <button
            @click="acceptDisclaimer"
            class="bg-green-600 hover:bg-green-500 text-black font-bold py-4 px-6 rounded border-2 border-green-400 hover:border-green-300 transition-all duration-300 transform hover:scale-105 font-mono tracking-wide"
          >
            [ACCEPT & CONTINUE]
          </button>
          <button
            @click="declineDisclaimer"
            class="bg-red-600 hover:bg-red-500 text-white font-bold py-4 px-6 rounded border-2 border-red-400 hover:border-red-300 transition-all duration-300 font-mono tracking-wide"
          >
            [EXIT SYSTEM]
          </button>
        </div>
      </div>
    </div>

    <!-- Professional Directory Results Modal -->
    <div
      v-if="showDirectoryResults"
      class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-90 backdrop-blur-md animate__animated animate__fadeIn p-4"
      @click.self="showDirectoryResults = false"
    >
      <div
        class="bg-gray-950 border-2 border-green-400 rounded-xl p-4 md:p-8 max-w-full sm:max-w-5xl mx-4 w-full max-h-[85vh] overflow-hidden shadow-2xl animate__animated animate__zoomIn"
        style="
          box-shadow:
            0 25px 50px -12px rgba(0, 255, 65, 0.25),
            0 0 0 1px rgba(34, 197, 94, 0.1);
        "
      >
        <!-- Header with gradient border -->
        <div class="relative mb-8">
          <div
            class="absolute inset-0 bg-gradient-to-r from-green-500/20 via-blue-500/20 to-purple-500/20 rounded-lg blur"
          ></div>
          <div
            class="relative bg-gray-900 border border-green-400/50 rounded-lg p-6"
          >
            <div class="flex justify-between items-center">
              <div>
                <h2
                  class="text-2xl font-bold text-green-300 font-mono tracking-wider mb-2"
                >
                  [LIVE DIRECTORY SCAN MONITOR]
                </h2>
                <p class="text-green-400 font-mono text-sm opacity-80">
                  Real-time directory enumeration results
                </p>
              </div>
              <button
                @click="showDirectoryResults = false"
                class="p-2 text-green-400 hover:text-green-300 hover:bg-green-500/10 rounded-lg transition-all duration-200"
              >
                <svg
                  class="w-6 h-6"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M6 18L18 6M6 6l12 12"
                  ></path>
                </svg>
              </button>
            </div>
          </div>
        </div>

        <!-- Terminal Interface -->
        <div
          class="bg-black border border-green-600 rounded-lg overflow-hidden"
        >
          <!-- Terminal Header -->
          <div
            class="bg-gray-800 px-4 py-3 border-b border-green-600 flex items-center justify-between"
          >
            <div class="flex items-center space-x-2">
              <div class="w-3 h-3 bg-red-500 rounded-full"></div>
              <div class="w-3 h-3 bg-yellow-500 rounded-full"></div>
              <div class="w-3 h-3 bg-green-500 rounded-full"></div>
              <span class="text-green-400 font-mono text-sm ml-4"
                >root@matrix:~/scan-session</span
              >
            </div>
            <div class="text-green-400 font-mono text-xs">
              SESSION: {{ sessionId }}
            </div>
          </div>

          <!-- Terminal Content -->
          <div class="p-6 font-mono text-sm">
            <div class="text-green-400 mb-4">
              <span class="text-green-300">$</span> ./dirbuster --target
              {{ targetUrl }} --wordlist=common.txt --live
            </div>

            <div class="bg-gray-950 rounded p-4 border border-green-500/30">
              <div
                v-if="liveDirectoryResults && liveDirectoryResults.length > 0"
                class="space-y-3"
              >
                <div class="flex items-center justify-between mb-4">
                  <div class="text-green-400">
                    <span class="animate-pulse mr-2">⚡</span>
                    SCANNING ACTIVE - {{ liveDirectoryResults.length }} paths
                    tested
                  </div>
                  <div class="text-yellow-400 text-xs">
                    {{
                      liveDirectoryResults.filter((r) => r.found).length
                    }}
                    FOUND /
                    {{
                      liveDirectoryResults.filter((r) => !r.found).length
                    }}
                    NOT FOUND
                  </div>
                </div>

                <div class="max-h-96 overflow-y-auto space-y-2">
                  <div
                    v-for="result in liveDirectoryResults.slice(-15)"
                    :key="result.path"
                    class="flex items-center justify-between p-3 rounded border-l-4 transition-all duration-200 hover:bg-gray-800/50"
                    :class="
                      result.found
                        ? 'border-green-500 bg-green-500/5'
                        : 'border-gray-600 bg-gray-800/20'
                    "
                  >
                    <div class="flex items-center space-x-3">
                      <span
                        :class="
                          result.found ? 'text-green-400' : 'text-gray-400'
                        "
                      >
                        {{ result.found ? "✓" : "✗" }}
                      </span>
                      <span class="text-green-300 font-mono">{{
                        result.path
                      }}</span>
                      <span class="text-xs text-gray-500">
                        {{ result.found ? "(ACCESSIBLE)" : "(NOT FOUND)" }}
                      </span>
                    </div>
                    <div class="flex items-center space-x-2">
                      <span class="text-xs text-gray-400">{{
                        result.response || "N/A"
                      }}</span>
                      <span
                        class="px-3 py-1 rounded-full text-xs font-bold"
                        :class="
                          result.found
                            ? 'bg-green-600 text-black'
                            : 'bg-gray-600 text-green-300'
                        "
                      >
                        {{ result.found ? "EXPOSED" : "SECURE" }}
                      </span>
                    </div>
                  </div>
                </div>

                <div class="mt-4 pt-4 border-t border-green-500/30">
                  <div class="flex justify-between text-xs text-green-400">
                    <span
                      >Scan Progress:
                      {{
                        Math.round(
                          (liveDirectoryResults.filter((r) => r.checked)
                            .length /
                            50) *
                            100,
                        )
                      }}%</span
                    >
                    <span
                      >{{
                        liveDirectoryResults.filter((r) => r.found).length
                      }}
                      vulnerabilities detected</span
                    >
                  </div>
                  <div class="w-full bg-gray-700 h-2 rounded-full mt-2">
                    <div
                      class="bg-gradient-to-r from-green-500 to-blue-500 h-2 rounded-full transition-all duration-500"
                      :style="{
                        width:
                          Math.round(
                            (liveDirectoryResults.filter((r) => r.checked)
                              .length /
                              50) *
                              100,
                          ) + '%',
                      }"
                    ></div>
                  </div>
                </div>
              </div>

              <div v-else class="text-center py-12">
                <div
                  class="inline-flex items-center space-x-2 text-green-400 mb-4"
                >
                  <span class="animate-spin">⟳</span>
                  <span class="font-mono"
                    >INITIALIZING DIRECTORY ENUMERATION...</span
                  >
                </div>
                <div class="text-gray-500 text-sm">
                  Preparing wordlist and establishing connection
                </div>
              </div>
            </div>

            <!-- Footer Actions -->
            <div class="flex justify-end mt-6 space-x-3">
              <button
                @click="showDirectoryResults = false"
                class="px-4 py-2 bg-gray-700 hover:bg-gray-600 text-green-400 border border-green-500/50 rounded-lg transition-all duration-200 font-mono text-sm"
              >
                CLOSE MONITOR
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Header - Compact and Better Positioned -->
    <header
      class="sticky top-0 z-40 bg-black border-b border-green-500 shadow-lg"
    >
      <div class="max-w-7xl mx-auto px-4 py-4">
        <div class="flex items-center justify-between">
          <!-- Left side - Logo and Title -->
          <div class="flex items-center space-x-4">
            <div
              class="w-10 h-10 border border-green-500 flex items-center justify-center animate-pulse"
            >
              <svg
                class="w-6 h-6 text-green-400"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"
                ></path>
              </svg>
            </div>
            <div>
              <h1
                class="text-xl font-bold text-green-400 font-mono tracking-wider"
              >
                WEB SECURITY MATRIX
              </h1>
              <p class="text-xs text-green-300 font-mono">
                v2.0 - PENETRATION FRAMEWORK
              </p>
            </div>
          </div>

          <!-- Center - Status Display -->
          <div
            class="hidden sm:flex items-center space-x-3 md:space-x-6 text-xs text-green-400 font-mono"
          >
            <div class="flex items-center space-x-1 md:space-x-2">
              <span class="animate-pulse">●</span>
              <span class="hidden lg:inline">SYSTEM: ONLINE</span>
              <span class="lg:hidden">ONLINE</span>
            </div>
            <div class="flex items-center space-x-1 md:space-x-2">
              <span class="animate-pulse">●</span>
              <span class="hidden lg:inline">SECURITY: ACTIVE</span>
              <span class="lg:hidden">SECURE</span>
            </div>
            <div class="flex items-center space-x-1 md:space-x-2">
              <span class="animate-pulse">●</span>
              <span class="hidden lg:inline">ENGINES: 4</span>
              <span class="lg:hidden">4 ENG</span>
            </div>
          </div>

          <!-- Right side - Time and Session -->
          <div
            class="flex items-center space-x-4 text-xs text-green-400 font-mono"
          >
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
      <div
        class="bg-black border-2 border-green-500 rounded-lg p-6 mb-8 shadow-2xl"
      >
        <div class="flex items-center mb-4 text-green-400 text-sm font-mono">
          <span class="animate-pulse">●</span>
          <span class="ml-2">TERMINAL ACCESS GRANTED</span>
          <span class="ml-auto">SESSION: {{ sessionId }}</span>
        </div>

        <!-- Terminal Header -->
        <div class="border border-green-600 rounded p-4 mb-6 bg-gray-900">
          <div class="text-green-400 font-mono text-sm mb-2">
            <span class="text-green-300">root@matrix</span>:<span
              class="text-blue-400"
              >~</span
            >$ security-audit --target [INPUT_REQUIRED]
          </div>
          <div class="text-green-400 font-mono text-xs opacity-75">
            Web Security Audit Framework v2.0 - Advanced Penetration Testing
            Suite
          </div>
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
                <input
                  v-model="targetUrl"
                  type="text"
                  placeholder="https://target-system.com"
                  class="flex-1 bg-black border border-green-500 rounded px-3 py-3 md:py-2 text-green-400 font-mono text-sm md:text-base focus:outline-none focus:border-green-400 transition-colors"
                  :class="{ 'animate__animated animate__pulse': loading }"
                />
                <button
                  @click="startAudit"
                  :disabled="loading || !targetUrl.trim()"
                  class="px-6 py-3 md:py-2 bg-green-600 hover:bg-green-500 disabled:bg-gray-600 text-black font-mono font-bold rounded border border-green-400 hover:border-green-300 transition-all duration-300 disabled:cursor-not-allowed min-h-[44px] touch-manipulation"
                  :class="{ 'animate__animated animate__bounce': loading }"
                >
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
                <label
                  class="flex items-center text-green-300 font-mono text-xs md:text-sm"
                >
                  <input
                    v-model="scanOptions.enable_dns"
                    type="checkbox"
                    class="mr-2 accent-green-500 w-4 h-4"
                  />
                  <span class="hidden sm:inline">[DNS] Domain enumeration</span>
                  <span class="sm:hidden">[DNS]</span>
                </label>
                <label
                  class="flex items-center text-green-300 font-mono text-xs md:text-sm"
                >
                  <input
                    v-model="scanOptions.enable_ports"
                    type="checkbox"
                    class="mr-2 accent-green-500 w-4 h-4"
                  />
                  <span class="hidden sm:inline"
                    >[NET] Port reconnaissance</span
                  >
                  <span class="sm:hidden">[NET]</span>
                </label>
                <label
                  class="flex items-center text-green-300 font-mono text-xs md:text-sm"
                >
                  <input
                    v-model="scanOptions.enable_vulns"
                    type="checkbox"
                    class="mr-2 accent-green-500 w-4 h-4"
                  />
                  <span class="hidden sm:inline"
                    >[VULN] Vulnerability assessment</span
                  >
                  <span class="sm:hidden">[VULN]</span>
                </label>
                <label
                  class="flex items-center text-green-300 font-mono text-xs md:text-sm"
                >
                  <input
                    v-model="scanOptions.enable_directories"
                    type="checkbox"
                    class="mr-2 accent-green-500 w-4 h-4"
                  />
                  <span class="hidden sm:inline"
                    >[DIR] Directory traversal</span
                  >
                  <span class="sm:hidden">[DIR]</span>
                </label>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Progress Bar -->
      <div
        v-if="loading"
        class="bg-black border-2 border-green-500 rounded-lg p-6 mb-8 shadow-2xl"
      >
        <div class="flex justify-between items-center mb-6">
          <div
            class="text-green-400 font-mono text-lg font-bold tracking-wider"
          >
            <span class="text-green-300">[SYSTEM SCAN IN PROGRESS]</span>
          </div>
          <button
            @click="stopScan"
            class="px-6 py-3 bg-red-600 hover:bg-red-700 text-white font-mono text-sm font-bold rounded border-2 border-red-500 hover:border-red-400 transition-all duration-300 shadow-lg hover:shadow-red-500/25"
          >
            [TERMINATE SCAN]
          </button>
        </div>
        <div class="border border-green-600 rounded p-4 bg-gray-900">
          <div class="text-green-400 font-mono text-xs mb-2">
            <span class="text-green-300">root@matrix</span>:<span
              class="text-blue-400"
              >~</span
            >$ ./security-audit --verbose
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
            <div
              v-if="scanOptions.enable_dns"
              class="flex items-center text-green-300 font-mono text-xs"
            >
              <span
                class="mr-2"
                :class="
                  scanProgress.dns === 'DONE'
                    ? 'text-green-400'
                    : 'animate-spin'
                "
              >
                {{ scanProgress.dns === "DONE" ? "✓" : "⟳" }}
              </span>
              <span>DNS enumeration & reconnaissance...</span>
              <span
                class="ml-auto"
                :class="
                  scanProgress.dns === 'DONE'
                    ? 'text-green-400'
                    : 'text-yellow-400'
                "
              >
                [{{ scanProgress.dns }}]
              </span>
            </div>
            <div
              v-if="scanOptions.enable_ports"
              class="flex items-center text-green-300 font-mono text-xs"
            >
              <span
                class="mr-2"
                :class="
                  scanProgress.ports === 'DONE'
                    ? 'text-green-400'
                    : scanProgress.ports === 'IN PROGRESS'
                      ? 'animate-spin'
                      : ''
                "
              >
                {{
                  scanProgress.ports === "DONE"
                    ? "✓"
                    : scanProgress.ports === "IN PROGRESS"
                      ? "⟳"
                      : ">"
                }}
              </span>
              <span>Port scanning & service detection...</span>
              <span
                class="ml-auto"
                :class="
                  scanProgress.ports === 'DONE'
                    ? 'text-green-400'
                    : scanProgress.ports === 'IN PROGRESS'
                      ? 'text-yellow-400'
                      : 'text-gray-500'
                "
              >
                [{{ scanProgress.ports }}]
              </span>
            </div>
            <div
              v-if="scanOptions.enable_vulns"
              class="flex items-center text-green-300 font-mono text-xs"
            >
              <span
                class="mr-2"
                :class="
                  scanProgress.vulnerabilities === 'DONE'
                    ? 'text-green-400'
                    : scanProgress.vulnerabilities === 'IN PROGRESS'
                      ? 'animate-spin'
                      : ''
                "
              >
                {{
                  scanProgress.vulnerabilities === "DONE"
                    ? "✓"
                    : scanProgress.vulnerabilities === "IN PROGRESS"
                      ? "⟳"
                      : ">"
                }}
              </span>
              <span>Vulnerability assessment...</span>
              <span
                class="ml-auto"
                :class="
                  scanProgress.vulnerabilities === 'DONE'
                    ? 'text-green-400'
                    : scanProgress.vulnerabilities === 'IN PROGRESS'
                      ? 'text-yellow-400'
                      : 'text-gray-500'
                "
              >
                [{{ scanProgress.vulnerabilities }}]
              </span>
            </div>
            <div
              v-if="scanOptions.enable_directories"
              class="flex items-center text-green-300 font-mono text-xs"
            >
              <span
                class="mr-2"
                :class="
                  scanProgress.directories === 'DONE'
                    ? 'text-green-400'
                    : scanProgress.directories === 'IN PROGRESS'
                      ? 'animate-spin'
                      : ''
                "
              >
                {{
                  scanProgress.directories === "DONE"
                    ? "✓"
                    : scanProgress.directories === "IN PROGRESS"
                      ? "⟳"
                      : ">"
                }}
              </span>
              <span>Directory traversal & exposure check...</span>
              <span
                class="ml-auto"
                :class="
                  scanProgress.directories === 'DONE'
                    ? 'text-green-400'
                    : scanProgress.directories === 'IN PROGRESS'
                      ? 'text-yellow-400'
                      : 'text-gray-500'
                "
              >
                [{{ scanProgress.directories }}]
              </span>
            </div>
            <div class="flex items-center text-green-300 font-mono text-xs">
              <span
                class="mr-2"
                :class="
                  scanProgress.technologies === 'DONE'
                    ? 'text-green-400'
                    : scanProgress.technologies === 'IN PROGRESS'
                      ? 'animate-spin'
                      : ''
                "
              >
                {{
                  scanProgress.technologies === "DONE"
                    ? "✓"
                    : scanProgress.technologies === "IN PROGRESS"
                      ? "⟳"
                      : ">"
                }}
              </span>
              <span>Technology stack fingerprinting...</span>
              <span
                class="ml-auto"
                :class="
                  scanProgress.technologies === 'DONE'
                    ? 'text-green-400'
                    : scanProgress.technologies === 'IN PROGRESS'
                      ? 'text-yellow-400'
                      : 'text-gray-500'
                "
              >
                [{{ scanProgress.technologies }}]
              </span>
            </div>
          </div>
          <div class="mt-4">
            <div class="w-full bg-gray-700 h-2 rounded">
              <div
                class="bg-green-500 h-2 rounded animate-pulse"
                style="width: 100%"
              ></div>
            </div>
            <div class="text-center text-green-300 font-mono text-xs mt-2">
              <span class="animate-pulse">█</span
              ><span class="animate-pulse ml-1">█</span
              ><span class="animate-pulse ml-1">█</span>
              EXECUTING ACTIVE SCAN MODULES
              <span class="animate-pulse ml-1">█</span
              ><span class="animate-pulse ml-1">█</span
              ><span class="animate-pulse ml-1">█</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Error Notification -->
      <div
        v-if="error"
        class="bg-black border-2 border-red-500 rounded-lg p-6 mb-8 shadow-2xl"
      >
        <div class="text-red-400 font-mono text-sm mb-4">
          <span class="text-red-300">[ERROR]</span> Scan execution failed
        </div>
        <div class="border border-red-600 rounded p-4 bg-gray-900">
          <div class="text-red-400 font-mono text-xs mb-2">
            <span class="text-red-300">root@matrix</span>:<span
              class="text-blue-400"
              >~</span
            >$ ./security-audit --target {{ targetUrl }}
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
      <div v-if="results" class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <!-- System Information -->
        <div
          class="bg-black bg-opacity-80 border border-green-500 rounded-lg p-6"
        >
          <h3 class="text-xl font-bold text-green-400 mb-4 flex items-center">
            <svg
              class="w-6 h-6 mr-2"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
              ></path>
            </svg>
            System Information
          </h3>
          <div class="space-y-3">
            <div class="flex justify-between">
              <span class="text-green-300">Target:</span>
              <span class="text-green-400 font-mono">{{ results.domain }}</span>
            </div>
            <div class="flex justify-between">
              <span class="text-green-300">URL:</span>
              <span class="text-green-400 font-mono text-sm">{{
                results.url
              }}</span>
            </div>
            <div
              v-if="
                results.hostnames &&
                results.hostnames.length > 0 &&
                results.hostnames[0] !== 'No hostnames found'
              "
              class="flex justify-between"
            >
              <span class="text-green-300">Hostnames:</span>
              <div
                class="text-green-400 font-mono text-sm max-h-20 overflow-y-auto"
              >
                <div
                  v-for="hostname in results.hostnames"
                  :key="hostname"
                  class="mb-1"
                >
                  {{ hostname }}
                </div>
              </div>
            </div>
            <div
              v-if="results.ip_info && !results.ip_info.error"
              class="space-y-2"
            >
              <div class="flex justify-between">
                <span class="text-green-300">Location:</span>
                <span class="text-green-400"
                  >{{ results.ip_info.city }},
                  {{ results.ip_info.country }}</span
                >
              </div>
              <div class="flex justify-between">
                <span class="text-green-300">ISP:</span>
                <span class="text-green-400 font-mono">{{
                  results.ip_info.isp
                }}</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Technology Stack -->
        <div
          class="bg-black bg-opacity-80 border border-green-500 rounded-lg p-6"
        >
          <h3 class="text-xl font-bold text-green-400 mb-4 flex items-center">
            <svg
              class="w-6 h-6 mr-2"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"
              ></path>
            </svg>
            Technology Stack
          </h3>
          <div
            v-if="results.technologies && results.technologies.length > 0"
            class="space-y-2"
          >
            <div
              v-for="tech in results.technologies"
              :key="tech.name"
              class="flex justify-between items-center p-2 bg-gray-900 rounded"
            >
              <div class="flex items-center">
                <img
                  v-if="tech.icon"
                  :src="tech.icon"
                  :alt="tech.name"
                  class="w-6 h-6 mr-3"
                  @error="handleIconError"
                />
                <div>
                  <span class="text-green-300 text-sm">{{
                    tech.category
                  }}</span>
                  <div class="text-green-400 font-mono">{{ tech.name }}</div>
                </div>
              </div>
              <span
                class="text-xs px-2 py-1 rounded"
                :class="
                  tech.confidence === 'High' ? 'bg-green-600' : 'bg-yellow-600'
                "
              >
                {{ tech.confidence }}
              </span>
            </div>
          </div>
          <div v-else class="text-green-300">No technologies detected</div>
        </div>

        <!-- Security Analysis -->
        <div
          class="bg-black bg-opacity-80 border border-green-500 rounded-lg p-6"
        >
          <h3 class="text-xl font-bold text-green-400 mb-4 flex items-center">
            <svg
              class="w-6 h-6 mr-2"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"
              ></path>
            </svg>
            Security Analysis
          </h3>
          <div class="space-y-3">
            <div v-if="results.ssl_info">
              <div class="flex justify-between items-center">
                <span class="text-green-300">SSL Certificate:</span>
                <span
                  class="px-2 py-1 rounded text-xs"
                  :class="
                    results.ssl_info.valid ? 'bg-green-600' : 'bg-red-600'
                  "
                >
                  {{ results.ssl_info.valid ? "Valid" : "Invalid" }}
                </span>
              </div>
            </div>
            <div>
              <span class="text-green-300">Security Headers:</span>
              <div class="mt-2 space-y-1">
                <div
                  v-for="(value, header) in results.headers"
                  :key="header"
                  class="text-xs"
                >
                  <span class="text-green-400">{{ header }}:</span>
                  <span
                    class="text-green-300 ml-2"
                    :class="value ? 'text-green-400' : 'text-red-400'"
                  >
                    {{ value ? "✓" : "✗" }}
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Vulnerabilities -->
        <div
          class="bg-black bg-opacity-80 border border-green-500 rounded-lg p-6"
        >
          <h3 class="text-xl font-bold text-green-400 mb-4 flex items-center">
            <svg
              class="w-6 h-6 mr-2"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z"
              ></path>
            </svg>
            Security Vulnerabilities
          </h3>

          <div
            v-if="securityVulnerabilities && securityVulnerabilities.length > 0"
            class="space-y-3"
          >
            <div
              v-for="vuln in securityVulnerabilities"
              :key="vuln.description"
              class="p-3 bg-gray-900 rounded border-l-4"
              :class="
                vuln.severity === 'Critical'
                  ? 'border-red-500'
                  : vuln.severity === 'High'
                    ? 'border-orange-500'
                    : 'border-yellow-500'
              "
            >
              <div class="flex justify-between items-start">
                <div>
                  <span class="text-green-400 font-bold">{{ vuln.type }}</span>
                  <p class="text-green-300 text-sm mt-1">
                    {{ vuln.description }}
                  </p>
                </div>
                <span
                  class="px-2 py-1 rounded text-xs font-bold"
                  :class="
                    vuln.severity === 'Critical'
                      ? 'bg-red-600'
                      : vuln.severity === 'High'
                        ? 'bg-orange-600'
                        : vuln.severity === 'Medium'
                          ? 'bg-yellow-600'
                          : 'bg-blue-600'
                  "
                >
                  {{ vuln.severity }}
                </span>
              </div>
            </div>
          </div>

          <div
            v-else-if="
              securityVulnerabilities &&
              securityVulnerabilities.length > 0 &&
              securityVulnerabilities[0]?.type === 'Vulnerability Scan Disabled'
            "
            class="text-center py-8"
          >
            <div
              class="w-16 h-16 bg-green-500 rounded-full flex items-center justify-center mx-auto mb-4 border-2 border-green-400"
            >
              <svg
                class="w-8 h-8 text-black"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
                ></path>
              </svg>
            </div>
            <p
              class="text-green-400 text-lg font-bold font-mono tracking-wider"
            >
              SCAN MODULE DISABLED
            </p>
            <p class="text-green-300 text-sm">
              Module was disabled in scan configuration
            </p>
          </div>

          <div v-else class="text-center py-8">
            <div
              class="w-16 h-16 bg-green-500 rounded-full flex items-center justify-center mx-auto mb-4 border-2 border-green-400"
            >
              <svg
                class="w-8 h-8 text-black"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
                ></path>
              </svg>
            </div>
            <p
              class="text-green-400 text-lg font-bold font-mono tracking-wider"
            >
              NO SECURITY VULNERABILITIES FOUND
            </p>
            <p class="text-green-300 text-sm">
              Target appears secure from common attacks
            </p>
          </div>
        </div>

        <!-- Directory Scan Results -->
        <div
          class="bg-black bg-opacity-80 border border-green-500 rounded-lg p-6"
        >
          <h3 class="text-xl font-bold text-green-400 mb-4 flex items-center">
            <svg
              class="w-6 h-6 mr-2"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2H5a2 2 0 00-2-2z"
              ></path>
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M8 5a2 2 0 012-2h4a2 2 0 012 2v2H8V5z"
              ></path>
            </svg>
            Directory Scan Results
          </h3>
          <div
            v-if="
              directoryResults &&
              directoryResults.length > 0 &&
              directoryResults[0].type !== 'Directory Scan Disabled'
            "
            class="space-y-3"
          >
            <div
              v-for="result in directoryResults"
              :key="result.description"
              class="p-3 bg-gray-900 rounded border-l-4"
              :class="
                result.type === 'Directory Exposure'
                  ? 'border-orange-500'
                  : 'border-blue-500'
              "
            >
              <div class="flex justify-between items-start">
                <div>
                  <span class="text-green-400 font-bold">{{
                    result.type
                  }}</span>
                  <p class="text-green-300 text-sm mt-1">
                    {{ result.description }}
                  </p>
                </div>
                <span
                  class="px-2 py-1 rounded text-xs font-bold"
                  :class="
                    result.severity === 'Medium'
                      ? 'bg-orange-600'
                      : result.severity === 'High'
                        ? 'bg-red-600'
                        : 'bg-blue-600'
                  "
                >
                  {{ result.severity }}
                </span>
              </div>
            </div>
          </div>

          <div
            v-else-if="
              directoryResults &&
              directoryResults.length > 0 &&
              directoryResults[0].type === 'Directory Scan Disabled'
            "
            class="text-center py-8"
          >
            <div
              class="w-16 h-16 bg-green-500 rounded-full flex items-center justify-center mx-auto mb-4 border-2 border-green-400"
            >
              <svg
                class="w-8 h-8 text-black"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
                ></path>
              </svg>
            </div>
            <p
              class="text-green-400 text-lg font-bold font-mono tracking-wider"
            >
              SCAN MODULE DISABLED
            </p>
            <p class="text-green-300 text-sm">
              Module was disabled in scan configuration
            </p>
          </div>

          <div v-else class="text-center py-8">
            <div
              class="w-16 h-16 bg-green-500 rounded-full flex items-center justify-center mx-auto mb-4 border-2 border-green-400"
            >
              <svg
                class="w-8 h-8 text-black"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
                ></path>
              </svg>
            </div>
            <p
              class="text-green-400 text-lg font-bold font-mono tracking-wider"
            >
              NO SECURITY VULNERABILITIES FOUND
            </p>
            <p class="text-green-300 text-sm">
              Target appears secure from common attacks
            </p>
          </div>
        </div>

        <!-- Network Information -->
        <div
          class="bg-black bg-opacity-80 border border-green-500 rounded-lg p-6 lg:col-span-2"
        >
          <h3 class="text-xl font-bold text-green-400 mb-4 flex items-center">
            <svg
              class="w-6 h-6 mr-2"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M21 12a9 9 0 01-9 9m9-9a9 9 0 00-9-9m9 9H3m9 9v-9m0-9v9"
              ></path>
            </svg>
            Network Intelligence
          </h3>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <!-- Open Ports -->
            <div>
              <h4 class="text-green-400 font-bold mb-3">Open Ports</h4>
              <div
                v-if="results.ports && results.ports.length > 0"
                class="space-y-2"
              >
                <div
                  v-for="port in results.ports"
                  :key="port.port"
                  class="flex justify-between items-center p-2 bg-gray-900 rounded"
                >
                  <div>
                    <span class="text-green-400 font-mono"
                      >{{ port.port }}/{{ port.protocol || "tcp" }}</span
                    >
                    <span class="text-green-300 ml-2">{{ port.service }}</span>
                  </div>
                  <span
                    class="px-2 py-1 bg-green-600 text-black text-xs rounded"
                    >OPEN</span
                  >
                </div>
              </div>
              <div v-else class="text-green-300">No open ports detected</div>
            </div>

            <!-- DNS Information -->
            <div>
              <h4 class="text-green-400 font-bold mb-3">DNS Records</h4>
              <div
                v-if="results.dns && results.dns.A_records"
                class="space-y-2"
              >
                <div
                  v-for="record in results.dns.A_records"
                  :key="record"
                  class="p-2 bg-gray-900 rounded"
                >
                  <span class="text-green-400 font-mono">{{ record }}</span>
                </div>
              </div>
              <div v-else class="text-green-300">
                {{ results.dns?.note || "No DNS records found" }}
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script>
export default {
  name: "App",
  data() {
    return {
      showDisclaimer: true,
      targetUrl: "",
      loading: false,
      results: null,
      error: null,
      showDirectoryResults: false,
      liveDirectoryResults: [],
      abortController: null,
      currentTime: new Date(),
      scanProgress: {
        initialization: "DONE",
        dns: "PENDING",
        ports: "PENDING",
        vulnerabilities: "PENDING",
        directories: "PENDING",
        technologies: "PENDING",
      },
      scanOptions: {
        enable_dns: true,
        enable_ports: true,
        enable_vulns: true,
        enable_directories: true,
        nmap_options: "-sV --version-intensity 5",
      },
    };
  },
  computed: {
    securityVulnerabilities() {
      return this.results?.vulnerabilities || [];
    },
    directoryResults() {
      return this.results?.directories || [];
    },
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
        this.error = "Please enter a valid URL";
        return;
      }

      this.loading = true;
      this.error = null;
      this.results = null;

      // Initialize progress states
      this.resetScanProgress();

      try {
        const formData = new FormData();
        formData.append("url", this.targetUrl);

        // Add scan options - handle booleans and strings differently
        // Boolean options: convert to 'true'/'false' strings
        formData.append(
          "enable_dns",
          this.scanOptions.enable_dns ? "true" : "false",
        );
        formData.append(
          "enable_ports",
          this.scanOptions.enable_ports ? "true" : "false",
        );
        formData.append(
          "enable_vulns",
          this.scanOptions.enable_vulns ? "true" : "false",
        );
        formData.append(
          "enable_directories",
          this.scanOptions.enable_directories ? "true" : "false",
        );

        // String options: send as-is
        formData.append("nmap_options", this.scanOptions.nmap_options);

        // Show which protocol and port are being tested
        const hasProtocol =
          this.targetUrl.startsWith("http://") ||
          this.targetUrl.startsWith("https://");
        const protocol = this.targetUrl.startsWith("http://")
          ? "HTTP"
          : this.targetUrl.startsWith("https://")
            ? "HTTPS"
            : "HTTPS (auto)";

        // Extract port from URL or use default
        const url = hasProtocol ? this.targetUrl : `https://${this.targetUrl}`;
        let port = url.startsWith("https://") ? "443" : "80"; // Default ports

        if (url.includes(":")) {
          const parts = url.split(":");
          if (parts.length >= 3) {
            // Has protocol:host:port format (e.g., https://example.com:8443)
            port = parts[2].split("/")[0];
          } else if (parts.length === 2 && parts[1]) {
            // Has host:port format without protocol (e.g., example.com:8080)
            port = parts[1].split("/")[0];
          }
          // If parts[1] is empty (like https://example.com), keep default port
        }

        console.log(`Testing with protocol: ${protocol}, port: ${port}`);

        // Start dynamic progress simulation
        this.simulateScanProgress();

        // Create abort controller for request cancellation
        this.abortController = new AbortController();

        const response = await fetch(`${import.meta.env.VITE_API_URL}/audit`, {
          method: "POST",
          body: formData,
          signal: this.abortController.signal, // Enable request cancellation
        });

        if (!response.ok) {
          throw new Error("Audit failed");
        }

        this.results = await response.json();

        // Mark all remaining modules as DONE when results arrive
        this.completeAllProgress();
      } catch (err) {
        this.error = err.message;
        // Reset progress on error
        this.resetScanProgress();
      } finally {
        this.loading = false;
      }
    },

    resetScanProgress() {
      this.scanProgress = {
        initialization: "DONE",
        dns: this.scanOptions.enable_dns ? "PENDING" : "DISABLED",
        ports: this.scanOptions.enable_ports ? "PENDING" : "DISABLED",
        vulnerabilities: this.scanOptions.enable_vulns ? "PENDING" : "DISABLED",
        directories: this.scanOptions.enable_directories
          ? "PENDING"
          : "DISABLED",
        technologies: "PENDING",
      };
    },

    simulateScanProgress() {
      // Start with initialization
      this.scanProgress.initialization = "DONE";

      // Set initial states for enabled modules
      if (this.scanOptions.enable_dns) this.scanProgress.dns = "IN PROGRESS";
      if (this.scanOptions.enable_ports) this.scanProgress.ports = "PENDING";
      if (this.scanOptions.enable_vulns)
        this.scanProgress.vulnerabilities = "PENDING";
      if (this.scanOptions.enable_directories)
        this.scanProgress.directories = "PENDING";
      this.scanProgress.technologies = "PENDING";

      // Simulate realistic progression without marking DONE prematurely
      let step = 0;
      const progressSteps = [
        // Ports start after DNS begins
        () => {
          if (this.scanOptions.enable_ports)
            this.scanProgress.ports = "IN PROGRESS";
        },
        // Vulnerabilities start
        () => {
          if (this.scanOptions.enable_vulns)
            this.scanProgress.vulnerabilities = "IN PROGRESS";
        },
        // Directories start
        () => {
          if (this.scanOptions.enable_directories)
            this.scanProgress.directories = "IN PROGRESS";
        },
        // Technology detection starts
        () => {
          this.scanProgress.technologies = "IN PROGRESS";
        },
        // NOTE: We don't mark anything as DONE until actual results arrive
      ];

      const runNextStep = () => {
        if (step < progressSteps.length && this.loading) {
          progressSteps[step]();
          step++;

          // Realistic timing - keep everything in progress until completion
          const delays = [500, 1000, 1500, 2000];
          if (step < delays.length) {
            setTimeout(runNextStep, delays[step]);
          }
        }
      };

      // Start the progress simulation
      setTimeout(runNextStep, 200);
    },

    completeAllProgress() {
      // Mark all enabled modules as DONE when scan completes
      if (this.scanOptions.enable_dns) this.scanProgress.dns = "DONE";
      if (this.scanOptions.enable_ports) this.scanProgress.ports = "DONE";
      if (this.scanOptions.enable_vulns)
        this.scanProgress.vulnerabilities = "DONE";
      if (this.scanOptions.enable_directories)
        this.scanProgress.directories = "DONE";
      this.scanProgress.technologies = "DONE";
    },

    acceptDisclaimer() {
      this.showDisclaimer = false;
    },

    declineDisclaimer() {
      window.close();
      // Alternative: redirect to a safe page
      // window.location.href = 'about:blank'
    },

    stopScan() {
      // Stop the current scan
      this.loading = false;
      this.error = "Scan stopped by user";
      // If there's an abort controller, abort it
      if (this.abortController) {
        this.abortController.abort();
      }
    },

    handleIconError(event) {
      // Replace broken icon with default icon
      event.target.src = "https://img.icons8.com/ios-filled/50/00ff41/web.png";
    },

    startLiveClock() {
      // Update the clock every second
      setInterval(() => {
        this.currentTime = new Date();
      }, 1000);
    },

    initMatrixRain() {
      const canvas = document.getElementById("matrix-canvas");
      if (!canvas) return;

      const ctx = canvas.getContext("2d");
      let animationId;
      let lastTime = 0;

      // Responsive font size and performance settings
      const getResponsiveSettings = () => {
        const width = window.innerWidth;
        if (width <= 640) {
          // Mobile: smaller font, slower animation
          return { fontSize: 10, speed: 0.8, opacity: 0.03 };
        } else if (width <= 1024) {
          // Tablet: medium font, medium speed
          return { fontSize: 12, speed: 1.0, opacity: 0.035 };
        } else {
          // Desktop: larger font, faster but still smooth
          return { fontSize: 14, speed: 1.2, opacity: 0.04 };
        }
      };

      let settings = getResponsiveSettings();

      const resizeCanvas = () => {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
        settings = getResponsiveSettings();
      };

      resizeCanvas();

      const matrix =
        "ABCDEFGHIJKLMNOPQRSTUVWXYZ123456789@#$%^&*()*&^%+-/~{[|`]}";
      const matrixArray = matrix.split("");
      const columns = Math.floor(canvas.width / settings.fontSize);
      const drops = new Array(columns).fill(1);

      const draw = (currentTime) => {
        // Limit frame rate for smoother animation (approximately 30 FPS)
        if (currentTime - lastTime < 33) {
          animationId = requestAnimationFrame(draw);
          return;
        }
        lastTime = currentTime;

        // Semi-transparent overlay for trail effect
        ctx.fillStyle = `rgba(0, 0, 0, ${settings.opacity})`;
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        ctx.fillStyle = "#00ff41";
        ctx.font = `${settings.fontSize}px 'Courier New', monospace`;

        for (let i = 0; i < drops.length; i++) {
          const text =
            matrixArray[Math.floor(Math.random() * matrixArray.length)];
          ctx.fillText(
            text,
            i * settings.fontSize,
            drops[i] * settings.fontSize,
          );

          // Reset drop to top when it reaches bottom with some randomness
          if (
            drops[i] * settings.fontSize > canvas.height &&
            Math.random() > 0.98
          ) {
            drops[i] = 0;
          }
          // Smooth movement with variable speed
          drops[i] += settings.speed;
        }

        animationId = requestAnimationFrame(draw);
      };

      const startAnimation = () => {
        if (animationId) cancelAnimationFrame(animationId);
        lastTime = 0;
        animationId = requestAnimationFrame(draw);
      };

      // Throttled resize handler
      let resizeTimeout;
      const handleResize = () => {
        clearTimeout(resizeTimeout);
        resizeTimeout = setTimeout(() => {
          resizeCanvas();
          // Recreate drops array for new column count
          const newColumns = Math.floor(canvas.width / settings.fontSize);
          drops.length = newColumns;
          for (let i = 0; i < newColumns; i++) {
            if (drops[i] === undefined)
              drops[i] = (Math.random() * canvas.height) / settings.fontSize;
          }
        }, 150);
      };

      window.addEventListener("resize", handleResize);
      startAnimation();

      // Store cleanup function
      this.matrixCleanup = () => {
        if (animationId) cancelAnimationFrame(animationId);
        window.removeEventListener("resize", handleResize);
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
  0%,
  100% {
    background-position: 0% 50%;
  }
  50% {
    background-position: 100% 50%;
  }
}

.animate-pulse {
  animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}

@keyframes pulse {
  0%,
  100% {
    opacity: 1;
  }
  50% {
    opacity: 0.5;
  }
}

.animate-bounce {
  animation: bounce 1s infinite;
}

@keyframes bounce {
  0%,
  20%,
  53%,
  80%,
  100% {
    animation-timing-function: cubic-bezier(0.215, 0.61, 0.355, 1);
    transform: translate3d(0, 0, 0);
  }
  40%,
  43% {
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
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
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
  0%,
  100% {
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
</style>
