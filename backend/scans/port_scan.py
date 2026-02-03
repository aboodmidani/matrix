import subprocess
from typing import Dict, List, Any

def run_nmap_scan(domain: str) -> List[Dict[str, Any]]:
    """Run nmap command to scan open ports"""
    try:
        # Check if nmap is available
        check_result = subprocess.run(
            ['which', 'nmap'],
            capture_output=True,
            text=True
        )
        
        if check_result.returncode != 0:
            return [{
                "error": "Port scanning tool (nmap) not available in this environment. Please use a platform that supports system packages or configure nmap manually."
            }]
        
        # Scan common ports
        result = subprocess.run(
            ['nmap', '-sV', '--version-intensity', '2', '-p', '21,22,23,25,53,80,110,143,443,993,995,3306,5432', domain],
            capture_output=True,
            text=True,
            timeout=60
        )
        
        if result.returncode == 0:
            output = result.stdout
            ports = parse_nmap_output(output)
            return ports
        else:
            return [{"error": f"Port scan failed: {result.stderr}"}]
            
    except subprocess.TimeoutExpired:
        return [{"error": "Port scan timed out"}]
    except Exception as e:
        return [{"error": f"Port scan error: {str(e)}"}]

def parse_nmap_output(output: str) -> List[Dict[str, Any]]:
    """Parse nmap output to extract open ports"""
    ports = []
    
    lines = output.split('\n')
    for line in lines:
        if '/tcp' in line and 'open' in line:
            # Parse line like: "80/tcp   open  http    nginx 1.18.0"
            parts = line.split()
            if len(parts) >= 3:
                port_info = parts[0].split('/')
                port = port_info[0]
                protocol = port_info[1] if len(port_info) > 1 else 'tcp'
                service = parts[2] if len(parts) > 2 else 'unknown'
                
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
