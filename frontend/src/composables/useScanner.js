import { reactive } from 'vue'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

// ── State ─────────────────────────────────────────────────────────────────────

export const scanState = reactive({
  isScanning: false,
  currentScan: '',
  progress: 0,
  done: false,
})

export const scans = reactive({
  dns:        { status: 'idle', data: null, error: null },
  ports:      { status: 'idle', data: null, error: null },
  firewall:   { status: 'idle', data: null, error: null },
  technology: { status: 'idle', data: null, error: null },
  subdomains: { status: 'idle', data: null, error: null },
})

// ── Config ────────────────────────────────────────────────────────────────────

export const SCAN_CONFIGS = {
  dns:        { label: 'DNS Reconnaissance',   endpoint: '/scan/dns',          icon: '🌐', color: 'blue'   },
  ports:      { label: 'Port Scan (nmap)',      endpoint: '/scan/ports',        icon: '🔌', color: 'yellow' },
  firewall:   { label: 'Firewall / WAF',        endpoint: '/scan/firewall',     icon: '🛡️', color: 'red'    },
  technology: { label: 'Technologies',          endpoint: '/scan/technologies', icon: '🔧', color: 'purple' },
  subdomains: { label: 'Subdomain Discovery',   endpoint: '/scan/subdomains',   icon: '🔍', color: 'green'  },
}

// ── Internal helpers ──────────────────────────────────────────────────────────

async function _runScan(key, url) {
  const cfg = SCAN_CONFIGS[key]
  scans[key].status = 'scanning'
  scans[key].data   = null
  scans[key].error  = null
  scanState.currentScan = cfg.label

  try {
    const body = new URLSearchParams({ url })
    const res = await fetch(`${API_URL}${cfg.endpoint}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body,
    })
    const json = await res.json()
    if (!res.ok) throw new Error(json.detail || `HTTP ${res.status}`)
    scans[key].data   = json
    scans[key].status = 'done'
  } catch (err) {
    scans[key].error  = err.message
    scans[key].status = 'error'
  }
}

// ── Public API ────────────────────────────────────────────────────────────────

export async function runAllScans(url) {
  // Reset
  scanState.isScanning = true
  scanState.progress   = 0
  scanState.done       = false
  for (const key of Object.keys(scans)) {
    scans[key].status = 'idle'
    scans[key].data   = null
    scans[key].error  = null
  }

  const keys = Object.keys(SCAN_CONFIGS)
  let completed = 0

  // Run all scans in parallel
  await Promise.all(
    keys.map(async (key) => {
      await _runScan(key, url)
      completed++
      scanState.progress = Math.round((completed / keys.length) * 100)
    })
  )

  scanState.isScanning  = false
  scanState.currentScan = ''
  scanState.progress    = 100
  scanState.done        = true
}

export function resetScans() {
  for (const key of Object.keys(scans)) {
    scans[key].status = 'idle'
    scans[key].data   = null
    scans[key].error  = null
  }
  scanState.isScanning  = false
  scanState.currentScan = ''
  scanState.progress    = 0
  scanState.done        = false
}
