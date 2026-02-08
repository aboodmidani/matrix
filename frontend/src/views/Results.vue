<template>
  <div class="bg-black border-2 border-green-500 rounded-lg p-6 shadow-2xl">
    <div class="flex items-center mb-4 text-green-400 text-sm font-mono">
      <span class="animate-pulse">●</span>
      <span class="ml-2">SCAN RESULTS DASHBOARD</span>
      <span class="ml-auto">SESSION: {{ sessionId }}</span>
    </div>

    <!-- Terminal Header -->
    <div class="border border-green-600 rounded p-4 mb-6 bg-gray-900">
      <div class="text-green-400 font-mono text-sm mb-2">
        <span class="text-green-300">root@matrix</span>:<span class="text-blue-400">~</span>$ results --view [ALL_SCANS]
      </div>
      <div class="text-green-400 font-mono text-xs opacity-75">Comprehensive scan results and analysis dashboard</div>
    </div>

    <!-- Results Summary -->
    <div class="grid grid-cols-1 lg:grid-cols-4 gap-4 mb-8">
      <div class="bg-gray-900 p-4 rounded border border-green-600">
        <div class="text-green-300 text-sm">Total Scans</div>
        <div class="text-green-400 font-mono text-lg font-bold">{{ getTotalScans() }}</div>
      </div>
      <div class="bg-gray-900 p-4 rounded border border-green-600">
        <div class="text-green-300 text-sm">Completed</div>
        <div class="text-green-400 font-mono text-lg font-bold">{{ getCompletedScans() }}</div>
      </div>
      <div class="bg-gray-900 p-4 rounded border border-green-600">
        <div class="text-green-300 text-sm">Issues Found</div>
        <div class="text-green-400 font-mono text-lg font-bold">{{ getTotalIssues() }}</div>
      </div>
      <div class="bg-gray-900 p-4 rounded border border-green-600">
        <div class="text-green-300 text-sm">High Risk</div>
        <div class="text-green-400 font-mono text-lg font-bold">{{ getHighRiskCount() }}</div>
      </div>
    </div>

    <!-- Scan Results Grid -->
    <div class="space-y-6">
      <!-- Directory Scan Results -->
      <div v-if="directoryResults" class="bg-black bg-opacity-80 border border-blue-500 rounded-lg p-6">
        <div class="flex justify-between items-center mb-4">
          <h3 class="text-xl font-bold text-blue-400 flex items-center">
            <svg class="w-6 h-6 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2H5a2 2 0 00-2-2z"></path>
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 5a2 2 0 012-2h4a2 2 0 012 2v2H8V5z"></path>
            </svg>
            Directory Enumeration Results
          </h3>
          <div class="flex space-x-2">
            <button @click="downloadReport('directories')" class="px-4 py-2 bg-blue-600 hover:bg-blue-500 text-black font-mono text-sm font-bold rounded border border-blue-400 transition-all duration-300">[DOWNLOAD]</button>
          </div>
        </div>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-4">
          <div class="bg-gray-900 p-4 rounded border border-blue-600">
            <span class="text-blue-300 text-sm">Target:</span>
            <span class="text-blue-400 font-mono block mt-1">{{ directoryResults.url }}</span>
          </div>
          <div class="bg-gray-900 p-4 rounded border border-blue-600">
            <span class="text-blue-300 text-sm">Directories Found:</span>
            <span class="text-blue-400 font-mono text-sm block mt-1">{{ getDirectoryCount() }}</span>
          </div>
          <div class="bg-gray-900 p-4 rounded border border-blue-600">
            <span class="text-blue-300 text-sm">Total Checked:</span>
            <span class="text-blue-400 font-mono text-sm block mt-1">{{ getTotalDirectoryCount() }}</span>
          </div>
          <div class="bg-gray-900 p-4 rounded border border-blue-600">
            <span class="text-blue-300 text-sm">Status:</span>
            <span class="text-blue-400 font-mono text-sm block mt-1">COMPLETED</span>
          </div>
        </div>
        <div v-if="directoryResults.directories && directoryResults.directories.length > 0" class="overflow-x-auto">
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
              <tr v-for="result in directoryResults.directories" :key="result.url" class="border-b border-gray-700 hover:bg-gray-800">
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
      </div>

      <!-- Vulnerability Scan Results -->
      <div v-if="vulnerabilityResults" class="bg-black bg-opacity-80 border border-red-500 rounded-lg p-6">
        <div class="flex justify-between items-center mb-4">
          <h3 class="text-xl font-bold text-red-400 flex items-center">
            <svg class="w-6 h-6 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z"></path>
            </svg>
            Vulnerability Assessment Results
          </h3>
          <div class="flex space-x-2">
            <button @click="downloadReport('vulnerabilities')" class="px-4 py-2 bg-blue-600 hover:bg-blue-500 text-black font-mono text-sm font-bold rounded border border-blue-400 transition-all duration-300">[DOWNLOAD]</button>
          </div>
        </div>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-4">
          <div class="bg-gray-900 p-4 rounded border border-red-600">
            <span class="text-red-300 text-sm">Target:</span>
            <span class="text-red-400 font-mono block mt-1">{{ vulnerabilityResults.url }}</span>
          </div>
          <div class="bg-gray-900 p-4 rounded border border-red-600">
            <span class="text-red-300 text-sm">Vulnerabilities Found:</span>
            <span class="text-red-400 font-mono text-sm block mt-1">{{ getVulnerabilityCount() }}</span>
          </div>
          <div class="bg-gray-900 p-4 rounded border border-red-600">
            <span class="text-red-300 text-sm">High Risk Issues:</span>
            <span class="text-red-400 font-mono text-sm block mt-1">{{ getHighVulnerabilityCount() }}</span>
          </div>
          <div class="bg-gray-900 p-4 rounded border border-red-600">
            <span class="text-red-300 text-sm">Status:</span>
            <span class="text-red-400 font-mono text-sm block mt-1">COMPLETED</span>
          </div>
        </div>
        <div v-if="vulnerabilityResults.vulnerabilities && vulnerabilityResults.vulnerabilities.length > 0" class="space-y-4">
          <div v-for="vuln in vulnerabilityResults.vulnerabilities" :key="vuln.description" class="p-4 bg-gray-900 rounded border-l-4" :class="vuln.severity === 'High' ? 'border-red-500' : vuln.severity === 'Medium' ? 'border-yellow-500' : 'border-blue-500'">
            <div class="flex justify-between items-start">
              <div>
                <span class="text-red-400 font-bold break-all">{{ vuln.type }}</span>
                <p class="text-red-300 text-sm mt-1 break-all">{{ vuln.description }}</p>
              </div>
              <span class="px-2 py-1 rounded text-xs font-bold" :class="vuln.severity === 'High' ? 'bg-red-600' : vuln.severity === 'Medium' ? 'bg-yellow-600' : 'bg-blue-600'">{{ vuln.severity }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- DNS Scan Results -->
      <div v-if="dnsResults" class="bg-black bg-opacity-80 border border-blue-500 rounded-lg p-6">
        <div class="flex justify-between items-center mb-4">
          <h3 class="text-xl font-bold text-blue-400 flex items-center">
            <svg class="w-6 h-6 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 01-9 9m9-9a9 9 0 00-9-9m9 9H3m9 9v-9m0-9v9m0 9c-5 0-9-4-9-9s4-9 9-9"></path>
            </svg>
            DNS Reconnaissance Results
          </h3>
          <div class="flex space-x-2">
            <button @click="downloadReport('dns')" class="px-4 py-2 bg-blue-600 hover:bg-blue-500 text-black font-mono text-sm font-bold rounded border border-blue-400 transition-all duration-300">[DOWNLOAD]</button>
          </div>
        </div>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-4">
          <div class="bg-gray-900 p-4 rounded border border-blue-600">
            <span class="text-blue-300 text-sm">Target:</span>
            <span class="text-blue-400 font-mono block mt-1">{{ dnsResults.url }}</span>
          </div>
          <div class="bg-gray-900 p-4 rounded border border-blue-600">
            <span class="text-blue-300 text-sm">Records Found:</span>
            <span class="text-blue-400 font-mono text-sm block mt-1">{{ getDNSRecordCount() }}</span>
          </div>
          <div class="bg-gray-900 p-4 rounded border border-blue-600">
            <span class="text-blue-300 text-sm">Subdomains:</span>
            <span class="text-blue-400 font-mono text-sm block mt-1">{{ getDNSSubdomainCount() }}</span>
          </div>
          <div class="bg-gray-900 p-4 rounded border border-blue-600">
            <span class="text-blue-300 text-sm">Status:</span>
            <span class="text-blue-400 font-mono text-sm block mt-1">COMPLETED</span>
          </div>
        </div>
        <div v-if="dnsResults.dns_records && dnsResults.dns_records.length > 0" class="space-y-4">
          <div v-for="record in dnsResults.dns_records" :key="record.type" class="p-4 bg-gray-900 rounded border border-blue-600">
            <div class="flex justify-between items-start">
              <div>
                <span class="text-blue-400 font-bold">{{ record.type }}</span>
                <p class="text-blue-300 text-sm mt-1 break-all">{{ record.value }}</p>
              </div>
              <span class="px-2 py-1 rounded text-xs font-bold bg-blue-600">{{ record.status }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Port Scan Results -->
      <div v-if="portResults" class="bg-black bg-opacity-80 border border-yellow-500 rounded-lg p-6">
        <div class="flex justify-between items-center mb-4">
          <h3 class="text-xl font-bold text-yellow-400 flex items-center">
            <svg class="w-6 h-6 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"></path>
            </svg>
            Port Scanning Results
          </h3>
          <div class="flex space-x-2">
            <button @click="downloadReport('ports')" class="px-4 py-2 bg-blue-600 hover:bg-blue-500 text-black font-mono text-sm font-bold rounded border border-blue-400 transition-all duration-300">[DOWNLOAD]</button>
          </div>
        </div>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-4">
          <div class="bg-gray-900 p-4 rounded border border-yellow-600">
            <span class="text-yellow-300 text-sm">Target:</span>
            <span class="text-yellow-400 font-mono block mt-1">{{ portResults.url }}</span>
          </div>
          <div class="bg-gray-900 p-4 rounded border border-yellow-600">
            <span class="text-yellow-300 text-sm">Open Ports:</span>
            <span class="text-yellow-400 font-mono text-sm block mt-1">{{ getOpenPortCount() }}</span>
          </div>
          <div class="bg-gray-900 p-4 rounded border border-yellow-600">
            <span class="text-yellow-300 text-sm">Services Detected:</span>
            <span class="text-yellow-400 font-mono text-sm block mt-1">{{ getServiceCount() }}</span>
          </div>
          <div class="bg-gray-900 p-4 rounded border border-yellow-600">
            <span class="text-yellow-300 text-sm">Status:</span>
            <span class="text-yellow-400 font-mono text-sm block mt-1">COMPLETED</span>
          </div>
        </div>
        <div v-if="portResults.ports && portResults.ports.length > 0" class="overflow-x-auto">
          <table class="w-full text-sm">
            <thead>
              <tr class="border-b border-yellow-600">
                <th class="text-left text-yellow-400 font-mono py-2">Port</th>
                <th class="text-left text-yellow-400 font-mono py-2">Protocol</th>
                <th class="text-left text-yellow-400 font-mono py-2">Service</th>
                <th class="text-left text-yellow-400 font-mono py-2">Status</th>
                <th class="text-left text-yellow-400 font-mono py-2">Version</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="port in portResults.ports" :key="port.port" class="border-b border-gray-700 hover:bg-gray-800">
                <td class="text-yellow-400 font-mono text-sm py-2">{{ port.port }}</td>
                <td class="text-yellow-400 font-mono py-2">{{ port.protocol }}</td>
                <td class="text-yellow-400 font-mono py-2">{{ port.service }}</td>
                <td class="py-2">
                  <span class="px-2 py-1 rounded text-xs font-bold" :class="port.status === 'open' ? 'bg-green-600' : 'bg-red-600'">
                    {{ port.status.toUpperCase() }}
                  </span>
                </td>
                <td class="text-yellow-400 font-mono py-2">{{ port.version || 'Unknown' }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Technology Scan Results -->
      <div v-if="technologyResults" class="bg-black bg-opacity-80 border border-purple-500 rounded-lg p-6">
        <div class="flex justify-between items-center mb-4">
          <h3 class="text-xl font-bold text-purple-400 flex items-center">
            <svg class="w-6 h-6 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"></path>
            </svg>
            Technology Detection Results
          </h3>
          <div class="flex space-x-2">
            <button @click="downloadReport('technology')" class="px-4 py-2 bg-blue-600 hover:bg-blue-500 text-black font-mono text-sm font-bold rounded border border-blue-400 transition-all duration-300">[DOWNLOAD]</button>
          </div>
        </div>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-4">
          <div class="bg-gray-900 p-4 rounded border border-purple-600">
            <span class="text-purple-300 text-sm">Target:</span>
            <span class="text-purple-400 font-mono block mt-1">{{ technologyResults.url }}</span>
          </div>
          <div class="bg-gray-900 p-4 rounded border border-purple-600">
            <span class="text-purple-300 text-sm">Technologies Found:</span>
            <span class="text-purple-400 font-mono text-sm block mt-1">{{ getTechnologyCount() }}</span>
          </div>
          <div class="bg-gray-900 p-4 rounded border border-purple-600">
            <span class="text-purple-300 text-sm">Categories:</span>
            <span class="text-purple-400 font-mono text-sm block mt-1">{{ getTechnologyCategoryCount() }}</span>
          </div>
          <div class="bg-gray-900 p-4 rounded border border-purple-600">
            <span class="text-purple-300 text-sm">Status:</span>
            <span class="text-purple-400 font-mono text-sm block mt-1">COMPLETED</span>
          </div>
        </div>
        <div v-if="technologyResults.technologies && technologyResults.technologies.length > 0" class="space-y-4">
          <div v-for="tech in technologyResults.technologies" :key="tech.name" class="p-4 bg-gray-900 rounded border border-purple-600">
            <div class="flex justify-between items-start">
              <div>
                <span class="text-purple-400 font-bold">{{ tech.name }}</span>
                <p class="text-purple-300 text-sm mt-1">{{ tech.version || 'Version unknown' }}</p>
                <p class="text-purple-300 text-xs mt-1">{{ tech.category }}</p>
              </div>
              <span class="px-2 py-1 rounded text-xs font-bold bg-purple-600">{{ tech.confidence || 'High' }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- WAF Scan Results -->
      <div v-if="wafResults" class="bg-black bg-opacity-80 border border-red-500 rounded-lg p-6">
        <div class="flex justify-between items-center mb-4">
          <h3 class="text-xl font-bold text-red-400 flex items-center">
            <svg class="w-6 h-6 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z"></path>
            </svg>
            WAF Detection Results
          </h3>
          <div class="flex space-x-2">
            <button @click="downloadReport('firewall')" class="px-4 py-2 bg-blue-600 hover:bg-blue-500 text-black font-mono text-sm font-bold rounded border border-blue-400 transition-all duration-300">[DOWNLOAD]</button>
          </div>
        </div>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-4">
          <div class="bg-gray-900 p-4 rounded border border-red-600">
            <span class="text-red-300 text-sm">Target:</span>
            <span class="text-red-400 font-mono block mt-1">{{ wafResults.url }}</span>
          </div>
          <div class="bg-gray-900 p-4 rounded border border-red-600">
            <span class="text-red-300 text-sm">WAF Detected:</span>
            <span class="text-red-400 font-mono text-sm block mt-1">{{ wafResults.waf_detected ? 'YES' : 'NO' }}</span>
          </div>
          <div class="bg-gray-900 p-4 rounded border border-red-600">
            <span class="text-red-300 text-sm">WAF Type:</span>
            <span class="text-red-400 font-mono text-sm block mt-1">{{ wafResults.waf_type || 'Unknown' }}</span>
          </div>
          <div class="bg-gray-900 p-4 rounded border border-red-600">
            <span class="text-red-300 text-sm">Status:</span>
            <span class="text-red-400 font-mono text-sm block mt-1">COMPLETED</span>
          </div>
        </div>
        <div v-if="wafResults.waf_results && wafResults.waf_results.length > 0" class="space-y-4">
          <div v-for="waf in wafResults.waf_results" :key="waf.name" class="p-4 bg-gray-900 rounded border border-red-600">
            <div class="flex justify-between items-start">
              <div>
                <span class="text-red-400 font-bold">{{ waf.name }}</span>
                <p class="text-red-300 text-sm mt-1">{{ waf.version || 'Version unknown' }}</p>
                <p class="text-red-300 text-xs mt-1">{{ waf.confidence || 'High' }} confidence</p>
              </div>
              <span class="px-2 py-1 rounded text-xs font-bold" :class="waf.detected ? 'bg-red-600' : 'bg-green-600'">{{ waf.detected ? 'DETECTED' : 'NOT DETECTED' }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- No Results Message -->
      <div v-if="!hasAnyResults" class="bg-gray-900 border border-green-600 rounded-lg p-8 text-center">
        <div class="text-green-400 font-mono text-lg mb-2">[NO SCAN RESULTS AVAILABLE]</div>
        <div class="text-green-300 font-mono text-sm">Please run scans from the individual scan modules to view results here.</div>
        <div class="mt-4">
          <router-link to="/directory-scan" class="px-4 py-2 bg-blue-600 hover:bg-blue-500 text-black font-mono text-sm font-bold rounded border border-blue-400 transition-all duration-300 mr-2">[RUN DIRECTORY SCAN]</router-link>
          <router-link to="/vulnerability-scan" class="px-4 py-2 bg-red-600 hover:bg-red-500 text-white font-mono text-sm font-bold rounded border border-red-400 transition-all duration-300">[RUN VULNERABILITY SCAN]</router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useApi } from '../utils/api'

export default {
  name: 'Results',
  setup() {
    const sessionId = Math.random().toString(36).substring(2, 8).toUpperCase()
    const directoryResults = ref(null)
    const vulnerabilityResults = ref(null)
    const dnsResults = ref(null)
    const portResults = ref(null)
    const technologyResults = ref(null)
    const wafResults = ref(null)

    const { executeRequest } = useApi()

    const getTotalScans = () => {
      let count = 0
      if (directoryResults.value) count++
      if (vulnerabilityResults.value) count++
      if (dnsResults.value) count++
      if (portResults.value) count++
      if (technologyResults.value) count++
      if (wafResults.value) count++
      return count
    }

    const getCompletedScans = () => getTotalScans()

    const getTotalIssues = () => {
      let count = 0
      if (directoryResults.value && directoryResults.value.directories) {
        count += directoryResults.value.directories.filter(d => d.found).length
      }
      if (vulnerabilityResults.value && vulnerabilityResults.value.vulnerabilities) {
        count += vulnerabilityResults.value.vulnerabilities.length
      }
      return count
    }

    const getHighRiskCount = () => {
      let count = 0
      if (vulnerabilityResults.value && vulnerabilityResults.value.vulnerabilities) {
        count += vulnerabilityResults.value.vulnerabilities.filter(v => v.severity === 'High').length
      }
      return count
    }

    const getDirectoryCount = () => {
      if (!directoryResults.value || !directoryResults.value.directories) return 0
      return directoryResults.value.directories.filter(d => d.found).length
    }

    const getTotalDirectoryCount = () => {
      if (!directoryResults.value || !directoryResults.value.directories) return 0
      return directoryResults.value.directories.length
    }

    const getVulnerabilityCount = () => {
      if (!vulnerabilityResults.value || !vulnerabilityResults.value.vulnerabilities) return 0
      return vulnerabilityResults.value.vulnerabilities.length
    }

    const getHighVulnerabilityCount = () => {
      if (!vulnerabilityResults.value || !vulnerabilityResults.value.vulnerabilities) return 0
      return vulnerabilityResults.value.vulnerabilities.filter(v => v.severity === 'High').length
    }

    const getDNSRecordCount = () => {
      if (!dnsResults.value || !dnsResults.value.dns_records) return 0
      return dnsResults.value.dns_records.length
    }

    const getDNSSubdomainCount = () => {
      if (!dnsResults.value || !dnsResults.value.dns_records) return 0
      return dnsResults.value.dns_records.filter(r => r.type === 'CNAME' || r.type === 'A').length
    }

    const getOpenPortCount = () => {
      if (!portResults.value || !portResults.value.ports) return 0
      return portResults.value.ports.filter(p => p.status === 'open').length
    }

    const getServiceCount = () => {
      if (!portResults.value || !portResults.value.ports) return 0
      return portResults.value.ports.filter(p => p.service && p.service !== 'unknown').length
    }

    const getTechnologyCount = () => {
      if (!technologyResults.value || !technologyResults.value.technologies) return 0
      return technologyResults.value.technologies.length
    }

    const getTechnologyCategoryCount = () => {
      if (!technologyResults.value || !technologyResults.value.technologies) return 0
      const categories = new Set(technologyResults.value.technologies.map(t => t.category))
      return categories.size
    }

    const hasAnyResults = () => {
      return !!(directoryResults.value || vulnerabilityResults.value || dnsResults.value || portResults.value || technologyResults.value || wafResults.value)
    }

    const downloadReport = async (scanType) => {
      let results = null
      
      switch (scanType) {
        case 'directories':
          results = directoryResults.value
          break
        case 'vulnerabilities':
          results = vulnerabilityResults.value
          break
        case 'dns':
          results = dnsResults.value
          break
        case 'ports':
          results = portResults.value
          break
        case 'technology':
          results = technologyResults.value
          break
        case 'firewall':
          results = wafResults.value
          break
      }

      if (!results) return

      try {
        const success = await fetch('/download-results', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            results: results,
            scan_type: scanType
          })
        })

        if (!success) {
          alert('Failed to download report')
        }
      } catch (error) {
        console.error('Download error:', error)
        alert('Failed to download report')
      }
    }

    onMounted(() => {
      // Load results from localStorage or API
      const savedResults = localStorage.getItem('scan_results')
      if (savedResults) {
        try {
          const results = JSON.parse(savedResults)
          directoryResults.value = results.directoryResults || null
          vulnerabilityResults.value = results.vulnerabilityResults || null
          dnsResults.value = results.dnsResults || null
          portResults.value = results.portResults || null
          technologyResults.value = results.technologyResults || null
          wafResults.value = results.wafResults || null
        } catch (error) {
          console.error('Error loading saved results:', error)
        }
      }
    })

    return {
      sessionId,
      directoryResults,
      vulnerabilityResults,
      dnsResults,
      portResults,
      technologyResults,
      wafResults,
      getTotalScans,
      getCompletedScans,
      getTotalIssues,
      getHighRiskCount,
      getDirectoryCount,
      getTotalDirectoryCount,
      getVulnerabilityCount,
      getHighVulnerabilityCount,
      getDNSRecordCount,
      getDNSSubdomainCount,
      getOpenPortCount,
      getServiceCount,
      getTechnologyCount,
      getTechnologyCategoryCount,
      hasAnyResults,
      downloadReport
    }
  }
}
</script>

<style scoped>
/* Enhanced animations */
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
  background: #00ff41;
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: #00cc33;
}

/* Enhanced hover effects */
button:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 20px rgba(0, 255, 65, 0.3);
}

input:focus {
  box-shadow: 0 0 0 3px rgba(0, 255, 65, 0.2);
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