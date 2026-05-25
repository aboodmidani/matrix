import json
import tempfile
import os
import logging
from typing import Dict, Any
from tools import check_tool, run_command

logger = logging.getLogger(__name__)


def scan_firewall(url: str) -> Dict[str, Any]:
    if not check_tool('wafw00f'):
        raise RuntimeError("Required tool 'wafw00f' is not installed")
    return _wafw00f_scan(url)


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
