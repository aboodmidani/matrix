import re
import socket
from typing import List, Dict, Any
from tools import check_tool, run_command

# Common ports to scan
PORTS = [21, 22, 23, 25, 53, 80, 110, 143, 443, 993, 995, 3306, 5432, 8080, 8443]

PORT_SERVICES = {
    21: 'ftp', 22: 'ssh', 23: 'telnet', 25: 'smtp',
    53: 'dns', 80: 'http', 110: 'pop3', 143: 'imap',
    443: 'https', 993: 'imaps', 995: 'pop3s',
    3306: 'mysql', 5432: 'postgresql',
    8080: 'http-alt', 8443: 'https-alt',
}


def run_nmap_scan(domain: str) -> List[Dict[str, Any]]:
    """Scan open ports using nmap. Falls back to socket scan if nmap is unavailable."""
    if check_tool('nmap'):
        return _nmap_scan(domain)
    return _socket_scan(domain)


def _nmap_scan(domain: str) -> List[Dict[str, Any]]:
    port_list = ','.join(str(p) for p in PORTS)
    success, stdout, stderr = run_command(
        ['nmap', '-sV', '--version-intensity', '2', '-p', port_list, '--open', domain],
        timeout=60
    )
    if success and stdout:
        return _parse_nmap_output(stdout)
    # nmap ran but found nothing or failed — fall back to socket
    return _socket_scan(domain)


def _parse_nmap_output(output: str) -> List[Dict[str, Any]]:
    ports = []
    for line in output.splitlines():
        # Match lines like: 80/tcp   open  http    Apache httpd 2.4
        match = re.match(r'(\d+)/(tcp|udp)\s+open\s+(\S+)\s*(.*)', line)
        if match:
            ports.append({
                'port': int(match.group(1)),
                'protocol': match.group(2),
                'service': match.group(3),
                'version': match.group(4).strip(),
                'state': 'open',
            })
    return ports


def _socket_scan(domain: str) -> List[Dict[str, Any]]:
    """Fallback: basic TCP connect scan using sockets."""
    # Strip www. for resolution
    host = domain.lstrip('www.') if domain.startswith('www.') else domain
    ports = []
    for port in PORTS:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        try:
            if sock.connect_ex((host, port)) == 0:
                ports.append({
                    'port': port,
                    'protocol': 'tcp',
                    'service': PORT_SERVICES.get(port, 'unknown'),
                    'version': '',
                    'state': 'open',
                })
        except Exception:
            pass
        finally:
            sock.close()
    return ports
