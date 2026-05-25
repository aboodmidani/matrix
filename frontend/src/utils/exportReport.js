export function exportTxt(targetUrl, scans, SCAN_CONFIGS) {
  const now  = new Date()
  const date = now.toISOString().replace('T', ' ').slice(0, 19) + ' UTC'
  const sep  = '='.repeat(60)
  const thin = '-'.repeat(60)

  const lines = []

  lines.push(sep)
  lines.push('  MATRIX SCANNER — SECURITY ASSESSMENT REPORT')
  lines.push(sep)
  lines.push(`  Target  : ${targetUrl}`)
  lines.push(`  Date    : ${date}`)
  lines.push(`  Tool    : Matrix Scanner v2.0.0`)
  lines.push(sep)
  lines.push('')

  function section(title, key, fn) {
    lines.push(`[ ${title} ]`)
    lines.push(thin)
    const s = scans[key]
    if (s.status === 'done' && s.data) {
      fn(s.data)
    } else if (s.status === 'error') {
      lines.push(`  ERROR: ${s.error}`)
    } else {
      lines.push('  Not scanned.')
    }
    lines.push('')
  }

  function fmt(data) {
    return data !== null && data !== undefined ? String(data) : '--'
  }

  section('DNS RECONNAISSANCE', 'dns', (data) => {
    const rec = data.records
    if (!rec) { lines.push('  No DNS records found.'); return }
    const types = ['A', 'AAAA', 'MX', 'NS', 'TXT', 'SOA', 'SRV', 'CNAME']
    let any = false
    for (const t of types) {
      if (rec[t] && rec[t].length) {
        any = true
        lines.push(`  ${t} Records:`)
        for (const r of rec[t]) lines.push(`    . ${r}`)
      }
    }
    if (!any) lines.push('  No DNS records found.')
  })

  section('PORT SCAN', 'ports', (data) => {
    if (data.ports && data.ports.length) {
      lines.push(`  ${data.ports.length} open port(s) detected:`)
      lines.push(`  ${'PORT'.padEnd(8)} ${'PROTO'.padEnd(8)} ${'SERVICE'.padEnd(16)} VERSION`)
      lines.push(`  ${'-'.repeat(50)}`)
      for (const p of data.ports) {
        lines.push(`  ${String(p.port).padEnd(8)} ${(p.protocol || '').padEnd(8)} ${(p.service || '').padEnd(16)} ${p.version || '--'}`)
      }
    } else {
      lines.push('  No open ports found on scanned range.')
    }
  })

  section('FIREWALL / WAF DETECTION', 'firewall', (data) => {
    const f = data.firewall
    if (f) {
      lines.push(`  Detected   : ${f.detected ? 'YES' : 'NO'}`)
      lines.push(`  WAF Name   : ${f.waf_name || '--'}`)
      if (f.manufacturer && f.manufacturer !== f.waf_name) {
        lines.push(`  Vendor     : ${f.manufacturer}`)
      }
      lines.push(`  Confidence : ${f.confidence || '--'}`)
    }
  })

  section('TECHNOLOGIES', 'technology', (data) => {
    const techs = data.technologies
    if (techs && Object.keys(techs).length) {
      lines.push(`  ${Object.keys(techs).length} technology/technologies identified:`)
      for (const [name, info] of Object.entries(techs)) {
        let line = `    . ${name}`
        if (info.version) line += ` v${info.version}`
        if (info.confidence) line += ` (${info.confidence}% confidence)`
        lines.push(line)
      }
    } else {
      lines.push('  No technologies detected.')
    }
  })

  section('SUBDOMAIN DISCOVERY', 'subdomains', (data) => {
    if (data.subdomains && data.subdomains.length) {
      lines.push(`  ${data.subdomains.length} subdomain(s) discovered:`)
      for (const s of data.subdomains) {
        lines.push(`    . ${s.subdomain}`)
      }
    } else {
      lines.push('  No subdomains discovered.')
    }
  })

  section('LIVE STATUS', 'live', (data) => {
    const l = data.live
    if (l) {
      lines.push(`  Alive       : ${l.alive ? 'YES' : 'NO'}`)
      lines.push(`  Ping Time   : ${fmt(l.ping_time_ms)} ms`)
      lines.push(`  HTTP Status : ${fmt(l.http_status)}`)
    }
  })

  section('SSL / TLS CERTIFICATE', 'ssl', (data) => {
    const s = data.ssl
    if (s && s.certificate) {
      const c = s.certificate
      lines.push(`  Subject     : ${fmt(c.subject)}`)
      lines.push(`  Issuer      : ${fmt(c.issuer)}`)
      lines.push(`  Serial      : ${fmt(c.serial)}`)
      lines.push(`  Not Before  : ${fmt(c.not_before)}`)
      lines.push(`  Not After   : ${fmt(c.not_after)}`)
      lines.push(`  Days Left   : ${fmt(c.days_remaining)}`)
      lines.push(`  Expired     : ${c.expired ? 'YES' : 'NO'}`)
      if (c.san && c.san.length) lines.push(`  SAN Count   : ${c.san.length}`)
    }
  })

  section('SECURITY HEADERS', 'headers', (data) => {
    const h = data.headers
    if (h) {
      lines.push(`  Total headers         : ${fmt(h.total_headers)}`)
      lines.push(`  Security headers found: ${fmt(h.security_headers_found)}/${fmt(h.security_headers_total)}`)
      if (h.missing_security_headers && h.missing_security_headers.length) {
        lines.push(`  Missing:`)
        for (const m of h.missing_security_headers) lines.push(`    . ${m}`)
      }
    }
  })

  section('WEB CRAWL', 'crawl', (data) => {
    const c = data.crawl
    if (c) {
      lines.push(`  URLs found   : ${fmt(c.urls ? c.urls.length : 0)}`)
      lines.push(`  Links found  : ${fmt(c.links ? c.links.length : 0)}`)
      lines.push(`  JS files     : ${fmt(c.js_files ? c.js_files.length : 0)}`)
      lines.push(`  Forms        : ${fmt(c.forms ? c.forms.length : 0)}`)
      lines.push(`  Emails       : ${fmt(c.emails ? c.emails.length : 0)}`)
      lines.push(`  Comments     : ${fmt(c.comments ? c.comments.length : 0)}`)
    }
  })

  section('DIRECTORY SCAN', 'directories', (data) => {
    const d = data.directories
    if (d) {
      lines.push(`  Paths scanned : ${fmt(d.total_scanned)}`)
      lines.push(`  Paths found   : ${fmt(d.found ? d.found.length : 0)}`)
      if (d.found && d.found.length) {
        for (const f of d.found) {
          lines.push(`    . ${f.path} (${f.status})`)
        }
      }
    }
  })

  section('DNS EXTENDED (CAA / PTR)', 'dnsExtended', (data) => {
    const x = data.dns_extended
    if (x) {
      lines.push(`  CAA Records   : ${x.caa_records && x.caa_records.length ? x.caa_records.join(', ') : 'None'}`)
      lines.push(`  DNSSEC        : ${fmt(x.dnssec)}`)
      lines.push(`  Zone Transfer : ${fmt(x.zone_transfer)}`)
    }
  })

  lines.push(sep)
  lines.push('  FOR AUTHORIZED USE ONLY -- Matrix Scanner')
  lines.push(sep)

  const content  = lines.join('\n')
  const blob     = new Blob([content], { type: 'text/plain;charset=utf-8' })
  const url      = URL.createObjectURL(blob)
  const a        = document.createElement('a')
  const filename = `matrix-scan_${targetUrl.replace(/https?:\/\//, '').replace(/[^a-z0-9]/gi, '_')}_${now.toISOString().slice(0,10)}.txt`
  a.href         = url
  a.download     = filename
  a.click()
  URL.revokeObjectURL(url)
}

export function exportJson(targetUrl, scans, SCAN_CONFIGS) {
  const now = new Date()
  const report = {
    tool: 'Matrix Scanner',
    version: '2.0.0',
    target: targetUrl,
    timestamp: now.toISOString(),
    scans: {},
  }

  for (const [key, cfg] of Object.entries(SCAN_CONFIGS)) {
    const scan = scans[key]
    report.scans[key] = {
      label: cfg.label,
      status: scan.status,
      data: scan.status === 'done' ? scan.data : null,
      error: scan.status === 'error' ? scan.error : null,
    }
  }

  const blob = new Blob([JSON.stringify(report, null, 2)], { type: 'application/json' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  const filename = `matrix-scan_${targetUrl.replace(/https?:\/\//, '').replace(/[^a-z0-9]/gi, '_')}_${now.toISOString().slice(0,10)}.json`
  a.href = url
  a.download = filename
  a.click()
  URL.revokeObjectURL(url)
}

export async function copyToClipboard(text) {
  try {
    await navigator.clipboard.writeText(text)
    return true
  } catch {
    const textarea = document.createElement('textarea')
    textarea.value = text
    textarea.style.position = 'fixed'
    textarea.style.opacity = '0'
    document.body.appendChild(textarea)
    textarea.select()
    try {
      document.execCommand('copy')
      return true
    } catch {
      return false
    } finally {
      document.body.removeChild(textarea)
    }
  }
}
