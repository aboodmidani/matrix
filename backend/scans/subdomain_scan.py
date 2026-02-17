import socket
from typing import List, Dict, Any
from tools import tool_manager


def run_subfinder_scan(domain: str) -> List[Dict[str, Any]]:
    """Run subfinder command"""
    if not tool_manager.check_tool_availability('subfinder'):
        # Fallback to basic subdomain enumeration
        return basic_subdomain_enum(domain)
    
    success, stdout, stderr = tool_manager.run_command([
        'subfinder', '-d', domain, '-silent'
    ], timeout=60)
    
    if success:
        return parse_subdomains(stdout, domain)
    else:
        return basic_subdomain_enum(domain)


def basic_subdomain_enum(domain: str) -> List[Dict[str, Any]]:
    """Basic subdomain enumeration using common prefixes"""
    subdomains = []
    common_prefixes = ['www', 'mail', 'ftp', 'localhost', 'webmail', 'smtp', 'pop', 'ns1', 'webdisk', 'ns2', 'cpanel', 'whm', 'autodiscover', 'autoconfig', 'm', 'imap', 'test', 'ns', 'blog', 'pop3', 'dev', 'www2', 'admin', 'forum', 'news', 'vpn', 'ns3', 'mail2', 'new', 'mysql', 'old', 'lists', 'support', 'mobile', 'mx', 'static', 'docs', 'beta', 'shop', 'sql', 'secure', 'demo', 'cdc', 'git', 'staging', 'backup', 'moodle', 'stage', 'pre', 'v2', 'owa', 'en', 'start', 'share', 's1', 's2', 's3', 's4', 's5']
    
    for prefix in common_prefixes:
        subdomain = f"{prefix}.{domain}"
        try:
            socket.gethostbyname(subdomain)
            subdomains.append({"subdomain": subdomain, "discovered": True})
        except:
            pass
    
    return subdomains


def parse_subdomains(text: str, domain: str) -> List[Dict[str, Any]]:
    """Parse subfinder output"""
    subdomains = []
    seen = set()
    
    for line in text.strip().split('\n'):
        line = line.strip()
        if line and domain in line:
            if line not in seen:
                seen.add(line)
                subdomains.append({"subdomain": line, "discovered": True})
    
    # If no results, try basic enumeration
    if not subdomains:
        return basic_subdomain_enum(domain)
    
    return subdomains
