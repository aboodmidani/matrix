import json
import logging
from typing import Dict, Any, List
from tools import check_tool, run_command

logger = logging.getLogger(__name__)


def run_dnsrecon(domain: str) -> Dict[str, Any]:
    if check_tool('dnsrecon'):
        return _dnsrecon_scan(domain)
    return _nslookup_fallback(domain)


def _dnsrecon_scan(domain: str) -> Dict[str, Any]:
    success, stdout, stderr = run_command(
        ['dnsrecon', '-d', domain, '-t', 'std', '--json', '/dev/stdout'],
        timeout=60
    )
    if success and stdout.strip():
        try:
            result = _parse_json_output(stdout, domain)
            if result and any(result['records'].values()):
                return result
        except (json.JSONDecodeError, KeyError):
            logger.debug("dnsrecon JSON parsing failed, trying text output")

    success, stdout, stderr = run_command(
        ['dnsrecon', '-d', domain, '-t', 'std'],
        timeout=60
    )
    if success and stdout:
        return _parse_text_output(stdout, domain)

    return {'records': {k: [] for k in ['A', 'AAAA', 'MX', 'NS', 'TXT', 'SOA', 'SRV', 'CNAME']}}


def _parse_json_output(text: str, domain: str) -> Dict[str, Any]:
    records = {
        'A': [], 'AAAA': [], 'MX': [], 'NS': [], 'TXT': [],
        'SOA': [], 'SRV': [], 'CNAME': [],
    }
    data = json.loads(text)
    for entry in data:
        rtype = entry.get('type', '')
        if rtype == 'A':
            ip = entry.get('address', '')
            if ip and ip not in records['A'] and not ip.startswith('127.'):
                records['A'].append(ip)
        elif rtype == 'AAAA':
            ip = entry.get('address', '')
            if ip and ip not in records['AAAA']:
                records['AAAA'].append(ip)
        elif rtype == 'MX':
            target = entry.get('exchange', entry.get('target', ''))
            priority = entry.get('priority', '')
            if target:
                entry_str = f"{priority} {target}".strip() if priority else target
                if entry_str not in records['MX']:
                    records['MX'].append(entry_str)
        elif rtype == 'NS':
            target = entry.get('ns', entry.get('target', ''))
            if target and target not in records['NS'] and target.rstrip('.') != domain:
                records['NS'].append(target.rstrip('.'))
        elif rtype == 'TXT':
            txt = entry.get('strings', entry.get('text', ''))
            if txt and txt not in records['TXT']:
                records['TXT'].append(txt)
        elif rtype == 'SOA':
            mname = entry.get('mname', '')
            if mname:
                records['SOA'].append(mname.rstrip('.'))
        elif rtype == 'SRV':
            target = entry.get('target', '')
            port = entry.get('port', '')
            if target:
                entry_str = f"{target}:{port}" if port else target
                if entry_str not in records['SRV']:
                    records['SRV'].append(entry_str)
        elif rtype == 'CNAME':
            target = entry.get('target', '')
            if target and target not in records['CNAME']:
                records['CNAME'].append(target.rstrip('.'))
    return {'records': records}


def _parse_text_output(text: str, domain: str) -> Dict[str, Any]:
    import re
    records = {
        'A': [], 'AAAA': [], 'MX': [], 'NS': [], 'TXT': [],
        'SOA': [], 'SRV': [], 'CNAME': [],
    }
    for line in text.splitlines():
        line = re.sub(r'^\[\*\]\s*', '', line).strip()
        if not line:
            continue
        if re.match(r'^A\s+', line):
            m = re.search(r'(\d{1,3}(?:\.\d{1,3}){3})', line)
            if m and not m.group(1).startswith('127.'):
                ip = m.group(1)
                if ip not in records['A']:
                    records['A'].append(ip)
        if re.match(r'^AAAA\s+', line):
            m = re.search(r'([0-9a-fA-F:]{4,}:[0-9a-fA-F:]+)', line)
            if m:
                addr = m.group(1)
                if addr not in records['AAAA']:
                    records['AAAA'].append(addr)
        if re.match(r'^MX\s+', line):
            m = re.search(r'MX\s+(\d+)\s+([\w.-]+\.\w{2,})', line)
            if m:
                entry = f"{m.group(1)} {m.group(2)}"
                if entry not in records['MX']:
                    records['MX'].append(entry)
        if re.match(r'^NS\s+', line):
            m = re.search(r'NS\s+([\w.-]+\.\w{2,})', line)
            if m:
                host = m.group(1).rstrip('.')
                if host not in records['NS'] and host != domain:
                    records['NS'].append(host)
        if re.match(r'^TXT\s+', line):
            m = re.search(r'"([^"]+)"', line)
            if m:
                txt = m.group(1)
                if txt not in records['TXT']:
                    records['TXT'].append(txt)
        if re.match(r'^SOA\s+', line):
            m = re.search(r'SOA\s+([\w.-]+\.\w{2,})', line)
            if m:
                host = m.group(1).rstrip('.')
                if host not in records['SOA']:
                    records['SOA'].append(host)
        if re.match(r'^SRV\s+', line):
            m = re.search(r'SRV\s+\d+\s+\d+\s+\d+\s+([\w.-]+\.\w{2,})', line)
            if m:
                host = m.group(1)
                if host not in records['SRV']:
                    records['SRV'].append(host)
        if re.match(r'^CNAME\s+', line):
            m = re.search(r'CNAME\s+([\w.-]+\.\w{2,})', line)
            if m:
                host = m.group(1)
                if host not in records['CNAME']:
                    records['CNAME'].append(host)
    return {'records': records}


def _nslookup_fallback(domain: str) -> Dict[str, Any]:
    import re
    records = {k: [] for k in ['A', 'AAAA', 'MX', 'NS', 'TXT', 'SOA', 'SRV', 'CNAME']}
    queries = [
        ('A', ['nslookup', '-type=A', domain]),
        ('AAAA', ['nslookup', '-type=AAAA', domain]),
        ('MX', ['nslookup', '-type=MX', domain]),
        ('NS', ['nslookup', '-type=NS', domain]),
        ('TXT', ['nslookup', '-type=TXT', domain]),
        ('SOA', ['nslookup', '-type=SOA', domain]),
        ('CNAME', ['nslookup', '-type=CNAME', domain]),
    ]
    for rtype, cmd in queries:
        success, stdout, _ = run_command(cmd, timeout=10)
        if not success or not stdout:
            continue
        if rtype == 'A':
            for m in re.finditer(r'Name:\s+\S+\s+Address[es]?:\s+(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', stdout):
                ip = m.group(1)
                if not ip.startswith('127.') and ip not in records['A']:
                    records['A'].append(ip)
        elif rtype == 'AAAA':
            for m in re.finditer(r'Name:\s+\S+\s+Address[es]?:\s+([0-9a-fA-F:]+)', stdout):
                addr = m.group(1)
                if addr not in records['AAAA']:
                    records['AAAA'].append(addr)
        elif rtype == 'MX':
            for line in stdout.splitlines():
                m = re.search(r'MX preference\s*=\s*(\d+),\s*mail exchanger\s*=\s*(\S+)', line, re.IGNORECASE)
                if m:
                    entry = f"{m.group(1)} {m.group(2).rstrip('.')}"
                    if entry not in records['MX']:
                        records['MX'].append(entry)
        elif rtype == 'NS':
            for m in re.finditer(r'nameserver\s*=\s*(\S+)', stdout, re.IGNORECASE):
                host = m.group(1).rstrip('.')
                if host not in records['NS'] and host != domain:
                    records['NS'].append(host)
        elif rtype == 'TXT':
            for m in re.finditer(r'"([^"]+)"', stdout):
                txt = m.group(1)
                if txt not in records['TXT']:
                    records['TXT'].append(txt)
        elif rtype == 'SOA':
            for line in stdout.splitlines():
                m = re.search(r'primary name server\s*=\s*(\S+)', line, re.IGNORECASE)
                if m:
                    host = m.group(1).rstrip('.')
                    if host not in records['SOA']:
                        records['SOA'].append(host)
        elif rtype == 'CNAME':
            for line in stdout.splitlines():
                m = re.search(r'(\S+)\s+canonical name\s*=\s*(\S+)', line, re.IGNORECASE)
                if m:
                    host = m.group(2).rstrip('.')
                    if host not in records['CNAME']:
                        records['CNAME'].append(host)
    return {'records': records, 'fallback': 'nslookup'}
