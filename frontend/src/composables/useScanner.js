import { reactive } from 'vue'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

// ── State ─────────────────────────────────────────────────────────────────────

export const scanState = reactive({
  isScanning:  false,
  isStopped:   false,
  currentScan: '',
  progress:    0,
  done:        false,
  completed:   0,
  total:       0,
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
  dns:        { label: 'DNS Reconnaissance',  endpoint: '/scan/dns',          icon: '🌐', color: 'blue'   },
  ports:      { label: 'Port Scan (nmap)',     endpoint: '/scan/ports',        icon: '🔌', color: 'yellow' },
  firewall:   { label: 'Firewall / WAF',       endpoint: '/scan/firewall',     icon: '🛡️', color: 'red'    },
  technology: { label: 'Technologies',         endpoint: '/scan/technologies', icon: '🔧', color: 'purple' },
  subdomains: { label: 'Subdomain Discovery',  endpoint: '/scan/subdomains',   icon: '🔍', color: 'green'  },
}

// ── Abort controller (stop scan) ──────────────────────────────────────────────

let _abortController = null

// ── Internal helpers ──────────────────────────────────────────────────────────

function updateCurrentScan() {
  const running = Object.entries(scans)
    .filter(([, s]) => s.status === 'scanning')
    .map(([key]) => SCAN_CONFIGS[key].label)
  scanState.currentScan = running.length > 0 ? running.join(' · ') : ''
}

function updateProgress() {
  const keys    = Object.keys(SCAN_CONFIGS)
  const done    = keys.filter(k => scans[k].status === 'done' || scans[k].status === 'error').length
  const scanning = keys.filter(k => scans[k].status === 'scanning').length
  scanState.completed = done
  scanState.total     = keys.length
  const base  = (done / keys.length) * 100
  const bonus = scanning > 0 ? (1 / keys.length) * 30 : 0
  scanState.progress = Math.min(99, Math.round(base + bonus))
}

async function _runScan(key, url, signal) {
  // Skip if already aborted before this scan starts
  if (signal.aborted) {
    scans[key].status = 'error'
    scans[key].error  = 'Scan stopped by user'
    updateCurrentScan()
    updateProgress()
    return
  }

  scans[key].status = 'scanning'
  scans[key].data   = null
  scans[key].error  = null
  updateCurrentScan()
  updateProgress()

  try {
    const body = new URLSearchParams({ url })
    const res  = await fetch(`${API_URL}${SCAN_CONFIGS[key].endpoint}`, {
      method:  'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body,
      signal,
    })
    const json = await res.json()
    if (!res.ok) throw new Error(json.detail || `HTTP ${res.status}`)
    scans[key].data   = json
    scans[key].status = 'done'
  } catch (err) {
    if (err.name === 'AbortError') {
      scans[key].status = 'error'
      scans[key].error  = 'Stopped'
    } else {
      scans[key].error  = err.message
      scans[key].status = 'error'
    }
  }

  updateCurrentScan()
  updateProgress()
}

// ── Public API ────────────────────────────────────────────────────────────────

export async function runAllScans(url) {
  _abortController = new AbortController()
  const signal = _abortController.signal

  scanState.isScanning  = true
  scanState.isStopped   = false
  scanState.progress    = 0
  scanState.done        = false
  scanState.completed   = 0
  scanState.total       = Object.keys(SCAN_CONFIGS).length
  scanState.currentScan = 'Initializing…'

  for (const key of Object.keys(scans)) {
    scans[key].status = 'idle'
    scans[key].data   = null
    scans[key].error  = null
  }

  await Promise.all(
    Object.keys(SCAN_CONFIGS).map(key => _runScan(key, url, signal))
  )

  scanState.isScanning  = false
  scanState.currentScan = ''
  scanState.progress    = scanState.isStopped ? scanState.progress : 100
  scanState.done        = true
}

export function stopScans() {
  if (_abortController) {
    _abortController.abort()
    _abortController = null
  }
  scanState.isStopped   = true
  scanState.isScanning  = false
  scanState.currentScan = 'Stopped'
}

export function resetScans() {
  if (_abortController) {
    _abortController.abort()
    _abortController = null
  }
  for (const key of Object.keys(scans)) {
    scans[key].status = 'idle'
    scans[key].data   = null
    scans[key].error  = null
  }
  scanState.isScanning  = false
  scanState.isStopped   = false
  scanState.currentScan = ''
  scanState.progress    = 0
  scanState.done        = false
  scanState.completed   = 0
  scanState.total       = 0
}
