import { reactive } from 'vue'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'
const STORAGE_KEY = 'matrix-scanner-state'

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
  live:       { status: 'idle', data: null, error: null },
  ssl:        { status: 'idle', data: null, error: null },
  headers:    { status: 'idle', data: null, error: null },
  crawl:      { status: 'idle', data: null, error: null },
  directories:{ status: 'idle', data: null, error: null },
  dnsExtended:{ status: 'idle', data: null, error: null },
})

export const SCAN_CONFIGS = {
  dns:        { label: 'DNS Reconnaissance',    endpoint: '/scan/dns',          icon: 'A', color: 'blue'   },
  ports:      { label: 'Port Scan',              endpoint: '/scan/ports',        icon: 'P', color: 'yellow' },
  firewall:   { label: 'Firewall / WAF',         endpoint: '/scan/firewall',     icon: 'F', color: 'red'    },
  technology: { label: 'Fingerprinting',         endpoint: '/scan/technologies', icon: 'T', color: 'purple' },
  subdomains: { label: 'Subdomain Discovery',    endpoint: '/scan/subdomains',   icon: 'S', color: 'green'  },
  live:       { label: 'Live Status',            endpoint: '/scan/live',         icon: 'L', color: 'cyan'   },
  ssl:        { label: 'SSL/TLS Certificate',    endpoint: '/scan/ssl',          icon: 'Z', color: 'yellow' },
  headers:    { label: 'Security Headers',        endpoint: '/scan/headers',     icon: 'H', color: 'blue'   },
  crawl:      { label: 'Web Crawl',              endpoint: '/scan/crawl',        icon: 'C', color: 'purple' },
  directories:{ label: 'Directory Scan',          endpoint: '/scan/directories', icon: 'D', color: 'red'    },
  dnsExtended:{ label: 'DNS Extended (CAA/PTR)',  endpoint: '/scan/dns-extended',icon: 'X', color: 'green'  },
}

let _abortController = null

function updateCurrentScan() {
  const running = Object.entries(scans)
    .filter(([, s]) => s.status === 'scanning')
    .map(([key]) => SCAN_CONFIGS[key].label)
  scanState.currentScan = running.length > 0 ? running.join(' · ') : ''
}

function updateProgress() {
  const keys   = Object.keys(SCAN_CONFIGS)
  const done    = keys.filter(k => scans[k].status === 'done' || scans[k].status === 'error').length
  const scanning = keys.filter(k => scans[k].status === 'scanning').length
  scanState.completed = done
  scanState.total     = keys.length
  const base  = (done / keys.length) * 100
  const bonus = scanning > 0 ? (1 / keys.length) * 30 : 0
  scanState.progress = Math.min(99, Math.round(base + bonus))
}

async function _runScan(key, url, signal) {
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

  const SCAN_TIMEOUT = 120000

  try {
    const body = new URLSearchParams({ url })
    const timeoutPromise = new Promise((_, reject) => {
      setTimeout(() => reject(new Error('Scan timed out (120s)')), SCAN_TIMEOUT)
    })
    const fetchPromise = fetch(`${API_URL}${SCAN_CONFIGS[key].endpoint}`, {
      method:  'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body,
      signal,
    })
    const res = await Promise.race([fetchPromise, timeoutPromise])
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
  _saveState(url)
}

export async function runSingleScan(key, url) {
  if (!_abortController) {
    _abortController = new AbortController()
  }
  const signal = _abortController.signal

  scanState.isScanning = true
  scanState.done       = false
  scanState.total      = Object.keys(SCAN_CONFIGS).length

  await _runScan(key, url, signal)

  const allDone = Object.keys(SCAN_CONFIGS).every(
    k => scans[k].status === 'done' || scans[k].status === 'error'
  )
  if (allDone) {
    scanState.isScanning = false
    scanState.done       = true
    scanState.progress   = 100
  }
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
  _clearSavedState()
}

function _saveState(url) {
  try {
    const saved = {
      url,
      timestamp: Date.now(),
      scans: {},
    }
    for (const key of Object.keys(scans)) {
      if (scans[key].status === 'done') {
        saved.scans[key] = { status: 'done', data: scans[key].data }
      }
    }
    localStorage.setItem(STORAGE_KEY, JSON.stringify(saved))
  } catch {
    // localStorage may be full or unavailable
  }
}

function _clearSavedState() {
  try {
    localStorage.removeItem(STORAGE_KEY)
  } catch {
    // ignore
  }
}

export function getSavedState() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY)
    if (!raw) return null
    const saved = JSON.parse(raw)
    if (Date.now() - saved.timestamp > 3600000) {
      _clearSavedState()
      return null
    }
    return saved
  } catch {
    return null
  }
}

export function restoreSavedScans(saved) {
  if (!saved || !saved.scans) return
  for (const [key, data] of Object.entries(saved.scans)) {
    if (scans[key]) {
      scans[key].status = data.status
      scans[key].data = data.data
    }
  }
  scanState.done = true
  scanState.progress = 100
  scanState.completed = Object.keys(saved.scans).length
  scanState.total = Object.keys(SCAN_CONFIGS).length
}
