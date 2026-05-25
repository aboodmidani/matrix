import logging
from typing import Dict, Any
from tools import check_tool, run_command

logger = logging.getLogger(__name__)


def scan_live(domain: str) -> Dict[str, Any]:
    result = {
        'alive': False,
        'ping_time_ms': None,
        'http_status': None,
        'error': None,
    }
    if check_tool('ping'):
        success, stdout, _ = run_command(
            ['ping', '-n', '1', domain],
            timeout=10
        )
        if success:
            result['alive'] = True
            import re
            m = re.search(r'time[=<]\s*(\d+(?:\.\d+)?)\s*ms', stdout, re.IGNORECASE)
            if m:
                result['ping_time_ms'] = float(m.group(1))
    if check_tool('curl'):
        success, stdout, _ = run_command(
            ['curl', '-s', '-o', 'nul', '-w', '%{http_code}', f'https://{domain}'],
            timeout=15
        )
        if success and stdout.strip():
            try:
                result['http_status'] = int(stdout.strip())
                result['alive'] = True
            except ValueError:
                pass
    return result
