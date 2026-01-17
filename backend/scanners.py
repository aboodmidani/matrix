import requests
import ssl
import socket
import dns.resolver
import nmap

def get_ssl_info(domain):
    try:
        # Try with certificate verification first
        context = ssl.create_default_context()
        with socket.create_connection((domain, 443)) as sock:
            with context.wrap_socket(sock, server_hostname=domain) as ssock:
                cert = ssock.getpeercert()
                return {
                    "valid": True,
                    "issuer": dict(x[0] for x in cert['issuer']),
                    "subject": dict(x[0] for x in cert['subject']),
                    "version": cert['version'],
                    "notBefore": cert['notBefore'],
                    "notAfter": cert['notAfter']
                }
    except ssl.SSLCertVerificationError as e:
        # If cert verification fails, try without verification to get cert info
        try:
            context = ssl.create_default_context()
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE
            with socket.create_connection((domain, 443)) as sock:
                with context.wrap_socket(sock, server_hostname=domain) as ssock:
                    cert = ssock.getpeercert()
                    return {
                        "valid": False,
                        "verification_error": str(e),
                        "issuer": dict(x[0] for x in cert['issuer']),
                        "subject": dict(x[0] for x in cert['subject']),
                        "version": cert['version'],
                        "notBefore": cert['notBefore'],
                        "notAfter": cert['notAfter']
                    }
        except Exception as e2:
            return {"error": str(e2)}
    except Exception as e:
        return {"error": str(e)}

def get_security_headers(url):
    try:
        # Try with SSL verification first, fallback to no verification for IPs
        try:
            response = requests.get(url, timeout=10, verify=True)
        except requests.exceptions.SSLError:
            # If SSL verification fails (common with IP addresses), try without verification
            response = requests.get(url, timeout=10, verify=False)

        headers = response.headers
        security_headers = {
            'Strict-Transport-Security': headers.get('Strict-Transport-Security'),
            'Content-Security-Policy': headers.get('Content-Security-Policy'),
            'X-Frame-Options': headers.get('X-Frame-Options'),
            'X-Content-Type-Options': headers.get('X-Content-Type-Options'),
            'Referrer-Policy': headers.get('Referrer-Policy'),
            'Permissions-Policy': headers.get('Permissions-Policy')
        }
        return security_headers
    except Exception as e:
        return {"error": str(e)}

def get_dns_info(domain):
    """Comprehensive DNS enumeration using pure Python"""
    try:
        dns_info = {}

        # Get A records (IPv4 addresses)
        try:
            answers = dns.resolver.resolve(domain, 'A')
            dns_info["A_records"] = [str(rdata) for rdata in answers]
        except:
            dns_info["A_records"] = []

        # Get AAAA records (IPv6 addresses)
        try:
            answers = dns.resolver.resolve(domain, 'AAAA')
            dns_info["AAAA_records"] = [str(rdata) for rdata in answers]
        except:
            dns_info["AAAA_records"] = []

        # Get MX records (mail servers)
        try:
            answers = dns.resolver.resolve(domain, 'MX')
            dns_info["MX_records"] = [{"preference": rdata.preference, "exchange": str(rdata.exchange)} for rdata in answers]
        except:
            dns_info["MX_records"] = []

        # Get TXT records (SPF, DKIM, etc.)
        try:
            answers = dns.resolver.resolve(domain, 'TXT')
            dns_info["TXT_records"] = [str(rdata) for rdata in answers]
        except:
            dns_info["TXT_records"] = []

        # Get CNAME record if this is an alias
        try:
            answers = dns.resolver.resolve(domain, 'CNAME')
            dns_info["CNAME_records"] = [str(rdata) for rdata in answers]
        except:
            dns_info["CNAME_records"] = []

        # Get NS records (name servers)
        try:
            answers = dns.resolver.resolve(domain, 'NS')
            dns_info["NS_records"] = [str(rdata) for rdata in answers]
        except:
            dns_info["NS_records"] = []

        return dns_info

    except Exception as e:
        return {"error": str(e)}

def scan_ports(domain, nmap_options='-sV --version-intensity 2'):
    try:
        # Use faster nmap options and fewer ports for speed
        nm = nmap.PortScanner()
        # Reduced port range and faster options
        nm.scan(domain, '21,22,23,25,53,80,110,143,443', arguments='--host-timeout 30s --max-rtt-timeout 500ms')

        open_ports = []
        for host in nm.all_hosts():
            for proto in nm[host].all_protocols():
                lport = nm[host][proto].keys()
                for port in lport:
                    state = nm[host][proto][port]['state']
                    if state == 'open':
                        service = nm[host][proto][port]['name']
                        port_info = {
                            "port": port,
                            "protocol": proto,
                            "state": state,
                            "service": service
                        }
                        open_ports.append(port_info)

        return open_ports
    except Exception as e:
        # Fallback to basic socket scanning if nmap fails
        return scan_ports_fallback(domain)

def scan_ports_fallback(domain):
    common_ports = [21, 22, 23, 25, 53, 80, 110, 143, 443, 993, 995, 3306, 5432]
    open_ports = []

    for port in common_ports:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((domain, port))
            if result == 0:
                service = get_service_name(port)
                open_ports.append({"port": port, "service": service, "state": "open"})
            sock.close()
        except:
            pass

    return open_ports

def get_service_name(port):
    services = {
        21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP", 53: "DNS",
        80: "HTTP", 110: "POP3", 143: "IMAP", 443: "HTTPS", 993: "IMAPS",
        995: "POP3S", 3306: "MySQL", 5432: "PostgreSQL"
    }
    return services.get(port, "Unknown")

def analyze_seo(url):
    """Comprehensive SEO analysis for the target website"""
    seo_issues = []

    try:
        # Get main page
        response = requests.get(url, timeout=10, verify=False)
        html = response.text
        soup = None

        # Try to parse HTML with BeautifulSoup if available
        try:
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(html, 'html.parser')
        except ImportError:
            # Fallback without BeautifulSoup
            pass

        # 1. Title Tag Analysis
        title_tag = ""
        if soup:
            title_elem = soup.find('title')
            title_tag = title_elem.text.strip() if title_elem else ""
        else:
            # Fallback regex extraction
            import re
            title_match = re.search(r'<title[^>]*>(.*?)</title>', html, re.IGNORECASE | re.DOTALL)
            title_tag = title_match.group(1).strip() if title_match else ""

        if not title_tag:
            seo_issues.append({
                "type": "Missing Title Tag",
                "severity": "High",
                "description": "Title tag is missing - crucial for SEO"
            })
        elif len(title_tag) < 30:
            seo_issues.append({
                "type": "Title Too Short",
                "severity": "Medium",
                "description": f"Title tag is too short ({len(title_tag)} chars) - should be 30-60 characters"
            })
        elif len(title_tag) > 60:
            seo_issues.append({
                "type": "Title Too Long",
                "severity": "Medium",
                "description": f"Title tag is too long ({len(title_tag)} chars) - should be 30-60 characters"
            })

        # 2. Meta Description Analysis
        meta_desc = ""
        if soup:
            meta_desc_elem = soup.find('meta', attrs={'name': 'description'})
            meta_desc = meta_desc_elem.get('content', '').strip() if meta_desc_elem else ""
        else:
            desc_match = re.search(r'<meta[^>]*name=["\']description["\'][^>]*content=["\']([^"\']*)["\']', html, re.IGNORECASE)
            meta_desc = desc_match.group(1).strip() if desc_match else ""

        if not meta_desc:
            seo_issues.append({
                "type": "Missing Meta Description",
                "severity": "High",
                "description": "Meta description is missing - important for search result snippets"
            })
        elif len(meta_desc) < 120:
            seo_issues.append({
                "type": "Meta Description Too Short",
                "severity": "Low",
                "description": f"Meta description is too short ({len(meta_desc)} chars) - should be 120-160 characters"
            })
        elif len(meta_desc) > 160:
            seo_issues.append({
                "type": "Meta Description Too Long",
                "severity": "Low",
                "description": f"Meta description is too long ({len(meta_desc)} chars) - may be truncated in search results"
            })

        # 3. Heading Structure Analysis
        if soup:
            h1_tags = soup.find_all('h1')
            h2_tags = soup.find_all('h2')
            h3_tags = soup.find_all('h3')

            if len(h1_tags) == 0:
                seo_issues.append({
                    "type": "Missing H1 Tag",
                    "severity": "High",
                    "description": "No H1 tag found - each page should have exactly one H1 tag"
                })
            elif len(h1_tags) > 1:
                seo_issues.append({
                    "type": "Multiple H1 Tags",
                    "severity": "Medium",
                    "description": f"Multiple H1 tags found ({len(h1_tags)}) - use only one H1 per page"
                })

            if len(h2_tags) == 0:
                seo_issues.append({
                    "type": "Missing H2 Tags",
                    "severity": "Low",
                    "description": "No H2 tags found - use H2 tags to structure content hierarchy"
                })

        # 4. Image Alt Attributes
        if soup:
            images = soup.find_all('img')
            images_without_alt = [img for img in images if not img.get('alt')]
            if images_without_alt:
                seo_issues.append({
                    "type": "Images Missing Alt Attributes",
                    "severity": "Medium",
                    "description": f"{len(images_without_alt)} images missing alt attributes - affects accessibility and SEO"
                })

        # 5. Check for robots.txt
        try:
            robots_url = url.rstrip('/') + '/robots.txt'
            robots_response = requests.get(robots_url, timeout=5, verify=False)
            if robots_response.status_code != 200:
                seo_issues.append({
                    "type": "Missing robots.txt",
                    "severity": "Low",
                    "description": "robots.txt file not found - helps search engines crawl your site"
                })
        except:
            seo_issues.append({
                "type": "Missing robots.txt",
                "severity": "Low",
                "description": "robots.txt file not found - helps search engines crawl your site"
            })

        # 6. Check for sitemap
        try:
            sitemap_url = url.rstrip('/') + '/sitemap.xml'
            sitemap_response = requests.get(sitemap_url, timeout=5, verify=False)
            if sitemap_response.status_code != 200:
                seo_issues.append({
                    "type": "Missing XML Sitemap",
                    "severity": "Low",
                    "description": "XML sitemap not found - helps search engines discover all pages"
                })
        except:
            seo_issues.append({
                "type": "Missing XML Sitemap",
                "severity": "Low",
                "description": "XML sitemap not found - helps search engines discover all pages"
            })

        # 7. Check for Open Graph tags
        og_tags = ['og:title', 'og:description', 'og:image', 'og:url']
        missing_og = []
        if soup:
            for og_tag in og_tags:
                if not soup.find('meta', attrs={'property': og_tag}):
                    missing_og.append(og_tag)

        if missing_og:
            seo_issues.append({
                "type": "Missing Open Graph Tags",
                "severity": "Low",
                "description": f"Missing Open Graph tags: {', '.join(missing_og)} - affects social media sharing"
            })

        # 8. Check for Twitter Card tags
        twitter_tags = ['twitter:card', 'twitter:title', 'twitter:description']
        missing_twitter = []
        if soup:
            for twitter_tag in twitter_tags:
                if not soup.find('meta', attrs={'name': twitter_tag}):
                    missing_twitter.append(twitter_tag)

        if missing_twitter:
            seo_issues.append({
                "type": "Missing Twitter Card Tags",
                "severity": "Low",
                "description": f"Missing Twitter Card tags: {', '.join(missing_twitter)} - affects Twitter sharing"
            })

        # 9. Check for structured data (JSON-LD)
        if '"@context"' not in html and '"@type"' not in html:
            seo_issues.append({
                "type": "Missing Structured Data",
                "severity": "Low",
                "description": "No structured data (JSON-LD) found - helps search engines understand content"
            })

        # 10. Check for canonical URL
        if soup:
            canonical = soup.find('link', attrs={'rel': 'canonical'})
            if not canonical:
                seo_issues.append({
                    "type": "Missing Canonical URL",
                    "severity": "Medium",
                    "description": "Canonical URL not specified - helps prevent duplicate content issues"
                })

    except Exception as e:
        seo_issues.append({
            "type": "SEO Analysis Error",
            "severity": "Info",
            "description": f"SEO analysis failed: {str(e)}"
        })

    return seo_issues
