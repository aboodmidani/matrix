import requests
from typing import Dict, Any


def scan_technologies(url: str) -> Dict[str, Any]:
    """Scan for technologies using basic HTTP analysis"""
    try:
        response = requests.get(url, timeout=10, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
        technologies = detect_technologies(url, response)
        
        return {
            'url': url,
            'technologies': technologies,
            'status': 'success'
        }
    except Exception as e:
        return {
            'url': url,
            'technologies': {},
            'status': 'error',
            'error': str(e)
        }


def detect_technologies(url: str, response: requests.Response) -> Dict[str, Any]:
    """Detect technologies from HTTP response"""
    technologies = {}
    
    headers = {k.lower(): v.lower() for k, v in response.headers.items()}
    server = headers.get('server', '')
    powered_by = headers.get('x-powered-by', '')
    content_type = headers.get('content-type', '')
    html_content = response.text.lower()
    
    # Server detection
    if 'cloudflare' in server:
        technologies['Cloudflare'] = {'version': '', 'confidence': 100}
    if 'nginx' in server:
        technologies['Nginx'] = {'version': '', 'confidence': 90}
    if 'apache' in server:
        technologies['Apache'] = {'version': '', 'confidence': 90}
    if 'microsoft-iis' in server:
        technologies['IIS'] = {'version': '', 'confidence': 90}
    
    # PHP detection
    if 'php' in powered_by:
        technologies['PHP'] = {'version': '', 'confidence': 90}
    
    # Framework detection from headers
    if 'laravel' in powered_by or 'laravel' in html_content:
        technologies['Laravel'] = {'version': '', 'confidence': 80}
    if 'express' in powered_by:
        technologies['Express'] = {'version': '', 'confidence': 80}
    if 'django' in powered_by:
        technologies['Django'] = {'version': '', 'confidence': 80}
    if 'next.js' in powered_by:
        technologies['Next.js'] = {'version': '', 'confidence': 80}
    if 'nuxt' in powered_by:
        technologies['Nuxt.js'] = {'version': '', 'confidence': 80}
    
    # CMS detection
    if 'wordpress' in html_content or 'wp-content' in html_content:
        technologies['WordPress'] = {'version': '', 'confidence': 90}
    if 'drupal' in html_content:
        technologies['Drupal'] = {'version': '', 'confidence': 80}
    if 'joomla' in html_content:
        technologies['Joomla'] = {'version': '', 'confidence': 80}
    
    # JavaScript frameworks
    if 'react' in html_content:
        technologies['React'] = {'version': '', 'confidence': 70}
    if 'vue' in html_content:
        technologies['Vue.js'] = {'version': '', 'confidence': 70}
    if 'angular' in html_content:
        technologies['Angular'] = {'version': '', 'confidence': 70}
    
    # CDN detection
    if 'cdn' in headers or 'cloudflare' in str(headers):
        technologies['CDN'] = {'version': '', 'confidence': 70}
    
    # If no technologies detected, add basic info
    if not technologies:
        technologies['Web Server'] = {'version': server or 'Unknown', 'confidence': 50}
    
    return technologies
