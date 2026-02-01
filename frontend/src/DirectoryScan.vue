<template>
  <div class="min-h-screen bg-black text-green-400 font-mono overflow-hidden relative">
    <!-- Matrix Background Animation -->
    <canvas id="matrix-canvas" class="fixed inset-0 z-0 opacity-20"></canvas>

    <!-- Header -->
    <header class="sticky top-0 z-40 bg-black border-b border-green-500 shadow-lg">
      <div class="max-w-7xl mx-auto px-4 py-4">
        <div class="flex items-center justify-between">
          <div class="flex items-center space-x-4">
            <div class="w-10 h-10 border border-blue-500 flex items-center justify-center animate-pulse">
              <svg class="w-6 h-6 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2H5a2 2 0 00-2-2z"></path>
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 5a2 2 0 012-2h4a2 2 0 012 2v2H8V5z"></path>
              </svg>
            </div>
            <div>
              <h1 class="text-xl font-bold text-blue-400 font-mono tracking-wider">DIRECTORY SCANNER</h1>
              <p class="text-xs text-blue-300 font-mono">DIRSEARCH - Advanced Directory Enumeration</p>
            </div>
          </div>
          <div class="flex items-center space-x-4 text-xs text-blue-400 font-mono">
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
      <div class="bg-black border-2 border-blue-500 rounded-lg p-6 mb-8 shadow-2xl">
        <div class="flex items-center mb-4 text-blue-400 text-sm font-mono">
          <span class="animate-pulse">●</span>
          <span class="ml-2">DIRECTORY ENUMERATION MODULE</span>
          <span class="ml-auto">SESSION: {{ sessionId }}</span>
        </div>

        <!-- Terminal Header -->
        <div class="border border-blue-600 rounded p-4 mb-6 bg-gray-900">
          <div class="text-blue-400 font-mono text-sm mb-2">
            <span class="text-blue-300">root@matrix</span>:<span class="text-blue-400">~</span>$ dirsearch --target [INPUT_REQUIRED]
          </div>
          <div class="text-blue-400 font-mono text-xs opacity-75">Advanced directory and file enumeration scanner</div>
        </div>

        <!-- Input Section -->
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-4 md:gap-6">
          <!-- Left Panel - Target Input -->
          <div class="lg:col-span-2">
            <div class="border border-blue-600 rounded p-4 md:p-6 bg-gray-900">
              <div class="text-blue-400 font-mono text-sm mb-3">
                <span class="text-blue-300">></span> Enter target coordinates:
              </div>
              <div class="flex flex-col sm:flex-row gap-3">
                <input v-model="targetUrl" type="text" placeholder="https://target-system.com" class="flex-1 bg-black border border-blue-500 rounded px-3 py-3 md:py-2 text-blue-400 font-mono text-sm md:text-base focus:outline-none focus:border-blue-400 transition-colors" :class="{ 'animate__animated animate__pulse': loading }" />
                <button @click="startDirScan" :disabled="loading || !targetUrl.trim()" class="px-6 py-3 md:py-2 bg-blue-600 hover:bg-blue-500 disabled:bg-gray-600 text-black font-mono font-bold rounded border border-blue-400 hover:border-blue-300 transition-all duration-300 disabled:cursor-not-allowed min-h-[44px] touch-manipulation" :class="{ 'animate__animated animate__bounce': loading }">
                  <span v-if="loading" class="flex items-center">
                    <span class="animate-spin mr-2">⟳</span>
                    <span class="hidden sm:inline">ENUMERATING...</span>
                    <span class="sm:hidden">ENUMERATING</span>
                  </span>
                  <span v-else>
                    <span class="hidden sm:inline">INITIATE DIRECTORY SCAN</span>
                    <span class="sm:hidden">SCAN</span>
                  </span>
                </button>
              </div>
              <div class="mt-3 text-blue-300 font-mono text-xs">
                <span class="text-blue-400">[NOTE]</span> This scan may take 1-10 minutes depending on wordlist size
              </div>
            </div>
          </div>

          <!-- Right Panel - Scan Options -->
          <div class="space-y-4">
            <div class="border border-blue-600 rounded p-4 md:p-6 bg-gray-900">
              <div class="text-blue-400 font-mono text-sm mb-3">
                <span class="text-blue-300">></span> Wordlist selection:
              </div>
              <div class="space-y-3">
                <label class="flex items-center text-blue-300 font-mono text-xs md:text-sm">
                  <input v-model="scanOptions.wordlist" value="common" type="radio" class="mr-2 accent-blue-500 w-4 h-4" />
                  <span class="hidden sm:inline">[COMMON] Fast scan (1000 entries)</span>
                  <span class="sm:hidden">[COMMON]</span>
                </label>
                <label class="flex items-center text-blue-300 font-mono text-xs md:text-sm">
                  <input v-model="scanOptions.wordlist" value="fast" type="radio" class="mr-2 accent-blue-500 w-4 h-4" />
                  <span class="hidden sm:inline">[FAST] Small wordlist (5000 entries)</span>
                  <span class="sm:hidden">[FAST]</span>
                </label>
                <label class="flex items-center text-blue-300 font-mono text-xs md:text-sm">
                  <input v-model="scanOptions.wordlist" value="big" type="radio" class="mr-2 accent-blue-500 w-4 h-4" />
                  <span class="hidden sm:inline">[BIG] Comprehensive (20000 entries)</span>
                  <span class="sm:hidden">[BIG]</span>
                </label>
                <label class="flex items-center text-blue-300 font-mono text-xs md:text-sm">
                  <input v-model="scanOptions.wordlist" value="all" type="radio" class="mr-2 accent-blue-500 w-4 h-4" />
                  <span class="hidden sm:inline">[ALL] Extended scan (50000+ entries)</span>
                  <span class="sm:hidden">[ALL]</span>
                </label>
              </div>
            </div>

            <!-- Scan Configuration -->
            <div class="border border-blue-600 rounded p-4 md:p-6 bg-gray-900">
              <div class="text-blue-400 font-mono text-sm mb-3">
                <span class="text-blue-300">></span> Scan configuration:
              </div>
              <div class="space-y-3">
                <label class="flex items-center text-blue-300 font-mono text-xs md:text-sm">
                  <input v-model="scanOptions.enable_recursion" type="checkbox" class="mr-2 accent-blue-500 w-4 h-4" />
                  <span class="hidden sm:inline">[RECURSION] Deep directory scan</span>
                  <span class="sm:hidden">[RECURSION]</span>
                </label>
                <label class="flex items-center text-blue-300 font-mono text-xs md:text-sm">
                  <input v-model="scanOptions.enable_extensions" type="checkbox" class="mr-2 accent-blue-500 w-4 h-4" />
                  <span class="hidden sm:inline">[EXT] Check common file extensions</span>
                  <span class="sm:hidden">[EXT]</span>
                </label>
                <label class="flex items-center text-blue-300 font-mono text-xs md:text-sm">
                  <input v-model="scanOptions.enable_timing" type="checkbox" class="mr-2 accent-blue-500 w-4 h-4" />
                  <span class="hidden sm:inline">[TIMING] Extended timeout</span>
                  <span class="sm:hidden">[TIMING]</span>
                </label>
              </div>
            </div>

            <!-- Wordlist Information -->
            <div class="border border-blue-600 rounded p-4 md:p-6 bg-gray-900">
              <div class="text-blue-400 font-mono text-sm mb-3">
                <span class="text-blue-300">></span> Wordlist details:
              </div>
              <div class="text-blue-300 font-mono text-xs space-y-2">
                <div>• Common: Quick scan for obvious directories</div>
                <div>• Fast: Balanced speed and coverage</div>
                <div>• Big: Comprehensive directory enumeration</div>
                <div>• All: Maximum coverage, longest duration</div>
                <div class="text-blue-400 mt-2">• Estimated duration varies by selection</div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Progress Bar -->
      <div v-if="loading" class="bg-black border-2 border-blue-500 rounded-lg p-6 mb-8 shadow-2xl">
        <div class="flex justify-between items-center mb-6">
          <div class="text-blue-400 font-mono text-lg font-bold tracking-wider">
            <span class="text-blue-300">[DIRECTORY ENUMERATION IN PROGRESS]</span>
          </div>
          <button @click="stopScan" class="px-6 py-3 bg-red-600 hover:bg-red-700 text-white font-mono text-sm font-bold rounded border-2 border-red-500 hover:border-red-400 transition-all duration-300 shadow-lg hover:shadow-red-500/25">[TERMINATE SCAN]</button>
        </div>
        <div class="border border-blue-600 rounded p-4 bg-gray-900">
          <div class="text-blue-400 font-mono text-xs mb-2">
            <span class="text-blue-300">root@matrix</span>:<span class="text-blue-400">~</span>$ ./dirsearch --target {{ targetUrl }} --wordlist {{ scanOptions.wordlist }}
          </div>
          <div class="space-y-1">
            <div class="flex items-center text-blue-300 font-mono text-xs">
              <span class="animate-pulse mr-2">></span>
              <span>Initializing directory scanner...</span>
              <span class="ml-auto text-blue-400">[OK]</span>
            </div>
            <div class="flex items-center text-blue-300 font-mono text-xs">
              <span class="animate-pulse mr-2">></span>
              <span>Loading wordlist...</span>
              <span class="ml-auto text-blue-400">[OK]</span>
            </div>
            <div class="flex items-center text-blue-300 font-mono text-xs">
              <span class="mr-2" :class="scanProgress.wordlist === 'DONE' ? 'text-blue-400' : scanProgress.wordlist === 'IN PROGRESS' ? 'animate-spin' : ''">{{ scanProgress.wordlist === "DONE" ? "✓" : scanProgress.wordlist === "IN PROGRESS" ? "⟳" : ">" }}</span>
              <span>Wordlist: {{ scanOptions.wordlist }} ({{ getWordlistSize() }} entries)</span>
              <span class="ml-auto" :class="scanProgress.wordlist === 'DONE' ? 'text-blue-400' : scanProgress.wordlist === 'IN PROGRESS' ? 'text-yellow-400' : 'text-gray-500'">[{{ scanProgress.wordlist }}]</span>
            </div>
            <div class="flex items-center text-blue-300 font-mono text-xs">
              <span class="mr-2" :class="scanProgress.recursion === 'DONE' ? 'text-blue-400' : scanProgress.recursion === 'IN PROGRESS' ? 'animate-spin' : ''">{{ scanProgress.recursion === "DONE" ? "✓" : scanProgress.recursion === "IN PROGRESS" ? "⟳" : ">" }}</span>
              <span>Directory recursion analysis...</span>
              <span class="ml-auto" :class="scanProgress.recursion === 'DONE' ? 'text-blue-400' : scanProgress.recursion === 'IN PROGRESS' ? 'text-yellow-400' : 'text-gray-500'">[{{ scanProgress.recursion }}]</span>
            </div>
            <div class="flex items-center text-blue-300 font-mono text-xs">
              <span class="mr-2" :class="scanProgress.extensions === 'DONE' ? 'text-blue-400' : scanProgress.extensions === 'IN PROGRESS' ? 'animate-spin' : ''">{{ scanProgress.extensions === "DONE" ? "✓" : scanProgress.extensions === "IN PROGRESS" ? "⟳" : ">" }}</span>
              <span>File extension checking...</span>
              <span class="ml-auto" :class="scanProgress.extensions === 'DONE' ? 'text-blue-400' : scanProgress.extensions === 'IN PROGRESS' ? 'text-yellow-400' : 'text-gray-500'">[{{ scanProgress.extensions }}]</span>
            </div>
            <div class="flex items-center text-blue-300 font-mono text-xs">
              <span class="mr-2" :class="scanProgress.timing === 'DONE' ? 'text-blue-400' : scanProgress.timing === 'IN PROGRESS' ? 'animate-spin' : ''">{{ scanProgress.timing === "DONE" ? "✓" : scanProgress.timing === "IN PROGRESS" ? "⟳" : ">" }}</span>
              <span>Extended timeout analysis...</span>
              <span class="ml-auto" :class="scanProgress.timing === 'DONE' ? 'text-blue-400' : scanProgress.timing === 'IN PROGRESS' ? 'text-yellow-400' : 'text-gray-500'">[{{ scanProgress.timing }}]</span>
            </div>
          </div>
          <div class="mt-4">
            <div class="w-full bg-gray-700 h-2 rounded">
              <div class="bg-blue-500 h-2 rounded animate-pulse" style="width: 100%"></div>
            </div>
            <div class="text-center text-blue-300 font-mono text-xs mt-2">
              <span class="animate-pulse">█</span><span class="animate-pulse ml-1">█</span><span class="animate-pulse ml-1">█</span>
              EXECUTING DIRECTORY ENUMERATION
              <span class="animate-pulse ml-1">█</span><span class="animate-pulse ml-1">█</span><span class="animate-pulse ml-1">█</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Error Notification -->
      <div v-if="error" class="bg-black border-2 border-red-500 rounded-lg p-6 mb-8 shadow-2xl">
        <div class="text-red-400 font-mono text-sm mb-4">
          <span class="text-red-300">[ERROR]</span> Directory scan failed
        </div>
        <div class="border border-red-600 rounded p-4 bg-gray-900">
          <div class="text-red-400 font-mono text-xs mb-2">
            <span class="text-red-300">root@matrix</span>:<span class="text-blue-400">~</span>$ ./dirsearch --target {{ targetUrl }}
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
        <div class="bg-black bg-opacity-80 border border-blue-500 rounded-lg p-6">
          <div class="flex justify-between items-center mb-4">
            <h3 class="text-xl font-bold text-blue-400 flex items-center">
              <svg class="w-6 h-6 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
              </svg>
              Directory Enumeration Report
            </h3>
            <div class="flex space-x-2">
              <button @click="downloadReport()" class="px-4 py-2 bg-blue-600 hover:bg-blue-500 text-black font-mono text-sm font-bold rounded border border-blue-400 transition-all duration-300">[DOWNLOAD REPORT]</button>
            </div>
          </div>
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            <div class="bg-gray-900 p-4 rounded border border-blue-600">
              <span class="text-blue-300 text-sm">Target:</span>
              <span class="text-blue-400 font-mono block mt-1">{{ results.domain }}</span>
            </div>
            <div class="bg-gray-900 p-4 rounded border border-blue-600">
              <span class="text-blue-300 text-sm">Wordlist:</span>
              <span class="text-blue-400 font-mono text-sm block mt-1">{{ scanOptions.wordlist }}</span>
            </div>
            <div class="bg-gray-900 p-4 rounded border border-blue-600">
              <span class="text-blue-300 text-sm">Directories Found:</span>
              <span class="text-blue-400 font-mono text-sm block mt-1">{{ getFoundCount() }}</span>
            </div>
            <div class="bg-gray-900 p-4 rounded border border-blue-600">
              <span class="text-blue-300 text-sm">Total Checked:</span>
              <span class="text-blue-400 font-mono text-sm block mt-1">{{ getTotalCount() }}</span>
            </div>
          </div>
        </div>

        <!-- Directory Scan Results -->
        <div class="bg-black bg-opacity-80 border border-blue-500 rounded-lg p-6">
          <div class="flex justify-between items-center mb-4">
            <h3 class="text-xl font-bold text-blue-400 flex items-center">
              <svg class="w-6 h-6 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2H5a2 2 0 00-2-2z"></path>
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 5a2 2 0 012-2h4a2 2 0 012 2v2H8V5z"></path>
              </svg>
              Directory Enumeration Results
            </h3>
            <div class="flex space-x-2">
              <button @click="downloadReport()" class="px-4 py-2 bg-blue-600 hover:bg-blue-500 text-black font-mono text-sm font-bold rounded border border-blue-400 transition-all duration-300">[DOWNLOAD]</button>
            </div>
          </div>
          <div v-if="results.directories && results.directories.length > 0 && !results.directories[0].error" class="overflow-x-auto">
            <table class="w-full text-sm">
              <thead>
                <tr class="border-b border-blue-600">
                  <th class="text-left text-blue-400 font-mono py-2">Status</th>
                  <th class="text-left text-blue-400 font-mono py-2">URL</th>
                  <th class="text-left text-blue-400 font-mono py-2">Status Code</th>
                  <th class="text-left text-blue-400 font-mono py-2">Size</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="result in results.directories" :key="result.url" class="border-b border-gray-700 hover:bg-gray-800">
                  <td class="py-2">
                    <span class="px-2 py-1 rounded text-xs font-bold" :class="result.found ? 'bg-orange-600' : 'bg-blue-600'">
                      {{ result.found ? "EXPOSED" : "SECURE" }}
                    </span>
                  </td>
                  <td class="text-blue-400 font-mono text-sm py-2 break-all">{{ result.url }}</td>
                  <td class="text-blue-400 font-mono py-2 break-all">{{ result.status_code }}</td>
                  <td class="text-blue-400 font-mono py-2 break-all">{{ result.size || 'N/A' }}</td>
                </tr>
              </tbody>
            </table>
          </div>
          <div v-else-if="results.directories && results.directories[0] && results.directories[0].error" class="text-red-400">{{ results.directories[0].error }}</div>
          <div v-else class="text-blue-300">No directories found</div>
        </div>
      </div>
    </main>
  </div>
</template>

<script>
export default {
  name: 'DirectoryScan',
  data() {
    return {
      targetUrl: '',
      loading: false,
      results: null,
      error: null,
      currentTime: new Date(),
      scanProgress: {
        wordlist: 'PENDING',
        recursion: 'PENDING',
        extensions: 'PENDING',
        timing: 'PENDING',
      },
      scanOptions: {
        wordlist: 'common',
        enable_recursion: true,
        enable_extensions: true,
        enable_timing: false,
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
    async startDirScan() {
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
        formData.append('scan_type', 'directory');
        formData.append('wordlist', this.scanOptions.wordlist);
        formData.append('enable_recursion', this.scanOptions.enable_recursion ? 'true' : 'false');
        formData.append('enable_extensions', this.scanOptions.enable_extensions ? 'true' : 'false');
        formData.append('enable_timing', this.scanOptions.enable_timing ? 'true' : 'false');

        // Start dynamic progress simulation
        this.simulateScanProgress();

        const response = await fetch('http://localhost:8000/audit', {
          method: 'POST',
          body: formData,
        });

        if (!response.ok) {
          throw new Error('Directory scan failed');
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
        wordlist: 'PENDING',
        recursion: this.scanOptions.enable_recursion ? 'PENDING' : 'DISABLED',
        extensions: this.scanOptions.enable_extensions ? 'PENDING' : 'DISABLED',
        timing: this.scanOptions.enable_timing ? 'PENDING' : 'DISABLED',
      };
    },

    simulateScanProgress() {
      this.scanProgress.wordlist = 'IN PROGRESS';
      
      setTimeout(() => {
        if (this.scanOptions.enable_recursion) this.scanProgress.recursion = 'IN PROGRESS';
      }, 1000);

      setTimeout(() => {
        if (this.scanOptions.enable_extensions) this.scanProgress.extensions = 'IN PROGRESS';
      }, 2000);

      setTimeout(() => {
        if (this.scanOptions.enable_timing) this.scanProgress.timing = 'IN PROGRESS';
      }, 3000);
    },

    completeAllProgress() {
      this.scanProgress.wordlist = 'DONE';
      if (this.scanOptions.enable_recursion) this.scanProgress.recursion = 'DONE';
      if (this.scanOptions.enable_extensions) this.scanProgress.extensions = 'DONE';
      if (this.scanOptions.enable_timing) this.scanProgress.timing = 'DONE';
    },

    stopScan() {
      this.loading = false;
      this.error = 'Scan stopped by user';
    },

    async downloadReport() {
      if (!this.results) return;

      try {
        const response = await fetch('http://localhost:8000/download-results', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            results: this.results,
            scan_type: 'directories'
          })
        });

        if (response.ok) {
          const blob = await response.blob();
          const url = window.URL.createObjectURL(blob);
          const a = document.createElement('a');
          a.href = url;
          a.download = `directory_scan_${Date.now()}.txt`;
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

    getWordlistSize() {
      const sizes = {
        'common': '1,000',
        'fast': '5,000',
        'big': '20,000',
        'all': '50,000+'
      };
      return sizes[this.scanOptions.wordlist] || 'Unknown';
    },

    getFoundCount() {
      if (!this.results || !this.results.directories) return 0;
      return this.results.directories.filter(d => d.found).length;
    },

    getTotalCount() {
      if (!this.results || !this.results.directories) return 0;
      return this.results.directories.length;
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

        ctx.fillStyle = '#0041ff';
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
  background: linear-gradient(45deg, #000000, #000011, #000000);
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
    animation-timing-function: cubic-bezier(0.215, 0, 0.355, 1);
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
  background: #0041ff;
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: #0033cc;
}

/* Enhanced animations */
.animate-glow {
  animation: glow 2s ease-in-out infinite alternate;
}

@keyframes glow {
  from {
    text-shadow:
      0 0 5px rgba(0, 65, 255, 0.5),
      0 0 10px rgba(0, 65, 255, 0.3),
      0 0 15px rgba(0, 65, 255, 0.2);
  }
  to {
    text-shadow:
      0 0 10px rgba(0, 65, 255, 0.8),
      0 0 20px rgba(0, 65, 255, 0.6),
      0 0 30px rgba(0, 65, 255, 0.4);
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

/* Smooth transitions for all elements */
* {
  transition: all 0.3s ease;
}

/* Enhanced hover effects */
button:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 20px rgba(0, 65, 255, 0.3);
}

input:focus {
  box-shadow: 0 0 0 3px rgba(0, 65, 255, 0.2);
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
  box-shadow: 0 0 30px rgba(0, 65, 255, 0.2);
}

/* Smooth text animations */
.text-blue-400 {
  transition: color 0.3s ease;
}

.text-blue-400:hover {
  color: #4488ff;
}

/* Professional gradient backgrounds */
.matrix-bg {
  background: linear-gradient(
    135deg,
    #000000 0%,
    #000011 25%,
    #000000 50%,
    #001100 75%,
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
  background: linear-gradient(180deg, #0041ff, #0033cc);
  border-radius: 5px;
  border: 1px solid rgba(0, 0, 0, 0.5);
}

::-webkit-scrollbar-thumb:hover {
  background: linear-gradient(180deg, #4488ff, #0041ff);
}

/* Professional glow effects */
.glow {
  box-shadow:
    0 0 30px rgba(0, 65, 255, 0.4),
    0 0 60px rgba(0, 65, 255, 0.2),
    0 0 90px rgba(0, 65, 255, 0.1);
}

.text-shadow {
  text-shadow:
    0 0 10px rgba(0, 65, 255, 0.8),
    0 0 20px rgba(0, 65, 255, 0.4),
    0 0 30px rgba(0, 65, 255, 0.2);
}

/* Smooth focus transitions */
input:focus,
select:focus,
button:focus {
  outline: none;
  box-shadow:
    0 0 0 2px rgba(0, 65, 255, 0.5),
    0 0 0 4px rgba(0, 65, 255, 0.2);
}

/* Professional button states */
button:active {
  transform: translateY(0);
  box-shadow: 0 2px 10px rgba(0, 65, 255, 0.2);
}

/* Enhanced checkbox styling */
input[type="checkbox"] {
  accent-color: #0041ff;
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
  border-color: rgba(0, 65, 255, 0.3);
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