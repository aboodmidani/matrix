import os
import sys
import tempfile
import logging
from typing import Dict, Any
from tools import check_tool, run_command

logger = logging.getLogger(__name__)

NULL_DEVICE = 'nul' if sys.platform == 'win32' else '/dev/null'

WORDLIST = [
    'admin', 'login', 'wp-admin', 'administrator', 'backup',
    '.git', '.env', 'config', 'robots.txt', 'sitemap.xml',
    'api', 'v1', 'v2', 'graphql', 'swagger', 'docs',
    'phpmyadmin', 'pma', 'mysql', 'db', 'database',
    'test', 'dev', 'staging', 'debug', 'info',
    'status', 'health', 'metrics', 'monitor', 'dashboard',
    'uploads', 'files', 'download', 'assets', 'static',
    'cgi-bin', 'bin', 'tmp', 'cache', 'logs',
    'install', 'setup', 'config.php', 'config.php.bak',
    '.htaccess', '.htpasswd', 'web.config', '.DS_Store',
    'index.php', 'index.html', 'default.aspx',
    'server-status', 'server-info', 'actuator', 'prometheus',
    'crossdomain.xml', 'clientaccesspolicy.xml',
    '.well-known/security.txt', '.well-known/acme-challenge',
]


def scan_directories(url: str) -> Dict[str, Any]:
    if check_tool('gobuster'):
        return _gobuster_scan(url)
    return _curl_based_scan(url)


def _gobuster_scan(url: str) -> Dict[str, Any]:
    result = {
        'found': [],
        'total_scanned': len(WORDLIST),
        'error': None,
    }
    tmp = tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False)
    try:
        tmp.write('\n'.join(WORDLIST))
        tmp.close()
        success, stdout, stderr = run_command(
            ['gobuster', 'dir', '-u', url, '-w', tmp.name, '-q', '-t', '20'],
            timeout=120
        )
        if success and stdout:
            for line in stdout.splitlines():
                if line.strip():
                    parts = line.split()
                    if len(parts) >= 2:
                        result['found'].append({
                            'path': parts[0],
                            'status': parts[1],
                        })
    except Exception as e:
        result['error'] = str(e)
    finally:
        if os.path.exists(tmp.name):
            try:
                os.unlink(tmp.name)
            except OSError:
                pass
    return result


def _curl_based_scan(url: str) -> Dict[str, Any]:
    result = {
        'found': [],
        'total_scanned': len(WORDLIST),
        'error': None,
        'note': 'Using curl fallback (install gobuster for faster scanning)',
    }
    if not check_tool('curl'):
        result['error'] = 'curl not installed'
        return result
    base = url.rstrip('/')
    base_success, base_stdout, _ = run_command(
        ['curl', '-s', '-o', NULL_DEVICE, '-w', '%{size_download}', base],
        timeout=10
    )
    base_size = int(base_stdout.strip()) if base_success and base_stdout.strip().isdigit() else None
    for path in WORDLIST:
        target = f'{base}/{path}'
        success, stdout, _ = run_command(
            ['curl', '-s', '-o', NULL_DEVICE, '-w', '%{http_code}:%{size_download}', target],
            timeout=5
        )
        if success and ':' in stdout:
            code, size_str = stdout.strip().split(':', 1)
            if code not in ['404', '301', '302']:
                try:
                    size = int(size_str) if size_str.isdigit() else 0
                    if base_size is None or abs(size - base_size) > 200:
                        result['found'].append({
                            'path': f'/{path}',
                            'status': int(code),
                        })
                except ValueError:
                    pass
    return result
