import re
import logging
from typing import List, Dict, Any
from tools import check_tool, run_command

logger = logging.getLogger(__name__)


def run_subfinder_scan(domain: str) -> List[Dict[str, Any]]:
    if check_tool('subfinder'):
        result = _subfinder_scan(domain)
        if result:
            return result

    if check_tool('dig'):
        result = _dig_fallback(domain)
        if result:
            return result

    return _nslookup_fallback(domain)


def _subfinder_scan(domain: str) -> List[Dict[str, Any]]:
    success, stdout, stderr = run_command(
        ['subfinder', '-d', domain, '-silent', '-all'],
        timeout=120
    )
    if success and stdout.strip():
        return _parse_output(stdout, domain)
    return []


def _dig_fallback(domain: str) -> List[Dict[str, Any]]:
    seen = set()
    results = []
    domain_lower = domain.lower()

    # Try zone transfer (AXFR) via nameservers
    success, ns_stdout, _ = run_command(
        ['dig', '-t', 'NS', domain, '+short'],
        timeout=15
    )
    if success and ns_stdout.strip():
        nameservers = [line.strip().rstrip('.') for line in ns_stdout.splitlines()
                       if line.strip() and not line.strip().startswith(';')]
        for ns in nameservers:
            success, axfr_out, _ = run_command(
                ['dig', 'AXFR', domain, f'@{ns}', '+short'],
                timeout=30
            )
            if success and axfr_out.strip():
                for line in axfr_out.splitlines():
                    line = line.strip()
                    if not line:
                        continue
                    parts = line.split()
                    if parts and parts[0].endswith('.' + domain_lower):
                        sub = parts[0].rstrip('.').lower()
                        if sub not in seen:
                            seen.add(sub)
                            results.append({'subdomain': sub})
                if results:
                    return results

    # Try common subdomains via dig
    common = ['www', 'mail', 'ftp', 'admin', 'blog', 'api', 'cdn',
              'vpn', 'webmail', 'smtp', 'pop3', 'imap', 'ns1', 'ns2',
              'mx', 'docs', 'dev', 'staging', 'test', 'status',
              'help', 'support', 'shop', 'store', 'm', 'app',
              'beta', 'demo', 'forum', 'wiki', 'portal', 'remote',
              'dns', 'dns1', 'dns2', 'email', 'host', 'hosting',
              'cpanel', 'whm', 'server', 'git', 'jenkins', 'jira',
              'confluence', 'mysql', 'db', 'redis', 'backup', 'monitor']
    for sub in common:
        target = f'{sub}.{domain_lower}'
        success, out, _ = run_command(
            ['dig', '-t', 'A', target, '+short'],
            timeout=5
        )
        if success and out.strip():
            for ip in out.splitlines():
                ip = ip.strip()
                if ip and re.match(r'^\d+\.\d+\.\d+\.\d+$', ip) and target not in seen:
                    seen.add(target)
                    results.append({'subdomain': target})
                    break

    return results


def _nslookup_fallback(domain: str) -> List[Dict[str, Any]]:
    if not check_tool('nslookup'):
        return []
    seen = set()
    results = []
    common = ['www', 'mail', 'ftp', 'admin', 'blog', 'api', 'cdn',
              'vpn', 'webmail', 'smtp', 'pop3', 'imap', 'ns1', 'ns2',
              'mx', 'docs', 'dev', 'staging', 'test', 'status',
              'help', 'support', 'shop', 'store', 'm', 'app',
              'beta', 'demo', 'forum', 'wiki', 'portal', 'remote',
              'dns', 'dns1', 'dns2', 'email', 'host', 'hosting',
              'cpanel', 'whm', 'server', 'git', 'jenkins', 'jira',
              'mysql', 'db', 'redis', 'backup', 'monitor']
    for sub in common:
        target = f'{sub}.{domain}'
        success, stdout, _ = run_command(
            ['nslookup', target],
            timeout=5
        )
        if success:
            for m in re.finditer(r'Address[es]?:\s+(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', stdout):
                ip = m.group(1)
                if not ip.startswith('127.') and target not in seen:
                    seen.add(target)
                    results.append({'subdomain': target})
                    break
    return results


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
