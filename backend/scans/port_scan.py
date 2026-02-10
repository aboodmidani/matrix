import socket
from typing import Dict, List, Any
from tools import tool_manager

COMMON_PORTS = [21, 22, 25, 53, 80, 110, 143, 443, 993, 995, 3306, 5432, 8080]

SERVICE_NAMES = {
    21: 'ftp', 22: 'ssh', 25: 'smtp', 53: 'dns',
    80: 'http', 110: 'pop3', 143: 'imap', 443: 'https',
    993: 'imaps', 995: 'pop3s', 3306: 'mysql', 5432: 'postgresql',
    8080: 'http-alt'
}

def run_nmap_scan(domain: str) -> List[Dict[str, Any]]:
    """Fast port scan with simple nmap command"""
    try:
        # Check if nmap is available
        if not tool_manager.check_tool_availability('nmap'):
            return port_scan_socket(domain)
        
        # Run simple nmap command
        success, stdout, stderr = tool_manager.run_command([
            'nmap', '-p', '21,22,25,53,80,110,143,443,993,995,3306,5432,8080',
            '--open', '-oG', '-', domain
        ])
        
        if success:
            ports = parse_nmap_simple(stdout)
            if ports:
                return ports
            return port_scan_socket(domain)
        else:
            return port_scan_socket(domain)
            
    except Exception as e:
        return port_scan_socket(domain)

def port_scan_socket(domain: str) -> List[Dict[str, Any]]:
    """Fallback socket-based port scan"""
    open_ports = []
    try:
        ip = socket.gethostbyname(domain)
    except:
        return [{"error": f"Could not resolve: {domain}"}]
    
    for port in COMMON_PORTS:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((ip, port))
            sock.close()
            if result == 0:
                open_ports.append({
                    "port": port,
                    "protocol": "tcp",
                    "service": SERVICE_NAMES.get(port, 'unknown'),
                    "state": "open"
                })
        except:
            continue
    
    return open_ports

def parse_nmap_simple(output: str) -> List[Dict[str, Any]]:
    """Simple nmap parsing"""
    ports = []
    
    # Parse nmap -oG format: Host: 1.2.3.4 ()  Ports: 80/open/tcp//http//
    for line in output.split('\n'):
        if 'Ports:' in line:
            port_parts = line.split('Ports:')[1].split(',')
            for part in port_parts:
                part = part.strip()
                if '/open/' in part:
                    # Extract port
                    port_match = part.split('/')[0]
                    try:
                        port = int(port_match)
                        service = SERVICE_NAMES.get(port, 'unknown')
                        ports.append({
                            "port": port,
                            "protocol": "tcp",
                            "service": service,
                            "state": "open"
                        })
                    except:
                        continue
    
    return ports

def parse_nmap_output(output: str) -> List[Dict[str, Any]]:
    """Parse nmap output"""
    return parse_nmap_simple(output)
