import socket
import dns.resolver
from typing import Dict, List, Any
from tools import tool_manager

# Common subdomains to check
COMMON_SUBDOMAINS = [
    'www', 'mail', 'ftp', 'admin', 'test', 'dev', 'staging', 'api',
    'blog', 'shop', 'store', 'support', 'help', 'docs', 'wiki',
    'portal', 'cloud', 'app', 'm', 'mobile', 'cdn', 'static',
    'images', 'img', 'assets', 'files', 'download', 'upload',
    'vpn', 'ssh', 'remote', 'manager', 'cpanel', 'whm', 'phpmyadmin',
    'monitoring', 'metrics', 'logs', 'grafana', 'prometheus', 'jenkins',
    'gitlab', 'github', 'bitbucket', 'docker', 'kube', 'k8s'
]

def run_subfinder_scan(domain: str) -> List[Dict[str, Any]]:
    """Fast subdomain discovery using DNS"""
    subdomains = []
    
    for sub in COMMON_SUBDOMAINS:
        try:
            full_domain = f"{sub}.{domain}"
            # Try to resolve the subdomain
            dns.resolver.resolve(full_domain, 'A', lifetime=2)
            subdomains.append({
                "subdomain": full_domain,
                "discovered": True,
                "source": "dns-lookup"
            })
        except Exception:
            continue
    
    return subdomains

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
    
    return subdomains
