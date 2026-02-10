from typing import List, Dict, Any
from tools import tool_manager

def run_subfinder_scan(domain: str) -> List[Dict[str, Any]]:
    """Run subfinder command"""
    if not tool_manager.check_tool_availability('subfinder'):
        return [{"error": "subfinder not available"}]
    
    success, stdout, stderr = tool_manager.run_command([
        'subfinder', '-d', domain, '-silent'
    ])
    
    if success:
        return parse_subdomains(stdout)
    else:
        return [{"error": stderr}]

def parse_subdomains(output: str) -> List[Dict[str, Any]]:
    """Parse subfinder output"""
    subdomains = []
    for line in output.strip().split('\n'):
        subdomain = line.strip()
        if subdomain and '.' in subdomain:
            subdomains.append({
                "subdomain": subdomain,
                "discovered": True
            })
    return subdomains
