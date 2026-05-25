import re
import logging
from typing import Dict, Any
from tools import check_tool, run_command

logger = logging.getLogger(__name__)


def scan_ssl(domain: str) -> Dict[str, Any]:
    if not check_tool('openssl'):
        raise RuntimeError("Required tool 'openssl' is not installed")
    result = {
        'certificate': {
            'subject': None,
            'issuer': None,
            'not_before': None,
            'not_after': None,
            'days_remaining': None,
            'serial': None,
            'san': [],
            'expired': False,
        },
        'error': None,
    }
    success, stdout, stderr = run_command(
        [
            'openssl', 's_client',
            '-servername', domain,
            '-connect', f'{domain}:443',
            '-showcerts',
        ],
        input_text='Q\n',
        timeout=15
    )
    if not success and stderr:
        success, stdout, stderr = run_command(
            ['openssl', 's_client', '-connect', f'{domain}:443', '-showcerts'],
            input_text='Q\n',
            timeout=15
        )

    if not success:
        result['error'] = stderr or 'SSL connection failed'
        return result

    cert_match = re.search(r'-----BEGIN CERTIFICATE-----.*?-----END CERTIFICATE-----', stdout, re.DOTALL)
    if not cert_match:
        result['error'] = 'No certificate returned'
        return result

    cert_pem = cert_match.group(0)

    success, stdout2, _ = run_command(
        ['openssl', 'x509', '-noout', '-subject', '-issuer', '-dates', '-serial'],
        input_text=cert_pem,
        timeout=10
    )

    if success and stdout2:
        subject_m = re.search(r'subject=\s*(.+?)$', stdout2, re.MULTILINE)
        if subject_m:
            result['certificate']['subject'] = subject_m.group(1).strip()
        issuer_m = re.search(r'issuer=\s*(.+?)$', stdout2, re.MULTILINE)
        if issuer_m:
            result['certificate']['issuer'] = issuer_m.group(1).strip()
        serial_m = re.search(r'serial=\s*(.+?)$', stdout2, re.MULTILINE)
        if serial_m:
            result['certificate']['serial'] = serial_m.group(1).strip()
        not_before_m = re.search(r'notBefore=\s*(.+?)$', stdout2, re.MULTILINE)
        if not_before_m:
            result['certificate']['not_before'] = not_before_m.group(1).strip()
        not_after_m = re.search(r'notAfter=\s*(.+?)$', stdout2, re.MULTILINE)
        if not_after_m:
            result['certificate']['not_after'] = not_after_m.group(1).strip()

    success, stdout3, _ = run_command(
        ['openssl', 'x509', '-noout', '-text'],
        input_text=cert_pem,
        timeout=10
    )
    if success and stdout3:
        san_entries = re.findall(r'DNS:([^\s,]+)', stdout3)
        if san_entries:
            result['certificate']['san'] = [f'DNS:{e}' for e in san_entries]

    from datetime import datetime, timezone
    na = result['certificate']['not_after']
    if na:
        for fmt in ['%b %d %H:%M:%S %Y %Z', '%b %d %H:%M:%S %Y %z', '%Y%m%d%H%M%SZ']:
            try:
                parsed = datetime.strptime(na.strip(), fmt)
                parsed = parsed.replace(tzinfo=timezone.utc) if parsed.tzinfo is None else parsed
                now = datetime.now(timezone.utc)
                days = (parsed - now).days
                result['certificate']['days_remaining'] = days
                result['certificate']['expired'] = days < 0
                break
            except ValueError:
                continue

    return result
