import logging
from typing import Dict, Any
from tools import check_tool, run_command

logger = logging.getLogger(__name__)


def scan_dns_extended(domain: str) -> Dict[str, Any]:
    result = {
        'caa_records': [],
        'ptr_records': [],
        'dnssec': None,
        'zone_transfer': None,
        'error': None,
    }
    if check_tool('dig'):
        success, stdout, _ = run_command(
            ['dig', 'CAA', domain, '+short'],
            timeout=15
        )
        if success and stdout.strip():
            result['caa_records'] = [line.strip() for line in stdout.splitlines() if line.strip()]

        success, stdout, _ = run_command(
            ['dig', domain, '+dnssec', '+short'],
            timeout=15
        )
        if success:
            has_dnssec = any('RRSIG' in line for line in stdout.splitlines())
            result['dnssec'] = has_dnssec

    if check_tool('nslookup'):
        success, stdout, _ = run_command(
            ['nslookup', '-type=ANY', domain],
            timeout=15
        )
        if success and stdout:
            result['ptr_records'] = [
                line.strip() for line in stdout.splitlines()
                if 'PTR' in line or 'canonical name' in line.lower()
            ]

    if check_tool('dnsrecon'):
        success, stdout, _ = run_command(
            ['dnsrecon', '-d', domain, '-t', 'axfr'],
            timeout=30
        )
        if success:
            if 'Zone Transfer' in stdout and 'successful' in stdout:
                result['zone_transfer'] = 'vulnerable'
            elif 'Zone Transfer' in stdout and 'failed' in stdout:
                result['zone_transfer'] = 'secure'
            else:
                result['zone_transfer'] = 'unknown'

    return result
