import socket
import dns.resolver
from typing import Dict, List, Any
from tools import tool_manager

# Common subdomains
COMMON_SUBDOMAINS = [
    'www', 'mail', 'ftp', 'admin', 'test', 'dev', 'api', 'blog',
    'shop', 'store', 'support', 'docs', 'wiki', 'portal',
    'cloud', 'app', 'm', 'cdn', 'static', 'images'
]

def run_subfinder_scan(domain: str) -> List[Dict[str, Any]]:
    """Subdomain discovery using dnsrecon brute force or DNS"""
    try:
        # Check if subfinder is available
        if tool_manager.check_tool_availability('subfinder'):
            # Use subfinder
            success, stdout, stderr = tool_manager.run_command([
                'subfinder', '-d', domain, '-silent'
            ])
            if success:
                return parse_subfinder_simple(stdout)
        
        # Fallback: Use dnsrecon for subdomain brute force
        if tool_manager.check_tool_availability('dnsrecon'):
            success, stdout, stderr = tool_manager.run_command([
                'dnsrecon', '-d', domain, '-t', 'brt', '-f'
            ])
            if success:
                return parse_dnsrecon_subdomains(stdout)
        
        # Fallback: Simple DNS check
        return dns_subdomain_check(domain)
            
    except Exception as e:
        return dns_subdomain_check(domain)

def dns_subdomain_check(domain: str) -> List[Dict[str, Any]]:
    """Check common subdomains via DNS"""
    subdomains = []
    
    for sub in COMMON_SUBDOMAINS:
        try:
            full_domain = f"{sub}.{domain}"
            dns.resolver.resolve(full_domain, 'A', lifetime=2)
            subdomains.append({
                "subdomain": full_domain,
                "discovered": True,
                "source": "dns"
            })
        except:
            continue
    
    return subdomains

def parse_subfinder_simple(output: str) -> List[Dict[str, Any]]:
    """Simple subfinder parsing"""
    subdomains = []
    for line in output.strip().split('\n'):
        subdomain = line.strip()
        if subdomain and '.' in subdomain:
            subdomains.append({
                "subdomain": subdomain,
                "discovered": True,
                "source": "subfinder"
            })
    return subdomains

def parse_dnsrecon_subdomains(output: str) -> List[Dict[str, Any]]:
    """Parse dnsrecon subdomain brute force output"""
    subdomains = []
    
    for line in output.split('\n'):
        line = line.strip()
        if subdomain := extract_subdomain(line):
            subdomains.append({
                "subdomain": subdomain,
                "discovered": True,
                "source": "dnsrecon"
            })
    
    return subdomains

def extract_subdomain(line: str) -> str:
    """Extract subdomain from line"""
    import re
    # Look for subdomain patterns
    match = re.search(r'([a-zA-Z0-9_-]+\.' + r'\.'.join(['a-zA-Z0-9_-']*2) + ')', line)
    return match.group(1) if match else ''

def parse_subfinder_output(output: str) -> List[Dict[str, Any]]:
    """Parse subfinder output"""
    return parse_subfinder_simple(output)
