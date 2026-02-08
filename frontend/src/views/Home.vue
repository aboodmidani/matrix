<template>
  <div>
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
          <button @click="declineDisclaimer" class="bg-red-600 hover:bg-red-500 text-white font-bold py-4 px-6 rounded border-2 border-red-400 hover:border-red-400 transition-all duration-300 font-mono tracking-wide">[EXIT SYSTEM]</button>
        </div>
      </div>
    </div>

    <!-- Welcome Section -->
    <div class="bg-black border-2 border-green-500 rounded-lg p-6 mb-8 shadow-2xl">
      <div class="flex items-center mb-4 text-green-400 text-sm font-mono">
        <span class="animate-pulse">●</span>
        <span class="ml-2">SYSTEM STATUS: ONLINE</span>
        <span class="ml-auto">SESSION: {{ sessionId }}</span>
      </div>

      <div class="border border-green-600 rounded p-4 mb-6 bg-gray-900">
        <div class="text-green-400 font-mono text-sm mb-2">
          <span class="text-green-300">root@matrix</span>:<span class="text-blue-400">~</span>$ security-matrix --status
        </div>
        <div class="text-green-400 font-mono text-xs opacity-75">Advanced web security scanning and analysis framework</div>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div class="bg-gray-900 p-6 rounded border border-green-600">
          <h3 class="text-lg font-bold text-green-400 mb-4 font-mono">SYSTEM INFORMATION</h3>
          <div class="space-y-2 text-green-300 font-mono text-sm">
            <div>• Version: 3.0.0</div>
            <div>• Framework: Vue.js 3 + FastAPI</div>
            <div>• Environment: {{ environment }}</div>
            <div>• API Status: {{ apiStatus }}</div>
          </div>
        </div>

        <div class="bg-gray-900 p-6 rounded border border-green-600">
          <h3 class="text-lg font-bold text-green-400 mb-4 font-mono">AVAILABLE MODULES</h3>
          <div class="grid grid-cols-2 gap-2 text-green-300 font-mono text-sm">
            <div class="flex items-center">
              <span class="w-2 h-2 bg-green-500 rounded-full mr-2"></span>
              DNS Reconnaissance
            </div>
            <div class="flex items-center">
              <span class="w-2 h-2 bg-green-500 rounded-full mr-2"></span>
              Port Scanning
            </div>
            <!-- <div class="flex items-center">
              <span class="w-2 h-2 bg-green-500 rounded-full mr-2"></span>
              Directory Enumeration
            </div>
            <div class="flex items-center">
              <span class="w-2 h-2 bg-green-500 rounded-full mr-2"></span>
              Vulnerability Assessment
            </div> -->
            <div class="flex items-center">
              <span class="w-2 h-2 bg-green-500 rounded-full mr-2"></span>
              Technology Detection
            </div>
            <div class="flex items-center">
              <span class="w-2 h-2 bg-green-500 rounded-full mr-2"></span>
              WAF Detection
            </div>
            <div class="flex items-center">
              <span class="w-2 h-2 bg-green-500 rounded-full mr-2"></span>
              Subdomain Discovery
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Quick Actions -->
    <div class="bg-black border-2 border-green-500 rounded-lg p-6 mb-8 shadow-2xl">
      <h3 class="text-xl font-bold text-green-400 mb-4 font-mono">QUICK ACTIONS</h3>
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        <!-- <router-link to="/directory-scan" class="bg-gray-900 p-6 rounded border border-green-600 hover:border-green-400 transition-all duration-300 transform hover:scale-105">
          <div class="flex items-center justify-between">
            <div>
              <h4 class="text-green-400 font-bold font-mono">DIRECTORY SCAN</h4>
              <p class="text-green-300 text-sm font-mono">Find hidden directories and files</p>
            </div>
            <div class="w-8 h-8 border border-green-500 rounded flex items-center justify-center">
              <svg class="w-5 h-5 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2H5a2 2 0 00-2-2z"></path>
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 5a2 2 0 012-2h4a2 2 0 012 2v2H8V5z"></path>
              </svg>
            </div>
          </div>
        </router-link>

        <router-link to="/vulnerability-scan" class="bg-gray-900 p-6 rounded border border-green-600 hover:border-green-400 transition-all duration-300 transform hover:scale-105">
          <div class="flex items-center justify-between">
            <div>
              <h4 class="text-green-400 font-bold font-mono">VULNERABILITY SCAN</h4>
              <p class="text-green-300 text-sm font-mono">Detect security vulnerabilities</p>
            </div>
            <div class="w-8 h-8 border border-red-500 rounded flex items-center justify-center">
              <svg class="w-5 h-5 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z"></path>
              </svg>
            </div>
          </div>
        </router-link> -->

        <router-link to="/dns-scan" class="bg-gray-900 p-6 rounded border border-green-600 hover:border-green-400 transition-all duration-300 transform hover:scale-105">
          <div class="flex items-center justify-between">
            <div>
              <h4 class="text-green-400 font-bold font-mono">DNS SCAN</h4>
              <p class="text-green-300 text-sm font-mono">Analyze DNS records</p>
            </div>
            <div class="w-8 h-8 border border-blue-500 rounded flex items-center justify-center">
              <svg class="w-5 h-5 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 01-9 9m9-9a9 9 0 00-9-9m9 9H3m9 9v-9m0-9v9m0 9c-5 0-9-4-9-9s4-9 9-9"></path>
              </svg>
            </div>
          </div>
        </router-link>

        <router-link to="/port-scan" class="bg-gray-900 p-6 rounded border border-green-600 hover:border-green-400 transition-all duration-300 transform hover:scale-105">
          <div class="flex items-center justify-between">
            <div>
              <h4 class="text-green-400 font-bold font-mono">PORT SCAN</h4>
              <p class="text-green-300 text-sm font-mono">Discover open ports</p>
            </div>
            <div class="w-8 h-8 border border-yellow-500 rounded flex items-center justify-center">
              <svg class="w-5 h-5 text-yellow-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"></path>
              </svg>
            </div>
          </div>
        </router-link>

        <router-link to="/technology-scan" class="bg-gray-900 p-6 rounded border border-green-600 hover:border-green-400 transition-all duration-300 transform hover:scale-105">
          <div class="flex items-center justify-between">
            <div>
              <h4 class="text-green-400 font-bold font-mono">TECHNOLOGY SCAN</h4>
              <p class="text-green-300 text-sm font-mono">Identify technologies</p>
            </div>
            <div class="w-8 h-8 border border-purple-500 rounded flex items-center justify-center">
              <svg class="w-5 h-5 text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"></path>
              </svg>
            </div>
          </div>
        </router-link>

        <router-link to="/firewall-scan" class="bg-gray-900 p-6 rounded border border-green-600 hover:border-green-400 transition-all duration-300 transform hover:scale-105">
          <div class="flex items-center justify-between">
            <div>
              <h4 class="text-green-400 font-bold font-mono">WAF DETECTION</h4>
              <p class="text-green-300 text-sm font-mono">Detect web application firewalls</p>
            </div>
            <div class="w-8 h-8 border border-red-500 rounded flex items-center justify-center">
              <svg class="w-5 h-5 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"></path>
              </svg>
            </div>
          </div>
        </router-link>
      </div>
    </div>

    <!-- System Status -->
    <div class="bg-black border-2 border-green-500 rounded-lg p-6 shadow-2xl">
      <h3 class="text-xl font-bold text-green-400 mb-4 font-mono">SYSTEM STATUS</h3>
      <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div class="bg-gray-900 p-4 rounded border border-green-600">
          <div class="flex items-center justify-between">
            <div>
              <span class="text-green-300 text-sm">API Status</span>
              <div class="text-green-400 font-mono font-bold">{{ apiStatus }}</div>
            </div>
            <div class="w-3 h-3 bg-green-500 rounded-full animate-pulse"></div>
          </div>
        </div>
        <div class="bg-gray-900 p-4 rounded border border-green-600">
          <div class="flex items-center justify-between">
            <div>
              <span class="text-green-300 text-sm">Environment</span>
              <div class="text-green-400 font-mono font-bold">{{ environment }}</div>
            </div>
            <div class="text-green-400 font-mono text-xs">ENV</div>
          </div>
        </div>
        <div class="bg-gray-900 p-4 rounded border border-green-600">
          <div class="flex items-center justify-between">
            <div>
              <span class="text-green-300 text-sm">Version</span>
              <div class="text-green-400 font-mono font-bold">3.0.0</div>
            </div>
            <div class="text-green-400 font-mono text-xs">V3</div>
          </div>
        </div>
        <div class="bg-gray-900 p-4 rounded border border-green-600">
          <div class="flex items-center justify-between">
            <div>
              <span class="text-green-300 text-sm">Session</span>
              <div class="text-green-400 font-mono font-bold">{{ sessionId }}</div>
            </div>
            <div class="text-green-400 font-mono text-xs">ID</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { apiService } from '../utils/api'

export default {
  name: 'Home',
  setup() {
    const showDisclaimer = ref(true)
    const apiStatus = ref('CHECKING...')
    const environment = ref('DEVELOPMENT')
    const sessionId = Math.random().toString(36).substring(2, 8).toUpperCase()

    const acceptDisclaimer = () => {
      showDisclaimer.value = false
      localStorage.setItem('disclaimerAccepted', 'true')
    }

    const declineDisclaimer = () => {
      window.close()
    }

    const checkAPIStatus = async () => {
      try {
        const response = await apiService.get('/')
        if (response && response.message) {
          apiStatus.value = 'ONLINE'
          environment.value = response.environment || 'PRODUCTION'
        } else {
          apiStatus.value = 'OFFLINE'
        }
      } catch (error) {
        apiStatus.value = 'OFFLINE'
      }
    }

    onMounted(() => {
      // Check if disclaimer was already accepted
      if (localStorage.getItem('disclaimerAccepted') === 'true') {
        showDisclaimer.value = false
      }
      
      // Check API status
      checkAPIStatus()
    })

    return {
      showDisclaimer,
      apiStatus,
      environment,
      sessionId,
      acceptDisclaimer,
      declineDisclaimer
    }
  }
}
</script>