/**
 * Generate and download a plain-text scan report.
 * @param {string} targetUrl  - The scanned URL
 * @param {object} scans      - The reactive scans object from useScanner
 * @param {object} SCAN_CONFIGS - The scan config map
 */
export function exportTxt(targetUrl, scans, SCAN_CONFIGS) {
  const now  = new Date()
  const date = now.toISOString().replace('T', ' ').slice(0, 19) + ' UTC'
  const sep  = '═'.repeat(60)
  const thin = '─'.repeat(60)

  const lines = []

  lines.push(sep)
  lines.push('  MATRIX SCANNER — SECURITY ASSESSMENT REPORT')
  lines.push(sep)
  lines.push(`  Target  : ${targetUrl}`)
  lines.push(`  Date    : ${date}`)
  lines.push(`  Tool    : Matrix Scanner v1.0.0`)
  lines.push(sep)
  lines.push('')

  // ── DNS ──────────────────────────────────────────────────────────────────
  lines.push('[ DNS RECONNAISSANCE ]')
  lines.push(thin)
  const dns = scans.dns
  if (dns.status === 'done' && dns.data?.records) {
    const rec = dns.data.records
    const types = ['A', 'AAAA', 'MX', 'NS', 'TXT']
    let any = false
    for (const t of types) {
      if (rec[t] && rec[t].length) {
        any = true
        lines.push(`  ${t} Records:`)
        for (const r of rec[t]) lines.push(`    • ${r}`)
      }
    }
    if (!any) lines.push('  No DNS records found.')
  } else if (dns.status === 'error') {
    lines.push(`  ERROR: ${dns.error}`)
  } else {
    lines.push('  Not scanned.')
  }
  lines.push('')

  // ── Ports ─────────────────────────────────────────────────────────────────
  lines.push('[ PORT SCAN (nmap) ]')
  lines.push(thin)
  const ports = scans.ports
  if (ports.status === 'done' && ports.data?.ports?.length) {
    lines.push(`  ${ports.data.ports.length} open port(s) detected:`)
    lines.push(`  ${'PORT'.padEnd(8)} ${'PROTO'.padEnd(8)} ${'SERVICE'.padEnd(16)} VERSION`)
    lines.push(`  ${'─'.repeat(50)}`)
    for (const p of ports.data.ports) {
      const port    = String(p.port).padEnd(8)
      const proto   = (p.protocol || '').padEnd(8)
      const service = (p.service  || '').padEnd(16)
      const version = p.version   || '—'
      lines.push(`  ${port} ${proto} ${service} ${version}`)
    }
  } else if (ports.status === 'error') {
    lines.push(`  ERROR: ${ports.error}`)
  } else if (ports.status === 'done') {
    lines.push('  No open ports found on scanned range.')
  } else {
    lines.push('  Not scanned.')
  }
  lines.push('')

  // ── Firewall ──────────────────────────────────────────────────────────────
  lines.push('[ FIREWALL / WAF DETECTION ]')
  lines.push(thin)
  const fw = scans.firewall
  if (fw.status === 'done' && fw.data?.firewall) {
    const f = fw.data.firewall
    lines.push(`  Detected   : ${f.detected ? 'YES' : 'NO'}`)
    lines.push(`  WAF Name   : ${f.waf_name    || '—'}`)
    if (f.manufacturer && f.manufacturer !== f.waf_name) {
      lines.push(`  Vendor     : ${f.manufacturer}`)
    }
    lines.push(`  Confidence : ${f.confidence  || '—'}`)
  } else if (fw.status === 'error') {
    lines.push(`  ERROR: ${fw.error}`)
  } else {
    lines.push('  Not scanned.')
  }
  lines.push('')

  // ── Technologies ──────────────────────────────────────────────────────────
  lines.push('[ TECHNOLOGIES ]')
  lines.push(thin)
  const tech = scans.technology
  if (tech.status === 'done' && tech.data?.technologies) {
    const entries = Object.entries(tech.data.technologies)
    if (entries.length) {
      lines.push(`  ${entries.length} technology/technologies identified:`)
      for (const [name, info] of entries) {
        let line = `    • ${name}`
        if (info.version)    line += ` v${info.version}`
        if (info.confidence) line += ` (${info.confidence}% confidence)`
        lines.push(line)
      }
    } else {
      lines.push('  No technologies detected.')
    }
  } else if (tech.status === 'error') {
    lines.push(`  ERROR: ${tech.error}`)
  } else {
    lines.push('  Not scanned.')
  }
  lines.push('')

  // ── Subdomains ────────────────────────────────────────────────────────────
  lines.push('[ SUBDOMAIN DISCOVERY ]')
  lines.push(thin)
  const sub = scans.subdomains
  if (sub.status === 'done' && sub.data?.subdomains?.length) {
    lines.push(`  ${sub.data.subdomains.length} subdomain(s) discovered:`)
    for (const s of sub.data.subdomains) {
      lines.push(`    • ${s.subdomain}`)
    }
  } else if (sub.status === 'error') {
    lines.push(`  ERROR: ${sub.error}`)
  } else if (sub.status === 'done') {
    lines.push('  No subdomains discovered.')
  } else {
    lines.push('  Not scanned.')
  }
  lines.push('')

  // ── Footer ────────────────────────────────────────────────────────────────
  lines.push(sep)
  lines.push('  FOR AUTHORIZED USE ONLY — Matrix Scanner')
  lines.push(sep)

  // ── Download ──────────────────────────────────────────────────────────────
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
