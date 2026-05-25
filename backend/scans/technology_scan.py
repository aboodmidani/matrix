import json
import logging
from typing import Dict, Any
from tools import check_tool, run_command

logger = logging.getLogger(__name__)


def scan_technologies(url: str) -> Dict[str, Any]:
    if check_tool('whatweb'):
        return _whatweb_scan(url)
    return _curl_fallback_scan(url)


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


def _curl_fallback_scan(url: str) -> Dict[str, Any]:
    technologies = {}
    success, stdout, _ = run_command(['curl', '-sI', '-L', url], timeout=15)
    cms_indicators = {
        'wp-content': ('WordPress', ['CMS']),
        '/wp-': ('WordPress', ['CMS']),
        'Drupal': ('Drupal', ['CMS']),
        'Joomla': ('Joomla', ['CMS']),
        'Magento': ('Magento', ['CMS']),
        'Shopify': ('Shopify', ['Ecommerce']),
        ' Squarespace': ('Squarespace', ['CMS']),
        'Wix': ('Wix', ['CMS']),
    }
    if success:
        for line in stdout.splitlines():
            lower = line.lower()
            if lower.startswith('server:'):
                val = line.split(':', 1)[1].strip()
                technologies['Server'] = {'version': val, 'confidence': 100, 'categories': ['Web Server']}
            elif lower.startswith('x-powered-by:'):
                val = line.split(':', 1)[1].strip()
                technologies[val] = {'version': '', 'confidence': 90, 'categories': ['Framework']}
            elif lower.startswith('x-generator:'):
                val = line.split(':', 1)[1].strip()
                technologies[val.split('/')[0]] = {'version': val.split('/')[1] if '/' in val else '', 'confidence': 100, 'categories': ['CMS']}
            elif 'set-cookie:' in lower and 'phpsessid' in lower:
                technologies.setdefault('PHP', {'version': '', 'confidence': 85, 'categories': ['Programming Language']})
            elif 'set-cookie:' in lower and 'aspsessionid' in lower:
                technologies.setdefault('ASP.NET', {'version': '', 'confidence': 85, 'categories': ['Programming Language']})
    success, stdout, _ = run_command(['curl', '-sL', url], timeout=15)
    if success:
        import re
        gen_m = re.search(r'<meta[^>]+name=["\']generator["\'][^>]+content=["\']([^"\']+)["\']', stdout, re.IGNORECASE)
        if gen_m:
            content = gen_m.group(1).strip()
            parts = content.split(None, 1)
            tech_name = parts[0]
            ver = parts[1] if len(parts) > 1 else ''
            technologies.setdefault(tech_name, {'version': ver, 'confidence': 100, 'categories': ['CMS']})
        for indicator, (tech_name, categories) in cms_indicators.items():
            if indicator.lower() in stdout.lower():
                technologies.setdefault(tech_name, {'version': '', 'confidence': 80, 'categories': categories})
    return {'url': url, 'technologies': technologies, 'status': 'success', 'note': 'curl-based detection (install whatweb for full results)'}
