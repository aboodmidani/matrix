import { ref, reactive } from 'vue'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const scanState = reactive({
  isScanning: false,
  currentScan: '',
  progress: 0,
  results: null,
  error: null
})

const scans = reactive({
  dns: { status: 'idle', data: null },
  ports: { status: 'idle', data: null },
  technology: { status: 'idle', data: null },
  firewall: { status: 'idle', data: null },
  subdomain: { status: 'idle', data: null }
})

const scanConfigs = {
  dns: { name: 'DNS Reconnaissance', endpoint: '/scan/dns', color: 'blue', icon: '🌐' },
  ports: { name: 'Port Scanning', endpoint: '/scan/ports', color: 'yellow', icon: '🔌' },
  technology: { name: 'Technology Detection', endpoint: '/scan/technologies', color: 'purple', icon: '🔧' },
  firewall: { name: 'WAF Detection', endpoint: '/scan/firewall', color: 'red', icon: '🛡️' },
  subdomain: { name: 'Subdomain Discovery', endpoint: '/scan/subdomains', color: 'green', icon: '🔍' }
}

async function runSingleScan(scanType, url) {
  const config = scanConfigs[scanType]
  if (!config) return

  scans[scanType].status = 'scanning'
  scanState.currentScan = config.name

  try {
    const formData = new URLSearchParams()
    formData.append('url', url)

    const response = await fetch(`${API_URL}${config.endpoint}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: formData
    })

    if (response.ok) {
      const data = await response.json()
      scans[scanType].data = data
      scans[scanType].status = 'complete'
    } else {
      scans[scanType].status = 'error'
      scans[scanType].error = 'Scan failed'
    }
  } catch (err) {
    scans[scanType].status = 'error'
    scans[scanType].error = err.message
  }
}

async function runAllScans(url) {
  scanState.isScanning = true
  scanState.error = null
  scanState.results = null
  
  Object.keys(scans).forEach(key => {
    scans[key].status = 'idle'
    scans[key].data = null
    scans[key].error = null
  })

  const scanTypes = Object.keys(scanConfigs)
  const totalScans = scanTypes.length
  let completedScans = 0

  const scanPromises = scanTypes.map(async (scanType) => {
    await runSingleScan(scanType, url)
    completedScans++
    scanState.progress = Math.round((completedScans / totalScans) * 100)
  })

  await Promise.all(scanPromises)
  
  scanState.isScanning = false
  scanState.currentScan = ''
  scanState.progress = 100
  scanState.results = { url, timestamp: Date.now() }
}

function resetScans() {
  Object.keys(scans).forEach(key => {
    scans[key].status = 'idle'
    scans[key].data = null
    scans[key].error = null
  })
  
  scanState.isScanning = false
  scanState.currentScan = ''
  scanState.progress = 0
  scanState.results = null
  scanState.error = null
}

export function useScanner() {
  return {
    scanState,
    scans,
    scanConfigs,
    runSingleScan,
    runAllScans,
    resetScans
  }
}
