import os
import sys
import logging
from typing import Dict, Any
from tools import check_tool, run_command

logger = logging.getLogger(__name__)

NULL_DEVICE = 'nul' if sys.platform == 'win32' else '/dev/null'


def scan_live(domain: str) -> Dict[str, Any]:
    result = {
        'alive': False,
        'ping_time_ms': None,
        'http_status': None,
        'error': None,
    }
    if check_tool('ping'):
        import re
        success, stdout, _ = run_command(
            ['ping', '-n', '1', domain],
            timeout=10
        )
        if success:
            result['alive'] = True
            m = re.search(r'(?:time[=<]\s*(\d+(?:\.\d+)?)\s*ms|time=(\d+)ms)', stdout, re.IGNORECASE)
            if m:
                val = m.group(1) or m.group(2)
                result['ping_time_ms'] = float(val)
    if check_tool('curl'):
        success, stdout, _ = run_command(
            ['curl', '-s', '-o', NULL_DEVICE, '-w', '%{http_code}', f'https://{domain}'],
            timeout=15
        )
        if success and stdout.strip():
            try:
                result['http_status'] = int(stdout.strip())
                result['alive'] = True
            except ValueError:
                pass
    return result
