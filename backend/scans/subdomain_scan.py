import socket
from typing import List, Dict, Any
from tools import check_tool, run_command

# Common subdomains for fallback brute-force
COMMON_PREFIXES = [
    'www', 'mail', 'ftp', 'smtp', 'pop', 'imap', 'webmail',
    'ns1', 'ns2', 'ns3', 'mx', 'mx1', 'mx2',
    'admin', 'portal', 'api', 'dev', 'staging', 'test', 'beta',
    'blog', 'shop', 'store', 'app', 'mobile', 'm',
    'vpn', 'remote', 'secure', 'cdn', 'static', 'assets',
    'git', 'gitlab', 'github', 'jenkins', 'ci', 'docs',
    'support', 'help', 'forum', 'community', 'news',
    'backup', 'old', 'new', 'v2', 'demo', 'sandbox',
    'db', 'mysql', 'sql', 'mongo', 'redis', 'elastic',
    'cpanel', 'whm', 'webdisk', 'autodiscover', 'autoconfig',
]


def run_subfinder_scan(domain: str) -> List[Dict[str, Any]]:
    """Discover subdomains using subfinder CLI. Falls back to brute-force."""
    if check_tool('subfinder'):
        return _subfinder_scan(domain)
    return _bruteforce_scan(domain)


def _subfinder_scan(domain: str) -> List[Dict[str, Any]]:
    success, stdout, stderr = run_command(
        ['subfinder', '-d', domain, '-silent'],
        timeout=60
    )
    if success and stdout.strip():
        return _parse_output(stdout, domain)
    return _bruteforce_scan(domain)


def _parse_output(text: str, domain: str) -> List[Dict[str, Any]]:
    seen = set()
    results = []
    for line in text.strip().splitlines():
        sub = line.strip()
        if sub and domain in sub and sub not in seen:
            seen.add(sub)
            results.append({'subdomain': sub})
    return results


def _bruteforce_scan(domain: str) -> List[Dict[str, Any]]:
    """Fallback: resolve common subdomain prefixes."""
    results = []
    for prefix in COMMON_PREFIXES:
        fqdn = f"{prefix}.{domain}"
        try:
            socket.gethostbyname(fqdn)
            results.append({'subdomain': fqdn})
        except Exception:
            pass
    return results
