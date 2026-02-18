import re
import socket
from typing import List, Dict, Any
from tools import check_tool, run_command

# Ports to scan — common services
PORTS = [
    21, 22, 23, 25, 53, 80, 110, 143, 443,
    465, 587, 993, 995, 3306, 5432, 6379,
    8080, 8443, 8888, 9200, 27017,
]

PORT_SERVICES = {
    21: 'ftp',       22: 'ssh',       23: 'telnet',
    25: 'smtp',      53: 'dns',       80: 'http',
    110: 'pop3',     143: 'imap',     443: 'https',
    465: 'smtps',    587: 'smtp',     993: 'imaps',
    995: 'pop3s',    3306: 'mysql',   5432: 'postgresql',
    6379: 'redis',   8080: 'http-alt',8443: 'https-alt',
    8888: 'http',    9200: 'elasticsearch', 27017: 'mongodb',
}


def run_nmap_scan(domain: str) -> List[Dict[str, Any]]:
    """Scan open ports using nmap. Falls back to socket scan if unavailable."""
    if check_tool('nmap'):
        return _nmap_scan(domain)
    return _socket_scan(domain)


def _nmap_scan(domain: str) -> List[Dict[str, Any]]:
    port_list = ','.join(str(p) for p in PORTS)
    # -sT  : TCP connect scan (works without root, unlike -sS SYN scan)
    # -sV  : version detection
    # --version-intensity 2 : fast version probe
    # --open : only show open ports
    # -T4  : aggressive timing (faster)
    success, stdout, stderr = run_command(
        [
            'nmap', '-sT', '-sV',
            '--version-intensity', '2',
            '-T4',
            '-p', port_list,
            '--open',
            domain,
        ],
        timeout=90
    )
    if success and stdout:
        result = _parse_nmap_output(stdout)
        if result:
            return result
    # nmap ran but found nothing or failed — fall back to socket
    return _socket_scan(domain)


def _parse_nmap_output(output: str) -> List[Dict[str, Any]]:
    """Parse nmap output into structured port list.
    Handles both port lines and script output lines (|_http-title, ssl-cert, etc.)
    """
    ports = []
    current = None

    for line in output.splitlines():
        # Main port line: 80/tcp   open  http    Apache httpd 2.4
        match = re.match(r'(\d+)/(tcp|udp)\s+open\s+(\S+)\s*(.*)', line)
        if match:
            current = {
                'port':     int(match.group(1)),
                'protocol': match.group(2),
                'service':  match.group(3),
                'version':  match.group(4).strip(),
                'state':    'open',
                'info':     [],
            }
            ports.append(current)
            continue

        # Script output lines: |_http-title: Example Domain
        #                      | ssl-cert: Subject: commonName=...
        if current and re.match(r'\|', line):
            info_line = re.sub(r'^\|[_\s]*', '', line).strip()
            if info_line:
                current['info'].append(info_line)

    # Flatten info into version field if version is empty
    for p in ports:
        info = p.pop('info', [])
        if info and not p['version']:
            p['version'] = info[0]
        elif info:
            # Append first useful info line to version
            first = info[0]
            if first and first not in p['version']:
                p['version'] = f"{p['version']} | {first}".strip(' |')

    return ports


def _socket_scan(domain: str) -> List[Dict[str, Any]]:
    """Fallback: basic TCP connect scan using sockets."""
    host = domain.lstrip('www.') if domain.startswith('www.') else domain
    results = []
    for port in PORTS:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        try:
            if sock.connect_ex((host, port)) == 0:
                results.append({
                    'port':     port,
                    'protocol': 'tcp',
                    'service':  PORT_SERVICES.get(port, 'unknown'),
                    'version':  '',
                    'state':    'open',
                })
        except Exception:
            pass
        finally:
            sock.close()
    return results
