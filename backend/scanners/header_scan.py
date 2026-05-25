import logging
from typing import Dict, Any
from tools import check_tool, run_command

logger = logging.getLogger(__name__)

SECURITY_HEADERS = {
    'Strict-Transport-Security': 'HSTS — enforces HTTPS connections',
    'Content-Security-Policy': 'CSP — controls resources the browser can load',
    'X-Frame-Options': 'XFO — prevents clickjacking via iframes',
    'X-Content-Type-Options': 'XCTO — prevents MIME type sniffing',
    'Referrer-Policy': 'Controls referrer header behavior',
    'Permissions-Policy': 'Controls browser API access',
    'X-XSS-Protection': 'Legacy XSS filter (deprecated but still seen)',
    'Access-Control-Allow-Origin': 'CORS — controls cross-origin access',
    'Access-Control-Allow-Methods': 'CORS methods',
    'Access-Control-Allow-Headers': 'CORS headers',
    'Access-Control-Allow-Credentials': 'CORS credentials',
    'Set-Cookie': 'Cookie security flags (httponly, secure, samesite)',
}


def scan_headers(url: str) -> Dict[str, Any]:
    if not check_tool('curl'):
        raise RuntimeError("Required tool 'curl' is not installed")
    result = {
        'headers': {},
        'security_report': {},
        'total_headers': 0,
        'security_headers_found': 0,
        'security_headers_total': len(SECURITY_HEADERS),
        'missing_security_headers': [],
    }
    success, stdout, stderr = run_command(
        ['curl', '-sI', '-L', url],
        timeout=15
    )
    if not success:
        return result
    headers = {}
    for line in stdout.splitlines():
        if ':' in line:
            key, _, value = line.partition(':')
            headers[key.strip().lower()] = value.strip()
    result['total_headers'] = len(headers)
    result['headers'] = {k: v for k, v in headers.items()}
    for hdr, description in SECURITY_HEADERS.items():
        hdr_lower = hdr.lower()
        if hdr_lower in headers:
            result['security_report'][hdr] = {
                'present': True,
                'value': headers[hdr_lower],
                'description': description,
            }
            result['security_headers_found'] += 1
        else:
            result['missing_security_headers'].append(hdr)
            result['security_report'][hdr] = {
                'present': False,
                'value': None,
                'description': description,
            }
    return result
