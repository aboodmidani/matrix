import json
import tempfile
import os
import requests
from typing import Dict, Any
from tools import check_tool, run_command


def scan_firewall(url: str) -> Dict[str, Any]:
    """Detect WAF using wafw00f CLI. Falls back to header-based detection."""
    if check_tool('wafw00f'):
        return _wafw00f_scan(url)
    return _header_scan(url)


def _wafw00f_scan(url: str) -> Dict[str, Any]:
    """Run wafw00f with JSON output."""
    tmp = tempfile.NamedTemporaryFile(suffix='.json', delete=False)
    tmp.close()
    try:
        success, stdout, stderr = run_command(
            ['wafw00f', url, '-o', tmp.name, '-f', 'json'],
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
    except Exception:
        pass
    finally:
        if os.path.exists(tmp.name):
            os.unlink(tmp.name)

    # wafw00f ran but output was unusable — try header scan
    return _header_scan(url)


def _header_scan(url: str) -> Dict[str, Any]:
    """Fallback: detect WAF from HTTP response headers."""
    WAF_SIGNATURES = {
        'Cloudflare':  ['cf-ray', 'cf-cache-status', 'cloudflare'],
        'AWS WAF':     ['x-amz-cf-id', 'x-amzn-requestid'],
        'Akamai':      ['akamai-origin-hop', 'x-akamai-transformed'],
        'Imperva':     ['x-iinfo', 'incapsula'],
        'Sucuri':      ['x-sucuri-id', 'x-sucuri-cache'],
        'Fastly':      ['x-served-by', 'fastly-restarts'],
        'DDoS-Guard':  ['ddos-guard'],
        'Barracuda':   ['barra_counter_session'],
        'F5 BIG-IP':   ['bigipserver', 'x-wa-info'],
        'ModSecurity': ['mod_security', 'modsecurity'],
    }
    try:
        resp = requests.get(url, timeout=10, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }, allow_redirects=True)
        headers_lower = {k.lower(): v.lower() for k, v in resp.headers.items()}
        body_lower = resp.text.lower()

        for waf_name, signatures in WAF_SIGNATURES.items():
            for sig in signatures:
                if sig in headers_lower or sig in body_lower:
                    return {
                        'detected': True,
                        'waf_name': waf_name,
                        'manufacturer': waf_name,
                        'confidence': 'Medium',
                    }

        return {
            'detected': False,
            'waf_name': 'No WAF detected',
            'manufacturer': '',
            'confidence': 'Low',
        }
    except Exception as e:
        return {
            'detected': False,
            'waf_name': 'Unknown',
            'manufacturer': '',
            'confidence': 'None',
            'error': str(e),
        }
