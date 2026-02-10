from typing import List, Dict, Any
from tools import tool_manager

def run_nmap_scan(domain: str) -> List[Dict[str, Any]]:
    """Run nmap command"""
    if not tool_manager.check_tool_availability('nmap'):
        return [{"error": "nmap not available"}]
    
    success, stdout, stderr = tool_manager.run_command([
        'nmap', '-sV', '-p', '21,22,25,53,80,110,143,443,993,995,3306,5432', domain
    ])
    
    if success:
        return parse_ports(stdout)
    else:
        return [{"error": stderr}]

def parse_ports(output: str) -> List[Dict[str, Any]]:
    """Parse nmap output"""
    ports = []
    for line in output.split('\n'):
        if '/tcp' in line and 'open' in line:
            parts = line.split()
            port_info = parts[0].split('/')
            port = int(port_info[0])
            service = 'unknown'
            for part in parts[2:]:
                if part not in ['open', 'tcp', 'udp']:
                    service = part
                    break
            ports.append({
                "port": port,
                "protocol": "tcp",
                "service": service,
                "state": "open"
            })
    return ports
