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
        return find_open_ports(stdout)
    else:
        return [{"error": stderr, "raw_output": stdout}]

def find_open_ports(text: str) -> List[Dict[str, Any]]:
    """Find all open ports from nmap output"""
    ports = []
    text_lower = text.lower()
    
    # Common services
    services = {
        '80': 'http', '443': 'https', '22': 'ssh', '21': 'ftp',
        '25': 'smtp', '53': 'dns', '110': 'pop3', '143': 'imap',
        '993': 'imap', '995': 'pop3', '3306': 'mysql', '5432': 'postgresql'
    }
    
    # Look for port patterns like "80/tcp" or "PORT   STATE SERVICE"
    for match in re.finditer(r'(\d+)/tcp', text_lower):
        port = int(match.group(1))
        service = services.get(str(port), 'unknown')
        ports.append({
            "port": port,
            "protocol": "tcp",
            "service": service,
            "state": "open"
        })
    
    return ports

import re
