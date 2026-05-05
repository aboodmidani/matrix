import re
import logging
import requests
from typing import Dict, Any

logger = logging.getLogger(__name__)

# Try to use python-Wappalyzer for primary detection
try:
    from Wappalyzer import Wappalyzer, WebPage
    _WAPPALYZER_AVAILABLE = True
except ImportError:
    _WAPPALYZER_AVAILABLE = False

# Cache the Wappalyzer instance
_wappalyzer_instance = None


def _get_wappalyzer():
    """Get or create a cached Wappalyzer instance."""
    global _wappalyzer_instance
    if _wappalyzer_instance is None:
        try:
            _wappalyzer_instance = Wappalyzer.latest()
        except Exception as e:
            logger.debug("Failed to initialize Wappalyzer: %s", e)
    return _wappalyzer_instance


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
        logger.debug("HTTP request failed for %s: %s", url, e)
        return {'url': url, 'technologies': {}, 'status': 'error', 'error': str(e)}

    technologies: Dict[str, Any] = {}

    # ── Primary: python-Wappalyzer ────────────────────────────────────────────
    if _WAPPALYZER_AVAILABLE:
        try:
            wappalyzer = _get_wappalyzer()
            if wappalyzer:
                webpage = WebPage(url, resp.text, dict(resp.headers))
                detected = wappalyzer.analyze_with_versions_and_categories(webpage)
                for name, info in detected.items():
                    technologies[name] = {
                        'version':    info.get('version', ''),
                        'confidence': 90,
                        'categories': info.get('categories', []),
                    }
        except Exception as e:
            logger.debug("Wappalyzer analysis failed: %s", e)

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

    def add(name: str, version: str = '', confidence: int = 85, categories: list = None):
        if name not in techs:
            techs[name] = {'version': version, 'confidence': confidence}
            if categories:
                techs[name]['categories'] = categories
        elif version and not techs[name].get('version'):
            techs[name]['version'] = version

    def ver(pattern: str, text: str, flags=re.IGNORECASE) -> str:
        m = re.search(pattern, text, flags)
        return m.group(1).strip() if m else ''

    # ── Server ────────────────────────────────────────────────────────────────
    server = headers.get('server', '')
    server_lower = server.lower()
    if 'cloudflare' in server_lower:
        add('Cloudflare', confidence=100, categories=['CDN'])
    elif 'nginx' in server_lower:
        add('Nginx', ver(r'nginx/([\d.]+)', server), 95, categories=['Web servers'])
    elif 'apache' in server_lower:
        add('Apache', ver(r'Apache/([\d.]+)', server), 95, categories=['Web servers'])
    elif 'microsoft-iis' in server_lower:
        add('IIS', ver(r'Microsoft-IIS/([\d.]+)', server), 95, categories=['Web servers'])
    elif 'litespeed' in server_lower:
        add('LiteSpeed', confidence=95, categories=['Web servers'])
    elif 'openresty' in server_lower:
        add('OpenResty', confidence=90, categories=['Web servers'])
    elif 'caddy' in server_lower:
        add('Caddy', confidence=90, categories=['Web servers'])
    elif 'gunicorn' in server_lower:
        add('Gunicorn', ver(r'gunicorn/([\d.]+)', server), 90, categories=['Web servers'])
    elif 'uvicorn' in server_lower:
        add('Uvicorn', confidence=90, categories=['Web servers'])
    elif 'node' in server_lower:
        add('Node.js', confidence=80, categories=['Web servers'])
    elif 'werkzeug' in server_lower:
        add('Flask', confidence=85, categories=['Web frameworks'])
    elif 'tomcat' in server_lower:
        add('Apache Tomcat', ver(r'Apache Tomcat/([\d.]+)', server), 90, categories=['Web servers'])
    elif 'jetty' in server_lower:
        add('Jetty', ver(r'Jetty\(([\d.]+)', server), 90, categories=['Web servers'])
    elif 'weblogic' in server_lower:
        add('Oracle WebLogic', confidence=90, categories=['Web servers'])
    elif 'lighttpd' in server_lower:
        add('lighttpd', confidence=90, categories=['Web servers'])

    # ── CDN / proxy ───────────────────────────────────────────────────────────
    if 'cf-ray' in headers:
        add('Cloudflare', confidence=100, categories=['CDN'])
    if 'x-amz-cf-id' in headers or 'x-amz-cf-pop' in headers:
        add('Amazon CloudFront', confidence=100, categories=['CDN'])
    if 'x-fastly-request-id' in headers or 'fastly-restarts' in headers:
        add('Fastly', confidence=100, categories=['CDN'])
    if 'x-cache' in headers and 'varnish' in headers.get('x-cache', '').lower():
        add('Varnish', confidence=90, categories=['Caching'])
    if 'x-akamai-transformed' in headers:
        add('Akamai', confidence=95, categories=['CDN'])
    if 'x-sucuri-id' in headers:
        add('Sucuri', confidence=100, categories=['Security'])
    if 'x-vercel-id' in headers:
        add('Vercel', confidence=100, categories=['Hosting'])
    if 'x-nf-request-id' in headers:
        add('Netlify', confidence=100, categories=['Hosting'])
    if 'x-azure-ref' in headers:
        add('Microsoft Azure', confidence=95, categories=['CDN'])
    if 'x-amzn-requestid' in headers or 'x-amz-request-id' in headers:
        add('AWS', confidence=85, categories=['Hosting'])
    if 'x-goog-generation' in headers:
        add('Google Cloud', confidence=90, categories=['Hosting'])
    if 'x-served-by' in headers and 'stackpath' in headers.get('x-served-by', '').lower():
        add('StackPath', confidence=95, categories=['CDN'])
    if 'server' in headers and 'bunnycdn' in headers.get('server', '').lower():
        add('BunnyCDN', confidence=95, categories=['CDN'])

    # ── Language / runtime ────────────────────────────────────────────────────
    powered = headers.get('x-powered-by', '')
    if powered:
        if 'php' in powered.lower():
            add('PHP', ver(r'PHP/([\d.]+)', powered), 95, categories=['Programming languages'])
        if 'asp.net' in powered.lower():
            add('ASP.NET', ver(r'ASP\.NET(?: ([\d.]+))?', powered), 95, categories=['Web frameworks'])
        if 'express' in powered.lower():
            add('Express', confidence=90, categories=['Web frameworks'])
        if 'next.js' in powered.lower():
            add('Next.js', ver(r'Next\.js ([\d.]+)', powered), 95, categories=['Web frameworks'])
        if 'nuxt' in powered.lower():
            add('Nuxt.js', confidence=90, categories=['Web frameworks'])
    if 'x-php-version' in headers:
        add('PHP', headers['x-php-version'], 100, categories=['Programming languages'])
    if 'x-runtime' in headers:
        if 'rails' in body_low or 'rack.session' in headers.get('set-cookie', '').lower():
            add('Ruby on Rails', confidence=85, categories=['Web frameworks'])
    if 'x-aspnet-version' in headers:
        add('ASP.NET', headers['x-aspnet-version'], 95, categories=['Web frameworks'])

    # ── CMS ───────────────────────────────────────────────────────────────────
    if 'wp-content' in body_low or 'wp-includes' in body_low or '/wp-json/' in body_low:
        add('WordPress', ver(r'<meta[^>]+generator[^>]+WordPress ([\d.]+)', body), 95, categories=['CMS'])
    if 'drupal' in body_low or '/sites/default/files/' in body_low:
        add('Drupal', ver(r'Drupal ([\d.]+)', body), 90, categories=['CMS'])
    if 'joomla' in body_low or '/media/jui/' in body_low:
        add('Joomla', confidence=90, categories=['CMS'])
    if 'shopify' in body_low or 'cdn.shopify.com' in body_low:
        add('Shopify', confidence=95, categories=['E-commerce'])
    if 'squarespace' in body_low or 'static.squarespace.com' in body_low:
        add('Squarespace', confidence=95, categories=['CMS'])
    if 'wix.com' in body_low or 'wixsite.com' in body_low:
        add('Wix', confidence=95, categories=['CMS'])
    if 'ghost' in body_low and 'ghost.io' in body_low:
        add('Ghost', confidence=85, categories=['CMS'])
    if 'typo3' in body_low:
        add('TYPO3', confidence=85, categories=['CMS'])
    if 'magento' in body_low or 'mage/' in body_low:
        add('Magento', ver(r'Magento/([\d.]+)', body), 90, categories=['E-commerce'])
    if 'prestashop' in body_low:
        add('PrestaShop', confidence=85, categories=['E-commerce'])
    if 'opencart' in body_low:
        add('OpenCart', confidence=85, categories=['E-commerce'])
    if 'woocommerce' in body_low:
        add('WooCommerce', confidence=90, categories=['E-commerce'])
    if 'webflow' in body_low or 'webflow.com' in body_low:
        add('Webflow', confidence=90, categories=['CMS'])
    if 'contentful' in body_low:
        add('Contentful', confidence=85, categories=['CMS'])
    if 'sanity.io' in body_low:
        add('Sanity', confidence=85, categories=['CMS'])
    if 'strapi' in body_low:
        add('Strapi', confidence=85, categories=['CMS'])
    if 'craft cms' in body_low or 'craftcms' in body_low:
        add('Craft CMS', confidence=85, categories=['CMS'])

    # ── JS frameworks ─────────────────────────────────────────────────────────
    if ('__react' in body or 'reactdom' in body_low or 'data-reactroot' in body_low
            or 'react.development.js' in body_low or 'react.production.min.js' in body_low):
        add('React', ver(r'react[@/]([\d.]+)', body_low), 85, categories=['JavaScript frameworks'])
    if ('__vue' in body or 'v-app' in body_low or 'data-v-' in body
            or 'vue.runtime' in body_low or 'createapp' in body_low):
        add('Vue.js', ver(r'vue[@/]([\d.]+)', body_low), 85, categories=['JavaScript frameworks'])
    if ('ng-version' in body_low or 'ng-app' in body_low or '_nghost' in body
            or 'angular.min.js' in body_low):
        add('Angular', ver(r'ng-version="([\d.]+)"', body), 85, categories=['JavaScript frameworks'])
    if '__svelte' in body or 'svelte-' in body_low:
        add('Svelte', confidence=80, categories=['JavaScript frameworks'])
    if 'ember-application' in body_low or 'ember.min.js' in body_low:
        add('Ember.js', confidence=80, categories=['JavaScript frameworks'])
    if 'backbone.js' in body_low or 'backbone.min.js' in body_low:
        add('Backbone.js', confidence=75, categories=['JavaScript frameworks'])
    if 'jquery' in body_low:
        add('jQuery', ver(r'jquery[/-]([\d.]+)', body_low), 80, categories=['JavaScript libraries'])
    if 'bootstrap' in body_low:
        add('Bootstrap', ver(r'bootstrap[/-]([\d.]+)', body_low), 75, categories=['UI frameworks'])
    if 'tailwind' in body_low:
        add('Tailwind CSS', confidence=75, categories=['UI frameworks'])
    if '_next/static' in body_low or '__next_data__' in body_low:
        add('Next.js', confidence=90, categories=['Web frameworks'])
    if '__nuxt' in body or '_nuxt/' in body:
        add('Nuxt.js', confidence=90, categories=['Web frameworks'])
    if 'gatsby-' in body_low and 'gatsby' in body_low:
        add('Gatsby', confidence=85, categories=['Web frameworks'])
    if 'astro-island' in body_low or 'astro-slot' in body_low:
        add('Astro', confidence=85, categories=['Web frameworks'])
    if 'alpinejs' in body_low or 'x-data=' in body_low:
        add('Alpine.js', confidence=80, categories=['JavaScript libraries'])
    if 'htmx' in body_low:
        add('htmx', confidence=80, categories=['JavaScript libraries'])
    if 'stimulus' in body_low and 'data-controller' in body_low:
        add('Stimulus', confidence=75, categories=['JavaScript libraries'])
    if 'solid-js' in body_low or '$$type' in body:
        add('Solid.js', confidence=75, categories=['JavaScript frameworks'])
    if 'qwik' in body_low or 'qwikloader' in body_low:
        add('Qwik', confidence=80, categories=['JavaScript frameworks'])
    if 'remix' in body_low and 'remix-run' in body_low:
        add('Remix', confidence=80, categories=['Web frameworks'])

    # ── Backend frameworks ────────────────────────────────────────────────────
    if 'laravel' in body_low or 'laravel_session' in headers.get('set-cookie', '').lower():
        add('Laravel', confidence=85, categories=['Web frameworks'])
    if 'csrfmiddlewaretoken' in body_low or 'django' in body_low:
        add('Django', confidence=85, categories=['Web frameworks'])
    if 'werkzeug' in server_lower or 'flask' in body_low:
        add('Flask', confidence=80, categories=['Web frameworks'])
    if 'fastapi' in body_low:
        add('FastAPI', confidence=85, categories=['Web frameworks'])
    if 'x-application-context' in headers:
        add('Spring', confidence=80, categories=['Web frameworks'])
    if 'symfony' in body_low:
        add('Symfony', confidence=80, categories=['Web frameworks'])
    if 'codeigniter' in body_low:
        add('CodeIgniter', confidence=80, categories=['Web frameworks'])
    if 'yii' in body_low and 'yii2' in body_low:
        add('Yii', confidence=80, categories=['Web frameworks'])
    if 'nestjs' in body_low or '@nestjs' in body_low:
        add('NestJS', confidence=85, categories=['Web frameworks'])
    if 'koa' in body_low and 'koa-router' in body_low:
        add('Koa', confidence=80, categories=['Web frameworks'])
    if 'spring-boot' in body_low:
        add('Spring Boot', confidence=85, categories=['Web frameworks'])

    # ── Analytics & marketing ─────────────────────────────────────────────────
    if 'google-analytics.com' in body_low or 'gtag(' in body_low:
        add('Google Analytics', confidence=90, categories=['Analytics'])
    if 'googletagmanager.com' in body_low:
        add('Google Tag Manager', confidence=90, categories=['Tag managers'])
    if 'hotjar' in body_low:
        add('Hotjar', confidence=90, categories=['Analytics'])
    if 'segment.com' in body_low or 'analytics.js' in body_low:
        add('Segment', confidence=85, categories=['Analytics'])
    if 'mixpanel' in body_low:
        add('Mixpanel', confidence=85, categories=['Analytics'])
    if 'intercom' in body_low:
        add('Intercom', confidence=85, categories=['Live chat'])
    if 'hs-scripts.com' in body_low or 'hubspot' in body_low:
        add('HubSpot', confidence=85, categories=['Marketing'])
    if 'crisp.chat' in body_low:
        add('Crisp', confidence=85, categories=['Live chat'])
    if 'zendesk' in body_low:
        add('Zendesk', confidence=85, categories=['Customer support'])
    if 'fbevents.js' in body_low or 'facebook.net/en_US/fbevents' in body_low:
        add('Facebook Pixel', confidence=90, categories=['Analytics'])
    if 'tiktok' in body_low and 'analytics' in body_low:
        add('TikTok Pixel', confidence=80, categories=['Analytics'])
    if 'clarity.ms' in body_low:
        add('Microsoft Clarity', confidence=90, categories=['Analytics'])
    if 'plausible.io' in body_low:
        add('Plausible Analytics', confidence=90, categories=['Analytics'])
    if 'umami' in body_low and 'script.js' in body_low:
        add('Umami', confidence=80, categories=['Analytics'])
    if 'amplitude' in body_low:
        add('Amplitude', confidence=85, categories=['Analytics'])
    if 'heap' in body_low and 'heap.js' in body_low:
        add('Heap Analytics', confidence=85, categories=['Analytics'])
    if 'sentry' in body_low and 'sentry.io' in body_low:
        add('Sentry', confidence=90, categories=['Error tracking'])
    if 'logrocket' in body_low:
        add('LogRocket', confidence=85, categories=['Analytics'])
    if 'fullstory' in body_low:
        add('FullStory', confidence=85, categories=['Analytics'])
    if 'fathom' in body_low:
        add('Fathom Analytics', confidence=85, categories=['Analytics'])

    # ── Security ──────────────────────────────────────────────────────────────
    if 'x-fw-hash' in headers or 'x-fw-server' in headers:
        add('Wordfence', confidence=90, categories=['Security'])
    if 'recaptcha' in body_low or 'recaptcha.net' in body_low:
        add('reCAPTCHA', confidence=90, categories=['Security'])
    if 'hcaptcha' in body_low:
        add('hCaptcha', confidence=90, categories=['Security'])
    if 'turnstile' in body_low and 'cloudflare' in body_low:
        add('Cloudflare Turnstile', confidence=90, categories=['Security'])
    if 'x-sucuri-id' in headers:
        add('Sucuri WAF', confidence=95, categories=['Security'])
    if 'incapsula' in body_low or '_incapsula_resource' in body_low:
        add('Imperva', confidence=90, categories=['Security'])
    if 'datadome' in body_low or 'datadome' in headers.get('set-cookie', '').lower():
        add('DataDome', confidence=90, categories=['Security'])
    if 'perimeterx' in body_low or 'humansecurity' in body_low:
        add('HUMAN Security', confidence=85, categories=['Security'])
    if 'akamai-bot' in body_low:
        add('Akamai Bot Manager', confidence=85, categories=['Security'])

    # ── Hosting / infra ───────────────────────────────────────────────────────
    if 'vercel' in body_low:
        add('Vercel', confidence=90, categories=['Hosting'])
    if 'netlify' in body_low:
        add('Netlify', confidence=90, categories=['Hosting'])
    if 'heroku' in headers.get('server', '').lower():
        add('Heroku', confidence=90, categories=['Hosting'])
    if 'github' in body_low and 'github.io' in body_low:
        add('GitHub Pages', confidence=90, categories=['Hosting'])
    if 'firebase' in body_low:
        add('Firebase', confidence=85, categories=['Hosting'])
    if 'digitalocean' in body_low or 'x-do-orig' in headers:
        add('DigitalOcean', confidence=85, categories=['Hosting'])

    # ── UI libraries ──────────────────────────────────────────────────────────
    if 'fonts.googleapis.com' in body_low:
        add('Google Fonts', confidence=90, categories=['Fonts'])
    if 'fontawesome' in body_low:
        add('Font Awesome', ver(r'fontawesome[/-]([\d.]+)', body_low), 85, categories=['Fonts'])
    if 'material-ui' in body_low or '"@mui/' in body_low:
        add('Material UI', confidence=80, categories=['UI libraries'])
    if 'chakra-ui' in body_low:
        add('Chakra UI', confidence=80, categories=['UI libraries'])
    if 'ant-design' in body_low or '"antd"' in body_low:
        add('Ant Design', confidence=80, categories=['UI libraries'])
    if 'shadcn' in body_low:
        add('shadcn/ui', confidence=80, categories=['UI libraries'])
    if 'radix-ui' in body_low:
        add('Radix UI', confidence=80, categories=['UI libraries'])
    if 'styled-components' in body_low:
        add('styled-components', confidence=80, categories=['CSS-in-JS'])
    if 'emotion' in body_low and '@emotion' in body_low:
        add('Emotion', confidence=80, categories=['CSS-in-JS'])

    # ── Cookie / session hints ────────────────────────────────────────────────
    cookies = headers.get('set-cookie', '').lower()
    if 'phpsessid' in cookies:
        add('PHP', confidence=85, categories=['Programming languages'])
    if 'asp.net_sessionid' in cookies or 'aspsessionid' in cookies:
        add('ASP.NET', confidence=90, categories=['Web frameworks'])
    if 'jsessionid' in cookies:
        add('Java', confidence=80, categories=['Programming languages'])
    if 'laravel_session' in cookies:
        add('Laravel', confidence=90, categories=['Web frameworks'])
    if 'csrftoken' in cookies:
        add('Django', confidence=85, categories=['Web frameworks'])
    if '_rails' in cookies or 'rack.session' in cookies:
        add('Ruby on Rails', confidence=85, categories=['Web frameworks'])
    if '_ga' in cookies:
        add('Google Analytics', confidence=85, categories=['Analytics'])

    # ── Meta generator ────────────────────────────────────────────────────────
    gen = ver(r'<meta[^>]+name=["\']generator["\'][^>]+content=["\']([^"\']+)["\']', body)
    if gen:
        parts = gen.split(' ', 1)
        gname = parts[0]
        gver = parts[1] if len(parts) > 1 else ''
        add(gname, gver, 95)

    # ── Link header hints ─────────────────────────────────────────────────────
    link = headers.get('link', '').lower()
    if 'wp-json' in link:
        add('WordPress', confidence=95, categories=['CMS'])
    if 'api.w.org' in link:
        add('WordPress', confidence=95, categories=['CMS'])

    # ── Favicon hash (Shodan-style) ──────────────────────────────────────────
    try:
        favicon_url = url.rstrip('/') + '/favicon.ico'
        fav_resp = requests.get(favicon_url, timeout=5, headers=_HEADERS)
        if fav_resp.status_code == 200 and len(fav_resp.content) > 0:
            import hashlib
            import base64
            mmh3_hash = base64.b64encode(fav_resp.content).decode()
            techs['_favicon_hash'] = {'version': mmh3_hash, 'confidence': 100}
    except Exception:
        pass

    return techs
