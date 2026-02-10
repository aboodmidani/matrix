from typing import Dict, List, Any
from tools import tool_manager

def run_subfinder_scan(domain: str) -> List[Dict[str, Any]]:
    """Run subfinder command to discover subdomains"""
    try:
        # Check if subfinder is available
        if not tool_manager.check_tool_availability('subfinder'):
            return [{
                "error": "Subdomain discovery tool (subfinder) not available in this environment. Please install subfinder or use a platform that supports it."
            }]
        
        # Run subfinder command
        success, stdout, stderr = tool_manager.run_command([
            'subfinder', '-d', domain, '-silent'
        ])
        
        if success:
            subdomains = parse_subfinder_output(stdout)
            return subdomains
        else:
            return [{"error": f"Subdomain scan failed: {stderr}"}]
            
    except Exception as e:
        return [{"error": f"Subdomain scan error: {str(e)}"}]

def parse_subfinder_output(output: str) -> List[Dict[str, Any]]:
    """Parse subfinder output to extract discovered subdomains"""
    subdomains = []
    
    lines = output.strip().split('\n')
    for line in lines:
        subdomain = line.strip()
        if subdomain and '.' in subdomain:
            subdomain_data = {
                "subdomain": subdomain,
                "discovered": True,
                "source": "subfinder"
            }
            subdomains.append(subdomain_data)
    
    # If no subdomains found, return empty list instead of error
    if not subdomains:
        return []
    
    return subdomains