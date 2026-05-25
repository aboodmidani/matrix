import logging
from typing import List, Dict, Any
from tools import check_tool, run_command

logger = logging.getLogger(__name__)


def run_subfinder_scan(domain: str) -> List[Dict[str, Any]]:
    if not check_tool('subfinder'):
        raise RuntimeError("Required tool 'subfinder' is not installed")
    return _subfinder_scan(domain)


def _subfinder_scan(domain: str) -> List[Dict[str, Any]]:
    success, stdout, stderr = run_command(
        ['subfinder', '-d', domain, '-silent', '-all'],
        timeout=120
    )
    if success and stdout.strip():
        return _parse_output(stdout, domain)
    return []


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
