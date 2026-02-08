from typing import Dict, List, Any
from tools import tool_manager

def run_nmap_scan(domain: str) -> List[Dict[str, Any]]:
    """Run nmap command to scan open ports"""
    try:
        # Check if nmap is available
        if not tool_manager.check_tool_availability('nmap'):
            return [{
                "error": "Port scanning tool (nmap) not available in this environment. Please use a platform that supports system packages or configure nmap manually."
            }]
        
        # Scan common ports with specific range for faster results
        success, stdout, stderr = tool_manager.run_command([
            'nmap', '-sV', '--version-intensity', '2',
            '-p', '21,22,23,25,53,80,110,143,443,993,995,3306,5432',
            domain
        ])
        
        if success:
            ports = parse_nmap_output(stdout)
            return ports
        else:
            return [{"error": f"Port scan failed: {stderr}"}]
            
    except Exception as e:
        return [{"error": f"Port scan error: {str(e)}"}]

def parse_nmap_output(output: str) -> List[Dict[str, Any]]:
    """Parse nmap output to extract open ports"""
    ports = []
    
    lines = output.split('\n')
    for line in lines:
        if '/tcp' in line and 'open' in line:
            # Parse line like: "80/tcp   open  http    nginx 1.18.0"
            # Or: "22/tcp   open  ssh"
            parts = line.split()
            if len(parts) >= 3:
                port_info = parts[0].split('/')
                port = port_info[0]
                protocol = port_info[1] if len(port_info) > 1 else 'tcp'
                
                # Find the service name (usually the 3rd field)
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
            # Parse UDP ports similarly
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
    
    # If no ports found, return empty list instead of error
    if not ports:
        return []
    
    return ports
