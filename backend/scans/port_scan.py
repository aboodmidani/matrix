import socket
from typing import Dict, List, Any
from tools import tool_manager

# Common ports to scan
COMMON_PORTS = [
    21,   # FTP
    22,   # SSH
    23,   # Telnet
    25,   # SMTP
    53,   # DNS
    80,   # HTTP
    110,  # POP3
    143,  # IMAP
    443,  # HTTPS
    993,  # IMAPS
    995,  # POP3S
    3306, # MySQL
    5432, # PostgreSQL
    8080, # HTTP Alt
    8443  # HTTPS Alt
]

# Service name mapping
SERVICE_NAMES = {
    21: 'ftp',
    22: 'ssh',
    23: 'telnet',
    25: 'smtp',
    53: 'dns',
    80: 'http',
    110: 'pop3',
    143: 'imap',
    443: 'https',
    993: 'imaps',
    995: 'pop3s',
    3306: 'mysql',
    5432: 'postgresql',
    8080: 'http-alt',
    8443: 'https-alt'
}

def run_nmap_scan(domain: str) -> List[Dict[str, Any]]:
    """Fast port scan using socket connections"""
    try:
        # First try to resolve the domain
        ip = socket.gethostbyname(domain)
    except socket.gaierror:
        return [{"error": f"Could not resolve domain: {domain}"}]
    
    open_ports = []
    
    for port in COMMON_PORTS:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)  # 1 second timeout per port
            result = sock.connect_ex((ip, port))
            sock.close()
            
            if result == 0:
                open_ports.append({
                    "port": port,
                    "protocol": "tcp",
                    "service": SERVICE_NAMES.get(port, 'unknown'),
                    "state": "open"
                })
        except Exception:
            continue
    
    return open_ports

def parse_nmap_output(output: str) -> List[Dict[str, Any]]:
    """Parse nmap output to extract open ports"""
    ports = []
    
    lines = output.split('\n')
    for line in lines:
        if '/tcp' in line and 'open' in line:
            parts = line.split()
            if len(parts) >= 3:
                port_info = parts[0].split('/')
                port = port_info[0]
                protocol = port_info[1] if len(port_info) > 1 else 'tcp'
                
                service = 'unknown'
                for i, part in enumerate(parts):
                    if i >= 2 and part not in ['open', 'closed', 'filtered']:
                        service = part
                        break
                
                port_data = {
                    "port": int(port),
                    "protocol": protocol,
                    "service": service,
                    "state": "open"
                }
                ports.append(port_data)
        elif '/udp' in line and 'open' in line:
            parts = line.split()
            if len(parts) >= 3:
                port_info = parts[0].split('/')
                port = port_info[0]
                protocol = port_info[1] if len(port_info) > 1 else 'udp'
                
                service = 'unknown'
                for i, part in enumerate(parts):
                    if i >= 2 and part not in ['open', 'closed', 'filtered']:
                        service = part
                        break
                
                port_data = {
                    "port": int(port),
                    "protocol": protocol,
                    "service": service,
                    "state": "open"
                }
                ports.append(port_data)
    
    return ports
