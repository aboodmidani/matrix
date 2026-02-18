import re
import requests
from typing import Dict, Any

# Try to use python-Wappalyzer for primary detection
try:
    from Wappalyzer import Wappalyzer, WebPage
    _WAPPALYZER_AVAILABLE = True
except ImportError:
    _WAPPALYZER_AVAILABLE = False


# ── HTTP request ──────────────────────────────────────────────────────────────

_HEADERS = {
    'User-Agent': (
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
        'AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/120.0.0.0 Safari/537.36'
    ),
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
}


def scan_technologies(url: str) -> Dict[str, Any]:
    """Detect technologies using Wappalyzer (primary) + heuristics (always)."""
    try:
        resp = requests.get(url, timeout=15, allow_redirects=True, headers=_HEADERS)
    except Exception as e:
        return {'url': url, 'technologies': {}, 'status': 'error', 'error': str(e)}

    technologies: Dict[str, Any] = {}

    # ── Primary: python-Wappalyzer ────────────────────────────────────────────
    if _WAPPALYZER_AVAILABLE:
        try:
            wappalyzer = Wappalyzer.latest()
            webpage    = WebPage(url, resp.text, dict(resp.headers))
            detected   = wappalyzer.analyze_with_versions_and_categories(webpage)
            for name, info in detected.items():
                technologies[name] = {
                    'version':    info.get('version', ''),
                    'confidence': 90,
                    'categories': info.get('categories', []),
                }
        except Exception:
            pass  # Fall through to heuristics

    # ── Always run heuristics (fills gaps Wappalyzer misses) ─────────────────
    heuristic = _heuristic_detect(url, resp)
    for name, info in heuristic.items():
        if name not in technologies:
            technologies[name] = info
        elif info.get('version') and not technologies[name].get('version'):
            technologies[name]['version'] = info['version']

    return {'url': url, 'technologies': technologies, 'status': 'success'}


# ── Heuristic detection ───────────────────────────────────────────────────────

def _heuristic_detect(url: str, resp: requests.Response) -> Dict[str, Any]:
    techs: Dict[str, Any] = {}

    headers  = {k.lower(): v for k, v in resp.headers.items()}
    body     = resp.text
    body_low = body.lower()

    def add(name: str, version: str = '', confidence: int = 85):
        if name not in techs:
            techs[name] = {'version': version, 'confidence': confidence}
        elif version and not techs[name].get('version'):
            techs[name]['version'] = version

    def ver(pattern: str, text: str, flags=re.IGNORECASE) -> str:
        m = re.search(pattern, text, flags)
        return m.group(1).strip() if m else ''

    # ── Server ────────────────────────────────────────────────────────────────
    server = headers.get('server', '')
    if 'cloudflare' in server.lower():
        add('Cloudflare', confidence=100)
    elif 'nginx' in server.lower():
        add('Nginx', ver(r'nginx/([\d.]+)', server), 95)
    elif 'apache' in server.lower():
        add('Apache', ver(r'Apache/([\d.]+)', server), 95)
    elif 'microsoft-iis' in server.lower():
        add('IIS', ver(r'Microsoft-IIS/([\d.]+)', server), 95)
    elif 'litespeed' in server.lower():
        add('LiteSpeed', confidence=95)
    elif 'openresty' in server.lower():
        add('OpenResty', confidence=90)
    elif 'caddy' in server.lower():
        add('Caddy', confidence=90)
    elif 'gunicorn' in server.lower():
        add('Gunicorn', ver(r'gunicorn/([\d.]+)', server), 90)
    elif 'uvicorn' in server.lower():
        add('Uvicorn', confidence=90)
    elif 'node' in server.lower():
        add('Node.js', confidence=80)
    elif 'werkzeug' in server.lower():
        add('Flask', confidence=85)

    # ── CDN / proxy ───────────────────────────────────────────────────────────
    if 'cf-ray' in headers:
        add('Cloudflare', confidence=100)
    if 'x-amz-cf-id' in headers or 'x-amz-cf-pop' in headers:
        add('Amazon CloudFront', confidence=100)
    if 'x-fastly-request-id' in headers or 'fastly-restarts' in headers:
        add('Fastly', confidence=100)
    if 'x-cache' in headers and 'varnish' in headers.get('x-cache', '').lower():
        add('Varnish', confidence=90)
    if 'x-akamai-transformed' in headers:
        add('Akamai', confidence=95)
    if 'x-sucuri-id' in headers:
        add('Sucuri', confidence=100)
    if 'x-vercel-id' in headers:
        add('Vercel', confidence=100)
    if 'x-nf-request-id' in headers:
        add('Netlify', confidence=100)
    if 'x-azure-ref' in headers:
        add('Microsoft Azure', confidence=95)
    if 'x-amzn-requestid' in headers or 'x-amz-request-id' in headers:
        add('AWS', confidence=85)

    # ── Language / runtime ────────────────────────────────────────────────────
    powered = headers.get('x-powered-by', '')
    if powered:
        if 'php' in powered.lower():
            add('PHP', ver(r'PHP/([\d.]+)', powered), 95)
        if 'asp.net' in powered.lower():
            add('ASP.NET', ver(r'ASP\.NET(?: ([\d.]+))?', powered), 95)
        if 'express' in powered.lower():
            add('Express', confidence=90)
        if 'next.js' in powered.lower():
            add('Next.js', ver(r'Next\.js ([\d.]+)', powered), 95)
        if 'nuxt' in powered.lower():
            add('Nuxt.js', confidence=90)
    if 'x-php-version' in headers:
        add('PHP', headers['x-php-version'], 100)

    # ── CMS ───────────────────────────────────────────────────────────────────
    if 'wp-content' in body_low or 'wp-includes' in body_low or '/wp-json/' in body_low:
        add('WordPress', ver(r'<meta[^>]+generator[^>]+WordPress ([\d.]+)', body), 95)
    if 'drupal' in body_low or '/sites/default/files/' in body_low:
        add('Drupal', ver(r'Drupal ([\d.]+)', body), 90)
    if 'joomla' in body_low or '/media/jui/' in body_low:
        add('Joomla', confidence=90)
    if 'shopify' in body_low or 'cdn.shopify.com' in body_low:
        add('Shopify', confidence=95)
    if 'squarespace' in body_low or 'static.squarespace.com' in body_low:
        add('Squarespace', confidence=95)
    if 'wix.com' in body_low or 'wixsite.com' in body_low:
        add('Wix', confidence=95)
    if 'ghost' in body_low and 'ghost.io' in body_low:
        add('Ghost', confidence=85)
    if 'typo3' in body_low:
        add('TYPO3', confidence=85)
    if 'magento' in body_low or 'mage/' in body_low:
        add('Magento', ver(r'Magento/([\d.]+)', body), 90)
    if 'prestashop' in body_low:
        add('PrestaShop', confidence=85)
    if 'opencart' in body_low:
        add('OpenCart', confidence=85)
    if 'woocommerce' in body_low:
        add('WooCommerce', confidence=90)
    if 'webflow' in body_low or 'webflow.com' in body_low:
        add('Webflow', confidence=90)
    if 'contentful' in body_low:
        add('Contentful', confidence=85)
    if 'sanity.io' in body_low:
        add('Sanity', confidence=85)

    # ── JS frameworks ─────────────────────────────────────────────────────────
    if ('__react' in body or 'reactdom' in body_low or 'data-reactroot' in body_low
            or 'react.development.js' in body_low or 'react.production.min.js' in body_low):
        add('React', ver(r'react[@/]([\d.]+)', body_low), 85)
    if ('__vue' in body or 'v-app' in body_low or 'data-v-' in body
            or 'vue.runtime' in body_low or 'createapp' in body_low):
        add('Vue.js', ver(r'vue[@/]([\d.]+)', body_low), 85)
    if ('ng-version' in body_low or 'ng-app' in body_low or '_nghost' in body
            or 'angular.min.js' in body_low):
        add('Angular', ver(r'ng-version="([\d.]+)"', body), 85)
    if '__svelte' in body or 'svelte-' in body_low:
        add('Svelte', confidence=80)
    if 'ember-application' in body_low or 'ember.min.js' in body_low:
        add('Ember.js', confidence=80)
    if 'backbone.js' in body_low or 'backbone.min.js' in body_low:
        add('Backbone.js', confidence=75)
    if 'jquery' in body_low:
        add('jQuery', ver(r'jquery[/-]([\d.]+)', body_low), 80)
    if 'bootstrap' in body_low:
        add('Bootstrap', ver(r'bootstrap[/-]([\d.]+)', body_low), 75)
    if 'tailwind' in body_low:
        add('Tailwind CSS', confidence=75)
    if '_next/static' in body_low or '__next_data__' in body_low:
        add('Next.js', confidence=90)
    if '__nuxt' in body or '_nuxt/' in body:
        add('Nuxt.js', confidence=90)
    if 'gatsby-' in body_low and 'gatsby' in body_low:
        add('Gatsby', confidence=85)
    if 'astro-island' in body_low or 'astro-slot' in body_low:
        add('Astro', confidence=85)
    if 'alpinejs' in body_low or 'x-data=' in body_low:
        add('Alpine.js', confidence=80)
    if 'htmx' in body_low:
        add('htmx', confidence=80)
    if 'stimulus' in body_low and 'data-controller' in body_low:
        add('Stimulus', confidence=75)

    # ── Backend frameworks ────────────────────────────────────────────────────
    if 'laravel' in body_low or 'laravel_session' in headers.get('set-cookie', '').lower():
        add('Laravel', confidence=85)
    if 'csrfmiddlewaretoken' in body_low or 'django' in body_low:
        add('Django', confidence=85)
    if 'x-runtime' in headers and ('rails' in body_low or 'rack.session' in headers.get('set-cookie', '').lower()):
        add('Ruby on Rails', confidence=85)
    if 'werkzeug' in server.lower() or 'flask' in body_low:
        add('Flask', confidence=80)
    if 'fastapi' in body_low:
        add('FastAPI', confidence=85)
    if 'x-application-context' in headers:
        add('Spring', confidence=80)
    if 'strapi' in body_low:
        add('Strapi', confidence=85)
    if 'symfony' in body_low:
        add('Symfony', confidence=80)
    if 'codeigniter' in body_low:
        add('CodeIgniter', confidence=80)
    if 'yii' in body_low and 'yii2' in body_low:
        add('Yii', confidence=80)

    # ── Analytics & marketing ─────────────────────────────────────────────────
    if 'google-analytics.com' in body_low or 'gtag(' in body_low:
        add('Google Analytics', confidence=90)
    if 'googletagmanager.com' in body_low:
        add('Google Tag Manager', confidence=90)
    if 'hotjar' in body_low:
        add('Hotjar', confidence=90)
    if 'segment.com' in body_low or 'analytics.js' in body_low:
        add('Segment', confidence=85)
    if 'mixpanel' in body_low:
        add('Mixpanel', confidence=85)
    if 'intercom' in body_low:
        add('Intercom', confidence=85)
    if 'hs-scripts.com' in body_low or 'hubspot' in body_low:
        add('HubSpot', confidence=85)
    if 'crisp.chat' in body_low:
        add('Crisp', confidence=85)
    if 'zendesk' in body_low:
        add('Zendesk', confidence=85)
    if 'fbevents.js' in body_low or 'facebook.net/en_US/fbevents' in body_low:
        add('Facebook Pixel', confidence=90)
    if 'tiktok' in body_low and 'analytics' in body_low:
        add('TikTok Pixel', confidence=80)
    if 'clarity.ms' in body_low:
        add('Microsoft Clarity', confidence=90)
    if 'plausible.io' in body_low:
        add('Plausible Analytics', confidence=90)
    if 'umami' in body_low and 'script.js' in body_low:
        add('Umami', confidence=80)

    # ── Security ──────────────────────────────────────────────────────────────
    if 'x-fw-hash' in headers or 'x-fw-server' in headers:
        add('Wordfence', confidence=90)
    if 'recaptcha' in body_low or 'recaptcha.net' in body_low:
        add('reCAPTCHA', confidence=90)
    if 'hcaptcha' in body_low:
        add('hCaptcha', confidence=90)
    if 'turnstile' in body_low and 'cloudflare' in body_low:
        add('Cloudflare Turnstile', confidence=90)

    # ── Hosting / infra ───────────────────────────────────────────────────────
    if 'vercel' in body_low:
        add('Vercel', confidence=90)
    if 'netlify' in body_low:
        add('Netlify', confidence=90)
    if 'heroku' in headers.get('server', '').lower():
        add('Heroku', confidence=90)

    # ── UI libraries ──────────────────────────────────────────────────────────
    if 'fonts.googleapis.com' in body_low:
        add('Google Fonts', confidence=90)
    if 'fontawesome' in body_low:
        add('Font Awesome', ver(r'fontawesome[/-]([\d.]+)', body_low), 85)
    if 'material-ui' in body_low or '"@mui/' in body_low:
        add('Material UI', confidence=80)
    if 'chakra-ui' in body_low:
        add('Chakra UI', confidence=80)
    if 'ant-design' in body_low or '"antd"' in body_low:
        add('Ant Design', confidence=80)
    if 'shadcn' in body_low:
        add('shadcn/ui', confidence=80)
    if 'radix-ui' in body_low:
        add('Radix UI', confidence=80)

    # ── Cookie / session hints ────────────────────────────────────────────────
    cookies = headers.get('set-cookie', '').lower()
    if 'phpsessid' in cookies:
        add('PHP', confidence=85)
    if 'asp.net_sessionid' in cookies or 'aspsessionid' in cookies:
        add('ASP.NET', confidence=90)
    if 'jsessionid' in cookies:
        add('Java', confidence=80)
    if 'laravel_session' in cookies:
        add('Laravel', confidence=90)
    if 'csrftoken' in cookies:
        add('Django', confidence=85)
    if '_rails' in cookies or 'rack.session' in cookies:
        add('Ruby on Rails', confidence=85)
    if '_ga' in cookies:
        add('Google Analytics', confidence=85)

    # ── Meta generator ────────────────────────────────────────────────────────
    gen = ver(r'<meta[^>]+name=["\']generator["\'][^>]+content=["\']([^"\']+)["\']', body)
    if gen:
        parts   = gen.split(' ', 1)
        gname   = parts[0]
        gver    = parts[1] if len(parts) > 1 else ''
        add(gname, gver, 95)

    # ── Link header hints ─────────────────────────────────────────────────────
    link = headers.get('link', '').lower()
    if 'wp-json' in link:
        add('WordPress', confidence=95)
    if 'api.w.org' in link:
        add('WordPress', confidence=95)

    return techs
