import re
import socket
from typing import Dict, Any
from tools import check_tool, run_command


def run_dnsrecon(domain: str) -> Dict[str, Any]:
    """Run DNS recon using dnsrecon CLI. Falls back to socket-based lookup."""
    if check_tool('dnsrecon'):
        return _dnsrecon_scan(domain)
    return _socket_lookup(domain)


def _dnsrecon_scan(domain: str) -> Dict[str, Any]:
    success, stdout, stderr = run_command(
        ['dnsrecon', '-d', domain, '-t', 'std'],
        timeout=60
    )
    if success and stdout:
        return _parse_output(stdout, domain)
    return _socket_lookup(domain)


def _parse_output(text: str, domain: str) -> Dict[str, Any]:
    records = {
        'A': [], 'AAAA': [], 'MX': [], 'NS': [], 'TXT': []
    }
    for line in text.splitlines():
        line = line.strip()

        # A records — IPv4
        if re.search(r'\bA\b', line):
            m = re.search(r'(\d{1,3}(?:\.\d{1,3}){3})', line)
            if m and not m.group(1).startswith('127.'):
                ip = m.group(1)
                if ip not in records['A']:
                    records['A'].append(ip)

        # AAAA records — IPv6
        if 'AAAA' in line:
            m = re.search(r'([0-9a-fA-F:]{4,}:[0-9a-fA-F:]+)', line)
            if m:
                addr = m.group(1)
                if addr not in records['AAAA']:
                    records['AAAA'].append(addr)

        # MX records
        if 'MX' in line:
            m = re.search(r'([\w.-]+\.\w{2,})', line)
            if m:
                host = m.group(1)
                if host not in records['MX']:
                    records['MX'].append(host)

        # NS records
        if re.search(r'\bNS\b', line):
            m = re.search(r'([\w.-]+\.\w{2,})', line)
            if m:
                host = m.group(1)
                if host not in records['NS'] and host != domain:
                    records['NS'].append(host)

        # TXT records
        if 'TXT' in line:
            m = re.search(r'"([^"]+)"', line)
            if m:
                txt = m.group(1)
                if txt not in records['TXT']:
                    records['TXT'].append(txt)

    return {'records': records}


def _socket_lookup(domain: str) -> Dict[str, Any]:
    """Minimal fallback using socket."""
    records = {'A': [], 'AAAA': [], 'MX': [], 'NS': [], 'TXT': []}
    try:
        ip = socket.gethostbyname(domain)
        if ip:
            records['A'].append(ip)
        # gethostbyname_ex may return multiple IPs
        _, _, ips = socket.gethostbyname_ex(domain)
        for addr in ips:
            if addr not in records['A']:
                records['A'].append(addr)
    except Exception:
        pass
    return {'records': records}
