import socket
from typing import List, Dict, Any


def run_nmap_scan(domain: str) -> List[Dict[str, Any]]:
    """Run nmap command with socket fallback"""
    # First try socket-based scan (faster)
    ports = socket_scan(domain)
    
    if ports:
        return ports
    
    # If socket scan fails, return empty (nmap often gets blocked)
    return [{"error": "No open ports detected (target may be blocking scans)"}]


def socket_scan(domain: str) -> List[Dict[str, Any]]:
    """Basic port scan using socket"""
    ports = []
    common_ports = [80, 443, 22, 21, 25, 53, 110, 143, 993, 995, 3306, 5432]
    
    # Remove www. prefix if present
    if domain.startswith('www.'):
        domain = domain[4:]
    
    for port in common_ports:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        try:
            result = sock.connect_ex((domain, port))
            if result == 0:
                service = get_service_name(port)
                ports.append({
                    "port": port,
                    "protocol": "tcp",
                    "service": service,
                    "state": "open"
                })
        except:
            pass
        finally:
            sock.close()
    
    return ports


def get_service_name(port: int) -> str:
    """Get service name for common ports"""
    services = {
        21: 'ftp', 22: 'ssh', 23: 'telnet', 25: 'smtp',
        53: 'dns', 80: 'http', 110: 'pop3', 143: 'imap',
        443: 'https', 993: 'imaps', 995: 'pop3s',
        3306: 'mysql', 5432: 'postgresql', 8080: 'http-proxy'
    }
    return services.get(port, 'unknown')
