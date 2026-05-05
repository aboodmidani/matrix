import re
import json
import socket
import logging
from typing import Dict, Any
from tools import check_tool, run_command

logger = logging.getLogger(__name__)


def run_dnsrecon(domain: str) -> Dict[str, Any]:
    """Run DNS recon using dnsrecon CLI. Falls back to socket-based lookup."""
    if check_tool('dnsrecon'):
        return _dnsrecon_scan(domain)
    return _socket_lookup(domain)


def _dnsrecon_scan(domain: str) -> Dict[str, Any]:
    # Try JSON output first (more reliable parsing)
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

    # Fallback to text output parsing
    success, stdout, stderr = run_command(
        ['dnsrecon', '-d', domain, '-t', 'std'],
        timeout=60
    )
    if success and stdout:
        return _parse_text_output(stdout, domain)

    logger.warning("dnsrecon failed for %s, falling back to socket lookup", domain)
    return _socket_lookup(domain)


def _parse_json_output(text: str, domain: str) -> Dict[str, Any]:
    """Parse dnsrecon JSON output."""
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
    """Parse dnsrecon text output with improved regex matching."""
    records = {
        'A': [], 'AAAA': [], 'MX': [], 'NS': [], 'TXT': [],
        'SOA': [], 'SRV': [], 'CNAME': [],
    }
    for line in text.splitlines():
        line = line.strip()

        # A records — match lines like: "A  192.168.1.1  example.com"
        if re.match(r'^A\s+', line):
            m = re.search(r'(\d{1,3}(?:\.\d{1,3}){3})', line)
            if m and not m.group(1).startswith('127.'):
                ip = m.group(1)
                if ip not in records['A']:
                    records['A'].append(ip)

        # AAAA records
        if re.match(r'^AAAA\s+', line):
            m = re.search(r'([0-9a-fA-F:]{4,}:[0-9a-fA-F:]+)', line)
            if m:
                addr = m.group(1)
                if addr not in records['AAAA']:
                    records['AAAA'].append(addr)

        # MX records — "MX  10  mail.example.com"
        if re.match(r'^MX\s+', line):
            m = re.search(r'MX\s+(\d+)\s+([\w.-]+\.\w{2,})', line)
            if m:
                priority = m.group(1)
                host = m.group(2)
                entry = f"{priority} {host}"
                if entry not in records['MX']:
                    records['MX'].append(entry)

        # NS records
        if re.match(r'^NS\s+', line):
            m = re.search(r'NS\s+([\w.-]+\.\w{2,})', line)
            if m:
                host = m.group(1).rstrip('.')
                if host not in records['NS'] and host != domain:
                    records['NS'].append(host)

        # TXT records
        if re.match(r'^TXT\s+', line):
            m = re.search(r'"([^"]+)"', line)
            if m:
                txt = m.group(1)
                if txt not in records['TXT']:
                    records['TXT'].append(txt)

        # SOA records
        if re.match(r'^SOA\s+', line):
            m = re.search(r'SOA\s+([\w.-]+\.\w{2,})', line)
            if m:
                host = m.group(1).rstrip('.')
                if host not in records['SOA']:
                    records['SOA'].append(host)

        # SRV records
        if re.match(r'^SRV\s+', line):
            m = re.search(r'SRV\s+\d+\s+\d+\s+\d+\s+([\w.-]+\.\w{2,})', line)
            if m:
                host = m.group(1)
                if host not in records['SRV']:
                    records['SRV'].append(host)

        # CNAME records
        if re.match(r'^CNAME\s+', line):
            m = re.search(r'CNAME\s+([\w.-]+\.\w{2,})', line)
            if m:
                host = m.group(1)
                if host not in records['CNAME']:
                    records['CNAME'].append(host)

    return {'records': records}


def _socket_lookup(domain: str) -> Dict[str, Any]:
    """Fallback using socket + dnspython if available."""
    records = {
        'A': [], 'AAAA': [], 'MX': [], 'NS': [], 'TXT': [],
        'SOA': [], 'SRV': [], 'CNAME': [],
    }

    # A records
    try:
        _, _, ips = socket.gethostbyname_ex(domain)
        for addr in ips:
            if addr not in records['A']:
                records['A'].append(addr)
    except Exception as e:
        logger.debug("Socket A record lookup failed for %s: %s", domain, e)

    # Try to get more records via dnspython if available
    try:
        import dns.resolver
        resolver = dns.resolver.Resolver()
        resolver.timeout = 5
        resolver.lifetime = 10

        for rtype in ['MX', 'NS', 'TXT', 'SOA', 'SRV', 'CNAME']:
            try:
                answers = resolver.resolve(domain, rtype)
                for rdata in answers:
                    entry = str(rdata).rstrip('.')
                    if entry not in records[rtype]:
                        records[rtype].append(entry)
            except Exception:
                pass
    except ImportError:
        logger.debug("dnspython not available, limited DNS fallback")

    return {'records': records}
