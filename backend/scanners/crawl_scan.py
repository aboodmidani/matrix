import json
import re
import logging
from typing import Dict, Any
from tools import check_tool, run_command

logger = logging.getLogger(__name__)


def scan_crawl(url: str) -> Dict[str, Any]:
    if check_tool('gospider'):
        return _gospider_scan(url)
    return _curl_crawl(url)


def _gospider_scan(url: str) -> Dict[str, Any]:
    result = {
        'urls': [],
        'forms': [],
        'js_files': [],
        'links': [],
        'emails': [],
        'comments': [],
        'error': None,
    }
    success, stdout, stderr = run_command(
        ['gospider', '-s', url, '--json'],
        timeout=60
    )
    if not success:
        result['error'] = stderr or 'gospider failed'
        return result
    for line in stdout.splitlines():
        try:
            entry = json.loads(line)
            etype = entry.get('type', '')
            data = entry.get('data', '')
            if etype == 'url':
                result['urls'].append(data)
            elif etype == 'form':
                result['forms'].append(data)
            elif etype == 'jsfile':
                result['js_files'].append(data)
            elif etype == 'link':
                result['links'].append(data)
            elif etype == 'email':
                result['emails'].append(data)
            elif etype == 'comment':
                result['comments'].append(data)
        except json.JSONDecodeError:
            continue
    return result


def _curl_crawl(url: str) -> Dict[str, Any]:
    result = {
        'urls': [],
        'forms': [],
        'js_files': [],
        'links': [],
        'emails': [],
        'comments': [],
        'error': None,
        'note': 'Using curl fallback (install gospider for deeper crawl)',
    }
    if not check_tool('curl'):
        result['error'] = 'curl not installed'
        return result
    success, stdout, _ = run_command(
        ['curl', '-sL', url],
        timeout=15
    )
    if not success:
        result['error'] = 'Failed to fetch page'
        return result
    body = stdout
    result['links'] = list(set(re.findall(r'href=["\'](https?://[^"\']+)["\']', body)))
    result['urls'] = list(set(re.findall(r'(https?://[^\s"\'<>]+)', body)))
    result['js_files'] = list(set(re.findall(r'src=["\']([^"\']+\.js[^"\']*)["\']', body)))
    result['emails'] = list(set(re.findall(r'([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})', body)))
    result['comments'] = list(set(re.findall(r'<!--(.*?)-->', body, re.DOTALL)))
    form_pattern = re.compile(r'<form[^>]*action=["\']([^"\']*)["\'][^>]*>', re.IGNORECASE)
    result['forms'] = list(set(form_pattern.findall(body)))
    return result
