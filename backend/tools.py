import subprocess
import shutil
import logging
from typing import List, Tuple, Optional
from config import settings

logger = logging.getLogger(__name__)

TOOLS = {
    'nmap':      'Network port scanner',
    'dnsrecon':  'DNS reconnaissance tool',
    'wafw00f':   'WAF detection tool',
    'subfinder': 'Subdomain discovery tool',
    'whatweb':   'Web technology fingerprinter',
    'gobuster':  'Directory/file brute-forcer',
    'gospider':  'Web crawler / spider',
    'openssl':   'SSL/TLS toolkit',
    'curl':      'HTTP request tool',
    'ping':      'Network reachability tester',
    'nslookup':  'DNS lookup utility',
    'dig':       'DNS lookup utility',
}


def check_tool(name: str) -> bool:
    found = shutil.which(name) is not None
    if not found:
        logger.warning("Tool '%s' not found in PATH", name)
    return found


def run_command(command: List[str], timeout: Optional[int] = None, input_text: Optional[str] = None) -> Tuple[bool, str, str]:
    timeout = timeout or settings.SCAN_TIMEOUT
    try:
        logger.info(f"Running: {' '.join(command)}")
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=timeout,
            input=input_text,
        )
        return result.returncode == 0, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        logger.error(f"Command timed out: {' '.join(command)}")
        return False, "", "Command timed out"
    except Exception as e:
        logger.error(f"Command error: {e}")
        return False, "", str(e)
