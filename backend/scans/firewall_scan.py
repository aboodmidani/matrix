import json
import tempfile
import os
import logging
from typing import Dict, Any
from tools import check_tool, run_command

logger = logging.getLogger(__name__)


WAF_SIGNATURES = {
    'Cloudflare': ['cf-ray', '__cfduid', 'cf-cache-status', 'server: cloudflare'],
    'Cloudfront': ['x-amz-cf-id', 'x-amz-cf-pop', 'server: cloudfront'],
    'Akamai': ['x-akamai-transformed', 'server: akamai'],
    'Fastly': ['x-served-by', 'x-timer', 'server: fastly'],
    'AWS WAF': ['x-amzn-requestid', 'x-amzn-trace-id', 'x-amzn-waf'],
    'Sucuri': ['x-sucuri-id', 'x-sucuri-cache', 'x-sucuri-block'],
    'ModSecurity': ['x-mod-security', 'server: modsecurity'],
    'F5 BIG-IP': ['x-wa-info', 'server: bigip'],
    'Barracuda': ['barracuda'],
    'Imperva': ['imperva', 'incapsula', 'x-iinfo'],
}


def scan_firewall(url: str) -> Dict[str, Any]:
    if check_tool('wafw00f'):
        return _wafw00f_scan(url)
    return _curl_waf_detect(url)


def _wafw00f_scan(url: str) -> Dict[str, Any]:
    tmp = tempfile.NamedTemporaryFile(suffix='.json', delete=False)
    tmp.close()
    try:
        success, stdout, stderr = run_command(
            ['wafw00f', url, '-a', '-o', tmp.name, '-f', 'json'],
            timeout=30
        )
        if os.path.exists(tmp.name) and os.path.getsize(tmp.name) > 0:
            with open(tmp.name) as f:
                data = json.load(f)
            if isinstance(data, list) and data:
                entry = data[0]
                detected = bool(entry.get('detected'))
                waf_name = entry.get('firewall') or 'None'
                manufacturer = entry.get('manufacturer') or ''
                return {
                    'detected': detected,
                    'waf_name': waf_name if detected else 'No WAF detected',
                    'manufacturer': manufacturer,
                    'confidence': 'High' if detected else 'None',
                }
    except Exception as e:
        logger.debug("wafw00f scan error: %s", e)
    finally:
        if os.path.exists(tmp.name):
            try:
                os.unlink(tmp.name)
            except OSError:
                pass
    return {
        'detected': False,
        'waf_name': 'No WAF detected',
        'manufacturer': '',
        'confidence': 'None',
    }


def _curl_waf_detect(url: str) -> Dict[str, Any]:
    success, stdout, _ = run_command(['curl', '-sI', '-L', url], timeout=15)
    if not success:
        return {'detected': False, 'waf_name': 'No WAF detected', 'manufacturer': '', 'confidence': 'None', 'error': 'Failed to fetch headers'}
    headers_lower = stdout.lower()
    for waf_name, signatures in WAF_SIGNATURES.items():
        for sig in signatures:
            if sig in headers_lower:
                return {'detected': True, 'waf_name': waf_name, 'manufacturer': waf_name, 'confidence': 'Medium', 'note': 'Detected via curl header signatures (install wafw00f for full scan)'}
    return {'detected': False, 'waf_name': 'No WAF detected', 'manufacturer': '', 'confidence': 'Low', 'note': 'curl-based detection (install wafw00f for full scan)'}
