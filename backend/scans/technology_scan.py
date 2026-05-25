import json
import logging
from typing import Dict, Any
from tools import check_tool, run_command

logger = logging.getLogger(__name__)


def scan_technologies(url: str) -> Dict[str, Any]:
    if not check_tool('whatweb'):
        raise RuntimeError("Required tool 'whatweb' is not installed")
    return _whatweb_scan(url)


def _whatweb_scan(url: str) -> Dict[str, Any]:
    success, stdout, stderr = run_command(
        ['whatweb', '-a', '3', '--log-json=-', url],
        timeout=60
    )
    technologies = {}
    if success and stdout.strip():
        try:
            data = json.loads(stdout)
            if isinstance(data, list):
                for entry in data:
                    plugins = entry.get('plugins', entry)
                    if isinstance(plugins, dict):
                        for name, info in plugins.items():
                            if name in ['HTTP-Status', 'HTTPServer', 'IP', 'Country', 'Title']:
                                continue
                            version = ''
                            certainty = 85
                            if isinstance(info, dict):
                                version_list = info.get('version', [])
                                if isinstance(version_list, list) and version_list:
                                    version = version_list[0]
                                certainty_list = info.get('certainty', [])
                                if isinstance(certainty_list, list) and certainty_list:
                                    certainty = certainty_list[0]
                            elif isinstance(info, str):
                                version = info
                            if name and name not in technologies:
                                technologies[name] = {
                                    'version': version,
                                    'confidence': certainty,
                                    'categories': [],
                                }
        except (json.JSONDecodeError, KeyError):
            logger.debug("whatweb JSON parsing failed for %s", url)
    return {'url': url, 'technologies': technologies, 'status': 'success'}
