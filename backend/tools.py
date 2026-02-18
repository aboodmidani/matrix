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
}


def check_tool(name: str) -> bool:
    """Return True if the tool binary is available in PATH."""
    found = shutil.which(name) is not None
    if not found:
        logger.warning(f"Tool '{name}' not found in PATH")
    return found


def run_command(command: List[str], timeout: Optional[int] = None) -> Tuple[bool, str, str]:
    """
    Run a CLI command.
    Returns (success, stdout, stderr).
    """
    timeout = timeout or settings.SCAN_TIMEOUT
    try:
        logger.info(f"Running: {' '.join(command)}")
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        return result.returncode == 0, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        logger.error(f"Command timed out: {' '.join(command)}")
        return False, "", "Command timed out"
    except Exception as e:
        logger.error(f"Command error: {e}")
        return False, "", str(e)
