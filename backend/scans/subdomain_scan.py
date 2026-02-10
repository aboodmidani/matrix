from typing import List, Dict, Any
from tools import tool_manager
import re

def run_subfinder_scan(domain: str) -> List[Dict[str, Any]]:
    """Run subfinder command"""
    if not tool_manager.check_tool_availability('subfinder'):
        return [{"error": "subfinder not available"}]
    
    success, stdout, stderr = tool_manager.run_command([
        'subfinder', '-d', domain, '-silent'
    ])
    
    if success:
        return find_subdomains(stdout, domain)
    else:
        return [{"error": stderr, "raw_output": stdout}]

def find_subdomains(text: str, domain: str) -> List[Dict[str, Any]]:
    """Find all subdomains matching the domain"""
    subdomains = []
    seen = set()
    
    # Find all domain-like patterns
    for match in re.finditer(r'([a-zA-Z0-9][a-zA-Z0-9.-]*\.' + re.escape(domain) + ')', text):
        sub = match.group(1)
        if sub not in seen:
            seen.add(sub)
            subdomains.append({
                "subdomain": sub,
                "discovered": True
            })
    
    # Also try each line
    for line in text.strip().split('\n'):
        line = line.strip()
        if domain in line and '.' in line:
            # Extract subdomain
            parts = line.split()
            for part in parts:
                if domain in part and part not in seen:
                    subdomains.append({
                        "subdomain": part,
                        "discovered": True
                    })
                    seen.add(part)
    
    return subdomains
