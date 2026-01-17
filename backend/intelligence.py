import requests
import socket
from urllib.parse import urlparse

def get_reverse_dns(ip):
    try:
        hostname, aliases, addresses = socket.gethostbyaddr(ip)
        return [hostname] + aliases
    except Exception as e:
        return ["No reverse DNS found"]

def get_related_hostnames(domain):
    """Enhanced hostname discovery using DNS enumeration"""
    hostnames = set()

    # Add the original domain
    hostnames.add(domain)

    try:
        # Try common subdomain enumeration
        common_prefixes = ['www', 'mail', 'ftp', 'admin', 'api', 'dev', 'test', 'staging', 'blog', 'shop', 'app']

        for prefix in common_prefixes:
            try:
                subdomain = f"{prefix}.{domain}"
                # Quick DNS resolution check
                socket.gethostbyname(subdomain)
                hostnames.add(subdomain)
            except:
                pass

        # Try reverse DNS if domain resolves to IP
        try:
            ip = socket.gethostbyname(domain)
            reverse_hostnames = get_reverse_dns(ip)
            hostnames.update(reverse_hostnames)
        except:
            pass

    except Exception as e:
        pass

    # Remove "No reverse DNS found" if present
    hostnames.discard("No reverse DNS found")

    return list(hostnames) if hostnames else ["No hostnames found"]

def get_ip_info(ip):
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}", timeout=5)
        if response.status_code == 200:
            data = response.json()
            return {
                "country": data.get("country"),
                "countryCode": data.get("countryCode"),
                "region": data.get("regionName"),
                "city": data.get("city"),
                "isp": data.get("isp"),
                "org": data.get("org"),
                "as": data.get("as"),
                "lat": data.get("lat"),
                "lon": data.get("lon")
            }
    except Exception as e:
        pass
    return {"error": "Could not retrieve IP information"}

def detect_technologies(url):
    """Advanced web technology detection using pure Python - no external tools required"""
    technologies = []

    try:
        # Get the main page
        response = requests.get(url, timeout=5, verify=False)
        headers = response.headers
        html = response.text.lower()

        # 1. Server Detection
        server = headers.get('Server', '')
        if server:
            technologies.append({
                "category": "Server",
                "name": server,
                "confidence": "High",
                "icon": get_technology_icon(server)
            })

        # 2. Framework Detection from Headers
        framework_headers = {
            'x-powered-by': 'Framework',
            'x-aspnet-version': 'ASP.NET',
            'x-generator': 'Generator',
            'x-drupal-cache': 'Drupal',
            'x-joomla-version': 'Joomla'
        }

        for header, category in framework_headers.items():
            if header in headers:
                value = headers[header]
                technologies.append({
                    "category": category,
                    "name": value,
                    "confidence": "High",
                    "icon": get_technology_icon(value)
                })

        # 3. Content Management Systems
        cms_patterns = {
            "WordPress": ["wp-content", "wp-includes", "wp-admin", "wordpress", "wp-json", "/wp-login.php"],
            "Joomla": ["joomla", "com_content", "/administrator/", "option=com_"],
            "Drupal": ["drupal", "sites/default", "sites/all", "/node/", "/user/"],
            "Magento": ["magento", "var/cache", "skin/frontend", "Mage.Cookies"],
            "PrestaShop": ["prestashop", "classes/controller", "/modules/", "id_product"],
            "OpenCart": ["opencart", "catalog/view", "admin/view", "route=common/home"],
            "Shopify": ["shopify", "cdn.shopify.com", "myshopify.com", "Shopify.theme"],
            "Wix": ["wix", "wixstatic.com", "wix.com", "_wix"],
            "Squarespace": ["squarespace", "squarespace.com", "static.squarespace.com"],
            "Weebly": ["weebly", "weebly.com", "editor.weebly.com"]
        }

        for cms, patterns in cms_patterns.items():
            if any(pattern in html for pattern in patterns):
                technologies.append({
                    "category": "CMS",
                    "name": cms,
                    "confidence": "High",
                    "icon": get_technology_icon(cms)
                })
                break  # Only detect one CMS

        # 4. Web Frameworks & Libraries
        framework_patterns = {
            "React": ["react", "react-dom", "_react", "reactjs", "jsx"],
            "Vue.js": ["vue", "vue-router", "vuejs", "_vue", "nuxt"],
            "Angular": ["angular", "ng-app", "ng-controller", "angularjs", "ng-version"],
            "jQuery": ["jquery", "jquery.min.js", "jquery.js", "$("],
            "Bootstrap": ["bootstrap", "bootstrap.min.css", "bootstrap.css"],
            "Tailwind CSS": ["tailwind", "tailwindcss", "tailwind.config"],
            "Laravel": ["laravel", "_token", "csrf-token", "laravel_session"],
            "Django": ["csrfmiddlewaretoken", "django", "csrftoken"],
            "Express": ["express", "x-powered-by.*express"],
            "Ruby on Rails": ["rails", "csrf-token", "authenticity_token"],
            "ASP.NET": ["asp.net", "__VIEWSTATE", "__EVENTVALIDATION"],
            "Spring": ["spring", "springframework", "spring-boot"],
            "Next.js": ["nextjs", "_next", "next/head", "next/router"],
            "Nuxt.js": ["nuxt", "__nuxt", "nuxt.config"],
            "Gatsby": ["gatsby", "__gatsby", "gatsby-browser"],
            "Svelte": ["svelte", "__svelte"]
        }

        found_frameworks = set()
        for framework, patterns in framework_patterns.items():
            if any(pattern in html for pattern in patterns):
                if framework not in found_frameworks:
                    technologies.append({
                        "category": "Framework" if framework in ["React", "Vue.js", "Angular", "Laravel", "Django", "Express", "Rails", "Spring", "Next.js", "Nuxt.js", "Gatsby", "Svelte"] else "Library",
                        "name": framework,
                        "confidence": "Medium",
                        "icon": get_technology_icon(framework)
                    })
                    found_frameworks.add(framework)

        # 5. Programming Languages
        language_patterns = {
            "PHP": ["php", "x-powered-by.*php", "<?php", "<?= "],
            "Python": ["python", "django", "flask", "fastapi", "tornado"],
            "Node.js": ["node", "nodejs", "express", "npm"],
            "Ruby": ["ruby", "rails", "sinatra", "gem"],
            "Java": ["java", "jsp", "servlet", "spring", "tomcat"],
            "Go": ["go", "golang", "gin-gonic"],
            "C#": [".net", "asp.net", "csharp", "dotnet"]
        }

        for language, patterns in language_patterns.items():
            if any(pattern in html for pattern in patterns) or any(pattern in str(headers) for pattern in patterns):
                technologies.append({
                    "category": "Language",
                    "name": language,
                    "confidence": "Medium",
                    "icon": get_technology_icon(language)
                })
                break  # Usually only one server-side language

        # 6. Web Servers
        server_patterns = {
            "Apache": ["apache", "httpd", "mod_", "apache/2"],
            "Nginx": ["nginx", "ngx_http", "nginx/1"],
            "IIS": ["iis", "microsoft-iis", "asp.net"],
            "LiteSpeed": ["litespeed", "lsws"],
            "Caddy": ["caddy", "caddyserver"],
            "Tomcat": ["tomcat", "apache-tomcat"],
            "JBoss": ["jboss", "wildfly"],
            "WebLogic": ["weblogic", "bea"]
        }

        for server_name, patterns in server_patterns.items():
            if any(pattern in str(headers).lower() for pattern in patterns):
                technologies.append({
                    "category": "Web Server",
                    "name": server_name,
                    "confidence": "High",
                    "icon": get_technology_icon(server_name)
                })
                break

        # 7. Databases (inferred from patterns)
        db_patterns = {
            "MySQL": ["mysql", "mysqli", "pdo_mysql"],
            "PostgreSQL": ["postgresql", "pdo_pgsql", "pg_"],
            "MongoDB": ["mongodb", "mongoose", "mongo"],
            "Redis": ["redis", "predis"],
            "SQLite": ["sqlite", "pdo_sqlite"],
            "Oracle": ["oracle", "oci_", "pdo_oci"],
            "SQL Server": ["sqlsrv", "pdo_sqlsrv", "mssql"]
        }

        for db, patterns in db_patterns.items():
            if any(pattern in html for pattern in patterns):
                technologies.append({
                    "category": "Database",
                    "name": db,
                    "confidence": "Low",
                    "icon": get_technology_icon(db)
                })

        # 8. CDNs & Cloud Services
        cdn_patterns = {
            "Cloudflare": ["cf-ray", "cloudflare", "cf-browser-verification"],
            "Akamai": ["akamai", "akaamai", "akamai.net"],
            "Fastly": ["fastly", "fastly.net"],
            "CloudFront": ["cloudfront", "amazonaws.com"],
            "MaxCDN": ["maxcdn", "netdna-cdn.com"],
            "KeyCDN": ["keycdn", "kxcdn.com"]
        }

        for cdn, patterns in cdn_patterns.items():
            if any(pattern in str(headers).lower() for pattern in patterns):
                technologies.append({
                    "category": "CDN",
                    "name": cdn,
                    "confidence": "High",
                    "icon": get_technology_icon(cdn)
                })

        # 9. Analytics & Marketing
        analytics_patterns = {
            "Google Analytics": ["googletagmanager", "google-analytics", "gtag", "ga("],
            "Facebook Pixel": ["facebook", "fbq(", "connect.facebook.net"],
            "Hotjar": ["hotjar", "_hj"],
            "Mixpanel": ["mixpanel", "mixpanel.com"],
            "Segment": ["segment", "segment.com"]
        }

        for analytics, patterns in analytics_patterns.items():
            if any(pattern in html for pattern in patterns):
                technologies.append({
                    "category": "Analytics",
                    "name": analytics,
                    "confidence": "Medium",
                    "icon": get_technology_icon("default")
                })

        # Remove duplicates based on name
        unique_technologies = []
        seen_names = set()
        for tech in technologies:
            if tech['name'] not in seen_names:
                unique_technologies.append(tech)
                seen_names.add(tech['name'])

        print(f"DEBUG: Technology detection completed, found {len(unique_technologies)} technologies")

    except Exception as e:
        # Provide user-friendly error messages
        if "Connection refused" in str(e) or "actively refused" in str(e):
            unique_technologies = [{"error": "No web server detected on target"}]
        elif "Connection timed out" in str(e) or "timeout" in str(e).lower():
            unique_technologies = [{"error": "Target unreachable or connection timeout"}]
        elif "Name resolution failure" in str(e) or "getaddrinfo failed" in str(e):
            unique_technologies = [{"error": "DNS resolution failed"}]
        else:
            unique_technologies = [{"error": "Technology detection failed"}]

    return unique_technologies

def detect_technologies_manual(url):
    """Manual technology detection as fallback when whatweb is not available"""
    technologies = []

    try:
        # Faster timeout and don't verify SSL to speed up detection
        response = requests.get(url, timeout=5, verify=False)
        headers = response.headers
        html = response.text.lower()

        # Server detection
        server = headers.get('Server', '')
        if server:
            technologies.append({
                "category": "Server",
                "name": server,
                "confidence": "High",
                "icon": get_technology_icon(server)
            })

        # Web frameworks
        if 'x-powered-by' in headers:
            framework = headers['x-powered-by']
            technologies.append({
                "category": "Framework",
                "name": framework,
                "confidence": "High",
                "icon": get_technology_icon(framework)
            })

        # Basic technology detection
        tech_indicators = {
            "WordPress": ["wp-content", "wp-includes", "wordpress"],
            "Joomla": ["joomla", "/components/com_"],
            "Drupal": ["drupal", "/sites/default/"],
            "Apache": ["apache", "httpd"],
            "Nginx": ["nginx"],
            "PHP": ["php", "x-powered-by.*php"],
            "Cloudflare": ["cf-ray", "cloudflare"]
        }

        found_techs = set()
        for tech, indicators in tech_indicators.items():
            if any(indicator in html for indicator in indicators):
                if tech not in found_techs:
                    technologies.append({
                        "category": "Technology",
                        "name": tech,
                        "confidence": "Medium",
                        "icon": get_technology_icon(tech)
                    })
                    found_techs.add(tech)

        print(f"DEBUG: Manual detection found {len(technologies)} technologies")

    except Exception as e:
        # Provide user-friendly error messages
        if "Connection refused" in str(e) or "actively refused" in str(e):
            technologies.append({"error": "No web server detected on target"})
        elif "Connection timed out" in str(e) or "timeout" in str(e).lower():
            technologies.append({"error": "Target unreachable or connection timeout"})
        elif "Name resolution failure" in str(e) or "getaddrinfo failed" in str(e):
            technologies.append({"error": "DNS resolution failed"})
        else:
            technologies.append({"error": "Technology detection failed"})

    return technologies

def get_technology_icon(tech_name):
    """Return icon URL with original brand colors for technology"""
    # Original brand colored icons - using icons8 and brand resources
    icons = {
        # Web Servers
        "Apache": "https://img.icons8.com/color/48/000000/apache.png",
        "nginx": "https://img.icons8.com/color/48/000000/nginx.png",
        "IIS": "https://img.icons8.com/color/48/000000/windows-server.png",
        "LiteSpeed": "https://img.icons8.com/color/48/000000/server.png",

        # Programming Languages
        "PHP": "https://img.icons8.com/officel/48/000000/php-logo.png",
        "Python": "https://img.icons8.com/color/48/000000/python.png",
        "Node.js": "https://img.icons8.com/color/48/000000/nodejs.png",
        "Ruby": "https://img.icons8.com/color/48/000000/ruby-programming-language.png",
        "Java": "https://img.icons8.com/color/48/000000/java-coffee-cup-logo.png",
        "Go": "https://img.icons8.com/color/48/000000/golang.png",

        # Frameworks & CMS
        "WordPress": "https://img.icons8.com/color/48/000000/wordpress.png",
        "Joomla": "https://img.icons8.com/color/48/000000/joomla.png",
        "Drupal": "https://img.icons8.com/color/48/000000/drupal.png",
        "Laravel": "https://img.icons8.com/color/48/000000/laravel.png",
        "Django": "https://img.icons8.com/color/48/000000/django.png",
        "Express": "https://img.icons8.com/color/48/000000/express.png",
        "Rails": "https://img.icons8.com/color/48/000000/ruby-on-rails.png",
        "Spring": "https://img.icons8.com/color/48/000000/spring-logo.png",

        # Frontend Frameworks
        "React": "https://img.icons8.com/color/48/000000/react-native.png",
        "Vue.js": "https://img.icons8.com/color/48/000000/vue-js.png",
        "Angular": "https://img.icons8.com/color/48/000000/angularjs.png",
        "Svelte": "https://img.icons8.com/color/48/000000/svelte.png",

        # Libraries & Tools
        "Bootstrap": "https://img.icons8.com/color/48/000000/bootstrap.png",
        "jQuery": "https://img.icons8.com/ios-filled/50/0769ad/jquery.png",
        "Tailwind CSS": "https://img.icons8.com/color/48/000000/tailwindcss.png",
        "Sass": "https://img.icons8.com/color/48/000000/sass.png",

        # Databases
        "MySQL": "https://img.icons8.com/color/48/000000/mysql-logo.png",
        "PostgreSQL": "https://img.icons8.com/color/48/000000/postgreesql.png",
        "MongoDB": "https://img.icons8.com/color/48/000000/mongodb.png",
        "Redis": "https://img.icons8.com/color/48/000000/redis.png",

        # CDNs & Services
        "Cloudflare": "https://img.icons8.com/color/48/000000/cloudflare.png",
        "AWS": "https://img.icons8.com/color/48/000000/amazon-web-services.png",
        "Azure": "https://img.icons8.com/color/48/000000/azure-1.png",
        "Google Cloud": "https://img.icons8.com/color/48/000000/google-cloud.png",

        # Microsoft Technologies
        "ASP.NET": "https://img.icons8.com/color/48/000000/dotnet.png",
        ".NET": "https://img.icons8.com/color/48/000000/dotnet.png",
        "C#": "https://img.icons8.com/color/48/000000/c-sharp-logo.png",

        # Default fallback
        "default": "https://img.icons8.com/color/48/000000/web.png"
    }

    # Try exact match first
    if tech_name in icons:
        return icons[tech_name]

    # Try partial match for common variations
    tech_lower = tech_name.lower()
    for key, icon in icons.items():
        if key.lower() in tech_lower:
            return icon

    # Special cases for version numbers and variations
    if 'apache' in tech_lower:
        return icons["Apache"]
    elif 'nginx' in tech_lower:
        return icons["nginx"]
    elif 'iis' in tech_lower or 'microsoft' in tech_lower:
        return icons["IIS"]
    elif 'wordpress' in tech_lower:
        return icons["WordPress"]
    elif 'joomla' in tech_lower:
        return icons["Joomla"]
    elif 'drupal' in tech_lower:
        return icons["Drupal"]
    elif 'laravel' in tech_lower:
        return icons["Laravel"]
    elif 'django' in tech_lower:
        return icons["Django"]
    elif 'react' in tech_lower:
        return icons["React"]
    elif 'vue' in tech_lower:
        return icons["Vue.js"]
    elif 'angular' in tech_lower:
        return icons["Angular"]
    elif 'bootstrap' in tech_lower:
        return icons["Bootstrap"]
    elif 'jquery' in tech_lower:
        return icons["jQuery"]
    elif 'cloudflare' in tech_lower:
        return icons["Cloudflare"]
    elif 'asp.net' in tech_lower or '.net' in tech_lower:
        return icons["ASP.NET"]

    # Return default icon if no match found
    return icons["default"]
