import socket
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict, Any
from tools import check_tool, run_command

logger = logging.getLogger(__name__)

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
    's3', 'storage', 'console', 'dashboard', 'manage',
    'internal', 'intranet', 'corp', 'preprod', 'uat', 'qa',
    'graphql', 'grpc', 'ws', 'kubernetes', 'k8s', 'docker',
    'registry', 'grafana', 'prometheus', 'kibana', 'elastic',
    'vpn2', 'gateway', 'edge', 'smtp2', 'mx3', 'ns4',
    'login', 'auth', 'sso', 'id', 'identity',
    'media', 'img', 'images', 'video', 'upload',
    'crm', 'erp', 'hr', 'finance', 'billing',
    'monitor', 'status', 'health', 'metrics',
    'cache', 'proxy', 'lb', 'load',
]


def run_subfinder_scan(domain: str) -> List[Dict[str, Any]]:
    """Discover subdomains using subfinder CLI. Falls back to brute-force."""
    if check_tool('subfinder'):
        return _subfinder_scan(domain)
    return _bruteforce_scan(domain)


def _subfinder_scan(domain: str) -> List[Dict[str, Any]]:
    success, stdout, stderr = run_command(
        ['subfinder', '-d', domain, '-silent', '-all'],
        timeout=120
    )
    if success and stdout.strip():
        return _parse_output(stdout, domain)
    logger.warning("subfinder returned no results, falling back to brute-force")
    return _bruteforce_scan(domain)


def _parse_output(text: str, domain: str) -> List[Dict[str, Any]]:
    seen = set()
    results = []
    domain_lower = domain.lower()
    for line in text.strip().splitlines():
        sub = line.strip().lower()
        if sub and (sub.endswith('.' + domain_lower) or sub == domain_lower) and sub not in seen:
            seen.add(sub)
            results.append({'subdomain': sub})
    return results


def _check_subdomain(fqdn: str) -> str | None:
    """Check if a subdomain resolves. Returns the FQDN or None."""
    try:
        socket.gethostbyname(fqdn)
        return fqdn
    except Exception:
        return None


def _detect_wildcard(domain: str) -> bool:
    """Check if the domain has wildcard DNS by testing a random subdomain."""
    import uuid
    random_prefix = uuid.uuid4().hex[:16]
    random_fqdn = f"{random_prefix}.{domain}"
    try:
        socket.gethostbyname(random_fqdn)
        logger.warning("Wildcard DNS detected for %s", domain)
        return True
    except Exception:
        return False


def _bruteforce_scan(domain: str) -> List[Dict[str, Any]]:
    """Fallback: resolve common subdomain prefixes using parallel DNS."""
    if _detect_wildcard(domain):
        logger.warning("Skipping brute-force for %s — wildcard DNS detected", domain)
        return []

    results = []
    with ThreadPoolExecutor(max_workers=30) as executor:
        futures = {
            executor.submit(_check_subdomain, f"{prefix}.{domain}"): prefix
            for prefix in COMMON_PREFIXES
        }
        for future in as_completed(futures, timeout=60):
            try:
                fqdn = future.result()
                if fqdn:
                    results.append({'subdomain': fqdn})
            except Exception as e:
                logger.debug("Subdomain check error: %s", e)

    results.sort(key=lambda x: x['subdomain'])
    return results
