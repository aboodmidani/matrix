import re
import requests
from typing import Dict, Any


# ── HTTP request ──────────────────────────────────────────────────────────────

def scan_technologies(url: str) -> Dict[str, Any]:
    """Detect technologies via HTTP headers + HTML body analysis."""
    try:
        resp = requests.get(
            url,
            timeout=15,
            allow_redirects=True,
            headers={
                'User-Agent': (
                    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                    'AppleWebKit/537.36 (KHTML, like Gecko) '
                    'Chrome/120.0.0.0 Safari/537.36'
                ),
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
            }
        )
        technologies = _detect(url, resp)
        return {'url': url, 'technologies': technologies, 'status': 'success'}
    except Exception as e:
        return {'url': url, 'technologies': {}, 'status': 'error', 'error': str(e)}


# ── Core detection ────────────────────────────────────────────────────────────

def _detect(url: str, resp: requests.Response) -> Dict[str, Any]:
    techs: Dict[str, Any] = {}

    headers  = {k.lower(): v for k, v in resp.headers.items()}
    body     = resp.text
    body_low = body.lower()

    def add(name: str, version: str = '', confidence: int = 90):
        if name not in techs:
            techs[name] = {'version': version, 'confidence': confidence}
        elif version and not techs[name]['version']:
            techs[name]['version'] = version

    def ver(pattern: str, text: str, flags=re.IGNORECASE) -> str:
        """Extract version string from text using regex."""
        m = re.search(pattern, text, flags)
        return m.group(1).strip() if m else ''

    # ── Server / hosting ─────────────────────────────────────────────────────
    server = headers.get('server', '')
    if server:
        if 'cloudflare' in server.lower():
            add('Cloudflare', confidence=100)
        elif 'nginx' in server.lower():
            v = ver(r'nginx/([\d.]+)', server)
            add('Nginx', v, 95)
        elif 'apache' in server.lower():
            v = ver(r'Apache/([\d.]+)', server)
            add('Apache', v, 95)
        elif 'microsoft-iis' in server.lower():
            v = ver(r'Microsoft-IIS/([\d.]+)', server)
            add('IIS', v, 95)
        elif 'litespeed' in server.lower():
            add('LiteSpeed', confidence=95)
        elif 'openresty' in server.lower():
            add('OpenResty', confidence=90)
        elif 'caddy' in server.lower():
            add('Caddy', confidence=90)
        elif 'gunicorn' in server.lower():
            v = ver(r'gunicorn/([\d.]+)', server)
            add('Gunicorn', v, 90)
        elif 'uvicorn' in server.lower():
            add('Uvicorn', confidence=90)
        elif 'node' in server.lower():
            add('Node.js', confidence=80)

    # ── CDN / proxy ───────────────────────────────────────────────────────────
    if 'cf-ray' in headers:
        add('Cloudflare', confidence=100)
    if 'x-amz-cf-id' in headers or 'x-amz-cf-pop' in headers:
        add('Amazon CloudFront', confidence=100)
    if 'x-fastly-request-id' in headers or 'fastly-restarts' in headers:
        add('Fastly', confidence=100)
    if 'x-cache' in headers and 'varnish' in headers.get('x-cache', '').lower():
        add('Varnish', confidence=90)
    if 'x-akamai-transformed' in headers or 'akamai' in headers.get('server', '').lower():
        add('Akamai', confidence=95)
    if 'x-sucuri-id' in headers:
        add('Sucuri', confidence=100)
    if 'x-cdn' in headers:
        add('CDN', headers['x-cdn'], 70)

    # ── Language / runtime ────────────────────────────────────────────────────
    powered = headers.get('x-powered-by', '')
    if powered:
        if 'php' in powered.lower():
            v = ver(r'PHP/([\d.]+)', powered)
            add('PHP', v, 95)
        if 'asp.net' in powered.lower():
            v = ver(r'ASP\.NET(?: ([\d.]+))?', powered)
            add('ASP.NET', v, 95)
        if 'express' in powered.lower():
            add('Express', confidence=90)
        if 'next.js' in powered.lower():
            v = ver(r'Next\.js ([\d.]+)', powered)
            add('Next.js', v, 95)
        if 'nuxt' in powered.lower():
            add('Nuxt.js', confidence=90)

    # PHP version from header
    if 'x-php-version' in headers:
        add('PHP', headers['x-php-version'], 100)

    # ── CMS ───────────────────────────────────────────────────────────────────
    if 'wp-content' in body_low or 'wp-includes' in body_low or '/wp-json/' in body_low:
        v = ver(r'<meta[^>]+generator[^>]+WordPress ([\d.]+)', body)
        add('WordPress', v, 95)
    if 'drupal' in body_low or '/sites/default/files/' in body_low:
        v = ver(r'Drupal ([\d.]+)', body)
        add('Drupal', v, 90)
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
        v = ver(r'Magento/([\d.]+)', body)
        add('Magento', v, 90)
    if 'prestashop' in body_low:
        add('PrestaShop', confidence=85)
    if 'opencart' in body_low:
        add('OpenCart', confidence=85)
    if 'woocommerce' in body_low:
        add('WooCommerce', confidence=90)

    # ── JS frameworks ─────────────────────────────────────────────────────────
    if 'react' in body_low and ('__react' in body or 'reactdom' in body_low or 'data-reactroot' in body_low):
        v = ver(r'react[@/]([\d.]+)', body_low)
        add('React', v, 85)
    if 'vue' in body_low and ('__vue' in body or 'v-app' in body_low or 'data-v-' in body):
        v = ver(r'vue[@/]([\d.]+)', body_low)
        add('Vue.js', v, 85)
    if 'angular' in body_low and ('ng-version' in body_low or 'ng-app' in body_low or '_nghost' in body):
        v = ver(r'ng-version="([\d.]+)"', body)
        add('Angular', v, 85)
    if 'svelte' in body_low and '__svelte' in body:
        add('Svelte', confidence=80)
    if 'ember' in body_low and 'ember-application' in body_low:
        add('Ember.js', confidence=80)
    if 'backbone' in body_low and 'backbone.js' in body_low:
        add('Backbone.js', confidence=75)
    if 'jquery' in body_low:
        v = ver(r'jquery[/-]([\d.]+)', body_low)
        add('jQuery', v, 80)
    if 'bootstrap' in body_low:
        v = ver(r'bootstrap[/-]([\d.]+)', body_low)
        add('Bootstrap', v, 75)
    if 'tailwind' in body_low:
        add('Tailwind CSS', confidence=75)
    if 'next.js' in body_low or '_next/static' in body_low:
        v = ver(r'"version":"([\d.]+)".*?"next"', body)
        add('Next.js', v, 90)
    if 'nuxt' in body_low and ('__nuxt' in body or '_nuxt/' in body):
        add('Nuxt.js', confidence=90)
    if 'gatsby' in body_low and 'gatsby-' in body_low:
        add('Gatsby', confidence=85)
    if 'astro' in body_low and 'astro-' in body_low:
        add('Astro', confidence=80)

    # ── Backend frameworks ────────────────────────────────────────────────────
    if 'laravel' in body_low or 'laravel_session' in str(headers.get('set-cookie', '')).lower():
        add('Laravel', confidence=85)
    if 'django' in body_low or 'csrfmiddlewaretoken' in body_low:
        add('Django', confidence=85)
    if 'rails' in body_low and ('x-request-id' in headers or 'x-runtime' in headers):
        add('Ruby on Rails', confidence=80)
    if 'flask' in body_low or ('werkzeug' in headers.get('server', '').lower()):
        add('Flask', confidence=80)
    if 'fastapi' in body_low or 'fastapi' in headers.get('server', '').lower():
        add('FastAPI', confidence=85)
    if 'spring' in body_low and 'x-application-context' in headers:
        add('Spring', confidence=80)
    if 'strapi' in body_low:
        add('Strapi', confidence=85)

    # ── Analytics & tracking ──────────────────────────────────────────────────
    if 'google-analytics.com' in body_low or 'gtag(' in body_low or 'ga(' in body_low:
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
    if 'hubspot' in body_low or 'hs-scripts.com' in body_low:
        add('HubSpot', confidence=85)
    if 'crisp.chat' in body_low or 'crisp-client' in body_low:
        add('Crisp', confidence=85)
    if 'zendesk' in body_low:
        add('Zendesk', confidence=85)
    if 'facebook.net' in body_low or 'fbevents.js' in body_low:
        add('Facebook Pixel', confidence=85)

    # ── Security / WAF ────────────────────────────────────────────────────────
    if 'x-sucuri-id' in headers:
        add('Sucuri WAF', confidence=100)
    if 'x-fw-hash' in headers or 'x-fw-server' in headers:
        add('Wordfence', confidence=90)
    if 'recaptcha' in body_low or 'recaptcha.net' in body_low:
        add('reCAPTCHA', confidence=90)
    if 'hcaptcha' in body_low:
        add('hCaptcha', confidence=90)

    # ── Hosting / infrastructure ──────────────────────────────────────────────
    if 'vercel' in body_low or 'x-vercel-id' in headers:
        add('Vercel', confidence=95)
    if 'netlify' in body_low or 'x-nf-request-id' in headers:
        add('Netlify', confidence=95)
    if 'heroku' in headers.get('server', '').lower() or 'x-heroku-queue-wait-time' in headers:
        add('Heroku', confidence=90)
    if 'x-amzn-requestid' in headers or 'x-amz-request-id' in headers:
        add('AWS', confidence=85)
    if 'x-azure-ref' in headers:
        add('Microsoft Azure', confidence=90)
    if 'x-goog-' in str(headers) or 'google.com/recaptcha' in body_low:
        add('Google Cloud', confidence=75)

    # ── Fonts & UI libs ───────────────────────────────────────────────────────
    if 'fonts.googleapis.com' in body_low:
        add('Google Fonts', confidence=90)
    if 'fontawesome' in body_low:
        add('Font Awesome', confidence=85)
    if 'material-ui' in body_low or 'mui' in body_low:
        add('Material UI', confidence=75)
    if 'chakra-ui' in body_low:
        add('Chakra UI', confidence=75)
    if 'ant-design' in body_low or 'antd' in body_low:
        add('Ant Design', confidence=75)

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
    if 'django' in cookies or 'csrftoken' in cookies:
        add('Django', confidence=85)
    if '_rails' in cookies or 'rack.session' in cookies:
        add('Ruby on Rails', confidence=85)

    # ── Meta generator tag ────────────────────────────────────────────────────
    gen = ver(r'<meta[^>]+name=["\']generator["\'][^>]+content=["\']([^"\']+)["\']', body)
    if gen:
        name = gen.split(' ')[0]
        version = gen.split(' ')[1] if ' ' in gen else ''
        add(name, version, 95)

    return techs
