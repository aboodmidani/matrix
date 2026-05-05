import re
import socket
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict, Any
from tools import check_tool, run_command

logger = logging.getLogger(__name__)

# Ports to scan — common services + critical attack surface
PORTS = [
    21, 22, 23, 25, 53, 80, 110, 143, 443,
    445, 465, 587, 993, 995, 1433, 1521,
    2049, 2375, 2376, 3306, 3389, 5432, 5900,
    6379, 6443, 8000, 8080, 8443, 8888,
    9200, 9443, 11211, 27017, 27018, 50000,
]

PORT_SERVICES = {
    21: 'ftp',        22: 'ssh',         23: 'telnet',
    25: 'smtp',       53: 'dns',         80: 'http',
    110: 'pop3',      143: 'imap',       443: 'https',
    445: 'smb',       465: 'smtps',      587: 'smtp',
    993: 'imaps',     995: 'pop3s',      1433: 'mssql',
    1521: 'oracle',   2049: 'nfs',       2375: 'docker',
    2376: 'docker-tls', 3306: 'mysql',   3389: 'rdp',
    5432: 'postgresql', 5900: 'vnc',     6379: 'redis',
    6443: 'k8s-api',  8000: 'http-alt',  8080: 'http-proxy',
    8443: 'https-alt', 8888: 'http',     9200: 'elasticsearch',
    9443: 'https-alt', 11211: 'memcached', 27017: 'mongodb',
    27018: 'mongodb',  50000: 'sap-jenkins',
}


def run_nmap_scan(domain: str) -> List[Dict[str, Any]]:
    """Scan open ports using nmap. Falls back to socket scan if unavailable."""
    if check_tool('nmap'):
        return _nmap_scan(domain)
    return _socket_scan(domain)


def _nmap_scan(domain: str) -> List[Dict[str, Any]]:
    port_list = ','.join(str(p) for p in PORTS)
    # -sT  : TCP connect scan (works without root)
    # -sV  : version detection
    # --version-intensity 5 : better accuracy than 2
    # --open : only show open ports
    # -T4  : aggressive timing
    success, stdout, stderr = run_command(
        [
            'nmap', '-sT', '-sV',
            '--version-intensity', '5',
            '-T4',
            '-p', port_list,
            '--open',
            domain,
        ],
        timeout=120
    )
    if success and stdout:
        result = _parse_nmap_output(stdout)
        if result:
            return result
    # nmap ran but found nothing or failed — fall back to socket
    logger.warning("nmap returned no results for %s, falling back to socket scan", domain)
    return _socket_scan(domain)


def _parse_nmap_output(output: str) -> List[Dict[str, Any]]:
    """Parse nmap output into structured port list."""
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
            first = info[0]
            if first and first not in p['version']:
                p['version'] = f"{p['version']} | {first}".strip(' |')

    return ports


def _check_port(host: str, port: int) -> Dict[str, Any] | None:
    """Check if a single port is open. Returns port info or None."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(2)
    try:
        if sock.connect_ex((host, port)) == 0:
            return {
                'port':     port,
                'protocol': 'tcp',
                'service':  PORT_SERVICES.get(port, 'unknown'),
                'version':  '',
                'state':    'open',
            }
    except Exception as e:
        logger.debug("Port %d check error: %s", port, e)
    finally:
        sock.close()
    return None


def _socket_scan(domain: str) -> List[Dict[str, Any]]:
    """Fallback: parallel TCP connect scan using sockets."""
    host = domain.removeprefix('www.') if domain.startswith('www.') else domain
    results = []

    with ThreadPoolExecutor(max_workers=20) as executor:
        futures = {
            executor.submit(_check_port, host, port): port
            for port in PORTS
        }
        for future in as_completed(futures, timeout=30):
            try:
                result = future.result()
                if result:
                    results.append(result)
            except Exception as e:
                logger.debug("Socket scan error: %s", e)

    results.sort(key=lambda x: x['port'])
    return results
